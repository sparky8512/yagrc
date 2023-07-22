import os.path
import sys

from grpc_reflection.v1alpha import reflection
from grpc_reflection.v1alpha import reflection_pb2
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


# Override pytest-grpc plugin implementation to enable reflection
@pytest.fixture(scope='module')
def grpc_server(_grpc_server, grpc_addr, grpc_add_to_server, grpc_servicer):
    grpc_add_to_server(grpc_servicer, _grpc_server)
    service_names = (
        _Add_One_DESCRIPTOR.services_by_name['Addition'].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(service_names, _grpc_server)
    _grpc_server.add_insecure_port(grpc_addr)
    _grpc_server.start()
    yield _grpc_server
    _grpc_server.stop(grace=None)


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
            real_fake_handler = real_fake_stream_stream(method_path, *args,
                                                        **kwargs)

            def wrapped_fake_handler(request, timeout=None, **kwargs):
                if method_path.startswith(
                        "/grpc.reflection.v1alpha.ServerReflection/"):
                    assert timeout is not None
                return real_fake_handler(request)

            return wrapped_fake_handler

        if channel.__class__.__name__ == "FakeChannel":
            channel.stream_stream = wrapped_stream_stream

        yield channel


# Brittle hack of the reflection service to report error
@pytest.fixture
def force_list_services_error(monkeypatch):

    def mock_error(self):
        response = reflection_pb2.ServerReflectionResponse()
        response.error_response.error_code = 1
        response.error_response.error_message = "fake error"
        return response

    monkeypatch.setattr(reflection.BaseReflectionServicer, "_list_services",
                        mock_error)


# And another to simulate an unsatisfied dependency
@pytest.fixture
def force_unsatisfied_dep(monkeypatch):
    real_method = reflection.BaseReflectionServicer._file_by_filename

    def mock_file_by_filename(self, filename):
        response = real_method(self, filename)
        del response.file_descriptor_response.file_descriptor_proto[-1]
        return response

    monkeypatch.setattr(reflection.BaseReflectionServicer, "_file_by_filename",
                        mock_file_by_filename)
