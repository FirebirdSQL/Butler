###########################################
9/FBDP - Firebird Butler Data Pipe Protocol
###########################################

:domain: github.com/FirebirdSQL/Butler
:shortname: 9/FBDP
:name: Firebird Butler Data Pipe Protocol
:status: raw
:editor: Pavel Císař <pcisar@users.sourceforge.net>

The Firebird Butler Data Pipe Protocol (FBDP) defines unified data format, and formal rules for exchanging user data messages through a Data Pipe in accordance with the specification in |Data Pipe Definition|.

License
=======

Copyright (c) 2019 The Firebird Butler Project.

This Specification is distributed under Creative Commons Attribution-ShareAlike 4.0 International license.

You should have received a copy of the CC BY-SA 4.0 along with this document; if not, see https://creativecommons.org/licenses/by-sa/4.0/

Change Process
==============

This Specification is a free and open standard and is governed by the Consensus-Oriented Specification System (COSS) (see "|COSS-long|").

.. important::

   This specification is still incomplete (work in progress), hence the COSS change process is not yet fully applicable. All ideas and change proposals SHOULD be presented and discussed in `Firebird Butler forum <https://groups.google.com/d/forum/firebird-butler>`_.

Language
========

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in `RFC2119`_.

Related Specifications
======================

#. :doc:`/rfc/3/FBSD`

1. Goals
========

The purpose of this specification is to define a uniform message format and formal rules for the transmission of user data from their `Producer` to the `Consumer` through the exchange of messages via the transport channel in accordance with the |Data Pipe Definition|.

The main objectives are:

#. Simplicity.
#. Flexibility.
#. Extensibility.

2. Implementation
=================

2.1 The Data Pipe Architecture
------------------------------

The Data Pipe is an abstract device that transfers user data from virtual input to virtual output.

.. _fbdp-transport-channel:

2.1.1 Transport channel
^^^^^^^^^^^^^^^^^^^^^^^

The specification requires the existence of a transport channel capable of asynchronously transmitting messages in both directions (referred to as `Transport Channel`), where individual messages are constituted by one or more uniquely separate data blocks (referred to as `Frames`). The `Transport Channel` must also conform to following rules:

1. A message SHALL NOT be delivered more than once to any peer.
2. All messages between two immediate peers SHALL be delivered in order.
3. The channel MUST have an address to which one peer binds and to which the other peer connects.

.. tip::

   Such transmissions are provided by ZeroMQ Message Transfer Protocol (ZMTP_) over DEALER_ (and ROUTER_) sockets.

2.1.2 Peer roles
^^^^^^^^^^^^^^^^

The specification defines following peer roles:

- The peer that **binds** to the `Transport Channel` endpoint is referred to as a `Server`.
- The peer that **connects** to the `Transport Channel` endpoint is referred to as a `Client`.
- The peer that attaches itself to the `virual input` of the Data Pipe to **send** user data is referred to as a `Producer`.
- The peer that attaches itself to the `virual output` of the Data Pipe to **receive** user data is referred to as a `Consumer`.

2.1.3 Pipe attributes
^^^^^^^^^^^^^^^^^^^^^

- The Data Pipe MUST have a string name. The content of the name MAY be arbitrary but MUST be unique in the context of its use. The pipe name SHALL be used for all identification purposes.
- The Data Pipe MAY have assigned specification of format used for transmitted user data. This format specification is not negotiable, and COULD be used by `Server` and `Client` in any way.
- The Data Pipe MAY have arbitrary number of additional, implementation-specific attributes.

2.1.4 Overall Behavior
^^^^^^^^^^^^^^^^^^^^^^

.. _fbdp-connection:

Exchange of messages on the `Transport Channel` is implemented as a `Connection` between the `Server` and the `Client` where the connection has the following stages:

1. The `Client` MUST initiate the connection by sending the OPEN_ message to the `Server`. The OPEN_ message MUST contain `Data Pipe and endpoint Identification`, and MAY contain specification of the user data format and additional implementation-specific attributes.
2. The `Server` MUST reply to the OPEN_ message by sending a READY_ message to confirm the connection, and to specify how many DATA_ messages could be transmitted from/to the `Client` in first round of the data transfer loop. If the `Server` cannot accept the connection, it MUST send a CLOSE_ message with appropriate error code instead.
3. After a successful connection is confirmed, the transmission enters a loop that carries DATA_ messages in `N` message blocks and consists of the following steps:

   1. If the message count (referred to as `X`) specified in last READY_ message received by `Client` is zero, the `Client` SHALL wait for READY_ message from `Server` with non-zero value of the message count. The `Server` SHALL send READY_ message with non-zero message count when is ready to send/receive at least one DATA_ message.
   2. The `Client` SHALL reply to received READY_ message with non-zero message cout `X` by sending READY_ message to the `Server` with message cout `Y`, where `X` >= `Y` >= 0. The `Client` MUST be prepared to receive up to `Y` DATA_ messages.
   3. If the message count `Y` received by `Server` is greater than zero, the `Server` that acts as `Producer` SHOULD send DATA_ messages to the `Client`, and `Server` that acts as `Consumer` SHOULD receive DATA_ messages from the `Client`. The total number of DATA_ messages sent/received SHALL NOT exceed the `Y`. If the message count `Y` is zero, the `Server` SHALL send the READY_ message with non-zero message count again after some time.
   4. The `Client` that acts as `Consumer` SHOULD receive DATA_ messages, while `Client` that acts as `Producer` SHOULD send DATA_ messages to the `Server`.
   5. When `Y` DATA_ messages are transferred, both `Server` and `Client` continue at step 1.

