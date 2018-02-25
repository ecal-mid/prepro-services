# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import frames2bytes_pb2 as frames2bytes__pb2


class Frames2BytesStub(object):
  """The service definition.
  """

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.Run = channel.unary_unary(
        '/Frames2Bytes/Run',
        request_serializer=frames2bytes__pb2.Frames2BytesRequest.SerializeToString,
        response_deserializer=frames2bytes__pb2.Frames2BytesReply.FromString,
        )


class Frames2BytesServicer(object):
  """The service definition.
  """

  def Run(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_Frames2BytesServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'Run': grpc.unary_unary_rpc_method_handler(
          servicer.Run,
          request_deserializer=frames2bytes__pb2.Frames2BytesRequest.FromString,
          response_serializer=frames2bytes__pb2.Frames2BytesReply.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'Frames2Bytes', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
