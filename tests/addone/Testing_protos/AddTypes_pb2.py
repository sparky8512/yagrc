# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: Testing_protos/AddTypes.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from Testing_protos import AddAltTypes_pb2 as Testing__protos_dot_AddAltTypes__pb2

from Testing_protos.AddAltTypes_pb2 import *

DESCRIPTOR = _descriptor.FileDescriptor(
  name='Testing_protos/AddTypes.proto',
  package='Testing',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x1dTesting_protos/AddTypes.proto\x12\x07Testing\x1a Testing_protos/AddAltTypes.proto\"\x84\x01\n\x0bStatusQuery\x12,\n\x05\x63ount\x18\xe9\x07 \x01(\x0b\x32\x1a.Testing.StatusQuery.CountH\x00\x12,\n\x05state\x18\xea\x07 \x01(\x0b\x32\x1a.Testing.StatusQuery.StateH\x00\x1a\x07\n\x05\x43ount\x1a\x07\n\x05StateB\x07\n\x05query\"\xe3\x02\n\x0eStatusResponse\x12/\n\x05\x63ount\x18\xd1\x0f \x01(\x0b\x32\x1d.Testing.StatusResponse.CountH\x00\x12/\n\x05state\x18\xd2\x0f \x01(\x0b\x32\x1d.Testing.StatusResponse.StateH\x00\x1a\x17\n\x05\x43ount\x12\x0e\n\x06number\x18\x01 \x01(\r\x1a\xc9\x01\n\x05State\x12\x39\n\x06states\x18\x01 \x03(\x0b\x32).Testing.StatusResponse.State.StatesEntry\x1a/\n\x07Wrapper\x12$\n\x05state\x18\x01 \x01(\x0e\x32\x15.Testing.ServiceState\x1aT\n\x0bStatesEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x34\n\x05value\x18\x02 \x01(\x0b\x32%.Testing.StatusResponse.State.Wrapper:\x02\x38\x01\x42\n\n\x08response*?\n\x0cServiceState\x12\x0c\n\x08_UNKNOWN\x10\x00\x12\x16\n\x12\x42USY_COMPUTING_ONE\x10\x01\x12\t\n\x05READY\x10\x02P\x00\x62\x06proto3'
  ,
  dependencies=[Testing__protos_dot_AddAltTypes__pb2.DESCRIPTOR,],
  public_dependencies=[Testing__protos_dot_AddAltTypes__pb2.DESCRIPTOR,])

_SERVICESTATE = _descriptor.EnumDescriptor(
  name='ServiceState',
  full_name='Testing.ServiceState',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='_UNKNOWN', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='BUSY_COMPUTING_ONE', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='READY', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=569,
  serialized_end=632,
)
_sym_db.RegisterEnumDescriptor(_SERVICESTATE)

ServiceState = enum_type_wrapper.EnumTypeWrapper(_SERVICESTATE)
_UNKNOWN = 0
BUSY_COMPUTING_ONE = 1
READY = 2



_STATUSQUERY_COUNT = _descriptor.Descriptor(
  name='Count',
  full_name='Testing.StatusQuery.Count',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
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
  serialized_start=184,
  serialized_end=191,
)

_STATUSQUERY_STATE = _descriptor.Descriptor(
  name='State',
  full_name='Testing.StatusQuery.State',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
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
  serialized_start=193,
  serialized_end=200,
)

_STATUSQUERY = _descriptor.Descriptor(
  name='StatusQuery',
  full_name='Testing.StatusQuery',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='count', full_name='Testing.StatusQuery.count', index=0,
      number=1001, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='state', full_name='Testing.StatusQuery.state', index=1,
      number=1002, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[_STATUSQUERY_COUNT, _STATUSQUERY_STATE, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='query', full_name='Testing.StatusQuery.query',
      index=0, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
  ],
  serialized_start=77,
  serialized_end=209,
)


