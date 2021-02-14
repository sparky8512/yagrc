#!/usr/bin/python3
"""`yagrc.importer` client for the subtract_server example service."""
import logging

import grpc
from yagrc import importer as yagrc_importer


def main():
    importer = yagrc_importer.GrpcImporter()

    with grpc.insecure_channel("localhost:19002") as channel:
        importer.configure(channel, filenames=["arithmetic/subtract.proto"])

        from arithmetic import subtract_pb2
        from arithmetic import subtract_pb2_grpc

        stub = subtract_pb2_grpc.SubtractionStub(channel)
        response = stub.SubtractOne(subtract_pb2.Minuend(number=5))
    print(response)


if __name__ == '__main__':
    logging.basicConfig()
    main()
