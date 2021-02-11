import pytest

# Verify failure when nothing is done to make Testing_protos package available
# in module path.

# See comments in Add_One.proto about terrible naming

# Uncomment the following lines to verify that the test cases would otherwise
# pass if not for the import errors. (this will cause the test suite to fail)
#import os
#import sys
#sys.path.insert(
#    0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "service"))


@pytest.mark.xfail(raises=ImportError, strict=True)
def test_AddOne(grpc_channel):
    from Testing_protos import Add_One_pb2_grpc
    from Testing_protos import AddTypes_pb2
    stub = Add_One_pb2_grpc.AdditionStub(grpc_channel)
    response = stub.AddOne(AddTypes_pb2.Addend(number=5))
    assert response.number == 6


@pytest.mark.xfail(raises=ImportError, strict=True)
def test_AddOnes(grpc_channel):
    from Testing_protos import Add_One_pb2_grpc
    from Testing_protos import AddTypes_pb2
    stub = Add_One_pb2_grpc.AdditionStub(grpc_channel)
    responses = stub.AddOnes(AddTypes_pb2.Addend(number=5))
    for i, response in enumerate(responses):
        assert response.number == 6 + i
    assert i == 4


@pytest.mark.xfail(raises=ImportError, strict=True)
def test_AddsOne(grpc_channel):
    from Testing_protos import Add_One_pb2_grpc
    from Testing_protos import AddTypes_pb2
    stub = Add_One_pb2_grpc.AdditionStub(grpc_channel)
    response = stub.AddsOne((AddTypes_pb2.Addend(number=x) for x in range(5)))
    assert response.number == 0 + 1 + 2 + 3 + 4 + 1


@pytest.mark.xfail(raises=ImportError, strict=True)
def test_AddsOnes(grpc_channel):
    from Testing_protos import Add_One_pb2_grpc
    from Testing_protos import AddTypes_pb2
    stub = Add_One_pb2_grpc.AdditionStub(grpc_channel)
    responses = stub.AddsOnes((AddTypes_pb2.Addend(number=x) for x in range(5)))
    for i, response in enumerate(responses):
        assert response.number == i + 1
    assert i == 4


@pytest.mark.xfail(raises=ImportError, strict=True)
def test_CountQuery(grpc_channel):
    from Testing_protos import Add_One_pb2_grpc
    from Testing_protos import AddTypes_pb2
    stub = Add_One_pb2_grpc.AdditionStub(grpc_channel)
    response = stub.Status(AddTypes_pb2.StatusQuery(count={}))
    assert response.count.number > 0


@pytest.mark.xfail(raises=ImportError, strict=True)
def test_StatusQuery(grpc_channel):
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
