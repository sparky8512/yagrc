import pytest
from yagrc import reflector


@pytest.fixture(scope="module", params=["load_service", "load_all"])
def yagrc_reflector(request, grpc_channel):
    grpc_reflector = reflector.GrpcReflectionClient()
    if request.param == "load_service":
        grpc_reflector.load_protocols(grpc_channel,
                                      symbols=["Testing.Addition"])
    else:
        grpc_reflector.load_protocols(grpc_channel)
    return grpc_reflector


@pytest.fixture
def stub_class(yagrc_reflector):
    return yagrc_reflector.service_stub_class("Testing.Addition")


@pytest.fixture
def addend_class(yagrc_reflector):
    return yagrc_reflector.message_class("Testing.Addend")


@pytest.fixture
def query_class(yagrc_reflector):
    return yagrc_reflector.message_class("Testing.StatusQuery")


@pytest.fixture
def enum_class(yagrc_reflector):
    return yagrc_reflector.enum_class("Testing.ServiceState")


def test_AddOne(grpc_channel, stub_class, addend_class):
    stub = stub_class(grpc_channel)
    response = stub.AddOne(addend_class(number=5))
    assert response.number == 6


def test_AddOnes(grpc_channel, stub_class, addend_class):
    stub = stub_class(grpc_channel)
    responses = stub.AddOnes(addend_class(number=5))
    for i, response in enumerate(responses):
        assert response.number == 6 + i
    assert i == 4


def test_AddsOne(grpc_channel, stub_class, addend_class):
    stub = stub_class(grpc_channel)
    response = stub.AddsOne((addend_class(number=x) for x in range(5)))
    assert response.number == 0 + 1 + 2 + 3 + 4 + 1


def test_AddsOnes(grpc_channel, stub_class, addend_class):
    stub = stub_class(grpc_channel)
    responses = stub.AddsOnes((addend_class(number=x) for x in range(5)))
    for i, response in enumerate(responses):
        assert response.number == i + 1
    assert i == 4


def test_CountQuery(grpc_channel, stub_class, query_class):
    stub = stub_class(grpc_channel)
    response = stub.Status(query_class(count={}))
    assert response.count.number > 0


def test_StatusQuery(grpc_channel, stub_class, query_class, enum_class):
    stub = stub_class(grpc_channel)
    response = stub.Status(query_class(state={}))
    assert response.state.states["sum_engine"].state == enum_class.READY
    assert enum_class.Name(response.state.states["difference_engine"].state
                          ) == "BUSY_COMPUTING_ONE"
    # no reflector equivalent for AddTypes_pb2._UNKNOWN


def test_nested_messsage(yagrc_reflector):
    nested_class = yagrc_reflector.message_class(
        "Testing.StatusResponse.State.Wrapper")
    assert nested_class.DESCRIPTOR.full_name == "Testing.StatusResponse.State.Wrapper"


def test_list_services(grpc_channel):
    services = reflector.list_services(grpc_channel)
    assert "Testing.Addition" in services


@pytest.mark.xfail(raises=reflector.ServiceError, strict=True)
def test_list_error(grpc_channel, force_list_services_error):
    grpc_reflector = reflector.GrpcReflectionClient()
    grpc_reflector.load_protocols(grpc_channel)


@pytest.mark.xfail(raises=KeyError, strict=True)
def test_unsatisfied_dep(grpc_channel, force_unsatisfied_dep):
    grpc_reflector = reflector.GrpcReflectionClient()
    grpc_reflector.load_protocols(grpc_channel, symbols=["Testing.Addition"])


@pytest.mark.xfail(raises=reflector.ServiceError, strict=True)
def test_bad_proto(grpc_channel):
    grpc_reflector = reflector.GrpcReflectionClient()
    grpc_reflector.load_protocols(grpc_channel, symbols=["Testing.Subtraction"])
    assert False


@pytest.mark.xfail(raises=KeyError, strict=True)
def test_bad_service(yagrc_reflector):
    yagrc_reflector.service_stub_class("Testing.Subtraction")
    assert False


@pytest.mark.xfail(raises=KeyError, strict=True)
def test_bad_message(yagrc_reflector):
    yagrc_reflector.message_class("Testing.Minuend")
    assert False
