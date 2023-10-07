# SPDX-FileCopyrightText: 2018-present Pavel Cisar <pcisar@users.sourceforge.net>
#
# SPDX-License-Identifier: MIT

"""
ID:          butler-fbsd-protobuf
TITLE:       FDSD protobuf
DESCRIPTION:
NOTES:
"""

import pytest
import uuid
import firebird.butler.fbsd_pb2 as fbsd

_PEER_UID = uuid.uuid1().bytes
_PID = 100
_HOST = 'host'
_AGENT_UID = uuid.uuid1().bytes
_NAME = 'Agent name'
_AGENT_VERSION = 'agent version'
_VENDOR_ID = uuid.uuid1().bytes
_PLATFORM_ID = uuid.uuid1().bytes
_PLATFORM_VERSION = 'platform version'
_CLASSIFICATION = 'classification'
_API_NUM = 1
_API_ID = uuid.uuid1().bytes
_ERR_CODE = 100
_ERR_DESCRIPTION = "Fatal error"
_ERR_CONTEXT_KEY = "Context key"
_ERR_CONTEXT_VALUE = "Context value"
_ERR_ANNOTATION_KEY = "Annotation key"
_ERR_ANNOTATION_VALUE = "Annotation value"

def test_StateEnum():
    assert fbsd.StateEnum.STATE_RUNNING is fbsd.STATE_RUNNING

def test_AddressDomainEnum():
    assert fbsd.AddressDomainEnum.DOMAIN_LOCAL is fbsd.DOMAIN_LOCAL

def test_TransportProtocolEnum():
    assert fbsd.TransportProtocolEnum.PROTOCOL_INPROC is fbsd.PROTOCOL_INPROC

def test_SocketTypeEnum():
    assert fbsd.SocketTypeEnum.SOCKET_TYPE_ROUTER is fbsd.SOCKET_TYPE_ROUTER

def test_SocketUseEnum():
    assert fbsd.SocketUseEnum.SOCKET_USE_PRODUCER is fbsd.SOCKET_USE_PRODUCER

def test_DependencyTypeEnum():
    assert fbsd.DependencyTypeEnum.DEPTYPE_REQUIRED is fbsd.DEPTYPE_REQUIRED

def test_PlatformId():
    proto = fbsd.PlatformId()
    proto.uid = _PLATFORM_ID
    proto.version = _PLATFORM_VERSION
    msg = proto.SerializeToString()
    proto.Clear()
    proto.ParseFromString(msg)
    assert proto.uid == _PLATFORM_ID
    assert proto.version == _PLATFORM_VERSION

def test_VendorId():
    proto = fbsd.VendorId()
    proto.uid = _VENDOR_ID
    msg = proto.SerializeToString()
    proto.Clear()
    proto.ParseFromString(msg)
    assert proto.uid == _VENDOR_ID

def test_AgentIdentification():
    proto = fbsd.AgentIdentification()
    proto.uid = _AGENT_UID
    proto.name = _NAME
    proto.version = _AGENT_VERSION
    proto.vendor.uid = _VENDOR_ID
    proto.platform.uid = _PLATFORM_ID
    proto.platform.version = _PLATFORM_VERSION
    proto.classification = _CLASSIFICATION
    msg = proto.SerializeToString()
    proto.Clear()
    proto.ParseFromString(msg)
    assert proto.uid == _AGENT_UID
    assert proto.name == _NAME
    assert proto.version == _AGENT_VERSION
    assert proto.vendor.uid == _VENDOR_ID
    assert proto.platform.uid == _PLATFORM_ID
    assert proto.platform.version == _PLATFORM_VERSION
    assert proto.classification == _CLASSIFICATION

def test_PeerIdentification():
    proto = fbsd.PeerIdentification()
    proto.uid = _PEER_UID
    proto.host = _HOST
    proto.pid = _PID
    msg = proto.SerializeToString()
    proto.Clear()
    proto.ParseFromString(msg)
    assert proto.uid == _PEER_UID
    assert proto.host == _HOST
    assert proto.pid == _PID

def test_InterfaceSpec():
    proto = fbsd.InterfaceSpec(number=_API_NUM, uid=_API_ID)
    msg = proto.SerializeToString()
    proto.Clear()
    proto.ParseFromString(msg)
    assert proto.number == _API_NUM
    assert proto.uid == _API_ID

def test_ErrorDescription():
    proto = fbsd.ErrorDescription()
    proto.code = _ERR_CODE
    proto.description = _ERR_DESCRIPTION
    proto.context[_ERR_CONTEXT_KEY] = _ERR_CONTEXT_VALUE
    proto.annotation[_ERR_ANNOTATION_KEY] = _ERR_ANNOTATION_VALUE
    msg = proto.SerializeToString()
    proto.Clear()
    proto.ParseFromString(msg)
    assert proto.code == _ERR_CODE
    assert proto.description == _ERR_DESCRIPTION
    assert proto.context[_ERR_CONTEXT_KEY] == _ERR_CONTEXT_VALUE
    assert proto.annotation[_ERR_ANNOTATION_KEY] == _ERR_ANNOTATION_VALUE
