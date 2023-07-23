"""Utility function to dump FileDescriptorSet protocol buffers."""
from google.protobuf import descriptor_pb2

from yagrc import reflector


def dump_protocols(channel, filenames=None, symbols=None):
    """Get serialized FileDescriptorSet message via reflection.

    See `yagrc.reflector.GrpcReflectionClient.load_protocols` for arg and
    exception details.
    """
    fdset = descriptor_pb2.FileDescriptorSet()
    grpc_reflector = reflector.GrpcReflectionEngine()
    for filename in grpc_reflector.load_protocols(channel, filenames, symbols):
        proto = descriptor_pb2.FileDescriptorProto()
        descr = grpc_reflector.file_descriptor(filename)
        descr.CopyToProto(proto)
        fdset.file.append(proto)  # pylint: disable=no-member
    return fdset.SerializeToString()
