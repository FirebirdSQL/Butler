###########################################
9/FBDP - Firebird Butler Data Pipe Protocol
###########################################

:domain: github.com/FirebirdSQL/Butler
:shortname: 9/FBDP
:name: Firebird Butler Data Pipe Protocol
:status: draft
:editor: Pavel Císař <pcisar@users.sourceforge.net>

The Firebird Butler Data Pipe Protocol (FBDP) defines unified data format, and formal
rules for exchanging user data messages through a Data Pipe in accordance with
the specification in |Data Pipe Definition|.

License
=======

Copyright (c) 2019 The Firebird Butler Project.

This Specification is distributed under Creative Commons Attribution-ShareAlike 4.0 International license.

You should have received a copy of the CC BY-SA 4.0 along with this document; if not,
see https://creativecommons.org/licenses/by-sa/4.0/

Change Process
==============

This Specification is a free and open standard and is governed by the Consensus-Oriented
Specification System (COSS) (see "|COSS-long|").

.. important::

   This specification is still incomplete (work in progress), hence the COSS change process
   is not yet fully applicable. All ideas and change proposals SHOULD be presented and
   discussed in `Firebird Butler forum <https://groups.google.com/d/forum/firebird-butler>`_.

Language
========

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT",
"RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described
in `RFC2119`_.

Related Specifications
======================

#. :doc:`/rfc/3/FBSD`

1. Goals
========

The purpose of this specification is to define a uniform message format and formal rules
for the transmission of user data from their `Producer` to the `Consumer` through
the exchange of messages via the transport channel in accordance with the |Data Pipe Definition|.

The main objectives are:

#. Simplicity.
#. Flexibility.
#. Extensibility.

2. Implementation
=================

2.1 The Data Pipe Architecture
------------------------------

The Data Pipe is an abstract device that transfers user data from `virtual input` to
`virtual output` through a `Transport Channel` between exactly two peers. Virtual input
and output are referred to as Data Pipe input and output `Sockets`.

.. _fbdp-transport-channel:

2.1.1 Transport channel
^^^^^^^^^^^^^^^^^^^^^^^

The specification requires the existence of a transport channel capable of asynchronously
transmitting messages in both directions (referred to as `Transport Channel`), where
individual messages are constituted by one or more uniquely separate data blocks (referred
to as `Frames`). The `Transport Channel` must also conform to following rules:

1. A message SHALL NOT be delivered more than once to any peer.
2. All messages between two immediate peers SHALL be delivered in order.
3. The channel MUST have an address to which one peer binds and to which the other peer connects.

.. tip::

   Such transmissions are provided by ZeroMQ Message Transfer Protocol (ZMTP_) over DEALER_
   (and ROUTER_) sockets.

2.1.2 Peer roles
^^^^^^^^^^^^^^^^

The specification defines following peer roles:

- The peer that **binds** to the `Transport Channel` endpoint is referred to as a `Server`.
- The peer that **connects** to the `Transport Channel` endpoint is referred to as a `Client`.
- The peer that attaches itself to the **input** socket of the Data Pipe to **send** user
  data is referred to as a `Producer`.
- The peer that attaches itself to the **output** socket of the Data Pipe to **receive**
  user data is referred to as a `Consumer`.

The data pipe is **always** routed from the `Server` to the `Client`, and in this sense
the `Server` is its **owner**.

The `Client` always connects to one from the virtual sockets of the data pipe owned by
`Server`. By accepting a connection from the `Client` on the specified virtual pipe Socket,
the `Server` automatically establishes the connection to the `Client` on the corresponding
complementary virtual pipe Socket, assuming the corresponding role.

The above means that the `Client` connected to the data pipe **input** assumes
the `Producer's` role (with Server as a Consumer), and the `Client` connected to the data
pipe **output** assumes the `Consumer's` role (with the Server as a Producer).

2.1.3 Pipe attributes
^^^^^^^^^^^^^^^^^^^^^

- The Data Pipe MUST have a string name. The content of the name MAY be arbitrary but MUST
  be unique in the context of its use. The pipe name SHALL be used for all identification
  purposes.
- The Data Pipe MAY have assigned specification of format used for transmitted user data.
  This format specification is not negotiable, and COULD be used by `Server` and `Client`
  in any way.
- The Data Pipe MAY have arbitrary number of additional, implementation-specific attributes.

.. _fbdp-connection:

2.1.4 Overall Behavior
^^^^^^^^^^^^^^^^^^^^^^

Exchange of messages on the `Transport Channel` is implemented as a `Connection` between
the `Server` and the `Client` where the connection has the following stages:

1. The `Client` MUST initiate the connection by sending the OPEN_ message to the `Server`.
   The OPEN_ message MUST contain Data Pipe and Socket `Identification`, and MAY contain
   specification of the user data format and additional implementation-specific attributes.
2. The `Server` MUST reply to the OPEN_ message by sending a READY_ message to confirm
   the connection, and to start the data transmission loop (see step 3.1). If the `Server`
   cannot accept the connection, it MUST send a CLOSE_ message with appropriate |error-code|
   instead.
