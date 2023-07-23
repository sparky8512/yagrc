"""A gRPC reflection client.

This module provides a programmatic interface for getting grpc class types
discovered via gRPC reflection service.

See:
    https://grpc.io/ for more information on gRPC in general.

    https://github.com/grpc/grpc/blob/master/doc/server-reflection.md for more
    information on gRPC service reflection.
"""
from collections import deque

from google.protobuf import descriptor_pb2
from google.protobuf import descriptor_pool
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import message_factory
from grpc_reflection.v1alpha import reflection_pb2
from grpc_reflection.v1alpha import reflection_pb2_grpc

# This is somewhat arbitrary, and is just here to prevent hang in the case of
# dead network connection that the client side still believes to be open.
QUERY_TIMEOUT = 10
"""Max wait time for reflection query completion, in seconds."""


class ServiceError(Exception):
    """Error reported by reflection service."""


def __stub_init__(self, channel):
    """The __init__ method for service stub classes."""
    for name, call, full_name, out_serializer, in_serializer in self._methods:  # pylint: disable=protected-access
        setattr(
            self, name,
            getattr(channel, call)(full_name,
                                   request_serializer=out_serializer,
                                   response_deserializer=in_serializer))


def _list_services(stub):
    responses = stub.ServerReflectionInfo(iter(
        [reflection_pb2.ServerReflectionRequest(list_services="")]),
                                          timeout=QUERY_TIMEOUT)
    for response in responses:
        if response.HasField("error_response"):
            raise ServiceError(response.error_response.error_message)
        for service in response.list_services_response.service:
            yield service.name


def list_services(channel):
    """Get list of fully qualified service names via reflection.

    Args:
        channel (grpc.Channel): The RPC channel to use.

    Raises:
        ServiceError: Reflection service responded with an error.
        grpc.RpcError: Lower level RPC error.
    """
    stub = reflection_pb2_grpc.ServerReflectionStub(channel)
    return list(_list_services(stub))


def enum_from_descr(proto):
    """Get enum class from enum descriptor.

    Args:
        proto (google.protobuf.descriptor.EnumDescriptor): Enum descriptor.
        """
    return enum_type_wrapper.EnumTypeWrapper(proto)


class GrpcReflectionEngine():
    """Implementation class for gRPC reflection client.

    This class is not meant to be used directly. Instead, use
    `GrpcReflectionClient` or `yagrc.importer.GrpcImporter`
    """

    def __init__(self):
        self.methods_by_file = {}
        self.pool = descriptor_pool.DescriptorPool()

    def load_protocols(self, channel, filenames=None, symbols=None):
        """Implementation of `GrpcReflectionClient.load_protocols`"""
        stub = reflection_pb2_grpc.ServerReflectionStub(channel)

        requests = []
        if filenames:
            requests.extend(
                reflection_pb2.ServerReflectionRequest(file_by_filename=name)
                for name in filenames)
        if symbols:
            requests.extend(
                reflection_pb2.ServerReflectionRequest(
                    file_containing_symbol=symbol) for symbol in symbols)
        if not requests:
            requests.extend(
                reflection_pb2.ServerReflectionRequest(
                    file_containing_symbol=name)
                for name in _list_services(stub)
                if name != "grpc.reflection.v1alpha.ServerReflection")

        protos = {}
        traversed = set()
        while requests:
            responses = stub.ServerReflectionInfo(iter(requests),
                                                  timeout=QUERY_TIMEOUT)
            deps = set()
            for response in responses:
                if response.HasField("error_response"):
                    raise ServiceError(response.error_response.error_message)
                for desc_bytes in response.file_descriptor_response.file_descriptor_proto:
                    proto = descriptor_pb2.FileDescriptorProto.FromString(  # pylint: disable=no-member
                        desc_bytes)
                    traversed.add(proto.name)
                    deps.update(proto.dependency)
                    protos[proto.name] = proto
                    self.methods_by_file[proto.name] = {
                        service.name: service.method
                        for service in proto.service
                    }
            deps -= traversed
            requests = [
                reflection_pb2.ServerReflectionRequest(file_by_filename=dep)
                for dep in deps
            ]
            # prevent unsatisfied deps from looping forever
            traversed.update(deps)

        names = deque(protos.keys())
        traversed = set()
        while names:
            name = names[0]
            traversed.add(name)
            # raises KeyError if unsatisfied dep:
            proto = protos[name]
            deps = set(proto.dependency) - traversed
            if deps:
                names = deque(x for x in names if x not in deps)
                names.extendleft(deps)
            else:
                del names[0]
                self.pool.Add(proto)

        return protos.keys()

    def file_descriptor(self, name):
        """Get file descriptor for a proto file that has been loaded.

        Args:
            name (str): The file name of the .proto file, including path.

        Returns:
             google.protobuf.descriptor.FileDescriptor: The descriptor for the
                specified file.

        Raises:
            KeyError: File has not been loaded.
        """
        return self.pool.FindFileByName(name)

    def message_from_descr(self, proto):
        """Get message class from message descriptor.

        Args:
            proto (google.protobuf.descriptor.Descriptor): Message descriptor.
        """
        return message_factory.GetMessageClass(proto)

    def gen_stub_class(self, service, method_protos):
        """Get service stub class from service descriptor.

        Args:
            service (google.protobuf.descriptor.ServiceDescriptor): Service
                descriptor.
            method_protos (iterable): The
                `google.protobuf.descriptor_pb2.MethodDescriptorProto` objects
                for the methods in the service.
        """
        stub_methods = []
        dep_descrs = []
        for method_proto in method_protos:
            method = service.methods_by_name[method_proto.name]
            channel_call = "_".join(
                "stream" if x else "unary" for x in
                [method_proto.client_streaming, method_proto.server_streaming])
            dep_descrs.extend([method.input_type, method.output_type])
            stub_methods.append(
                (method.name, channel_call,
                 "/{}/{}".format(service.full_name, method.name),
                 self.message_from_descr(method.input_type).SerializeToString,
                 self.message_from_descr(method.output_type).FromString))
        class_name = service.name + "Stub"
        return type(class_name, (), {
            "_methods": stub_methods,
            "__init__": __stub_init__
        }), dep_descrs


