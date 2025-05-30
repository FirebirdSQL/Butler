# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: firebird/butler/fbsd.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import any_pb2 as google_dot_protobuf_dot_any__pb2
from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1a\x66irebird/butler/fbsd.proto\x12\x0f\x66irebird.butler\x1a\x19google/protobuf/any.proto\x1a\x1cgoogle/protobuf/struct.proto\"*\n\nPlatformId\x12\x0b\n\x03uid\x18\x01 \x01(\x0c\x12\x0f\n\x07version\x18\x02 \x01(\t\"\x17\n\x08VendorId\x12\x0b\n\x03uid\x18\x01 \x01(\x0c\"\xdd\x01\n\x13\x41gentIdentification\x12\x0b\n\x03uid\x18\x01 \x01(\x0c\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x0f\n\x07version\x18\x03 \x01(\t\x12)\n\x06vendor\x18\x04 \x01(\x0b\x32\x19.firebird.butler.VendorId\x12-\n\x08platform\x18\x05 \x01(\x0b\x32\x1b.firebird.butler.PlatformId\x12\x16\n\x0e\x63lassification\x18\x06 \x01(\t\x12(\n\nsupplement\x18\x07 \x03(\x0b\x32\x14.google.protobuf.Any\"f\n\x12PeerIdentification\x12\x0b\n\x03uid\x18\x01 \x01(\x0c\x12\x0b\n\x03pid\x18\x02 \x01(\r\x12\x0c\n\x04host\x18\x03 \x01(\t\x12(\n\nsupplement\x18\x04 \x03(\x0b\x32\x14.google.protobuf.Any\",\n\rInterfaceSpec\x12\x0e\n\x06number\x18\x01 \x01(\r\x12\x0b\n\x03uid\x18\x02 \x01(\x0c\"\x8c\x01\n\x10\x45rrorDescription\x12\x0c\n\x04\x63ode\x18\x01 \x01(\x04\x12\x13\n\x0b\x64\x65scription\x18\x02 \x01(\t\x12(\n\x07\x63ontext\x18\x03 \x01(\x0b\x32\x17.google.protobuf.Struct\x12+\n\nannotation\x18\x04 \x01(\x0b\x32\x17.google.protobuf.Struct*\xe4\x01\n\tStateEnum\x12\x11\n\rSTATE_UNKNOWN\x10\x00\x12\x0f\n\x0bSTATE_READY\x10\x01\x12\x11\n\rSTATE_RUNNING\x10\x02\x12\x11\n\rSTATE_WAITING\x10\x03\x12\x13\n\x0fSTATE_SUSPENDED\x10\x04\x12\x12\n\x0eSTATE_FINISHED\x10\x05\x12\x11\n\rSTATE_ABORTED\x10\x06\x12\x11\n\rSTATE_CREATED\x10\x01\x12\x11\n\rSTATE_BLOCKED\x10\x03\x12\x11\n\rSTATE_STOPPED\x10\x04\x12\x14\n\x10STATE_TERMINATED\x10\x06\x1a\x02\x10\x01*^\n\x11\x41\x64\x64ressDomainEnum\x12\x12\n\x0e\x44OMAIN_UNKNOWN\x10\x00\x12\x10\n\x0c\x44OMAIN_LOCAL\x10\x01\x12\x0f\n\x0b\x44OMAIN_NODE\x10\x02\x12\x12\n\x0e\x44OMAIN_NETWORK\x10\x03*\x9e\x01\n\x15TransportProtocolEnum\x12\x14\n\x10PROTOCOL_UNKNOWN\x10\x00\x12\x13\n\x0fPROTOCOL_INPROC\x10\x01\x12\x10\n\x0cPROTOCOL_IPC\x10\x02\x12\x10\n\x0cPROTOCOL_TCP\x10\x03\x12\x10\n\x0cPROTOCOL_PGM\x10\x04\x12\x11\n\rPROTOCOL_EPGM\x10\x05\x12\x11\n\rPROTOCOL_VMCI\x10\x06*\x89\x02\n\x0eSocketTypeEnum\x12\x17\n\x13SOCKET_TYPE_UNKNOWN\x10\x00\x12\x16\n\x12SOCKET_TYPE_DEALER\x10\x01\x12\x16\n\x12SOCKET_TYPE_ROUTER\x10\x02\x12\x13\n\x0fSOCKET_TYPE_PUB\x10\x03\x12\x13\n\x0fSOCKET_TYPE_SUB\x10\x04\x12\x14\n\x10SOCKET_TYPE_XPUB\x10\x05\x12\x14\n\x10SOCKET_TYPE_XSUB\x10\x06\x12\x14\n\x10SOCKET_TYPE_PUSH\x10\x07\x12\x14\n\x10SOCKET_TYPE_PULL\x10\x08\x12\x16\n\x12SOCKET_TYPE_STREAM\x10\t\x12\x14\n\x10SOCKET_TYPE_PAIR\x10\n*r\n\rSocketUseEnum\x12\x16\n\x12SOCKET_USE_UNKNOWN\x10\x00\x12\x17\n\x13SOCKET_USE_PRODUCER\x10\x01\x12\x17\n\x13SOCKET_USE_CONSUMER\x10\x02\x12\x17\n\x13SOCKET_USE_EXCHANGE\x10\x03*l\n\x12\x44\x65pendencyTypeEnum\x12\x13\n\x0f\x44\x45PTYPE_UNKNOWN\x10\x00\x12\x14\n\x10\x44\x45PTYPE_REQUIRED\x10\x01\x12\x15\n\x11\x44\x45PTYPE_PREFERRED\x10\x02\x12\x14\n\x10\x44\x45PTYPE_OPTIONAL\x10\x03\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'firebird.butler.fbsd_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_STATEENUM']._options = None
  _globals['_STATEENUM']._serialized_options = b'\020\001'
  _globals['_STATEENUM']._serialized_start=691
  _globals['_STATEENUM']._serialized_end=919
  _globals['_ADDRESSDOMAINENUM']._serialized_start=921
  _globals['_ADDRESSDOMAINENUM']._serialized_end=1015
  _globals['_TRANSPORTPROTOCOLENUM']._serialized_start=1018
  _globals['_TRANSPORTPROTOCOLENUM']._serialized_end=1176
  _globals['_SOCKETTYPEENUM']._serialized_start=1179
  _globals['_SOCKETTYPEENUM']._serialized_end=1444
  _globals['_SOCKETUSEENUM']._serialized_start=1446
  _globals['_SOCKETUSEENUM']._serialized_end=1560
  _globals['_DEPENDENCYTYPEENUM']._serialized_start=1562
  _globals['_DEPENDENCYTYPEENUM']._serialized_end=1670
  _globals['_PLATFORMID']._serialized_start=104
  _globals['_PLATFORMID']._serialized_end=146
  _globals['_VENDORID']._serialized_start=148
  _globals['_VENDORID']._serialized_end=171
  _globals['_AGENTIDENTIFICATION']._serialized_start=174
  _globals['_AGENTIDENTIFICATION']._serialized_end=395
  _globals['_PEERIDENTIFICATION']._serialized_start=397
  _globals['_PEERIDENTIFICATION']._serialized_end=499
  _globals['_INTERFACESPEC']._serialized_start=501
  _globals['_INTERFACESPEC']._serialized_end=545
  _globals['_ERRORDESCRIPTION']._serialized_start=548
  _globals['_ERRORDESCRIPTION']._serialized_end=688
# @@protoc_insertion_point(module_scope)
