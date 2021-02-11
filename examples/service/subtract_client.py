#!/usr/bin/python3
"""Non-reflection client for the subtract_server example service.

For comparison with the clients using `yagrc` for reflection.
"""
import logging

import grpc

from arithmetic import subtract_pb2
from arithmetic import subtract_pb2_grpc


def main():
    with grpc.insecure_channel("localhost:19002") as channel:
        stub = subtract_pb2_grpc.SubtractionStub(channel)
        response = stub.SubtractOne(subtract_pb2.Minuend(number=5))
    print(response)


if __name__ == '__main__':
    logging.basicConfig()
    main()
