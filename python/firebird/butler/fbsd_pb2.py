# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: firebird/butler/fbsd.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import any_pb2 as google_dot_protobuf_dot_any__pb2
from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='firebird/butler/fbsd.proto',
  package='firebird.butler',
  syntax='proto3',
  serialized_pb=_b('\n\x1a\x66irebird/butler/fbsd.proto\x12\x0f\x66irebird.butler\x1a\x19google/protobuf/any.proto\x1a\x1cgoogle/protobuf/struct.proto\"\x88\x01\n\x0f\x45ndpointAddress\x12.\n\x06\x64omain\x18\x01 \x01(\x0e\x32\x1e.firebird.butler.AddressDomain\x12\x34\n\x08protocol\x18\x02 \x01(\x0e\x32\".firebird.butler.TransportProtocol\x12\x0f\n\x07\x61\x64\x64ress\x18\x03 \x01(\t\"*\n\nPlatformId\x12\x0b\n\x03uid\x18\x01 \x01(\x0c\x12\x0f\n\x07version\x18\x02 \x01(\t\"\x17\n\x08VendorId\x12\x0b\n\x03uid\x18\x01 \x01(\x0c\"\xdd\x01\n\x13\x41gentIdentification\x12\x0b\n\x03uid\x18\x01 \x01(\x0c\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x0f\n\x07version\x18\x03 \x01(\t\x12)\n\x06vendor\x18\x04 \x01(\x0b\x32\x19.firebird.butler.VendorId\x12-\n\x08platform\x18\x05 \x01(\x0b\x32\x1b.firebird.butler.PlatformId\x12\x16\n\x0e\x63lassification\x18\x06 \x01(\t\x12(\n\nsupplement\x18\x07 \x03(\x0b\x32\x14.google.protobuf.Any\"f\n\x12PeerIdentification\x12\x0b\n\x03uid\x18\x01 \x01(\x0c\x12\x0b\n\x03pid\x18\x02 \x01(\r\x12\x0c\n\x04host\x18\x03 \x01(\t\x12(\n\nsupplement\x18\x04 \x03(\x0b\x32\x14.google.protobuf.Any\",\n\rInterfaceSpec\x12\x0e\n\x06number\x18\x01 \x01(\r\x12\x0b\n\x03uid\x18\x02 \x01(\x0c\"\x8c\x01\n\x10\x45rrorDescription\x12\x0c\n\x04\x63ode\x18\x01 \x01(\x04\x12\x13\n\x0b\x64\x65scription\x18\x02 \x01(\t\x12(\n\x07\x63ontext\x18\x03 \x01(\x0b\x32\x17.google.protobuf.Struct\x12+\n\nannotation\x18\x04 \x01(\x0b\x32\x17.google.protobuf.Struct\"\x8e\x02\n\x08\x44\x61taPipe\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x30\n\x0bsocket_type\x18\x02 \x01(\x0e\x32\x1b.firebird.butler.SocketType\x12\'\n\x03use\x18\x03 \x01(\x0e\x32\x1a.firebird.butler.SocketUse\x12\x10\n\x08protocol\x18\x04 \x01(\t\x12\r\n\x05owner\x18\x05 \x01(\x0c\x12\x0b\n\x03pid\x18\x06 \x01(\r\x12\x0c\n\x04host\x18\x07 \x01(\t\x12\x33\n\tendpoints\x18\x08 \x03(\x0b\x32 .firebird.butler.EndpointAddress\x12(\n\nsupplement\x18\t \x03(\x0b\x32\x14.google.protobuf.Any*\xa4\x01\n\x05State\x12\x11\n\rUNKNOWN_STATE\x10\x00\x12\t\n\x05READY\x10\x01\x12\x0b\n\x07RUNNING\x10\x02\x12\x0b\n\x07WAITING\x10\x03\x12\r\n\tSUSPENDED\x10\x04\x12\x0c\n\x08\x46INISHED\x10\x05\x12\x0b\n\x07\x41\x42ORTED\x10\x06\x12\x0b\n\x07\x43REATED\x10\x01\x12\x0b\n\x07\x42LOCKED\x10\x03\x12\x0b\n\x07STOPPED\x10\x04\x12\x0e\n\nTERMINATED\x10\x06\x1a\x02\x10\x01*E\n\rAddressDomain\x12\x12\n\x0eUNKNOWN_DOMAIN\x10\x00\x12\t\n\x05LOCAL\x10\x01\x12\x08\n\x04NODE\x10\x02\x12\x0b\n\x07NETWORK\x10\x03*d\n\x11TransportProtocol\x12\x14\n\x10UNKNOWN_PROTOCOL\x10\x00\x12\n\n\x06INPROC\x10\x01\x12\x07\n\x03IPC\x10\x02\x12\x07\n\x03TCP\x10\x03\x12\x07\n\x03PGM\x10\x04\x12\x08\n\x04\x45PGM\x10\x05\x12\x08\n\x04VMCI\x10\x06*\x86\x01\n\nSocketType\x12\x10\n\x0cUNKNOWN_TYPE\x10\x00\x12\n\n\x06\x44\x45\x41LER\x10\x01\x12\n\n\x06ROUTER\x10\x02\x12\x07\n\x03PUB\x10\x03\x12\x07\n\x03SUB\x10\x04\x12\x08\n\x04XPUB\x10\x05\x12\x08\n\x04XSUB\x10\x06\x12\x08\n\x04PUSH\x10\x07\x12\x08\n\x04PULL\x10\x08\x12\n\n\x06STREAM\x10\t\x12\x08\n\x04PAIR\x10\n*F\n\tSocketUse\x12\x0f\n\x0bUNKNOWN_USE\x10\x00\x12\x0c\n\x08PRODUCER\x10\x01\x12\x0c\n\x08\x43ONSUMER\x10\x02\x12\x0c\n\x08\x45XCHANGE\x10\x03*P\n\x0e\x44\x65pendencyType\x12\x13\n\x0fUNKNOWN_DEPTYPE\x10\x00\x12\x0c\n\x08REQUIRED\x10\x01\x12\r\n\tPREFERRED\x10\x02\x12\x0c\n\x08OPTIONAL\x10\x03\x62\x06proto3')
  ,
  dependencies=[google_dot_protobuf_dot_any__pb2.DESCRIPTOR,google_dot_protobuf_dot_struct__pb2.DESCRIPTOR,])