3. After a successful connection is confirmed, the transmission enters a loop that carries
   DATA_ messages in `N` message blocks and consists of the following steps:

   1. The `Client` SHALL wait for READY_ message from `Server` with non-zero value
      of the message count. The `Server` SHALL send READY_ message with non-zero message
      count when is ready to send/receive at least one DATA_ message.
   2. The `Client` SHALL reply to received READY_ message with non-zero message count `X`
      by sending READY_ message to the `Server` with message cout `Y`, where `X` >= `Y` >= 0.
      The `Client` MUST be prepared to send/receive up to `Y` DATA_ messages.
   3. If the message count `Y` received by `Server` is greater than zero, the `Server` that
      acts as `Producer` SHOULD send DATA_ messages to the `Client`, and `Server` that acts
      as `Consumer` SHOULD receive DATA_ messages from the `Client`. The total number of DATA_
      messages sent/received SHALL NOT exceed the `Y`. If the message count `Y` received by
      `Server` is zero, the `Server` SHALL send the READY_ message with non-zero message
      count again some time later.
   4. The `Client` that acts as `Consumer` SHOULD receive DATA_ messages, while `Client`
      that acts as `Producer` SHOULD send DATA_ messages to the `Server`.
   5. When `Y` DATA_ messages are transferred, both `Server` and `Client` continue at step 1.

4. The `Client` or `Server` can terminate the `Connection` at any time by sending a CLOSE_
   message, or by closing the `Transport Channel`. However, the peer initiating
   the connection termination SHOULD send the CLOSE_ message before it closes the
   `Transport Channel` to the other peer.

The specification allows multiple ways how to connect and chain individual elements with
different transmission characteristics. Flow charts of user data transmission in acceptable
contexts and perspectives are listed in `Appendix A. Flow charts`_. Typically used
transmission patterns are listed in `Appendix B. Transmission patterns`_

2.2 The Connection and the Transport Channel
--------------------------------------------

2.2.1 Using one Channel for multiple Connections
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A single `Transport channel <fbdp-transport-channel>`_ MAY be used for message transmission
for several concurrently active `Connections`. This specification does not define how
the message routing for individual connections should be done, neither the necessary
encapsulation of the FBDP protocol messages into the messages transmitted by
the multi-transport channel. However, the possible implementation of the multi-transport
channel MUST be completely transparent from the point of view of the FBDP.

.. note::

   For example, if transmission is implemented using ZeroMQ ROUTER_ socket, all FBDP
   messages flowing through it are / must be prefixed with extra `Data Frame` with routing
   address.


2.2.2 Bound and unbound Connections
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This specification assumes that message transfer provided by
`Transport Channel <fbdp-transport-channel>`_ is implemented via `Transport Connection`
established between the Client and the Server. In such a case, the FBDP
`Connection <fbdp-connection>`_ MAY be bound or not to the `Transport Connection`.
This means that:

a) A bound `Connection` SHALL be terminated automatically when the `Transport Connection`
   functionality is interrupted. An unbound `Connection` assumes a mechanism exists for
   restoring an interrupted `Transport Connection`, and SHALL be terminated only if this
   mechanism fails.
b) For unbound `Connection` the `Transport Connection` does not need to be closed together
   with closing `Connection`, and MAY be reused to carry another subsequent `Connection`
   between the same `Client` and `Server`. For bound `Connection` the `Transport Connection`
   SHOULD be closed together with closing `Connection`.

The method of agreement between the `Client` and the `Server` to use the bound or unbound
`Connection` mechanism is not defined by this specification and MUST be provided by other
means. If such other means are not used, the `Connection` MUST be **bound** to
the `Transport Connection`.

2.3 FBDP Messages
-----------------

The traffic between `Client` and `Server` consists of `Messages` in a unified format sent
in both directions via a `Transport Channel <fbdp-transport-channel>`_.

2.3.1 Formal message grammar
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. _fbdp-control-frame:
.. _fbdp-data-frame:
.. _fbdp-signature:
.. _fbdp-control-byte:
.. _fbdp-flags:
.. _fbdp-type-data:

The following ABNF grammar defines the message format used by FBSP protocol::

  fbdp          = *message

  ; The message consists of a control frame, and optional data frames
  message       = control-frame *data-frame

  ; The control frame consists of a signature, control byte, flags and message-type data
  control-frame = signature control-byte flags type-data

  ; The protocol signature is a FourCC
  signature     = "FBDP" ; %x46 %x42 %x44 %x50

  ; The control byte encodes a message type, and protocol version. Both are decimal numbers.
  ; msg-type on upper (leftmost) 5 bits, version on lower (rightmost) 3 bits
  control-byte  = 1OCTET

  ; Flags consists of a single octet containing various control flags as individual bits.
  ; Bit 0 is the least significant bit (rightmost bit)
  flags         = 1OCTET

  ; Message-type specific data are two bytes
  type-data     = 2OCTET

  ; A data frame consists from zero or more octets
  data-frame    = *OCTETS

.. _fbdp-message-type:

2.3.2 Message types
^^^^^^^^^^^^^^^^^^^

The message type is an integer in the range of 1..31 stored in 5 upper (leftmost) bits
of the |control-byte|. This protocol revision defines the next message types::

  unused      = 0 ; not a valid message type
  OPEN        = 1 ; initial message from client
  READY       = 2 ; transfer negotiation message
  NOOP        = 3 ; no operation, used for keep-alive & ping purposes
  DATA        = 4 ; user data
  CLOSE       = 5 ; sent by peer that is going to close the connection

