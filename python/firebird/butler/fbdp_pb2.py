# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: firebird/butler/fbdp.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='firebird/butler/fbdp.proto',
  package='firebird.butler',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x1a\x66irebird/butler/fbdp.proto\x12\x0f\x66irebird.butler\x1a\x1cgoogle/protobuf/struct.proto\"}\n\x11\x46\x42\x44POpenDataframe\x12\x11\n\tdata_pipe\x18\x01 \x01(\t\x12\x13\n\x0bpipe_socket\x18\x02 \x01(\r\x12\x13\n\x0b\x64\x61ta_format\x18\x03 \x01(\t\x12+\n\nparameters\x18\x04 \x01(\x0b\x32\x17.google.protobuf.Structb\x06proto3'
  ,
  dependencies=[google_dot_protobuf_dot_struct__pb2.DESCRIPTOR,])




_FBDPOPENDATAFRAME = _descriptor.Descriptor(
  name='FBDPOpenDataframe',
  full_name='firebird.butler.FBDPOpenDataframe',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='data_pipe', full_name='firebird.butler.FBDPOpenDataframe.data_pipe', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='pipe_socket', full_name='firebird.butler.FBDPOpenDataframe.pipe_socket', index=1,
      number=2, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='data_format', full_name='firebird.butler.FBDPOpenDataframe.data_format', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='parameters', full_name='firebird.butler.FBDPOpenDataframe.parameters', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=77,
  serialized_end=202,
)

_FBDPOPENDATAFRAME.fields_by_name['parameters'].message_type = google_dot_protobuf_dot_struct__pb2._STRUCT
DESCRIPTOR.message_types_by_name['FBDPOpenDataframe'] = _FBDPOPENDATAFRAME
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

FBDPOpenDataframe = _reflection.GeneratedProtocolMessageType('FBDPOpenDataframe', (_message.Message,), {
  'DESCRIPTOR' : _FBDPOPENDATAFRAME,
  '__module__' : 'firebird.butler.fbdp_pb2'
  # @@protoc_insertion_point(class_scope:firebird.butler.FBDPOpenDataframe)
  })
_sym_db.RegisterMessage(FBDPOpenDataframe)


# @@protoc_insertion_point(module_scope)