_STATE = _descriptor.EnumDescriptor(
  name='State',
  full_name='firebird.butler.State',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='UNKNOWN_STATE', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='READY', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='RUNNING', index=2, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='WAITING', index=3, number=3,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SUSPENDED', index=4, number=4,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='FINISHED', index=5, number=5,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ABORTED', index=6, number=6,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CREATED', index=7, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='BLOCKED', index=8, number=3,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='STOPPED', index=9, number=4,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='TERMINATED', index=10, number=6,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=_descriptor._ParseOptions(descriptor_pb2.EnumOptions(), _b('\020\001')),
  serialized_start=1103,
  serialized_end=1267,
)
_sym_db.RegisterEnumDescriptor(_STATE)

State = enum_type_wrapper.EnumTypeWrapper(_STATE)
_ADDRESSDOMAIN = _descriptor.EnumDescriptor(
  name='AddressDomain',
  full_name='firebird.butler.AddressDomain',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='UNKNOWN_DOMAIN', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='LOCAL', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='NODE', index=2, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='NETWORK', index=3, number=3,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=1269,
  serialized_end=1338,
)
_sym_db.RegisterEnumDescriptor(_ADDRESSDOMAIN)

AddressDomain = enum_type_wrapper.EnumTypeWrapper(_ADDRESSDOMAIN)
_TRANSPORTPROTOCOL = _descriptor.EnumDescriptor(
  name='TransportProtocol',
  full_name='firebird.butler.TransportProtocol',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='UNKNOWN_PROTOCOL', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='INPROC', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='IPC', index=2, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='TCP', index=3, number=3,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='PGM', index=4, number=4,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='EPGM', index=5, number=5,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='VMCI', index=6, number=6,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=1340,
  serialized_end=1440,
)
_sym_db.RegisterEnumDescriptor(_TRANSPORTPROTOCOL)