OPEN
""""

The OPEN message is a `Client` request to open a Data Pipe |Connection| to the `Server`.
The message includes |Connection| parameters required by the `Client`.

1. This message MUST be the first message sent by the `Client`.
2. The `Server` MUST reply to this message with READY_ or CLOSE_ message.
3. The first |data-frame| of this message MUST contain Data Pipe and endpoint `Identification`.
4. The content of |type-data| field in this message is not significant. **[RAW NOTE: Should we use it for something? OPEN protobuf format version? bitmap of requested common connection parameters?]**

.. seealso::

   :ref:`Data frames - OPEN <fbdp-open-dataframe>`

READY
"""""

A READY message indicates that the sender is available to transmit user data and is ready
to send / receive a specified number of DATA_ messages.

1. The |type-data| field must contain number of DATA_ messages that could be transmitted.
   Zero is an acceptable value to indicate that the sender wishes to continue transmission
   but is not ready to transmit any data at this time.
2. This message SHALL NOT have any |data-frame|.

NOOP
""""

The NOOP message means no operation. It's intended for *keep alive* purposes and
*peer availability checks*.

1. The receiving peer SHALL NOT respond to this message.
2. The sole exception to rule 1. is the case when ACK-REQUEST_ flag is set in received NOOP
   message. In such a case the receiving peer MUST respond according to rules for ACK-REQUEST_
   flag handling.
3. The content of |type-data| field in this message is not significant. However, because
   it’s returned by receiver without changes (when ACK-REQUEST flag is set), it MAY be used
   by sender for any purpose.
4. This message SHALL NOT have any |data-frame|.

.. seealso::

   `Flags - ACK-REQUEST <ACK-REQUEST>`_


DATA
""""

The DATA message is intended for delivery of arbitrary user data from `Producer` to `Consumer`.

1. The |type-data| field of the |control-frame| MAY have arbitrary content, and is fully
   available to carry information to the `Consumer`.
2. The message SHOULD contain one |data-frame| that MUST conform to the data format
   described in OPEN_ message.
3. When ACK-REQUEST_ flag is set in received DATA message, receiver MUST respond according
   to rules for ACK-REQUEST_ flag handling.

.. seealso::

   `Flags - ACK-REQUEST <ACK-REQUEST>`_, :ref:`Data frames - DATA <fbdp-data-dataframe>`


CLOSE
"""""

The CLOSE message notifies the receiver that sender is going to close the |connection|.

1. The |type-data| field of the |control-frame| MUST contain an |error-code| that indicates
   the reason why sender closed the connection.
2. The message MAY contain one or more |data-frame| that describe the error condition.
   Those data-frame parts MAY be ignored by Client.
3. The receiver SHALL NOT respond to this message.
4. The receiver SHALL NOT use the |connection| to send further messages to the sender.
5. For bound connections, the receiver SHALL close its end of the `Transport Channel`_
   immediately.

.. seealso::

   :ref:`Data frames - CLOSE <fbdp-close-dataframe>`


2.3.3 Flags
^^^^^^^^^^^

Flags are encoded as individual bits in |flags| field of the |control-frame|.

.. list-table:: Flags
   :widths: 20 10 70
   :header-rows: 1

   * - Name
     - Bit
     - Mask
   * - **ACK-REQUEST**
     - 0
     - 1
   * - **ACK-REPLY**
     - 1
     - 2

ACK-REQUEST
"""""""""""

The ACK-REQUEST flag is intended for verification and synchronization purposes.

1. Any received |control-frame| of |message-type| NOOP_ or DATA_ that have ACK-REQUEST flag
   set SHALL be sent back to the sender as confirmation of accepted message
2. Returned confirmatory message SHALL consists only from the received |control-frame| with
   ACK-REQUEST flag cleared, and with ACK-REPLY_ flag set (ie the |control-frame| MUST be
   otherwise unchanged).
3. The ACK-REQUEST flag SHALL be ignored for all |message-type| values not listed in rule 1.
4. NOOP_ message SHALL be acknowledged without any delay.
5. DATA_ message SHALL be acknowledged without any delay, unless a previous agreement
   between the `Client` and the `Server` exists to handle it differently (for example to
   send it when DATA message is actually processed and `Consumer` is able to accept another
   DATA message).

ACK-REPLY
"""""""""

The ACK-REPLY flag indicates that message is a confirmation of the message previously sent
by receiver.

1. The ACK-REPLY flag SHALL NOT be set for any message that is not a confirmation of previous
   message received with ACK-REQUEST_ flag set.
2. The message with ACK-REPLY flag set MUST conform to the rules defined for ACK-REQUEST_
   flag handling.


2.4 Data frames
---------------

Where |control-frame| contains semantic specification of the message, the |data-frame|
carry data associated with the message.

2.4.1 Common protobuf specifications
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

All Protocol Buffer definitions in this specifications build on protocol buffers defined
by :ref:`3/FBDS - 5.1 Common protobuf specifications <common-protobuf>`.

All Protocol Buffer definitions in this specifications use `proto3` syntax. This syntax
variant does not support required fields, and all fields are optional (basic types will
have the default "empty" value when they are not serialized). However, some fields in FBDP
specification are considered as mandatory (as "required" in `proto2`), and should be
validated as such by receiver.

2.4.2 FBDP Data Frames for message types
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. _fbdp-open-dataframe:

OPEN data
"""""""""

.. code-block:: protobuf

   package firebird.butler;

   import "google/protobuf/struct.proto";
   import "firebird/butler/fbsd.proto";

   message FBDPOpenDataframe {
     string                 data_pipe   = 1 ;
     uint32                 pipe_socket = 2 ;
     string                 data_format = 3 ;
     google.protobuf.Struct parameters  = 4 ;
   }

