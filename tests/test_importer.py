import importlib

import pytest
from yagrc import importer as yagrc_importer

# See comments in Add_One.proto about terrible naming


@pytest.fixture
def grpc_importer(grpc_channel):
    importer = yagrc_importer.GrpcImporter()
    importer.configure(grpc_channel, filenames=["Testing_protos/Add_One.proto"])
    yield importer
    importer.deconfigure()


def test_AddOne(grpc_channel, grpc_importer):
    from Testing_protos import Add_One_pb2_grpc
    from Testing_protos import AddTypes_pb2
    stub = Add_One_pb2_grpc.AdditionStub(grpc_channel)
    response = stub.AddOne(AddTypes_pb2.Addend(number=5))
    assert response.number == 6


def test_AddOnes(grpc_channel, grpc_importer):
    from Testing_protos import Add_One_pb2_grpc
    from Testing_protos import AddTypes_pb2
    stub = Add_One_pb2_grpc.AdditionStub(grpc_channel)
    responses = stub.AddOnes(AddTypes_pb2.Addend(number=5))
    for i, response in enumerate(responses):
        assert response.number == 6 + i
    assert i == 4


def test_AddsOne(grpc_channel, grpc_importer):
    from Testing_protos import Add_One_pb2_grpc
    from Testing_protos import AddTypes_pb2
    stub = Add_One_pb2_grpc.AdditionStub(grpc_channel)
    response = stub.AddsOne((AddTypes_pb2.Addend(number=x) for x in range(5)))
    assert response.number == 0 + 1 + 2 + 3 + 4 + 1


def test_AddsOnes(grpc_channel, grpc_importer):
    from Testing_protos import Add_One_pb2_grpc
    from Testing_protos import AddTypes_pb2
    stub = Add_One_pb2_grpc.AdditionStub(grpc_channel)
    responses = stub.AddsOnes((AddTypes_pb2.Addend(number=x) for x in range(5)))
    for i, response in enumerate(responses):
        assert response.number == i + 1
    assert i == 4


def test_CountQuery(grpc_channel, grpc_importer):
    from Testing_protos import Add_One_pb2_grpc
    from Testing_protos import AddTypes_pb2
    stub = Add_One_pb2_grpc.AdditionStub(grpc_channel)
    response = stub.Status(AddTypes_pb2.StatusQuery(count={}))
    assert response.count.number > 0


def test_StatusQuery(grpc_channel, grpc_importer):
    from Testing_protos import Add_One_pb2_grpc
    from Testing_protos import AddTypes_pb2
    stub = Add_One_pb2_grpc.AdditionStub(grpc_channel)
    response = stub.Status(AddTypes_pb2.StatusQuery(state={}))
    assert response.state.states[
        "sum_engine"].state == AddTypes_pb2.ServiceState.READY
    assert AddTypes_pb2.ServiceState.Name(
        response.state.states["difference_engine"].state
    ) == "BUSY_COMPUTING_ONE"
    assert response.state.states["chaos_engine"].state == AddTypes_pb2._UNKNOWN


def test_DESCRIPTOR(grpc_importer):
    from Testing_protos import Add_One_pb2
    assert Add_One_pb2.DESCRIPTOR.name == "Testing_protos/Add_One.proto"


def test_invalidate_caches(grpc_importer):
    from Testing_protos import Add_One_pb2
    assert grpc_importer._finder._imported
    importlib.invalidate_caches()
    assert not grpc_importer._finder._imported


def test_path_prepend(grpc_channel, grpc_importer):
    grpc_importer.configure(grpc_channel, path_prepend=True)
    from Testing_protos import Add_One_pb2


@pytest.mark.xfail(raises=ImportError, strict=True)
def test_deconfigure(grpc_channel):
    importer = yagrc_importer.GrpcImporter()
    importer.configure(grpc_channel, filenames=["Testing_protos/Add_One.proto"])
    from Testing_protos import Add_One_pb2
    importer.deconfigure()
    from Testing_protos import Add_One_pb2


# This is just to make sure following test is meaningful
@pytest.mark.xfail(raises=NameError, strict=True)
def test_no_import(grpc_importer):
    assert Testing_protos.AddAltTypes_pb2.Addend.DESCRIPTOR.name == "Addend"


# While it is probably bad practice to rely on this, the generated _pb2 modules
# import all their transitive dependencies into the package namespace, and the
# yagrc importer deliberately mimics that behavior.
def test_indirect_import(grpc_importer):
    import Testing_protos.Add_One_pb2_grpc
    assert Testing_protos.AddAltTypes_pb2.Addend.DESCRIPTOR.name == "Addend"


@pytest.mark.xfail(raises=ImportError, strict=True)
def test_bad_import(grpc_channel, grpc_importer):
    from Testing_protos import bad_import_pb2
    assert False
