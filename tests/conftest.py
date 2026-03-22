import os.path
import sys

import grpc
from grpc_reflection.v1alpha import reflection as reflection_v1a
from grpc_reflection.v1alpha import reflection_pb2 as reflection_pb2_v1a
try:
    from grpc_reflection.v1 import reflection as reflection_v1
    from grpc_reflection.v1 import reflection_pb2 as reflection_pb2_v1
except ModuleNotFoundError:
    # v1 not available in grpcio-reflection package yet, so use local copies
    from service.grpc_reflection_v1 import reflection as reflection_v1
    from yagrc.grpc_reflection.v1 import reflection_pb2 as reflection_pb2_v1
import pytest

# Testing_protos package is deliberately kept out of the import path, but the
# service still needs it. Can't just use relative imports, because the recursive
# imports in the generated _pb2 modules also need to be able to find it.
addone_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "service")
sys.path.insert(0, addone_path)

# See comments in Add_One.proto about terrible naming
from Testing_protos import Add_One_pb2_grpc as _service_Add_One_pb2_grpc
from Testing_protos.Add_One_pb2 import DESCRIPTOR as _Add_One_DESCRIPTOR
import addone_server

sys.path.remove(addone_path)
for name in ("Testing_protos", "Testing_protos.AddAltTypes_pb2",
             "Testing_protos.Add_One_pb2_grpc", "Testing_protos.AddTypes_pb2",
             "Testing_protos.Add_One_pb2"):
    if name in sys.modules:
        del sys.modules[name]


@pytest.fixture(scope='module')
def grpc_add_to_server():
    return _service_Add_One_pb2_grpc.add_AdditionServicer_to_server


@pytest.fixture(scope='module')
def grpc_servicer():
    return addone_server.Addition()


# grpc_stub_cls fixture not defined because stub creation is part of test


# Override this fixture in test module to test different combinations
@pytest.fixture(scope='module')
def server_modes():
    # enable v1alpha service, enable v1 service
    return True, True


# Override pytest-grpc plugin implementation to prevent reusing _grpc_server
# instances across different server mode configurations
@pytest.fixture(scope='module')
def grpc_interceptors(server_modes):
    return


# Override pytest-grpc plugin implementation to enable reflection
@pytest.fixture(scope='module')
def grpc_server(_grpc_server, grpc_addr, grpc_add_to_server, grpc_servicer,
                server_modes):
    grpc_add_to_server(grpc_servicer, _grpc_server)
    service_names = [_Add_One_DESCRIPTOR.services_by_name['Addition'].full_name]
    if server_modes[0]:
        service_names.append(reflection_v1a.SERVICE_NAME)
    if server_modes[1]:
        service_names.append(reflection_v1.SERVICE_NAME)
    if server_modes[0]:
        reflection_v1a.enable_server_reflection(service_names, _grpc_server)
    if server_modes[1]:
        reflection_v1.enable_server_reflection(service_names, _grpc_server)
    _grpc_server.add_insecure_port(grpc_addr)
    _grpc_server.start()
    yield _grpc_server
    _grpc_server.stop(grace=None)


# Simulate the exception client would get for unimplemented service or method
class FakeUnimplementedError(grpc.RpcError, grpc.Call):

    def code(self):
        return grpc.StatusCode.UNIMPLEMENTED


# Override pytest-grpc plugin implementation of grpc_channel to hack around
# unhandled optional args to handler methods. This is ugly as sin, only
# patches the one handler type the reflection service uses, and is liable to
# break with later versions of the plugin, but whatever.... On the plus side,
# this provides an opportunity to verify that reflection service operations
# always include a timeout arg.
@pytest.fixture(scope='module')
def grpc_channel(grpc_create_channel):
    with grpc_create_channel() as channel:
        real_fake_stream_stream = channel.stream_stream

        def wrapped_stream_stream(method_path, *args, **kwargs):
            try:
                real_fake_handler = real_fake_stream_stream(
                    method_path, *args, **kwargs)
            except KeyError as err:
                raise FakeUnimplementedError() from err

            def wrapped_fake_handler(request, timeout=None, **kwargs):
                if method_path.startswith(
                        "/grpc.reflection.v1alpha.ServerReflection/"
                ) or method_path.startswith(
                        "/grpc.reflection.v1.ServerReflection/"):
                    assert timeout is not None
                return real_fake_handler(request)

            return wrapped_fake_handler

        if channel.__class__.__name__ == "FakeChannel":
            channel.stream_stream = wrapped_stream_stream

        yield channel


# Brittle hack of the reflection service to report error
@pytest.fixture
def force_list_services_error(monkeypatch):

    def patch_service(reflection, reflection_pb2):

        def mock_error(self):
            response = reflection_pb2.ServerReflectionResponse()
            response.error_response.error_code = 1
            response.error_response.error_message = "fake error"
            return response

        monkeypatch.setattr(reflection.BaseReflectionServicer, "_list_services",
                            mock_error)

    patch_service(reflection_v1a, reflection_pb2_v1a)
    patch_service(reflection_v1, reflection_pb2_v1)


# And another to simulate an unsatisfied dependency
@pytest.fixture
def force_unsatisfied_dep(monkeypatch):

    def patch_service(reflection):
        real_method = reflection.BaseReflectionServicer._file_by_filename

        def mock_file_by_filename(self, filename):
            response = real_method(self, filename)
            del response.file_descriptor_response.file_descriptor_proto[-1]
            return response

        monkeypatch.setattr(reflection.BaseReflectionServicer,
                            "_file_by_filename", mock_file_by_filename)

    patch_service(reflection_v1a)
    patch_service(reflection_v1)