:data_pipe:
  MANDATORY Data Pipe Identification. The value MAY be arbitrary, but it is RECOMMENDED to
  use structured names, or *uuid* values in hexadecimal string representation.

:pipe_socket:
  MANDATORY Data Pipe socket Identification. Any implementation MUST support next values:

  - 0 = UNKNOWN data soscket. Not a valid option, defined only to handle undefined value.
  - 1 = INPUT data socket
  - 2 = OUTPUT data socket

:data_format:
  Specification of format for user data transmitted in DATA messages. The value MAY be
  arbitrary, but it is RECOMMENDED that the data format specification be determined by
  the open specification.

:parameters:
  Implementation-specific Data Pipe parameters.

.. _fbdp-data-dataframe:

DATA data
"""""""""

The |data-frame| content SHALL conform to following rules:

1. The total size of any single `data-frame` SHOULD NOT exceed 50MB.
2. The `Client` MAY set a |connection| limit on total size (in bytes) for any single
   message transmitted that SHALL NOT be smaller than 1MB. Such limit SHALL be announced
   to other peer in OPEN message.
3. All data formats and other specifications that define rules for |data-frame| content
   of DATA_ messages  SHOULD use serialization to store structured data into |data-frame|.
   The RECOMMENDED serialization methods are `Protocol Buffers`_ (preferred) or
   `Flat Buffers`_ (in case the direct access to parts of serialized data is required).
   It is NOT RECOMMENDED to use any verbose serialization format such as JSON or XML.
   The serialization method specified in the OPEN_ message MUST be used for all transmitted
   DATA messages within the |connection|.

.. _fbdp-close-dataframe:

CLOSE data
""""""""""

Each Data Frame must contain :ref:`3/FBSD - Error Description <error-description>` protobuf
message.


.. _fbdp-error-code:

2.5 Error codes
---------------

Error code is transmitted in |type-data| field of the CLOSE_ message, and indicates
the reason why sender closed the connection.

No error
^^^^^^^^

.. rst-class:: long-field

:0 - OK:
  The sender closes the connection normally.

General errors
^^^^^^^^^^^^^^

.. rst-class:: long-field

:1 - Invalid Message:
  The message received by peer was not a valid FBDP message.

:2 - Protocol violation:
  Received message was a valid FBDP message, but does not conformed to the protocol.
  Typically, a message of this type or content is not allowed at a particular point in
  the conversation.

:3 - Error:
  The sender encountered a condition that prevented it to continue in data transmission.

:4 - Internal Error:
  The sender encountered an unexpected condition that prevented it to continue in data transmission.

:5 - Invalid data:
  Data received in DATA_ message does not conform to the data format specification
  (if sender is a `Consumer`), or cannot be converted to the required data format
  (if sender is a `Producer`).

:6 - Timeout:
  Sender's waiting time has expired.

Errors that prevent the connection from opening
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. rst-class:: long-field

:100 - Pipe Endpoint Unavailable:
  The client requested connection to data pipe endpoint that is no available.

:101 - FBDP Version Not Supported:
  The server does not support, or refuses to support, the version of FBDP that was used in
  the OPEN_ message.

:102 - Not Implemented:
  The server does not support the functionality required by client.

:103 - Data format not supported:
  The server does not support data format required by client.


3. Reference Implementations
============================

The :ref:`Saturnin-SDK <saturnin-sdk>` provides the prime reference implementation for FBDP.

|
|

Appendix A. Flow charts
=======================

Flow charts of user data transmission in acceptable contexts and perspectives. For the sake
of clarity, NOOP_ messages and ACK-REQUEST_ flag messages are not included.

Consumer as Client
------------------

.. aafig::
   :textual:

             connect
        +=======+=======+
                |
                V
        +=======+=======+
        | send OPEN(OUT)|
        +=======+=======+
                |
                +<--------------------------------------+
                |                                       |
                V                                       |
        +=======+=======+                               |
        | WAIT for Msg  |                               |
        \-------+-------/                               |
                |                                       |
                +---------------------+                 |
                |                     |                 |
                |                     V                 |
                |             /-------+-------\         |
                |             | recv READY(X) |         |
                |             \-------+-------/         |
                |                     |                 |
                |                     V                 ^
                |             +-------+-------+ yes     |
                |             |    "X=0?"     +-------->+
                |             +-------+-------+         ^
                |                     | no              |
                |                     V                 |
                |             +=======+=======+         |
                |             | send READY(Y) |         |
                |             |   "{Y<=X}"    |         |
                |             +=======+=======+         |
                |                     | "set N=0"       |
                |                     |                 ^
                |             +-------+-------+ yes     |
                |             |    "Y=0?"     +-------->+
                |             +-------+-------+         ^
                |                     | no              |
                |                     +<------------+   |
                |                     |             |   |
                |                     V             |   |
                |             +=======+=======+     |   |
                |             | WAIT for Msg  |     |   |
                |             \-------+-------/     |   |
                |                     |             |   |
                +<--------------------+             |   |
                |                     |             |   |
                V                     V             |   |
        /-------+-------\     /-------+-------\     |   |
        | recv CLOSE(r) |     | recv DATA(d)  |     |   |
        \-------+-------/     \-------+-------/     |   |
                |                     | inc(N)      |   |
                V                     V             |   |
        +=======+=======+     +-------+-------+ yes |   |
           disconnect         +      N<Y?     +-----+   |
                              +-------+-------+         |
                                      | no              |
                                      +-----------------+


