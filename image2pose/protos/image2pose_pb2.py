# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: image2pose.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import pose_pb2 as pose__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='image2pose.proto',
  package='',
  syntax='proto3',
  serialized_pb=_b('\n\x10image2pose.proto\x1a\npose.proto\"\"\n\x11Image2PoseRequest\x12\r\n\x05image\x18\x01 \x01(\x0c\"-\n\x0fImage2PoseReply\x12\x1a\n\x06result\x18\x01 \x01(\x0b\x32\n.PoseFrame2;\n\nImage2Pose\x12-\n\x03Run\x12\x12.Image2PoseRequest\x1a\x10.Image2PoseReply\"\x00\x62\x06proto3')
  ,
  dependencies=[pose__pb2.DESCRIPTOR,])




_IMAGE2POSEREQUEST = _descriptor.Descriptor(
  name='Image2PoseRequest',
  full_name='Image2PoseRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='image', full_name='Image2PoseRequest.image', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=32,
  serialized_end=66,
)


_IMAGE2POSEREPLY = _descriptor.Descriptor(
  name='Image2PoseReply',
  full_name='Image2PoseReply',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='result', full_name='Image2PoseReply.result', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=68,
  serialized_end=113,
)

_IMAGE2POSEREPLY.fields_by_name['result'].message_type = pose__pb2._POSEFRAME
DESCRIPTOR.message_types_by_name['Image2PoseRequest'] = _IMAGE2POSEREQUEST
DESCRIPTOR.message_types_by_name['Image2PoseReply'] = _IMAGE2POSEREPLY
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Image2PoseRequest = _reflection.GeneratedProtocolMessageType('Image2PoseRequest', (_message.Message,), dict(
  DESCRIPTOR = _IMAGE2POSEREQUEST,
  __module__ = 'image2pose_pb2'
  # @@protoc_insertion_point(class_scope:Image2PoseRequest)
  ))
_sym_db.RegisterMessage(Image2PoseRequest)

Image2PoseReply = _reflection.GeneratedProtocolMessageType('Image2PoseReply', (_message.Message,), dict(
  DESCRIPTOR = _IMAGE2POSEREPLY,
  __module__ = 'image2pose_pb2'
  # @@protoc_insertion_point(class_scope:Image2PoseReply)
  ))
_sym_db.RegisterMessage(Image2PoseReply)



_IMAGE2POSE = _descriptor.ServiceDescriptor(
  name='Image2Pose',
  full_name='Image2Pose',
  file=DESCRIPTOR,
  index=0,
  options=None,
  serialized_start=115,
  serialized_end=174,
  methods=[
  _descriptor.MethodDescriptor(
    name='Run',
    full_name='Image2Pose.Run',
    index=0,
    containing_service=None,
    input_type=_IMAGE2POSEREQUEST,
    output_type=_IMAGE2POSEREPLY,
    options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_IMAGE2POSE)

DESCRIPTOR.services_by_name['Image2Pose'] = _IMAGE2POSE

# @@protoc_insertion_point(module_scope)
