# SPDX-FileCopyrightText: 2018-present Pavel Cisar <pcisar@users.sourceforge.net>
#
# SPDX-License-Identifier: MIT

"""
ID:          butler-fbsp-protobuf
TITLE:       FDSP protobuf
DESCRIPTION:
NOTES:
"""

import pytest
import uuid
import firebird.butler.fbsd_pb2 as fbsd
import firebird.butler.fbsp_pb2 as fbsp

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
_API_1_NUM = 1
_API_1_ID = uuid.uuid1().bytes
_API_2_NUM = 2
_API_2_ID = uuid.uuid1().bytes
_STATE = fbsd.STATE_RUNNING

def test_FBSPHelloDataframe():
    proto = fbsp.FBSPHelloDataframe()
    proto.instance.uid = _PEER_UID
    proto.instance.host = _HOST
    proto.instance.pid = _PID
    proto.client.uid = _AGENT_UID
    proto.client.name = _NAME
    proto.client.version = _AGENT_VERSION
    proto.client.vendor.uid = _VENDOR_ID
    proto.client.platform.uid = _PLATFORM_ID
    proto.client.platform.version = _PLATFORM_VERSION
    proto.client.classification = _CLASSIFICATION
    msg = proto.SerializeToString()
    proto.Clear()
    proto.ParseFromString(msg)
    assert proto.instance.uid == _PEER_UID
    assert proto.instance.host == _HOST
    assert proto.instance.pid == _PID
    assert proto.client.uid == _AGENT_UID
    assert proto.client.name == _NAME
    assert proto.client.version == _AGENT_VERSION
    assert proto.client.vendor.uid == _VENDOR_ID
    assert proto.client.platform.uid == _PLATFORM_ID
    assert proto.client.platform.version == _PLATFORM_VERSION
    assert proto.client.classification == _CLASSIFICATION

def test_FBSPWelcomeDataframe():
    proto = fbsp.FBSPWelcomeDataframe()
    proto.instance.uid = _PEER_UID
    proto.instance.host = _HOST
    proto.instance.pid = _PID
    proto.service.uid = _AGENT_UID
    proto.service.name = _NAME
    proto.service.version = _AGENT_VERSION
    proto.service.vendor.uid = _VENDOR_ID
    proto.service.platform.uid = _PLATFORM_ID
    proto.service.platform.version = _PLATFORM_VERSION
    proto.service.classification = _CLASSIFICATION
    api1 = fbsd.InterfaceSpec(number=_API_1_NUM, uid=_API_1_ID)
    api2 = fbsd.InterfaceSpec(number=_API_2_NUM, uid=_API_2_ID)
    proto.api.extend([api1, api2])
    msg = proto.SerializeToString()
    proto.Clear()
    proto.ParseFromString(msg)
    assert proto.instance.uid == _PEER_UID
    assert proto.instance.host == _HOST
    assert proto.instance.pid == _PID
    assert proto.service.uid == _AGENT_UID
    assert proto.service.name == _NAME
    assert proto.service.version == _AGENT_VERSION
    assert proto.service.vendor.uid == _VENDOR_ID
    assert proto.service.platform.uid == _PLATFORM_ID
    assert proto.service.platform.version == _PLATFORM_VERSION
    assert proto.service.classification == _CLASSIFICATION
    assert len(proto.api) == 2
    assert proto.api[0].number == api1.number
    assert proto.api[0].uid == api1.uid
    assert proto.api[1].number == api2.number
    assert proto.api[1].uid == api2.uid

def test_FBSPCancelRequests():
    proto = fbsp.FBSPCancelRequests()
    proto.token = _PEER_UID
    msg = proto.SerializeToString()
    proto.Clear()
    proto.ParseFromString(msg)
    assert proto.token == _PEER_UID

def test_FBSPStateInformation():
    proto = fbsp.FBSPStateInformation()
    proto.state = _STATE
    msg = proto.SerializeToString()
    proto.Clear()
    proto.ParseFromString(msg)
    assert proto.state == _STATE