Producer as Client
------------------

.. aafig::
   :textual:
   :proportional:

             connect
        +=======+=======+
                |
                V
        +=======+=======+
        | send OPEN(IN) |
        +=======+=======+
                |
                +<--------------------------------------+
                |                                       |
                V                                       |
        +=======+=======+                               |
        | WAIT for Msg  |                               |
        \-------+-------/                               |
                |                                       |
                +---------------------+                 |
                |                     |                 |
                +<---------+          |                 |
                |          |          |                 |
                V          |          V                 |
        /-------+-------\  |  /-------+-------\         |
        | recv CLOSE(r) |  |  | recv READY(X) |         |
        \-------+-------/  |  \-------+-------/         |
                |          |          |                 |
                V          |          V                 ^
        +=======+=======+  |  +-------+-------+ yes     |
           disconnect      |  |    "X=0?"     +-------->+
                           |  +-------+-------+         ^
                           |          | no              |
                           |          V                 |
                           |  +=======+=======+         |
                           |  | send READY(Y) |         |
                           |  |   "{Y<=X}"    |         |
                           |  +=======+=======+         |
                           |          |                 |
                           |          V                 ^
                           |  +-------+-------+ yes     |
                           |  |     "Y=0?"    +-------->+
                           |  +-------+-------+         ^
                           |          | "no, set N=0"   |
                           |          |                 |
                           |          +<------------+   |
                           |          |             |   |
                           |          V             |   |
                           |  +=======+=======+     |   |
                           |  | POLL for Msg  |     |   |
                           |  \-------+-------/     |   |
                           | if msg   |             |   |
                           +----------+             |   |
                                      | no msg      |   |
                                      V             |   |
                          yes +-------+-------+     |   |
               +--------------+      EOF?     |     |   |
               |              +-------+-------+     |   |
               V                      | no          |   |
       +=======+=======+              V             |   |
       | send CLOSE(OK)|      +=======+=======+     |   |
       +=======+=======+      | send DATA(d)  |     |   |
               |              +=======+=======+     |   |
               V                      | inc(N)      |   |
       +=======+=======+              V             |   |
          disconnect          +-------+-------+ yes |   |
                              |      N<Y?     +-----+   |
                              +-------+-------+         |
                                      | no              |
                                      +-----------------+

Consumer as Server
------------------

.. aafig::
   :textual:

              bind
        +=======+=======+
                |
                +<-----------------------------<-+<------------------+
                |                                ^                   |
                V                                |                   |
        +=======+=======+                        |                   |
        | WAIT for Msg  |                        |                   |
        \-------+-------/                        |                   |
                |                                |                   |
                V                                |                   |
        /-------+-------\                        |                   |
        | recv OPEN(IN) |                        |                   |
        \-------+-------/                        |                   |
                |                                |                   |
                V                                |                   |
        +-------+-------+ no  +===============+  |                   |
        |  request OK?  +---->+ send CLOSE(E) +--+                   |
        +-------+-------+     +===============+                      |
                | yes                                                |
                V                                                    |
        +-------+-------+ no  +===============+    +---------------+ |
     +->+ ready to rcv? +---->+ send READY(0) +--->+  get ready A  | |
     |  +-------+-------+     +===============+    +-------+-------+ |
     |          | yes                                      |         |
     |          V                                          |         |
     |  +=======+=======+                                  V         |
     |  | send READY(X) +<---------------------------------+         |
     |  +=======+=======+                                  ^         |
     |          |                                          |         |
     |          +---------------------+                    |         |
     |          |                     |                    |         |
     |          V                     V                    |         |
     |  /-------+-------\     /-------+-------\            |         |
     |  | recv READY(Y) |     | recv CLOSE(r) |            |         |
     |  \-------+-------/     \-------+-------/            |         ^
     |          |                     |                    |         |
     |          |                     +--------->--------- | ------->+
     |          |                                          |         ^
     |          |                                          |         |
     |          |                                          |         |
     |  +-------+-------+ yes                      +-------+-------+ |
     |  |    "Y=0?"     +------------------------->+  get ready B  | |
     |  +-------+-------+                          +---------------+ |
     |          | no                                                 |
     |          | "set N=0"                                          |
     |          V                                                    |
     |  +=======+=======+                                            |
     |  | WAIT for Msg  |<-----------------------+                   |
     |  \-------+-------/                        |                   |
     |          |                                |                   |
     |          +---------------------+          |                   |
     |          |                     |          |                   |
     |          V                     V          |                   |
     |  /-------+-------\     /-------+-------\  |                   |
     |  | recv DATA(d)  |     | recv CLOSE(r) |  |                   |
     |  \-------+-------/     \-------+-------/  |                   |
     |          | inc(N)              |          |                   |
     |          |                     +---->---- | ---------->-------+
     |          |                                |
     |          |                                |
     |  +-------+-------+ yes                    |
     |  |     N<Y?      +------------------------+
     |  +-------+-------+
     |          | no
     +----------+


:get ready A:
   The server SHALL eventually send either READY(X) or CLOSE(Err) message to the client.
   While Server is not ready to receive data, it MUST periodically check incoming messages
   for CLOSE message.

:get ready B:
   The server SHALL periodically send READY(X) message to the client, and MAY eventually
   send the CLOSE message.

Producer as Server
------------------