class GrpcReflectionClient():
    """Client to discover protocol types via gRPC service reflection.

    Protocol files must be loaded via `load_protocols` prior to getting any of
    the class types.

    Note that for nested types (fields, oneofs, etc) other than nested message
    types, the top-level message type should be requested and the nested types
    can be accessed on it via attribute.
    """

    def __init__(self):
        self._engine = GrpcReflectionEngine()

    def load_protocols(self, channel, filenames=None, symbols=None):
        """Load a set of proto files to use later for protocol types.

        Load one or more specified files and/or files containing specified
        symbols, as well as the transitive dependency files of those files.

        If neither `filenames` nor `symbols` is specified, then files
        containing the symbols for all services advertised by the RPC server,
        other than the reflection service, are loaded.

        This method may be called multiple times to load additional proto
        files; however, it is not recommended to use channels that point to
        different servers unless it is known that the symbols either do not
        overlap or contain the same exact version across all servers.

        The caller-supplied channel is only used within the context of this
        method call, so the caller is free to close it afterwards.

        Args:
            channel (grpc.Channel): The RPC channel to use.
            filenames (iterable[str]): Optional. Proto file names, with path,
                to request.
            symbols (iterable[str]): Optional. Fully qualified symbol names
                for which to request proto files.

        Raises:
            ServiceError: Reflection service responded with an error.
            grpc.RpcError: Lower level RPC error.
        """
        return self._engine.load_protocols(channel, filenames, symbols)

    def service_stub_class(self, name):
        """Get the stub class for the specified service type.

        Args:
            name: Fully qualified name of the protocol service.

        Raises:
            KeyError: File defining service has not been loaded.
        """
        service = self._engine.pool.FindServiceByName(name)
        methods = self._engine.methods_by_file[service.file.name][service.name]
        return self._engine.gen_stub_class(service, methods)[0]

    def message_class(self, name):
        """Get the class for the specified message type.

        Args:
            name: Fully qualified name of the protocol message.

        Raises:
            KeyError: File defining message has not been loaded.
        """
        return self._engine.message_from_descr(
            self._engine.pool.FindMessageTypeByName(name))

    def enum_class(self, name):
        """Get the class for the specified enum type.

        Args:
            name: Fully qualified name of the protocol enum.

        Raises:
            KeyError: File defining enum has not been loaded.
        """
        return enum_from_descr(self._engine.pool.FindEnumTypeByName(name))
