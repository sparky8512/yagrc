import importlib
import sys

import pytest
from yagrc import importer as yagrc_importer

# See comments in Add_One.proto about terrible naming


# lazy import intentionally has no cleanup mechanism, so do it the hard way
@pytest.fixture
def lazy_cleaner():
    yield
    if yagrc_importer._lazy_finder in sys.meta_path:
        sys.meta_path.remove(yagrc_importer._lazy_finder)
    yagrc_importer._lazy_finder._package_modules.clear()
    yagrc_importer._lazy_finder.pb2_imports.clear()
    yagrc_importer._lazy_finder.pb2_grpc_imports.clear()
    yagrc_importer._lazy_importer.deconfigure()
    for name in ("Testing_protos", "Testing_protos.other_pb2",
                 "Testing_protos.Add_One_pb2_grpc",
                 "Testing_protos.AddTypes_pb2"):
        if name in sys.modules:
            del sys.modules[name]


def test_AddOne(grpc_channel, lazy_cleaner):
    yagrc_importer.add_lazy_packages(["Testing_protos"])
    from Testing_protos import Add_One_pb2_grpc
    from Testing_protos import AddTypes_pb2
    yagrc_importer.resolve_lazy_imports(grpc_channel)
    stub = Add_One_pb2_grpc.AdditionStub(grpc_channel)
    response = stub.AddOne(AddTypes_pb2.Addend(number=5))
    assert response.number == 6


def test_unresolved(lazy_cleaner):
    yagrc_importer.add_lazy_packages(["Testing_protos"])
    from Testing_protos import other_pb2
    try:
        a = other_pb2.random_attribute
        assert False
    except AttributeError as e:
        assert str(e).find("unresolved lazy module") >= 0


def test_unlazy(grpc_channel, lazy_cleaner):
    yagrc_importer.add_lazy_packages(["Testing_protos"])
    import collections
    yagrc_importer.resolve_lazy_imports(grpc_channel)


@pytest.mark.xfail(raises=ImportError, strict=True)
def test_bad_import(lazy_cleaner):
    yagrc_importer.add_lazy_packages(["Testing_protos"])
    from Testing_protos import bad_import
    assert False


@pytest.mark.xfail(raises=ImportError, strict=True)
def test_bad_package(lazy_cleaner):
    yagrc_importer.add_lazy_packages(["Testing_protos"])
    from bad_package import bad_import
    assert False


def test_resolve_fail(grpc_channel, lazy_cleaner):
    yagrc_importer.add_lazy_packages(["Testing_protos"])
    from Testing_protos import AddTypes_pb2

    try:
        yagrc_importer.resolve_lazy_imports(None)
        assert False
    except AttributeError:
        pass

    # Test failure again to verify first failure did not lose state.
    try:
        yagrc_importer.resolve_lazy_imports(None)
        assert False
    except AttributeError:
        pass

    # Finally, test success case to make sure prior failures did not break
    # things permanently, including the ability to do more lazy imports.
    from Testing_protos import Add_One_pb2_grpc
    yagrc_importer.resolve_lazy_imports(grpc_channel)
    stub = Add_One_pb2_grpc.AdditionStub(grpc_channel)
    response = stub.AddOne(AddTypes_pb2.Addend(number=5))
    assert response.number == 6