.. aafig::
   :textual:

              bind
        +=======+=======+
                |
                +<-----------------------------<-+<------------------+
                |                                ^                   |
                V                                |                   |
        +=======+=======+                        |                   |
        | WAIT for Msg  |                        |                   |
        \-------+-------/                        |                   |
                |                                |                   |
                V                                |                   |
        /-------+-------\                        |                   |
        | recv OPEN(OUT)|                        |                   |
        \-------+-------/                        |                   |
                |                                |                   |
                V                                |                   |
        +-------+-------+ no  +===============+  |                   |
        |  request OK?  +---->+ send CLOSE(E) +--+                   |
        +-------+-------+     +===============+                      |
                | yes                                                |
                V                                                    |
        +-------+-------+ no  +===============+    +---------------+ |
     +->+ ready to snd? +---->+ send READY(0) +--->+  get ready A  | |
     |  +-------+-------+     +===============+    +-------+-------+ |
     |          | yes                                      |         |
     |          V                                          |         |
     |  +=======+=======+                                  V         |
     |  | send READY(X) +<---------------------------------+         |
     |  +=======+=======+                                  ^         |
     |          |                                          |         |
     |          +---------------------+                    |         |
     |          |                     |                    |         |
     |          V                     V                    |         |
     |  /-------+-------\     /-------+-------\            |         |
     |  | recv READY(Y) |     | recv CLOSE(r) |            |         |
     |  \-------+-------/     \-------+-------/            |         ^
     |          |                     |                    |         |
     |          |                     +--------->--------- | ------->+
     |          |                                          |         ^
     |  +-------+-------+ yes                      +-------+-------+ |
     |  |    "Y=0?"     +------------------------->+  get ready B  | |
     |  +-------+-------+                          +---------------+ |
     |          | no                                                 |
     |          | "set N=0"                                          |
     |          V                                                    |
     |  +-------+-------+ yes  +===============+                     |
     |  |      EOF?     +----->+ send CLOSE(OK)+--------->-----------+
     |  +-------+-------+      +===============+
     |          | no
     |          V
     |  +=======+=======+
     |  | send DATA(d)  +<---+
     |  +=======+=======+    |
     |          | inc(N)     |
     |          V            |
     |  +-------+-------+ no |
     |  |     "N=Y?"    +----+
     |  +-------+-------+
     |          | yes
     +----------+

:get ready A:
   The server SHALL eventually send either READY(X) or CLOSE(Err) message to the client.
   While Server is not ready to send data, it MUST periodically check incoming messages
   for CLOSE message.

:get ready B:
   The server SHALL periodically send READY(X) message to the client, and MAY eventually
   send the CLOSE message.


Appendix B. Transmission patterns
=================================

All patterns use only asynchronous transfer. This means that all processes constantly
monitor the communication channel for incoming messages. The **thick** line in the activity
diagram means that the process MUST wait for a specific message to be received. A **thin**
line means that the process performs normal processing, including the immediate processing
of incoming messages.


B.1 Producer - Filter - Consumer chains
---------------------------------------

Example transmission patterns send user data from `Producer <P>` through `Filter <F>` to
`Consumer <C>`.

- The `Filter` uses two transmission channels, one to get data from the `Producer`, and
  one to pass data to the `Consumer`.
- The `Filter` consumes two DATA packets from `Producer` to produce one data packet to `Consumer`.
- The `Consumer` accepts data in batch of 8 DATA messages if possible.
- The `Producer` sends data in batch of 5 DATA messages if possible.
- The `Filter` adapts data batch sizes to `Producer` and `Consumer` according to particular
  pattern.
- For the sake of clarity, NOOP messages and ACK-REQUEST flag messages are not used.

.. note::

   The same patterns apply to `Filters` that simply pass messages between `Producer` and
   `Consumer` as pure `Router`.


Client - Server/Client - Server
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. important::

   This pattern requires that peers are started in next order:

   1. Consumer
   2. Filter
   3. Producer

Batch sizes:

- Because the `Consumer` is `Server`, it requests batch of 8 DATA messages.
- The `Filter` as `Client` adapts to `Consumer` (uses requested batch size) and requests
  batch of 16 DATA messages from `Producer` (in attempt to streamline the transfer by batch
  end alignment). This request is downsized by `Producer` to 5 DATA messages and accepted
  by `Filter` as max. throughput from `Producer` (used for all subsequent batches).

.. aafig::
   :textual:

           P                        F                       C
      ===========      ==========================      ===========
            transport channel              transport channel
      <-------------------------->    <-------------------------->
      +---------+      +---------+    +---------+      +---------+
      | Client  |      | Server  |    | Client  |      | Server  |
      | OUTPUT  |      |  INPUT  |    | OUTPUT  |      |  INPUT  |
      +----+----+      +----+----+    +----+----+      +----+----+
           |                |              |                |
           |                |              |                X bind C
           |                |              |                X await conn
           |                X bind F       | connect C      X
           | connect F      X await conn   |                X
           |                X              |    OPEN(IN)    X
           |    OPEN(IN)    X              X--------------->X
           X--------------->X              X                |
           X    READY(0)    |              X                |
           X<---------------X              X                |
           X                X              X    READY(8)    |
           X                X  connected   X<---------------X
           X                X              |                X
           X                X<-------------+                X
           X    READY(16)   |              |                X
           X<---------------X              |                X
           |    READY(5)    X  data avail  |    READY(8)    X
           +--------------->X------------->+--------------->X
           |    DATA<1P>    X              |                X
           +--------------->X              |                X
           |    DATA<2P>    X produce data |    DATA<1F>    X
           +--------------->X------------->+--------------->X
           |    DATA<3P>    X              |                X
           +--------------->X              |                X
           |    DATA<4P>    X produce data |    DATA<2F>    X
           +--------------->X------------->+--------------->X
           |    DATA<5P>    X              |                X
           X--------------->X              |                X
           X    READY(5)    |              |                X
           X<---------------X              |                X
           |    READY(5)    X              |                X
           +--------------->X              |                X
           |    DATA<1P>    X produce data |    DATA<3F>    X
           +--------------->X------------->+--------------->X
           |    DATA<2P>    X              |                X
           +--------------->X              |                X
           |                X              |                X

      "alternative A - CLOSE from Producer"
      - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

           |                X              |                X
           |    CLOSE(rP)   X              |    CLOSE(rF)   X
           +--------------->X------------->+--------------->X
           | disconnect     X await conn   | disconnect     X await conn

      "alternative B - CLOSE from Consumer"
      - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

           |                X              |                X
           |    CLOSE(rF)   X              |    CLOSE(rC)   X
           +<---------------X<-------------+<---------------X
           | disconnect     X await conn   | disconnect     X await conn