_STATUSRESPONSE_COUNT = _descriptor.Descriptor(
  name='Count',
  full_name='Testing.StatusResponse.Count',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='number', full_name='Testing.StatusResponse.Count.number', index=0,
      number=1, type=13, cpp_type=3, label=1,
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
  serialized_start=328,
  serialized_end=351,
)

_STATUSRESPONSE_STATE_WRAPPER = _descriptor.Descriptor(
  name='Wrapper',
  full_name='Testing.StatusResponse.State.Wrapper',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='state', full_name='Testing.StatusResponse.State.Wrapper.state', index=0,
      number=1, type=14, cpp_type=8, label=1,
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
  serialized_start=422,
  serialized_end=469,
)

_STATUSRESPONSE_STATE_STATESENTRY = _descriptor.Descriptor(
  name='StatesEntry',
  full_name='Testing.StatusResponse.State.StatesEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='Testing.StatusResponse.State.StatesEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='value', full_name='Testing.StatusResponse.State.StatesEntry.value', index=1,
      number=2, type=11, cpp_type=10, label=1,
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
  serialized_options=b'8\001',
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=471,
  serialized_end=555,
)

_STATUSRESPONSE_STATE = _descriptor.Descriptor(
  name='State',
  full_name='Testing.StatusResponse.State',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='states', full_name='Testing.StatusResponse.State.states', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[_STATUSRESPONSE_STATE_WRAPPER, _STATUSRESPONSE_STATE_STATESENTRY, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=354,
  serialized_end=555,
)

_STATUSRESPONSE = _descriptor.Descriptor(
  name='StatusResponse',
  full_name='Testing.StatusResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='count', full_name='Testing.StatusResponse.count', index=0,
      number=2001, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='state', full_name='Testing.StatusResponse.state', index=1,
      number=2002, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[_STATUSRESPONSE_COUNT, _STATUSRESPONSE_STATE, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='response', full_name='Testing.StatusResponse.response',
      index=0, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
  ],
  serialized_start=212,
  serialized_end=567,
)

_STATUSQUERY_COUNT.containing_type = _STATUSQUERY
_STATUSQUERY_STATE.containing_type = _STATUSQUERY
_STATUSQUERY.fields_by_name['count'].message_type = _STATUSQUERY_COUNT
_STATUSQUERY.fields_by_name['state'].message_type = _STATUSQUERY_STATE
_STATUSQUERY.oneofs_by_name['query'].fields.append(
  _STATUSQUERY.fields_by_name['count'])
_STATUSQUERY.fields_by_name['count'].containing_oneof = _STATUSQUERY.oneofs_by_name['query']
_STATUSQUERY.oneofs_by_name['query'].fields.append(
  _STATUSQUERY.fields_by_name['state'])
_STATUSQUERY.fields_by_name['state'].containing_oneof = _STATUSQUERY.oneofs_by_name['query']
_STATUSRESPONSE_COUNT.containing_type = _STATUSRESPONSE
_STATUSRESPONSE_STATE_WRAPPER.fields_by_name['state'].enum_type = _SERVICESTATE
_STATUSRESPONSE_STATE_WRAPPER.containing_type = _STATUSRESPONSE_STATE
_STATUSRESPONSE_STATE_STATESENTRY.fields_by_name['value'].message_type = _STATUSRESPONSE_STATE_WRAPPER
_STATUSRESPONSE_STATE_STATESENTRY.containing_type = _STATUSRESPONSE_STATE
_STATUSRESPONSE_STATE.fields_by_name['states'].message_type = _STATUSRESPONSE_STATE_STATESENTRY
_STATUSRESPONSE_STATE.containing_type = _STATUSRESPONSE
_STATUSRESPONSE.fields_by_name['count'].message_type = _STATUSRESPONSE_COUNT
_STATUSRESPONSE.fields_by_name['state'].message_type = _STATUSRESPONSE_STATE
_STATUSRESPONSE.oneofs_by_name['response'].fields.append(
  _STATUSRESPONSE.fields_by_name['count'])
_STATUSRESPONSE.fields_by_name['count'].containing_oneof = _STATUSRESPONSE.oneofs_by_name['response']
_STATUSRESPONSE.oneofs_by_name['response'].fields.append(
  _STATUSRESPONSE.fields_by_name['state'])
_STATUSRESPONSE.fields_by_name['state'].containing_oneof = _STATUSRESPONSE.oneofs_by_name['response']
DESCRIPTOR.message_types_by_name['StatusQuery'] = _STATUSQUERY
DESCRIPTOR.message_types_by_name['StatusResponse'] = _STATUSRESPONSE
DESCRIPTOR.enum_types_by_name['ServiceState'] = _SERVICESTATE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

StatusQuery = _reflection.GeneratedProtocolMessageType('StatusQuery', (_message.Message,), {

  'Count' : _reflection.GeneratedProtocolMessageType('Count', (_message.Message,), {
    'DESCRIPTOR' : _STATUSQUERY_COUNT,
    '__module__' : 'Testing_protos.AddTypes_pb2'
    # @@protoc_insertion_point(class_scope:Testing.StatusQuery.Count)
    })
  ,

  'State' : _reflection.GeneratedProtocolMessageType('State', (_message.Message,), {
    'DESCRIPTOR' : _STATUSQUERY_STATE,
    '__module__' : 'Testing_protos.AddTypes_pb2'
    # @@protoc_insertion_point(class_scope:Testing.StatusQuery.State)
    })
  ,
  'DESCRIPTOR' : _STATUSQUERY,
  '__module__' : 'Testing_protos.AddTypes_pb2'
  # @@protoc_insertion_point(class_scope:Testing.StatusQuery)
  })
_sym_db.RegisterMessage(StatusQuery)
_sym_db.RegisterMessage(StatusQuery.Count)
_sym_db.RegisterMessage(StatusQuery.State)

StatusResponse = _reflection.GeneratedProtocolMessageType('StatusResponse', (_message.Message,), {

  'Count' : _reflection.GeneratedProtocolMessageType('Count', (_message.Message,), {
    'DESCRIPTOR' : _STATUSRESPONSE_COUNT,
    '__module__' : 'Testing_protos.AddTypes_pb2'
    # @@protoc_insertion_point(class_scope:Testing.StatusResponse.Count)
    })
  ,

  'State' : _reflection.GeneratedProtocolMessageType('State', (_message.Message,), {

    'Wrapper' : _reflection.GeneratedProtocolMessageType('Wrapper', (_message.Message,), {
      'DESCRIPTOR' : _STATUSRESPONSE_STATE_WRAPPER,
      '__module__' : 'Testing_protos.AddTypes_pb2'
      # @@protoc_insertion_point(class_scope:Testing.StatusResponse.State.Wrapper)
      })
    ,

    'StatesEntry' : _reflection.GeneratedProtocolMessageType('StatesEntry', (_message.Message,), {
      'DESCRIPTOR' : _STATUSRESPONSE_STATE_STATESENTRY,
      '__module__' : 'Testing_protos.AddTypes_pb2'
      # @@protoc_insertion_point(class_scope:Testing.StatusResponse.State.StatesEntry)
      })
    ,
    'DESCRIPTOR' : _STATUSRESPONSE_STATE,
    '__module__' : 'Testing_protos.AddTypes_pb2'
    # @@protoc_insertion_point(class_scope:Testing.StatusResponse.State)
    })
  ,
  'DESCRIPTOR' : _STATUSRESPONSE,
  '__module__' : 'Testing_protos.AddTypes_pb2'
  # @@protoc_insertion_point(class_scope:Testing.StatusResponse)
  })
_sym_db.RegisterMessage(StatusResponse)
_sym_db.RegisterMessage(StatusResponse.Count)
_sym_db.RegisterMessage(StatusResponse.State)
_sym_db.RegisterMessage(StatusResponse.State.Wrapper)
_sym_db.RegisterMessage(StatusResponse.State.StatesEntry)


_STATUSRESPONSE_STATE_STATESENTRY._options = None
# @@protoc_insertion_point(module_scope)
