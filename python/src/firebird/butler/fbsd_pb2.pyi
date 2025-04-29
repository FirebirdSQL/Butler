from google.protobuf import any_pb2 as _any_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class StateEnum(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    STATE_UNKNOWN: _ClassVar[StateEnum]
    STATE_READY: _ClassVar[StateEnum]
    STATE_RUNNING: _ClassVar[StateEnum]
    STATE_WAITING: _ClassVar[StateEnum]
    STATE_SUSPENDED: _ClassVar[StateEnum]
    STATE_FINISHED: _ClassVar[StateEnum]
    STATE_ABORTED: _ClassVar[StateEnum]
    STATE_CREATED: _ClassVar[StateEnum]
    STATE_BLOCKED: _ClassVar[StateEnum]
    STATE_STOPPED: _ClassVar[StateEnum]
    STATE_TERMINATED: _ClassVar[StateEnum]

class AddressDomainEnum(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DOMAIN_UNKNOWN: _ClassVar[AddressDomainEnum]
    DOMAIN_LOCAL: _ClassVar[AddressDomainEnum]
    DOMAIN_NODE: _ClassVar[AddressDomainEnum]
    DOMAIN_NETWORK: _ClassVar[AddressDomainEnum]

class TransportProtocolEnum(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PROTOCOL_UNKNOWN: _ClassVar[TransportProtocolEnum]
    PROTOCOL_INPROC: _ClassVar[TransportProtocolEnum]
    PROTOCOL_IPC: _ClassVar[TransportProtocolEnum]
    PROTOCOL_TCP: _ClassVar[TransportProtocolEnum]
    PROTOCOL_PGM: _ClassVar[TransportProtocolEnum]
    PROTOCOL_EPGM: _ClassVar[TransportProtocolEnum]
    PROTOCOL_VMCI: _ClassVar[TransportProtocolEnum]

class SocketTypeEnum(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SOCKET_TYPE_UNKNOWN: _ClassVar[SocketTypeEnum]
    SOCKET_TYPE_DEALER: _ClassVar[SocketTypeEnum]
    SOCKET_TYPE_ROUTER: _ClassVar[SocketTypeEnum]
    SOCKET_TYPE_PUB: _ClassVar[SocketTypeEnum]
    SOCKET_TYPE_SUB: _ClassVar[SocketTypeEnum]
    SOCKET_TYPE_XPUB: _ClassVar[SocketTypeEnum]
    SOCKET_TYPE_XSUB: _ClassVar[SocketTypeEnum]
    SOCKET_TYPE_PUSH: _ClassVar[SocketTypeEnum]
    SOCKET_TYPE_PULL: _ClassVar[SocketTypeEnum]
    SOCKET_TYPE_STREAM: _ClassVar[SocketTypeEnum]
    SOCKET_TYPE_PAIR: _ClassVar[SocketTypeEnum]

class SocketUseEnum(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SOCKET_USE_UNKNOWN: _ClassVar[SocketUseEnum]
    SOCKET_USE_PRODUCER: _ClassVar[SocketUseEnum]
    SOCKET_USE_CONSUMER: _ClassVar[SocketUseEnum]
    SOCKET_USE_EXCHANGE: _ClassVar[SocketUseEnum]

class DependencyTypeEnum(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DEPTYPE_UNKNOWN: _ClassVar[DependencyTypeEnum]
    DEPTYPE_REQUIRED: _ClassVar[DependencyTypeEnum]
    DEPTYPE_PREFERRED: _ClassVar[DependencyTypeEnum]
    DEPTYPE_OPTIONAL: _ClassVar[DependencyTypeEnum]
STATE_UNKNOWN: StateEnum
STATE_READY: StateEnum
STATE_RUNNING: StateEnum
STATE_WAITING: StateEnum
STATE_SUSPENDED: StateEnum
STATE_FINISHED: StateEnum
STATE_ABORTED: StateEnum
STATE_CREATED: StateEnum
STATE_BLOCKED: StateEnum
STATE_STOPPED: StateEnum
STATE_TERMINATED: StateEnum
DOMAIN_UNKNOWN: AddressDomainEnum
DOMAIN_LOCAL: AddressDomainEnum
DOMAIN_NODE: AddressDomainEnum
DOMAIN_NETWORK: AddressDomainEnum
PROTOCOL_UNKNOWN: TransportProtocolEnum
PROTOCOL_INPROC: TransportProtocolEnum
PROTOCOL_IPC: TransportProtocolEnum
PROTOCOL_TCP: TransportProtocolEnum
PROTOCOL_PGM: TransportProtocolEnum
PROTOCOL_EPGM: TransportProtocolEnum
PROTOCOL_VMCI: TransportProtocolEnum
SOCKET_TYPE_UNKNOWN: SocketTypeEnum
SOCKET_TYPE_DEALER: SocketTypeEnum
SOCKET_TYPE_ROUTER: SocketTypeEnum
SOCKET_TYPE_PUB: SocketTypeEnum
SOCKET_TYPE_SUB: SocketTypeEnum
SOCKET_TYPE_XPUB: SocketTypeEnum
SOCKET_TYPE_XSUB: SocketTypeEnum
SOCKET_TYPE_PUSH: SocketTypeEnum
SOCKET_TYPE_PULL: SocketTypeEnum
SOCKET_TYPE_STREAM: SocketTypeEnum
SOCKET_TYPE_PAIR: SocketTypeEnum
SOCKET_USE_UNKNOWN: SocketUseEnum
SOCKET_USE_PRODUCER: SocketUseEnum
SOCKET_USE_CONSUMER: SocketUseEnum
SOCKET_USE_EXCHANGE: SocketUseEnum
DEPTYPE_UNKNOWN: DependencyTypeEnum
DEPTYPE_REQUIRED: DependencyTypeEnum
DEPTYPE_PREFERRED: DependencyTypeEnum
DEPTYPE_OPTIONAL: DependencyTypeEnum

class PlatformId(_message.Message):
    __slots__ = ("uid", "version")
    UID_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    uid: bytes
    version: str
    def __init__(self, uid: _Optional[bytes] = ..., version: _Optional[str] = ...) -> None: ...

class VendorId(_message.Message):
    __slots__ = ("uid",)
    UID_FIELD_NUMBER: _ClassVar[int]
    uid: bytes
    def __init__(self, uid: _Optional[bytes] = ...) -> None: ...

class AgentIdentification(_message.Message):
    __slots__ = ("uid", "name", "version", "vendor", "platform", "classification", "supplement")
    UID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    VENDOR_FIELD_NUMBER: _ClassVar[int]
    PLATFORM_FIELD_NUMBER: _ClassVar[int]
    CLASSIFICATION_FIELD_NUMBER: _ClassVar[int]
    SUPPLEMENT_FIELD_NUMBER: _ClassVar[int]
    uid: bytes
    name: str
    version: str
    vendor: VendorId
    platform: PlatformId
    classification: str
    supplement: _containers.RepeatedCompositeFieldContainer[_any_pb2.Any]
    def __init__(self, uid: _Optional[bytes] = ..., name: _Optional[str] = ..., version: _Optional[str] = ..., vendor: _Optional[_Union[VendorId, _Mapping]] = ..., platform: _Optional[_Union[PlatformId, _Mapping]] = ..., classification: _Optional[str] = ..., supplement: _Optional[_Iterable[_Union[_any_pb2.Any, _Mapping]]] = ...) -> None: ...

class PeerIdentification(_message.Message):
    __slots__ = ("uid", "pid", "host", "supplement")
    UID_FIELD_NUMBER: _ClassVar[int]
    PID_FIELD_NUMBER: _ClassVar[int]
    HOST_FIELD_NUMBER: _ClassVar[int]
    SUPPLEMENT_FIELD_NUMBER: _ClassVar[int]
    uid: bytes
    pid: int
    host: str
    supplement: _containers.RepeatedCompositeFieldContainer[_any_pb2.Any]
    def __init__(self, uid: _Optional[bytes] = ..., pid: _Optional[int] = ..., host: _Optional[str] = ..., supplement: _Optional[_Iterable[_Union[_any_pb2.Any, _Mapping]]] = ...) -> None: ...

class InterfaceSpec(_message.Message):
    __slots__ = ("number", "uid")
    NUMBER_FIELD_NUMBER: _ClassVar[int]
    UID_FIELD_NUMBER: _ClassVar[int]
    number: int
    uid: bytes
    def __init__(self, number: _Optional[int] = ..., uid: _Optional[bytes] = ...) -> None: ...

class ErrorDescription(_message.Message):
    __slots__ = ("code", "description", "context", "annotation")
    CODE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    ANNOTATION_FIELD_NUMBER: _ClassVar[int]
    code: int
    description: str
    context: _struct_pb2.Struct
    annotation: _struct_pb2.Struct
    def __init__(self, code: _Optional[int] = ..., description: _Optional[str] = ..., context: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., annotation: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...
