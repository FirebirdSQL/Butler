from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class FBDPOpenDataframe(_message.Message):
    __slots__ = ("data_pipe", "pipe_socket", "data_format", "parameters")
    DATA_PIPE_FIELD_NUMBER: _ClassVar[int]
    PIPE_SOCKET_FIELD_NUMBER: _ClassVar[int]
    DATA_FORMAT_FIELD_NUMBER: _ClassVar[int]
    PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    data_pipe: str
    pipe_socket: int
    data_format: str
    parameters: _struct_pb2.Struct
    def __init__(self, data_pipe: _Optional[str] = ..., pipe_socket: _Optional[int] = ..., data_format: _Optional[str] = ..., parameters: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...
