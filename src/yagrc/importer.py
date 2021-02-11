"""An import provider that mimics generated grpc protocol module files.

This modules builds on top of `yagrc.reflector` to provide a drop-in
replacement for the generated _pb2 and _pb2_grpc modules supporting the
gRPC services advertised by a server that supports service reflection.
"""
import importlib
import importlib.abc
import importlib.machinery
import sys

from yagrc import reflector


def _proto_basename(name):
    return name.removesuffix(".proto").replace("/", ".")


class _DummyLoader(importlib.abc.Loader):  # pylint: disable=abstract-method

    def __init__(self, imported_set):
        super().__init__()
        self._imported = imported_set

    def create_module(self, spec):
        return None

    def exec_module(self, module):
        self._imported.add(module.__name__)


class _DynamicPb2Loader(importlib.abc.Loader):  # pylint: disable=abstract-method

    def __init__(self, imported_set, filename, yagrc_reflector):
        super().__init__()
        self._imported = imported_set
        self._filename = filename
        self._reflector = yagrc_reflector

    def create_module(self, spec):
        return None

    def exec_module(self, module):
        self._imported.add(module.__name__)
        file_descr = self._reflector.file_descriptor(self._filename)
        module.DESCRIPTOR = file_descr
        # mimic _pb2 module dependency import behavior
        for dep_descr in file_descr.dependencies:
            dep_mod = importlib.import_module(
                _proto_basename(dep_descr.name) + "_pb2")
            if dep_descr in file_descr.public_dependencies:
                module.__dict__.update((key, val)
                                       for key, val in dep_mod.__dict__.items()
                                       if not key.startswith("_"))
        for name, message in file_descr.message_types_by_name.items():
            setattr(module, name, self._reflector.message_from_descr(message))
        for name, enum in file_descr.enum_types_by_name.items():
            setattr(module, name, reflector.enum_from_descr(enum))
            for value in enum.values:
                # seems crazy to do this blindly, but the generated files do so
                setattr(module, value.name, value.number)


class _DynamicPb2GrpcLoader(importlib.abc.Loader):  # pylint: disable=abstract-method

    def __init__(self, imported_set, filename, yagrc_reflector):
        super().__init__()
        self._imported = imported_set
        self._filename = filename
        self._reflector = yagrc_reflector

    def create_module(self, spec):
        return None

    def exec_module(self, module):
        self._imported.add(module.__name__)
        file_descr = self._reflector.file_descriptor(self._filename)
        dep_filenames = set()
        method_proto_map = self._reflector.methods_by_file[self._filename]
        for service_name, method_protos in method_proto_map.items():
            service = file_descr.services_by_name[service_name]
            stub_class, dep_descrs = self._reflector.gen_stub_class(
                service, method_protos)
            stub_class.__module__ = module.__name__
            setattr(module, stub_class.__name__, stub_class)
            dep_filenames.update(descr.file.name for descr in dep_descrs)
        # mimic _pb2_grpc module dependency behavior
        for dep_filename in dep_filenames:
            importlib.import_module(_proto_basename(dep_filename) + "_pb2")


class _DynamicGrpcFinder(importlib.abc.MetaPathFinder):

    def __init__(self, yagrc_reflector):
        super().__init__()
        self._package_modules = set()
        self._pb2_modules = {}
        self._pb2_grpc_modules = {}
        self._imported = set()
        self._reflector = yagrc_reflector

    def configure_files(self, filenames):
        """Add modules and their containing package paths."""
        for filename in filenames:
            base = _proto_basename(filename)
            self._pb2_modules[base + "_pb2"] = filename
            self._pb2_grpc_modules[base + "_pb2_grpc"] = filename
            while base:
                base, _, _ = base.rpartition(".")
                if base:
                    self._package_modules.add(base)

    def reset_files(self):
        """Remove previously added modules and package paths."""
        self.invalidate_caches()
        self._package_modules.clear()
        self._pb2_modules.clear()
        self._pb2_grpc_modules.clear()

    def find_spec(self, fullname, path, target):  # pylint: disable=unused-argument
        if fullname in self._package_modules:
            return importlib.machinery.ModuleSpec(fullname,
                                                  _DummyLoader(self._imported),
                                                  is_package=True)
        if fullname in self._pb2_modules:
            return importlib.machinery.ModuleSpec(
                fullname,
                _DynamicPb2Loader(self._imported, self._pb2_modules[fullname],
                                  self._reflector),
                is_package=False)
        if fullname in self._pb2_grpc_modules:
            return importlib.machinery.ModuleSpec(
                fullname,
                _DynamicPb2GrpcLoader(self._imported,
                                      self._pb2_grpc_modules[fullname],
                                      self._reflector),
                is_package=False)
        return None

    def invalidate_caches(self):
        # can't do much more without requiring configure to be called again
        for name in self._imported:
            if name in sys.modules:
                del sys.modules[name]
        self._imported.clear()


class GrpcImporter():
    """Public API for supporting dynamic import of protocol modules."""

    def __init__(self):
        self._reflector = reflector.GrpcReflectionEngine()
        self._finder = _DynamicGrpcFinder(self._reflector)

    def configure(self, channel, filenames=None, path_prepend=False):
        """Load a set of proto files and enable their dynamic module imports.

        Load one or more specified files, as well as the transitive dependency
        files of those files. If `filenames` is not specified, then files
        containing the symbols for all services advertised by the RPC server,
        other than the reflection service, are loaded.

        For each proto file loaded, corresponding _pb2 and _pb2_grpc modules
        will be made available in the import path. The module names and
        package path will be the same as that generated by the protoc tool
        for the proto files used on the server, which is a function of
        directory layout of the proto files.

        This method may be called multiple times to load additional proto
        files.

        The caller-supplied channel is only used within the context of this
        method call, so the caller is free to close it afterwards.

        Args:
            channel (grpc.Channel): The RPC channel to use.
            filenames (list[str]): Optional. List of proto file names, with
                path, to request.
            path_prepend (bool): Optional. If set to True, places the dynamic
                proto modules ahead of any other import path, otherwise places
                them after other import paths.

        Raises:
            reflector.ServiceError: Reflection service responded with an error.
            grpc.RpcError: Lower level RPC error.
        """
        loaded = self._reflector.load_protocols(channel, filenames=filenames)
        self._finder.configure_files(loaded)

        if self._finder in sys.meta_path:
            sys.meta_path.remove(self._finder)
        if path_prepend:
            sys.meta_path.insert(0, self._finder)
        else:
            sys.meta_path.append(self._finder)

    def deconfigure(self):
        """Remove support for subsequent dynamic module imports.

        Dynamic modules that have already been imported remain usable by the
        modules that imported them, but new imports will fail unless the
        modules are provided elsewhere in the module path, or
        `GrpcImporter.configure` is called again.

        This is not normally required, but without it, the entry in the import
        meta path will remain in place, even if the `GrpcImporter` object that
        installed it is destroyed.
        """
        if self._finder in sys.meta_path:
            sys.meta_path.remove(self._finder)
        self._finder.reset_files()
