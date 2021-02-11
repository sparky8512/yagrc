#!/usr/bin/python3
"""`yagrc.reflector` client for the subtract_server example service."""
import logging

import grpc
from yagrc import reflector


def main():
    grpc_reflector = reflector.GrpcReflectionClient()

    with grpc.insecure_channel("localhost:19002") as channel:
        grpc_reflector.load_protocols(channel,
                                      symbols=["Arithmetic.Subtraction"])
        stub_class = grpc_reflector.service_stub_class("Arithmetic.Subtraction")
        request_class = grpc_reflector.message_class("Arithmetic.Minuend")

        stub = stub_class(channel)
        response = stub.SubtractOne(request_class(number=5))
    print(response)


if __name__ == '__main__':
    logging.basicConfig()
    main()