TransportProtocol = enum_type_wrapper.EnumTypeWrapper(_TRANSPORTPROTOCOL)
_SOCKETTYPE = _descriptor.EnumDescriptor(
  name='SocketType',
  full_name='firebird.butler.SocketType',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='UNKNOWN_TYPE', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='DEALER', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ROUTER', index=2, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='PUB', index=3, number=3,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SUB', index=4, number=4,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='XPUB', index=5, number=5,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='XSUB', index=6, number=6,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='PUSH', index=7, number=7,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='PULL', index=8, number=8,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='STREAM', index=9, number=9,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='PAIR', index=10, number=10,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=1443,
  serialized_end=1577,
)
_sym_db.RegisterEnumDescriptor(_SOCKETTYPE)

SocketType = enum_type_wrapper.EnumTypeWrapper(_SOCKETTYPE)
_SOCKETUSE = _descriptor.EnumDescriptor(
  name='SocketUse',
  full_name='firebird.butler.SocketUse',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='UNKNOWN_USE', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='PRODUCER', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CONSUMER', index=2, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='EXCHANGE', index=3, number=3,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=1579,
  serialized_end=1649,
)
_sym_db.RegisterEnumDescriptor(_SOCKETUSE)

SocketUse = enum_type_wrapper.EnumTypeWrapper(_SOCKETUSE)
_DEPENDENCYTYPE = _descriptor.EnumDescriptor(
  name='DependencyType',
  full_name='firebird.butler.DependencyType',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='UNKNOWN_DEPTYPE', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='REQUIRED', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='PREFERRED', index=2, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='OPTIONAL', index=3, number=3,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=1651,
  serialized_end=1731,
)
_sym_db.RegisterEnumDescriptor(_DEPENDENCYTYPE)

DependencyType = enum_type_wrapper.EnumTypeWrapper(_DEPENDENCYTYPE)
UNKNOWN_STATE = 0
READY = 1
RUNNING = 2
WAITING = 3
SUSPENDED = 4
FINISHED = 5
ABORTED = 6
CREATED = 1
BLOCKED = 3
STOPPED = 4
TERMINATED = 6
UNKNOWN_DOMAIN = 0
LOCAL = 1
NODE = 2
NETWORK = 3
UNKNOWN_PROTOCOL = 0
INPROC = 1
IPC = 2
TCP = 3
PGM = 4
EPGM = 5
VMCI = 6
UNKNOWN_TYPE = 0
DEALER = 1
ROUTER = 2
PUB = 3
SUB = 4
XPUB = 5
XSUB = 6
PUSH = 7
PULL = 8
STREAM = 9
PAIR = 10
UNKNOWN_USE = 0
PRODUCER = 1
CONSUMER = 2
EXCHANGE = 3
UNKNOWN_DEPTYPE = 0
REQUIRED = 1
PREFERRED = 2
OPTIONAL = 3



_ENDPOINTADDRESS = _descriptor.Descriptor(
  name='EndpointAddress',
  full_name='firebird.butler.EndpointAddress',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='domain', full_name='firebird.butler.EndpointAddress.domain', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='protocol', full_name='firebird.butler.EndpointAddress.protocol', index=1,
      number=2, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='address', full_name='firebird.butler.EndpointAddress.address', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
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
  serialized_start=105,
  serialized_end=241,
)


_PLATFORMID = _descriptor.Descriptor(
  name='PlatformId',
  full_name='firebird.butler.PlatformId',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='uid', full_name='firebird.butler.PlatformId.uid', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='version', full_name='firebird.butler.PlatformId.version', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
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
  serialized_start=243,
  serialized_end=285,
)


_VENDORID = _descriptor.Descriptor(
  name='VendorId',
  full_name='firebird.butler.VendorId',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='uid', full_name='firebird.butler.VendorId.uid', index=0,
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
  serialized_start=287,
  serialized_end=310,
)


_AGENTIDENTIFICATION = _descriptor.Descriptor(
  name='AgentIdentification',
  full_name='firebird.butler.AgentIdentification',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='uid', full_name='firebird.butler.AgentIdentification.uid', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='name', full_name='firebird.butler.AgentIdentification.name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='version', full_name='firebird.butler.AgentIdentification.version', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='vendor', full_name='firebird.butler.AgentIdentification.vendor', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='platform', full_name='firebird.butler.AgentIdentification.platform', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='classification', full_name='firebird.butler.AgentIdentification.classification', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='supplement', full_name='firebird.butler.AgentIdentification.supplement', index=6,
      number=7, type=11, cpp_type=10, label=3,
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
  serialized_start=313,
  serialized_end=534,
)