Server - Client/Server - Client
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. important::

   This pattern requires that peers are started in next order:

   1. Producer
   2. Filter
   3. Consumer

Batch sizes:

- Because the `Producer` is `Server`, the batch size of 5 DATA messages is accepted by
  `Filter` as max. throughput.
- The `Filter` announces batch size of 10 DATA messages to `Consumer` in attempt to
  streamline the transfer by batch end alignment. This request is downsized by `Consumer`
  to 8 DATA messages and accepted (used for all subsequent batches) by `Filter` as max.
  throughput to `Consumer`.


.. aafig::
   :textual:

           P                        F                       C
      -==========      ==========================      ===========
            transport channel              transport channel
      <-------------------------->    <-------------------------->
      +---------+      +---------+    +---------+      +---------+
      | Server  |      | Client  |    | Server  |      | Client  |
      | OUTPUT  |      |  INPUT  |    | OUTPUT  |      |  INPUT  |
      +----+----+      +----+----+    +----+----+      +----+----+
           |                |              |                |
           X bind P         |              |                |
           X await conn     | connect P    X bind F         |
           X                |              X await conn     |
           X   OPEN(OUT)    |              X                |
           X<---------------X              X                |
           |   READY(5)     X              X                |
           X--------------->X              X                | connect F
           X   READY(0)     |              X   OPEN(OUT)    |
           X<---------------X              X<---------------X
           |                X              |                X
           |   READY(5)     X  data avail  |   READY(10)    X
           X--------------->X------------->X--------------->X
           X   READY(5)     |  output set  X   READY(8)     |
           X<---------------X<-------------X<---------------X
           |   DATA<1P>     X              |                X
           +--------------->X              |                X
           |   DATA<2P>     X produce data |   DATA<1F>     X
           +--------------->X------------->+--------------->X
           |   DATA<3P>     X              |                X
           +--------------->X              |                X
           |   DATA<4P>     X produce data |   DATA<2F>     X
           +--------------->X------------->+--------------->X
           |   DATA<5P>     X              |                X
           +--------------->X              |                X
           |   READY(5)     X              |                X
           X--------------->X              |                X
           X   READY(5)     |              |                X
           X<---------------X              |                X
           |   DATA<1P>     X produce data |   DATA<3F>     X
           +--------------->X------------->+--------------->X
           |                X              |                X

      "alternative A - CLOSE from Producer"
      - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

           |                X              |                X
           |    CLOSE(rP)   X              |    CLOSE(rF)   X
           X--------------->X------------->X--------------->X
           X await conn     | disconnect   X await conn     | disconnect

      "alternative B - CLOSE from Consumer"
      - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

           |                X              |                X
           |    CLOSE(rF)   X              |    CLOSE(rC)   X
           X<---------------X<-------------X<---------------X
           X await conn     | disconnect   X await conn     | disconnect


Server - Client/Client - Server
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. important::

   This pattern requires that peers are started in next order:

   1. Producer & Consumer
   2. Filter

Batch sizes:

- Because both `Producer` and `Consumer` are servers, they impose sizes.
- `Filter` accepts to batch size from servers and adapts accordingly.

.. aafig::
   :textual:

           P                        F                       C
      ===========      ==========================      ===========
            transport channel              transport channel
      <-------------------------->    <-------------------------->
      +---------+      +---------+    +---------+      +---------+
      | Server  |      | Client  |    | Client  |      | Server  |
      | OUTPUT  |      |  INPUT  |    | OUTPUT  |      |  INPUT  |
      +----+----+      +----+----+    +----+----+      +----+----+
           |                |              |                |
           X bind P         |              |                X bind C
           X await conn     |              |                X await conn
           X                |              |                X
           X                | connect P    | connect C      X
           X                |              |                X
           X   OPEN(OUT)    |              |   OPEN(IN)     X
           X<---------------X              X--------------->X
           |   READY(5)     X              X    READY(8)    |
           X--------------->X              X<---------------X
           X   READY(5)     |              |    READY(8)    X
           X<---------------X              +--------------->X
           |   DATA<1P>     X              |                X
           +--------------->X              |                X
           |   DATA<2P>     X produce data |    DATA<1F>    X
           +--------------->X------------->+--------------->X
           |   DATA<3P>     X              |                X
           +--------------->X              |                X
           |   DATA<4P>     X produce data |    DATA<2F>    X
           +--------------->X------------->+--------------->X
           |   DATA<5P>     X              |                X
           +--------------->X              |                X
           |   READY(5)     X              |                X
           X--------------->X              |                X
           X   READY(5)     |              |                X
           X<---------------X              |                X
           |   DATA<1P>     X produce data |    DATA<3F>    X
           +--------------->X------------->+--------------->X
           |                X              |                X

      "alternative A - CLOSE from Producer"
      - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

           |                X              |                X
           |    CLOSE(rP)   X              |    CLOSE(rF)   X
           X--------------->X------------->X--------------->X
           X await conn     | disconnect   X await conn     | disconnect

      "alternative B - CLOSE from Consumer"
      - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

           |                X              |                X
           |    CLOSE(rF)   X              |    CLOSE(rC)   X
           X<---------------X<-------------X<---------------X
           X await conn     | disconnect   X await conn     | disconnect


