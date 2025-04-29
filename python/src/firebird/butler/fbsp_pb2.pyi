from google.protobuf import any_pb2 as _any_pb2
from firebird.butler import fbsd_pb2 as _fbsd_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class FBSPHelloDataframe(_message.Message):
    __slots__ = ("instance", "client", "supplement")
    INSTANCE_FIELD_NUMBER: _ClassVar[int]
    CLIENT_FIELD_NUMBER: _ClassVar[int]
    SUPPLEMENT_FIELD_NUMBER: _ClassVar[int]
    instance: _fbsd_pb2.PeerIdentification
    client: _fbsd_pb2.AgentIdentification
    supplement: _containers.RepeatedCompositeFieldContainer[_any_pb2.Any]
    def __init__(self, instance: _Optional[_Union[_fbsd_pb2.PeerIdentification, _Mapping]] = ..., client: _Optional[_Union[_fbsd_pb2.AgentIdentification, _Mapping]] = ..., supplement: _Optional[_Iterable[_Union[_any_pb2.Any, _Mapping]]] = ...) -> None: ...

class FBSPWelcomeDataframe(_message.Message):
    __slots__ = ("instance", "service", "api", "supplement")
    INSTANCE_FIELD_NUMBER: _ClassVar[int]
    SERVICE_FIELD_NUMBER: _ClassVar[int]
    API_FIELD_NUMBER: _ClassVar[int]
    SUPPLEMENT_FIELD_NUMBER: _ClassVar[int]
    instance: _fbsd_pb2.PeerIdentification
    service: _fbsd_pb2.AgentIdentification
    api: _containers.RepeatedCompositeFieldContainer[_fbsd_pb2.InterfaceSpec]
    supplement: _containers.RepeatedCompositeFieldContainer[_any_pb2.Any]
    def __init__(self, instance: _Optional[_Union[_fbsd_pb2.PeerIdentification, _Mapping]] = ..., service: _Optional[_Union[_fbsd_pb2.AgentIdentification, _Mapping]] = ..., api: _Optional[_Iterable[_Union[_fbsd_pb2.InterfaceSpec, _Mapping]]] = ..., supplement: _Optional[_Iterable[_Union[_any_pb2.Any, _Mapping]]] = ...) -> None: ...

class FBSPCancelRequests(_message.Message):
    __slots__ = ("token", "supplement")
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    SUPPLEMENT_FIELD_NUMBER: _ClassVar[int]
    token: bytes
    supplement: _containers.RepeatedCompositeFieldContainer[_any_pb2.Any]
    def __init__(self, token: _Optional[bytes] = ..., supplement: _Optional[_Iterable[_Union[_any_pb2.Any, _Mapping]]] = ...) -> None: ...

class FBSPStateInformation(_message.Message):
    __slots__ = ("state", "supplement")
    STATE_FIELD_NUMBER: _ClassVar[int]
    SUPPLEMENT_FIELD_NUMBER: _ClassVar[int]
    state: _fbsd_pb2.StateEnum
    supplement: _containers.RepeatedCompositeFieldContainer[_any_pb2.Any]
    def __init__(self, state: _Optional[_Union[_fbsd_pb2.StateEnum, str]] = ..., supplement: _Optional[_Iterable[_Union[_any_pb2.Any, _Mapping]]] = ...) -> None: ...