_PEERIDENTIFICATION = _descriptor.Descriptor(
  name='PeerIdentification',
  full_name='firebird.butler.PeerIdentification',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='uid', full_name='firebird.butler.PeerIdentification.uid', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='pid', full_name='firebird.butler.PeerIdentification.pid', index=1,
      number=2, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='host', full_name='firebird.butler.PeerIdentification.host', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='supplement', full_name='firebird.butler.PeerIdentification.supplement', index=3,
      number=4, type=11, cpp_type=10, label=3,
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
  serialized_start=536,
  serialized_end=638,
)


_INTERFACESPEC = _descriptor.Descriptor(
  name='InterfaceSpec',
  full_name='firebird.butler.InterfaceSpec',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='number', full_name='firebird.butler.InterfaceSpec.number', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='uid', full_name='firebird.butler.InterfaceSpec.uid', index=1,
      number=2, type=12, cpp_type=9, label=1,
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
  serialized_start=640,
  serialized_end=684,
)


_ERRORDESCRIPTION = _descriptor.Descriptor(
  name='ErrorDescription',
  full_name='firebird.butler.ErrorDescription',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='code', full_name='firebird.butler.ErrorDescription.code', index=0,
      number=1, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='description', full_name='firebird.butler.ErrorDescription.description', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='context', full_name='firebird.butler.ErrorDescription.context', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='annotation', full_name='firebird.butler.ErrorDescription.annotation', index=3,
      number=4, type=11, cpp_type=10, label=1,
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
  serialized_start=687,
  serialized_end=827,
)


_DATAPIPE = _descriptor.Descriptor(
  name='DataPipe',
  full_name='firebird.butler.DataPipe',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='firebird.butler.DataPipe.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='socket_type', full_name='firebird.butler.DataPipe.socket_type', index=1,
      number=2, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='use', full_name='firebird.butler.DataPipe.use', index=2,
      number=3, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='protocol', full_name='firebird.butler.DataPipe.protocol', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='owner', full_name='firebird.butler.DataPipe.owner', index=4,
      number=5, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='pid', full_name='firebird.butler.DataPipe.pid', index=5,
      number=6, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='host', full_name='firebird.butler.DataPipe.host', index=6,
      number=7, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='endpoints', full_name='firebird.butler.DataPipe.endpoints', index=7,
      number=8, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='supplement', full_name='firebird.butler.DataPipe.supplement', index=8,
      number=9, type=11, cpp_type=10, label=3,
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
  serialized_start=830,
  serialized_end=1100,
)

_ENDPOINTADDRESS.fields_by_name['domain'].enum_type = _ADDRESSDOMAIN
_ENDPOINTADDRESS.fields_by_name['protocol'].enum_type = _TRANSPORTPROTOCOL
_AGENTIDENTIFICATION.fields_by_name['vendor'].message_type = _VENDORID
_AGENTIDENTIFICATION.fields_by_name['platform'].message_type = _PLATFORMID
_AGENTIDENTIFICATION.fields_by_name['supplement'].message_type = google_dot_protobuf_dot_any__pb2._ANY
_PEERIDENTIFICATION.fields_by_name['supplement'].message_type = google_dot_protobuf_dot_any__pb2._ANY
_ERRORDESCRIPTION.fields_by_name['context'].message_type = google_dot_protobuf_dot_struct__pb2._STRUCT
_ERRORDESCRIPTION.fields_by_name['annotation'].message_type = google_dot_protobuf_dot_struct__pb2._STRUCT
_DATAPIPE.fields_by_name['socket_type'].enum_type = _SOCKETTYPE
_DATAPIPE.fields_by_name['use'].enum_type = _SOCKETUSE
_DATAPIPE.fields_by_name['endpoints'].message_type = _ENDPOINTADDRESS
_DATAPIPE.fields_by_name['supplement'].message_type = google_dot_protobuf_dot_any__pb2._ANY
DESCRIPTOR.message_types_by_name['EndpointAddress'] = _ENDPOINTADDRESS
DESCRIPTOR.message_types_by_name['PlatformId'] = _PLATFORMID
DESCRIPTOR.message_types_by_name['VendorId'] = _VENDORID
DESCRIPTOR.message_types_by_name['AgentIdentification'] = _AGENTIDENTIFICATION
DESCRIPTOR.message_types_by_name['PeerIdentification'] = _PEERIDENTIFICATION
DESCRIPTOR.message_types_by_name['InterfaceSpec'] = _INTERFACESPEC
DESCRIPTOR.message_types_by_name['ErrorDescription'] = _ERRORDESCRIPTION
DESCRIPTOR.message_types_by_name['DataPipe'] = _DATAPIPE
DESCRIPTOR.enum_types_by_name['State'] = _STATE
DESCRIPTOR.enum_types_by_name['AddressDomain'] = _ADDRESSDOMAIN
DESCRIPTOR.enum_types_by_name['TransportProtocol'] = _TRANSPORTPROTOCOL
DESCRIPTOR.enum_types_by_name['SocketType'] = _SOCKETTYPE
DESCRIPTOR.enum_types_by_name['SocketUse'] = _SOCKETUSE
DESCRIPTOR.enum_types_by_name['DependencyType'] = _DEPENDENCYTYPE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

