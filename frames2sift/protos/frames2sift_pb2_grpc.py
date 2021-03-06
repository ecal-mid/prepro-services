# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import frames2sift_pb2 as frames2sift__pb2


class Frames2SiftStub(object):
  """The service definition.
  """

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.Run = channel.unary_unary(
        '/Frames2Sift/Run',
        request_serializer=frames2sift__pb2.Frames2SiftRequest.SerializeToString,
        response_deserializer=frames2sift__pb2.Frames2SiftReply.FromString,
        )


class Frames2SiftServicer(object):
  """The service definition.
  """

  def Run(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_Frames2SiftServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'Run': grpc.unary_unary_rpc_method_handler(
          servicer.Run,
          request_deserializer=frames2sift__pb2.Frames2SiftRequest.FromString,
          response_serializer=frames2sift__pb2.Frames2SiftReply.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'Frames2Sift', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
