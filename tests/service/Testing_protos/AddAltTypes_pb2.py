# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: Testing_protos/AddAltTypes.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='Testing_protos/AddAltTypes.proto',
  package='Testing',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n Testing_protos/AddAltTypes.proto\x12\x07Testing\"\x18\n\x06\x41\x64\x64\x65nd\x12\x0e\n\x06number\x18\x01 \x01(\x05\"\x15\n\x03Sum\x12\x0e\n\x06number\x18\x01 \x01(\x05\x62\x06proto3'
)




_ADDEND = _descriptor.Descriptor(
  name='Addend',
  full_name='Testing.Addend',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='number', full_name='Testing.Addend.number', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
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
  serialized_start=45,
  serialized_end=69,
)


_SUM = _descriptor.Descriptor(
  name='Sum',
  full_name='Testing.Sum',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='number', full_name='Testing.Sum.number', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
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
  serialized_start=71,
  serialized_end=92,
)

DESCRIPTOR.message_types_by_name['Addend'] = _ADDEND
DESCRIPTOR.message_types_by_name['Sum'] = _SUM
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Addend = _reflection.GeneratedProtocolMessageType('Addend', (_message.Message,), {
  'DESCRIPTOR' : _ADDEND,
  '__module__' : 'Testing_protos.AddAltTypes_pb2'
  # @@protoc_insertion_point(class_scope:Testing.Addend)
  })
_sym_db.RegisterMessage(Addend)

Sum = _reflection.GeneratedProtocolMessageType('Sum', (_message.Message,), {
  'DESCRIPTOR' : _SUM,
  '__module__' : 'Testing_protos.AddAltTypes_pb2'
  # @@protoc_insertion_point(class_scope:Testing.Sum)
  })
_sym_db.RegisterMessage(Sum)


# @@protoc_insertion_point(module_scope)
