# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: bytes2features.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='bytes2features.proto',
  package='',
  syntax='proto3',
  serialized_pb=_b('\n\x14\x62ytes2features.proto\"&\n\x15\x42ytes2FeaturesRequest\x12\r\n\x05input\x18\x01 \x01(\x0c\"\'\n\x13\x42ytes2FeaturesReply\x12\x10\n\x08\x66\x65\x61tures\x18\x01 \x03(\x02\x32G\n\x0e\x42ytes2Features\x12\x35\n\x03Run\x12\x16.Bytes2FeaturesRequest\x1a\x14.Bytes2FeaturesReply\"\x00\x62\x06proto3')
)




_BYTES2FEATURESREQUEST = _descriptor.Descriptor(
  name='Bytes2FeaturesRequest',
  full_name='Bytes2FeaturesRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='input', full_name='Bytes2FeaturesRequest.input', index=0,
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
  serialized_start=24,
  serialized_end=62,
)


_BYTES2FEATURESREPLY = _descriptor.Descriptor(
  name='Bytes2FeaturesReply',
  full_name='Bytes2FeaturesReply',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='features', full_name='Bytes2FeaturesReply.features', index=0,
      number=1, type=2, cpp_type=6, label=3,
      has_default_value=False, default_value=[],
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
  serialized_start=64,
  serialized_end=103,
)

DESCRIPTOR.message_types_by_name['Bytes2FeaturesRequest'] = _BYTES2FEATURESREQUEST
DESCRIPTOR.message_types_by_name['Bytes2FeaturesReply'] = _BYTES2FEATURESREPLY
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Bytes2FeaturesRequest = _reflection.GeneratedProtocolMessageType('Bytes2FeaturesRequest', (_message.Message,), dict(
  DESCRIPTOR = _BYTES2FEATURESREQUEST,
  __module__ = 'bytes2features_pb2'
  # @@protoc_insertion_point(class_scope:Bytes2FeaturesRequest)
  ))
_sym_db.RegisterMessage(Bytes2FeaturesRequest)

Bytes2FeaturesReply = _reflection.GeneratedProtocolMessageType('Bytes2FeaturesReply', (_message.Message,), dict(
  DESCRIPTOR = _BYTES2FEATURESREPLY,
  __module__ = 'bytes2features_pb2'
  # @@protoc_insertion_point(class_scope:Bytes2FeaturesReply)
  ))
_sym_db.RegisterMessage(Bytes2FeaturesReply)



_BYTES2FEATURES = _descriptor.ServiceDescriptor(
  name='Bytes2Features',
  full_name='Bytes2Features',
  file=DESCRIPTOR,
  index=0,
  options=None,
  serialized_start=105,
  serialized_end=176,
  methods=[
  _descriptor.MethodDescriptor(
    name='Run',
    full_name='Bytes2Features.Run',
    index=0,
    containing_service=None,
    input_type=_BYTES2FEATURESREQUEST,
    output_type=_BYTES2FEATURESREPLY,
    options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_BYTES2FEATURES)

DESCRIPTOR.services_by_name['Bytes2Features'] = _BYTES2FEATURES

# @@protoc_insertion_point(module_scope)