EndpointAddress = _reflection.GeneratedProtocolMessageType('EndpointAddress', (_message.Message,), dict(
  DESCRIPTOR = _ENDPOINTADDRESS,
  __module__ = 'firebird.butler.fbsd_pb2'
  # @@protoc_insertion_point(class_scope:firebird.butler.EndpointAddress)
  ))
_sym_db.RegisterMessage(EndpointAddress)

PlatformId = _reflection.GeneratedProtocolMessageType('PlatformId', (_message.Message,), dict(
  DESCRIPTOR = _PLATFORMID,
  __module__ = 'firebird.butler.fbsd_pb2'
  # @@protoc_insertion_point(class_scope:firebird.butler.PlatformId)
  ))
_sym_db.RegisterMessage(PlatformId)

VendorId = _reflection.GeneratedProtocolMessageType('VendorId', (_message.Message,), dict(
  DESCRIPTOR = _VENDORID,
  __module__ = 'firebird.butler.fbsd_pb2'
  # @@protoc_insertion_point(class_scope:firebird.butler.VendorId)
  ))
_sym_db.RegisterMessage(VendorId)

AgentIdentification = _reflection.GeneratedProtocolMessageType('AgentIdentification', (_message.Message,), dict(
  DESCRIPTOR = _AGENTIDENTIFICATION,
  __module__ = 'firebird.butler.fbsd_pb2'
  # @@protoc_insertion_point(class_scope:firebird.butler.AgentIdentification)
  ))
_sym_db.RegisterMessage(AgentIdentification)

PeerIdentification = _reflection.GeneratedProtocolMessageType('PeerIdentification', (_message.Message,), dict(
  DESCRIPTOR = _PEERIDENTIFICATION,
  __module__ = 'firebird.butler.fbsd_pb2'
  # @@protoc_insertion_point(class_scope:firebird.butler.PeerIdentification)
  ))
_sym_db.RegisterMessage(PeerIdentification)

InterfaceSpec = _reflection.GeneratedProtocolMessageType('InterfaceSpec', (_message.Message,), dict(
  DESCRIPTOR = _INTERFACESPEC,
  __module__ = 'firebird.butler.fbsd_pb2'
  # @@protoc_insertion_point(class_scope:firebird.butler.InterfaceSpec)
  ))
_sym_db.RegisterMessage(InterfaceSpec)

ErrorDescription = _reflection.GeneratedProtocolMessageType('ErrorDescription', (_message.Message,), dict(
  DESCRIPTOR = _ERRORDESCRIPTION,
  __module__ = 'firebird.butler.fbsd_pb2'
  # @@protoc_insertion_point(class_scope:firebird.butler.ErrorDescription)
  ))
_sym_db.RegisterMessage(ErrorDescription)

DataPipe = _reflection.GeneratedProtocolMessageType('DataPipe', (_message.Message,), dict(
  DESCRIPTOR = _DATAPIPE,
  __module__ = 'firebird.butler.fbsd_pb2'
  # @@protoc_insertion_point(class_scope:firebird.butler.DataPipe)
  ))
_sym_db.RegisterMessage(DataPipe)


_STATE.has_options = True
_STATE._options = _descriptor._ParseOptions(descriptor_pb2.EnumOptions(), _b('\020\001'))
# @@protoc_insertion_point(module_scope)
