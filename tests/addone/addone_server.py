#!/usr/bin/python3
"""Server for the ridiculous Addition service.

This is meant only for running this project's test cases against.
"""
from concurrent import futures
import logging

import grpc
from grpc_reflection.v1alpha import reflection

# See comments in Add_One.proto about terrible naming
from Testing_protos import Add_One_pb2
from Testing_protos import Add_One_pb2_grpc
from Testing_protos import AddTypes_pb2


class Addition(Add_One_pb2_grpc.AdditionServicer):

    def __init__(self):
        super().__init__()
        self.count = 0

    def AddOne(self, request, context):
        self.count += 1
        return AddTypes_pb2.Sum(number=request.number + 1)

    def AddOnes(self, request, context):
        self.count += 1
        return (AddTypes_pb2.Sum(number=request.number + x + 1)
                for x in range(request.number))

    def AddsOne(self, request_iterator, context):
        self.count += 1
        return AddTypes_pb2.Sum(
            number=sum(request.number for request in request_iterator) + 1)

    def AddsOnes(self, request_iterator, context):
        self.count += 1
        return (AddTypes_pb2.Sum(number=request.number + 1)
                for request in request_iterator)

    def Status(self, request, context):
        self.count += 1
        if request.HasField("count"):
            return AddTypes_pb2.StatusResponse(count={"number": self.count})
        if request.HasField("state"):
            response = AddTypes_pb2.StatusResponse()
            response.state.states[
                "sum_engine"].state = AddTypes_pb2.ServiceState.READY
            response.state.states[
                "difference_engine"].state = AddTypes_pb2.ServiceState.BUSY_COMPUTING_ONE
            response.state.states[
                "chaos_engine"].state = AddTypes_pb2.ServiceState._UNKNOWN
            return response
        raise NotImplementedError("request not implemented: " +
                                  request.WhichOneof("query"))


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    Add_One_pb2_grpc.add_AdditionServicer_to_server(Addition(), server)
    service_names = (
        Add_One_pb2.DESCRIPTOR.services_by_name['Addition'].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(service_names, server)
    server.add_insecure_port('[::]:19001')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
