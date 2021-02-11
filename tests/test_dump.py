import pytest
from yagrc import dump as yagrc_dump


def test_dump(grpc_channel):
    pb = yagrc_dump.dump_protocols(grpc_channel, symbols=["Testing.Addition"])
    assert len(pb) > 0
