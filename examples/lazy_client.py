#!/usr/bin/python3
"""Lazy `yagrc.importer` client for the subtract_server example service."""
import logging

import grpc
from yagrc import importer as yagrc_importer

yagrc_importer.add_lazy_packages(["arithmetic"])

from arithmetic import subtract_pb2
from arithmetic import subtract_pb2_grpc


def main():
    with grpc.insecure_channel("localhost:19002") as channel:
        yagrc_importer.resolve_lazy_imports(channel)

        stub = subtract_pb2_grpc.SubtractionStub(channel)
        response = stub.SubtractOne(subtract_pb2.Minuend(number=5))
    print(response)


if __name__ == '__main__':
    logging.basicConfig()
    main()
