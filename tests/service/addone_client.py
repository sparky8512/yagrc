#!/usr/bin/python3
"""Non-reflection client for the addone_server test service.

This is not meant to be useful. See the clients in the examples directory for
slightly more useful grpc client code.
"""

import grpc

# See comments in Add_One.proto about terrible naming
from Testing_protos import Add_One_pb2_grpc
from Testing_protos import AddTypes_pb2


def main():
    with grpc.insecure_channel("localhost:19001") as channel:
        stub = Add_One_pb2_grpc.AdditionStub(channel)

        response = stub.AddOne(AddTypes_pb2.Addend(number=5))
        print(response)

        responses = stub.AddOnes(AddTypes_pb2.Addend(number=5))
        print(*responses)

        response = stub.AddsOne(
            (AddTypes_pb2.Addend(number=x) for x in range(5)))
        print(response)

        responses = stub.AddsOnes(
            (AddTypes_pb2.Addend(number=x) for x in range(5)))
        print(*responses)

        response = stub.Status(AddTypes_pb2.StatusQuery(count={}))
        print(response)

        response = stub.Status(AddTypes_pb2.StatusQuery(state={}))
        print(response)


if __name__ == '__main__':
    logging.basicConfig()
    main()