Client - Server/Server - Client
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. important::

   This pattern requires that peers are started in next order:

   1. Filter
   2. Producer & Consumer

Batch sizes:


- Because the `Filter` has the `Server` role for both `Producer` and `Consumer`, it has
  the ability to initialize the maximum batch size. For this case, this size is 1000 messages.

.. tip::

   This pattern is particularly useful for implementation of Services that provide stable,
   globally defined Data Pipes using a `Router` as a middleman.


.. aafig::
   :textual:

           P                        F                       C
      ===========      ==========================      ===========
            transport channel              transport channel
      <-------------------------->    <-------------------------->
      +---------+      +---------+    +---------+      +---------+
      | Client  |      | Server  |    | Server  |      | Client  |
      | OUTPUT  |      |  INPUT  |    | OUTPUT  |      |  INPUT  |
      +----+----+      +----+----+    +----+----+      +----+----+
           |                |              |                |
           |                X bind F       X bind F         |
           |                X await conn   X await conn     |
           | connect F      X              X                |
           |                X              X                |
           |   OPEN(IN)     X              X                |
           X--------------->X              X                |
           X   READY(0)     | no out peer  X                | connect F
           X<---------------+              X                |
           X                |              X   OPEN(OUT)    |
           X                |              X<---------------X
           X                |              |   READY(1000)  X
           X                |              X--------------->X
           X   READY(16)    | output avail X   READY(8)     |
           X<---------------X<-------------X<---------------X
           |   READY(5)     X              |                X
           +--------------->X              |                X
           |   DATA<1P>     X              |                X
           +--------------->X              |                X
           |   DATA<2P>     X produce data |   DATA<1F>     X
           +--------------->X------------->+--------------->X
           |   DATA<3P>     X              |                X
           +--------------->X              |                X
           |   DATA<4P>     X produce data |   DATA<2F>     X
           +--------------->X------------->+--------------->X
           |   DATA<5P>     X              |                X
           X--------------->X              |                X
           X   READY(5)     |              |                X
           X<---------------X              |                X
           |   READY(5)     X              |                X
           +--------------->X              |                X
           |   DATA<1P>     X produce data |   DATA<3F>     X
           +--------------->X------------->+--------------->X
           |   DATA<2P>     X              |                X
           +--------------->X              |                X
           |                X              |                X

      "alternative A - CLOSE from Producer"
      - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

           |                X              |                X
           |    CLOSE(rP)   X              |    CLOSE(rB)   X
           +--------------->X------------->X--------------->X
           | disconnect     X await conn   X await conn     | disconnect

      "alternative B - CLOSE from Consumer"
      - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

           |                X              |                X
           |    CLOSE(rP)   X              |    CLOSE(rB)   X
           +<---------------X<-------------X<---------------X
           | disconnect     X await conn   X await conn     | disconnect


|
|

.. _RFC2119: http://tools.ietf.org/html/rfc2119
.. _ZMTP: https://rfc.zeromq.org/spec:23/ZMTP
.. _ROUTER: https://rfc.zeromq.org/spec:28/REQREP/
.. _DEALER: https://rfc.zeromq.org/spec:28/REQREP/
.. _Protocol Buffers: https://developers.google.com/protocol-buffers/
.. _Flat Buffers: https://github.com/google/flatbuffers
.. |COSS-long| replace:: :doc:`/rfc/2/COSS`
.. |FBSD| replace:: :doc:`3/FBSD</rfc/3/FBSD>`
.. |FBSP| replace:: :doc:`4/FBSP</rfc/4/FBSP>`
.. |FBLP| replace:: :doc:`5/FBLP</rfc/5/FBLP>`
.. |SSTP| replace:: :doc:`6/SSTP</rfc/6/SSTP>`
.. |RSCFG| replace:: :doc:`7/RSCFG</rfc/7/RSCFG>`
.. |Data Pipe Definition| replace:: :ref:`3/FBSD - Data Pipe Definition<data pipes>`
.. |control-frame| replace:: :ref:`control-frame<fbdp-control-frame>`
.. |data-frame| replace:: :ref:`data-frame<fbdp-data-frame>`
.. |flags| replace:: :ref:`flags<fbdp-flags>`
.. |control-byte| replace:: :ref:`control-byte<fbdp-control-byte>`
.. |type-data| replace:: :ref:`type-data<fbdp-type-data>`
.. |message-type| replace:: :ref:`message-type<fbdp-message-type>`
.. |connection| replace:: :ref:`Connection<fbdp-connection>`
.. |error-code| replace:: :ref:`Error Code<fbdp-error-code>`
