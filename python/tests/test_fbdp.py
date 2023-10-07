# SPDX-FileCopyrightText: 2018-present Pavel Cisar <pcisar@users.sourceforge.net>
#
# SPDX-License-Identifier: MIT

"""
ID:          butler-fbdp-protobuf
TITLE:       FDBP protobuf
DESCRIPTION:
NOTES:
"""

import pytest
import firebird.butler.fbdp_pb2 as fbdp

def test_FBDPOpenDataframe():
    DATA_PIPE = 'Data Pipe Identification'
    PIPE_SOCKET = 1
    DATA_FORMAT = 'Specification of format for transmitted user data'
    PARAM1_KEY = 'param1'
    PARAM1_VAL = 'value1'
    proto = fbdp.FBDPOpenDataframe()
    proto.data_pipe = DATA_PIPE
    proto.pipe_socket = PIPE_SOCKET
    proto.data_format = DATA_FORMAT
    proto.parameters[PARAM1_KEY] = PARAM1_VAL
    msg = proto.SerializeToString()
    proto.Clear()
    proto.ParseFromString(msg)
    assert proto.data_pipe == DATA_PIPE
    assert proto.pipe_socket == PIPE_SOCKET
    assert proto.data_format == DATA_FORMAT
    assert proto.parameters[PARAM1_KEY] == PARAM1_VAL
