#!/usr/bin/python3
"""Server for the ridiculous Subtraction service.

This is meant for running this project's examples against.

Note that `arithmetic.subtract_pb2` and `arithmetic.subtract_pb2_grpc` are
deliberately kept out of the import path for the reflection-based example
clients, but the service needs them.
"""
from concurrent import futures
import logging

import grpc
from grpc_reflection.v1alpha import reflection

from arithmetic import subtract_pb2
from arithmetic import subtract_pb2_grpc


class Subtraction(subtract_pb2_grpc.SubtractionServicer):

    def SubtractOne(self, request, context):
        return subtract_pb2.Difference(number=request.number - 1)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    subtract_pb2_grpc.add_SubtractionServicer_to_server(Subtraction(), server)
    service_names = (
        subtract_pb2.DESCRIPTOR.services_by_name['Subtraction'].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(service_names, server)
    server.add_insecure_port('[::]:19002')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