4. The `Client` or `Service` can terminate the `Connection` at any time by sending a CLOSE_ message, or by closing the `Transport Channel`. However, the peer initiating the connection termination SHOULD send the CLOSE_ message before it closes the Transport Channel to the other peer.

The specification allows for a wide range of ways of connecting individual elements with different characteristics. Typically used transmission patterns are listed in `Appendix A. Transmission patterns`_

2.2 The Connection and the Transport Channel
--------------------------------------------

2.2.1 Using one Channel for multiple Connections
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A single `Transport channel <fbdp-transport-channel>`_ MAY be used for message transmission for several concurrently active `Connections`. This specification does not define how the message routing for individual connections should be done, neither the necessary encapsulation of the FBDP protocol messages into the messages transmitted by the multi-transport channel. However, the possible implementation of the multi-transport channel MUST be completely transparent from the point of view of the FBDP.

.. note::

   For example, if transmission is implemented using ZeroMQ ROUTER_ socket, all FBDP messages flowing through it are / must be prefixed with extra `Data Frame` with routing address.


2.2.2 Bound and unbound Connections
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This specification assumes that message transfer provided by `Transport Channel <fbdp-transport-channel>`_ is implemented via `Transport Connection` established between the Client and the Server. In such a case, the FBDP `Connection <fbdp-connection>`_ MAY be bound or not to the `Transport Connection`. This means that:

a) A bound `Connection` SHALL be terminated automatically when the `Transport Connection` functionality is interrupted. An unbound `Connection` assumes a mechanism exists for restoring an interrupted `Transport Connection`, and SHALL be terminated only if this mechanism fails.
b) For unbound `Connection` the `Transport Connection` does not need to be closed together with closing `Connection`, and MAY be reused to carry another subsequent `Connection` between the same `Client` and `Server`. For bound `Connection` the `Transport Connection` SHOULD be closed together with closing `Connection`.

The method of agreement between the `Client` and the `Server` to use the bound or unbound `Connection` mechanism is not defined by this specification and MUST be provided by other means. If such other means are not used, the `Connection` MUST be **bound** to the `Transport Connection`.

2.3 FBDP Messages
-----------------

The traffic between `Client` and `Server` consists of `Messages` in a unified format sent in both directions via a `Transport Channel <fbdp-transport-channel>`_.

2.3.1 Formal message grammar
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. _fbdp-control-frame:
.. _fbdp-data-frame:
.. _fbdp-signature:
.. _fbdp-control-byte:
.. _fbdp-flags:
.. _fbdp-type-data:

2.4.2 Message types
^^^^^^^^^^^^^^^^^^^

The message type is an integer in the range of 1..31 stored in 5 upper (leftmost) bits of the `control-byte <fbdp-control-byte>`_. This protocol revision defines the next message types::

  unused      = 0      ; not a valid message type
  OPEN        = 1      ; initial message from client
  READY       = 2      ; transfer negotiation message
  NOOP        = 3      ; no operation, used for keep-alive & ping purposes
  DATA        = 4      ; user data sent by either client or server
  CLOSE       = 5      ; sent by peer that is going to close the connection

OPEN
""""

READY
"""""

NOOP
""""

DATA
""""

CLOSE
"""""

|
|

3. Reference Implementations
============================

The :ref:`Saturnin-SDK <saturnin-sdk>` is the prime reference implementation for FBDP.

|
|

Appendix A. Transmission patterns
=================================


.. _RFC2119: http://tools.ietf.org/html/rfc2119
.. _ZMTP: https://rfc.zeromq.org/spec:23/ZMTP
.. _ROUTER: https://rfc.zeromq.org/spec:28/REQREP/
.. _DEALER: https://rfc.zeromq.org/spec:28/REQREP/
.. |COSS-long| replace:: :doc:`/rfc/2/COSS`
.. |FBSD| replace:: :doc:`3/FBSD</rfc/3/FBSD>`
.. |FBSP| replace:: :doc:`4/FBSP</rfc/4/FBSP>`
.. |FBLP| replace:: :doc:`5/FBLP</rfc/5/FBLP>`
.. |SSTP| replace:: :doc:`6/SSTP</rfc/6/SSTP>`
.. |RSCFG| replace:: :doc:`7/RSCFG</rfc/7/RSCFG>`
.. |Data Pipe Definition| replace:: :ref:`3/FBSD - Data Pipe Definition<data pipes>`
