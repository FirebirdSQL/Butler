#########################################
4/FBSP - Firebird Butler Service Protocol
#########################################

:domain: github.com/FirebirdSQL/Butler
:shortname: 4/FBSP
:name: Firebird Butler Service Protocol
:status: draft
:editor: Pavel Císař <pcisar@users.sourceforge.net>

The Firebird Butler Service Protocol (FBSP) defines formal rules for exchanging messages between Butler Service and its Client over Service Sockets as they are defined in |FBSD|.

License
=======

Copyright (c) 2018, 2019 The Firebird Butler Project.

This Specification is distributed under Creative Commons Attribution-ShareAlike 4.0 International license.

You should have received a copy of the CC BY-SA 4.0 along with this document; if not, see https://creativecommons.org/licenses/by-sa/4.0/

Change Process
==============

This Specification is a free and open standard and is governed by the Consensus-Oriented Specification System (COSS) (see "|COSS-long|").

.. important::

   This specification is still incomplete (work in progress), hence the COSS change process is not yet fully applicable. All ideas and change proposals SHOULD be presented and discussed first in the `Firebird Butler forum <https://groups.google.com/d/forum/firebird-butler>`_.

..
   Unfinished parts:

   .. todolist::

Language
========

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in `RFC2119`_.

Related Specifications
======================

#. :doc:`/rfc/3/FBSD`

1. Goals
========

The purpose of this specification is to define formal rules for exchanging messages between Butler Service and its Client. Its goals are:

#. Define the uniform structure of messages passed between the service and its client.
#. Standardize the format of the application interface between otherwise independent components.
#. Provide the resources necessary to implement efficient and reliable synchronous and asynchronous communication between components with both tight and loose bindings in diverse operating environments.


2. Implementation
=================

.. _connection:
.. _transport channel:

2.1 Overall Behavior
--------------------

The specification requires the existence of a transport channel capable of asynchronously transmitting messages in both directions (referred to as `Transport Channel`), where individual messages are constituted by one or more uniquely separate data blocks (referred to as `Frames`). The `Transport Channel` must also conform to following rules:

1. A message SHALL NOT be delivered more than once to any peer.
2. All messages between two immediate peers SHALL be delivered in order.

.. tip::

   Such transmissions are provided by ZeroMQ Message Transfer Protocol (ZMTP_) over ROUTER_ (and DEALER) sockets.

Exchange of messages on the `Transport Channel` is implemented as a `Connection` between the `Service` and the `Client` where the connection has the following stages:

1. The `Client` MUST initiate the connection by sending the HELLO_ message.
2. The `Service` MUST reply to the HELLO_ message by sending a WELCOME_ message to confirm the connection. If the Service cannot accept the connection, it MUST send the ERROR_ message instead.
3. After confirming a successful `Connection`, the `Client` can start sending messages to which the `Service` responds by sending one or more messages of its own.
4. The `Client` or `Service` can terminate the `Connection` at any time by sending a CLOSE_ message, or by closing the `Transport Channel`. However, the peer initiating the connection termination SHOULD send the CLOSE_ message before it closes the Transport Channel to the other peer.

.. important::

   The conversation is always managed by the `Client`, that is, each message sent by the `Service` is always part of the response to some previous message sent by `Client`.

.. _identity:
.. _Client Identity:
.. _Service Identity:

2.2 Client and Service Identity
-------------------------------

Both the `Client` and the `Service` must be uniquely identified. For this purpose, the specification introduces the concepts of `Client Identity` and `Service Identity`, collectively as `Identity`.

1. The content of the `Identity` MAY be arbitrary.
2. There MUST be a canonical string `Identity` representation.
3. Both the `Client Identity` and the `Service Identity` MUST be unique in the same namespace.
4. Both the `Client` and the `Service` MUST use the `Identity` for all identification purposes.
5. If `Service` acts as a `Client` to another Service, then MUST use its own `Service Identity` as the `Client Identity` to the another Service.
6. It is RECOMMENDED that both the `Client` and the `Service` use the `Identity` for routing purposes.
7. It is RECOMMENDED to use UUID_ as `Identity`.

.. tip::

   When implementing FBSP using ZeroMQ sockets as a `Transport Channel`_, it is RECOMMENDED that the `Client` or `Service` assign their `Identity` as the identity of all ZeroMQ sockets used for FBSP protocol messaging.

2.3 The Connection and the Transport Channel
--------------------------------------------

2.3.1 Using one Channel for multiple Connections
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A single `Transport channel`_ MAY be used for message transmission for several concurrently active `Connections`. This specification does not define how the message routing for individual connections should be done, neither the necessary encapsulation of the FBSP protocol messages into the messages transmitted by the multi-transport channel. However, the possible implementation of the multi-transport channel MUST be completely transparent from the point of view of the FBSP.

.. note::

   For example, if transmission is implemented using ZeroMQ ROUTER_ socket, all FBSP messages flowing through it are / must be prefixed with extra `Data Frame` with routing address.


2.3.2 Bound and unbound Connections
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This specification assumes that message transfer provided by `Transport Channel`_ is implemented via `Transport Connection` established between the Client and the Service. In such a case, the FBSP Connection_ MAY be bound or not to the `Transport Connection`. This means that:

a) A bound `Connection` SHALL be terminated automatically when the `Transport Connection` functionality is interrupted. An unbound `Connection` assumes a mechanism exists for restoring an interrupted `Transport Connection`, and SHALL be terminated only if this mechanism fails.
b) For unbound `Connection` the `Transport Connection` does not need to be closed together with closing `Connection`, and MAY be reused to carry another subsequent `Connection` between the same `Client` and `Service`. For bound `Connection` the `Transport Connection` SHOULD be closed together with closing `Connection`.

The method of agreement between the `Client` and the `Service` to use the bound or unbound `Connection` mechanism is not defined by this specification and MUST be provided by other means. If such other means are not used, the `Connection` MUST be **bound** to the `Transport Connection`.


2.4 FBSP Messages
-----------------

The traffic between `Client` and `Service` consists of `Messages` in a unified format sent in both directions via a `Transport Channel`_.

FBSP is designed to carry arbitrary `Service API` in unified message format. This is achieved by dividing the contents of the messages into a structural part (`Control Frame`) and a data (`Data Frames`). In addition to the basic structural information, the `Control Frame` also includes a space for the transmission of control data for the `Service API`. The API's main point is the `Request Code`_ that uniquely identifies the required functionality (API call). FBSP does not define (or reserve) any `Request Code`_ for itself, so all values are available for use by `Service`. With few exceptions, all `Data Frames` are considered as part of the `Service API`, and are not regulated by this specification.

2.4.1 Formal message grammar
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. _control-frame:
.. _data-frame:
.. _signature:
.. _control-byte:
.. _flags:
.. _type-data:
.. _token:

The following ABNF grammar defines the message format used by FBSP protocol::

  fbsp          = *message

  ; The message consists of a control frame, and zero or more data frames
  message       = control-frame *data-frame

  ; The control frame consists of a signature, control byte, flags, message-type data, and message token
  control-frame = signature control-byte flags type-data token

  ; The protocol signature is a FourCC
  signature     = "FBSP" ; %x46 %x42 %x53 %x50

  ; The control byte encodes a message type, and protocol version. Both are decimal numbers.
  ; msg-type on upper (leftmost) 5 bits, version on lower (rightmost) 3 bits
  control-byte  = 1OCTET

  ; Flags consists of a single octet containing various control flags as individual bits.
  ; Bit 0 is the least significant bit (rightmost bit)
  flags         = 1OCTET

  ; Message-type specific data are two bytes
  type-data     = 2OCTET

  ; Message token is 8 bytes
  token         = 8OCTET

  ; A data frame consists from zero or more octets
  data-frame    = *OCTETS

.. _message-token:

2.4.2 Message token
^^^^^^^^^^^^^^^^^^^

The FBSP allows asynchronous communication between the `Client` and the `Service`, and also allows the `Service` to send several messages in response to one message sent by the `Client`. `Message Token` is a client-specified data block that is sent back to the `Client` by a `Service` without change, in each message that is a logical response to that message.

Processing of the token is governed by the following rules:

1. The content of the `Message Token` MAY be arbitrary.
2. The content of the `Message Token` SHALL be specified by `Client` only.
3. The `Message Token` MUST be returned without change in any message sent by the `Service`, which is a logical response to the original message sent by the `Client` containing that token.
4. Messages sent by a `Service` that can not be uniquely identified as a logical response to a previous message sent by a `Client` (such as unexpected general ERROR_, CLOSE_, or NOOP_ sent to check the client's availability) MUST contain the `Message Token` passed by the `Client` in the HELLO_ message.

.. important::

   This specification does not define in any way how the `Client` should use the `Message Token`, nor does it prescribe that it should be used at all. However, the `Message Token` SHOULD be used by the `Client` whenever there is a need to assign messages sent by the `Service` to the original request source (for example for internal routing purposes or reliable implementation of parallel `Client` requests).

.. _message-type:

2.4.3 Message types
^^^^^^^^^^^^^^^^^^^

The message type is an integer in the range of 1..31 stored in 5 upper (leftmost) bits of the control-byte_. This protocol revision defines the next message types::

  unused      = 0      ; not a valid message type
  HELLO       = 1      ; initial message from client
  WELCOME     = 2      ; initial message from service
  NOOP        = 3      ; no operation, used for keep-alive & ping purposes
  REQUEST     = 4      ; client request
  REPLY       = 5      ; service response to client request
  DATA        = 6      ; separate data sent by either client or service
  CANCEL      = 7      ; cancel request
  STATE       = 8      ; operating state information
  CLOSE       = 9      ; sent by peer that is going to close the connection
  reserved    = 10..30 ; reserved for future use
  ERROR       = 31     ; error reported by service

The `Client` SHALL send only messages of following types::

  HELLO       : must be the first message in conversation
  NOOP        : presence check
  REQUEST     : request to service
  CANCEL      : cancel previous request
  DATA        : data package sent to service
  CLOSE       : client is about to close the connection

The `Service` SHALL send only messages of following types::

  ERROR       : error is always an error
  WELCOME     : must be the first message in conversation
  NOOP        : presence check
  REPLY       : reply to REQUEST message
  DATA        : data package sent to client
  STATE       : operating state information
  CLOSE       : service is about to close the connection

HELLO
"""""

The HELLO message is a `Client` request to open a Connection_ to the `Service`. The message includes basic information about the `Client` and Connection_ parameters required by the `Client`.

1. This message MUST be the first message sent by the `Client`.
2. The `Service` MUST reply to this message with WELCOME_ or ERROR_ message.
3. The first data-frame_ of this message MUST contain the `Client Identity`_.
4. If the `Service` records an open Connection_ for a `Client` with the same `Client Identity`_, it MUST respond with ERROR_ message, and refuse the connection.
5. The content of type-data_ field in this message is not significant. **[RAW NOTE: Should we use it for something? HELLO protobuf format version? bitmap of requested common connection parameters?]**

.. seealso::

   :ref:`Data frames - HELLO <hello-dataframe>`

WELCOME
"""""""

The WELCOME message is the response of the `Service` to the HELLO_ message sent by the `Client`, which confirms the successful creation of the required Connection_ and announces basic parameters of the `Service` and the Connection_.

1. The first data-frame_ of this message MUST contain the `Service Identity`_ and the specification of `Service API`_.
2. The content of type-data_ field in this message is not significant. **[RAW NOTE: Should we use it for something? WELCOME protobuf format version? bitmap of available common service abilities?]**

.. seealso::

   :ref:`Data frames - WELCOME <welcome-dataframe>`

NOOP
""""

The NOOP message means no operation. It's intended for *keep alive* purposes and *peer availability checks*.

1. The receiving peer SHALL NOT respond to this message.
2. The sole exception to rule 1. is the case when ACK-REQUEST_ flag is set in received NOOP message. In such a case the receiving peer MUST respond according to rules for ACK-REQUEST_ flag handling.
3. The content of type-data_ field in this message is not significant. However, because it’s returned by receiver without changes (when ACK-REQUEST flag is set), it MAY be used by sender for any purpose.
4. This message SHALL NOT have any data-frame_.

.. seealso::

   `Flags - ACK-REQUEST <ACK-REQUEST>`_

REQUEST
"""""""

The REQUEST message is a `Client` request to the `Service`.

1. The type-data_ field of the control-frame_ MUST contain a `Request Code`_.
2. The message MAY contain one or more data-frame_ that MUST conform to the API defined for particular `Request Code`_.
3. The `Service` MUST respond to this message by sending REPLY_ or ERROR_ message with the same `Request Code`_ in type-data_ field.
4. The `Service` MAY send additional subsequent messages in response to the same REQUEST message.
5. The type and number of messages in reply to particular request, as well as method for indicating the end of the message stream to the `Client` SHALL be defined by the API for particular `Request Code`_.
6. When ACK-REQUEST_ flag is set in received REQUEST message, the `Service` MUST respond according to rules for ACK-REQUEST_ flag handling.

.. seealso::

   `Flags - ACK-REQUEST <ACK-REQUEST>`_

REPLY
"""""

The REPLY message is a `Service` reply to the REQUEST_ message previously sent by `Client`.

1. The type-data_ field of the control-frame_ MUST contain the `Request Code`_ from Client REQUEST_ message.
2. The message MAY contain one or more data-frame_ that MUST conform to the API defined for particular `Request Code`_.
3. The `Service` SHOULD NOT send more than one REPLY message to any single REQUEST message received. If reply requires more than single message, the REPLY message SHALL be the first message sent and subsequent messages SHOULD be of type DATA_ or STATE_.
4. The `Client` SHALL NOT respond to this message.
5. The sole exception to rule 4. is the case when ACK-REQUEST_ flag is set in received REPLY message. In such a case the `Client` MUST respond according to rules for ACK-REQUEST_ flag handling.

.. seealso::

   `Flags - ACK-REQUEST <ACK-REQUEST>`_

DATA
""""

The DATA message is intended for delivery of arbitrary data between connected peers.

1. The type-data_ field of the control-frame_ MAY have arbitrary content, and is fully available for the `Service` API.
2. The message SHOULD contain one or more data-frame_ that MUST conform to the API defined for particular `Request Code`_.
3. The FBSP does not provide any means to pair DATA messages sent by `Client` to the request they are related to. If `Service` API requires such assignment, it MUST be handled by API itself via content of transmitted data-frame_ parts of the message, or by type-data_ field of the control-frame_.
4. The receiver SHALL NOT respond to this message, with sole exceptions defined by rules 5. and 6.
5. When ACK-REQUEST_ flag is set in received DATA message, receiver MUST respond according to rules for ACK-REQUEST_ flag handling.
6. The `Service` MAY reply to received DATA message with ERROR_ message.

.. seealso::

   `Flags - ACK-REQUEST <ACK-REQUEST>`_

CANCEL
""""""

The CANCEL message represents a request for a `Service` to stop processing the previous request from the `Client`.

1. One CANCEL message is a request to end the processing of one active request.
2. The content of type-data_ field in this message is not significant.
3. The message MUST have a data-frame_ with specification of the request whose processing is to be terminated. The data-frame_ MAY contain additional information.
4. The `Service` MUST respond with the ERROR_ message with appropriate `Error Code`_. 
5. If `Service` successfully terminated specified active `Client` request, the ERROR_ message MUST have `Request Cancelled` `Error Code`_.
6. The ERROR_ message MAY have a data-frame_ with additional information.

.. seealso::

   `Flags - ACK-REQUEST <ACK-REQUEST>`_, :ref:`Data frames - CANCEL <cancel-dataframe>`

STATE
"""""

The STATE message is sent by `Service` to report its operating state to the `Client`.

1. The `Service` SHALL NOT send the STATE message on its own discretion, but only in relation to REQUEST_ message previously sent by `Client`.
2. The type-data_ field of the control-frame_ MUST contain the `Request Code`_ from Client REQUEST_ message this STATE message relates to.
3. The message MUST contain a data-frame_ with state information that conforms to the API defined for particular `Request Code`_.
4. The `Client` SHALL NOT respond to this message.
5. The sole exception to rule 4. is the case when ACK-REQUEST_ flag is set in received STATE message. In such a case the `Client` MUST respond according to rules for ACK-REQUEST_ flag handling.

.. seealso::

   `Flags - ACK-REQUEST <ACK-REQUEST>`_, :ref:`Data frames - STATE <state-dataframe>`

CLOSE
"""""

The CLOSE message notifies the receiver that sender is going to close the Connection_.

1. The receiver SHALL NOT respond to this message.
2. The receiver SHALL NOT use the Connection_ to send further messages to the sender.
3. For bound connections, the receiver SHALL close its end of the `Transport Channel`_ immediately.


ERROR
"""""

The ERROR message notifies the `Client` about error condition detected by `Service`.

1. The type-data_ field of the control-frame_ MUST contain the `Error Code`_.
2. The message MAY contain one or more data-frame_ that describe the error condition. Those data-frame_ parts MAY be ignored by `Client`.
3. The `Client` SHALL NOT respond to this message.

.. seealso::

   `Error codes`_, :ref:`Data frames - ERROR <error-dataframe>`

2.4.4 Flags
^^^^^^^^^^^

Flags are encoded as individual bits in flags_ field of the control-frame_.

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
   * - **MORE**
     - 3
     - 4

ACK-REQUEST
"""""""""""

The ACK-REQUEST flag is intended for verification and synchronization purposes.

1. Any received control-frame_ of message-type_ NOOP_, REQUEST_, REPLY_, DATA_ or STATE_ that have ACK-REQUEST flag set SHALL be sent back to the sender as confirmation of accepted message, unless the receiver is a `Service` and an error condition occurs. In such a case the ERROR_ message SHALL be sent by `Service` instead confirmation message.
2. Returned confirmatory message SHALL consists only from the received control-frame_ with ACK-REQUEST flag cleared, and with ACK-REPLY_ flag set (ie the control-frame_ MUST be otherwise unchanged).
3. The ACK-REQUEST flag SHALL be ignored for all message-type_ values not listed in rule 1.

Rules for ACK-REQUEST received by `Service`:

1. NOOP_ message SHALL be acknowledged without any delay.
2. REQUEST_ message SHALL be acknowledged at the time the `Service` has positively decided to accept the client's request and before commencing the fulfillment of the client's request.
3. DATA_ message SHALL be acknowledged without any delay, unless a previous agreement between the `Client` and the `Service` exists to handle it differently (for example to send it when DATA message is actually processed and Service is able to accept another DATA message).

Rules for ACK-REQUEST received by `Client`:

1. NOOP_ and STATE_ message SHALL be acknowledged without any delay.
2. REPLY_ and DATA_ messages SHALL be acknowledged without any delay, unless a previous agreement between the `Client` and the `Service` exists to handle it differently (for example when `Client` is prepared to accept subsequent DATA or other messages from Service).

ACK-REPLY
"""""""""

The ACK-REPLY flag indicates that message is a confirmation of the message previously sent by receiver.

1. The ACK-REPLY flag SHALL NOT be set for any message that is not a confirmation of previous message received with ACK-REQUEST_ flag set.
2. The message with ACK-REPLY flag set MUST conform to the rules defined for ACK-REQUEST_ flag handling.

MORE
""""

The MORE flag is intended to signal the end of the logical message stream to the receiver.

1. The MORE flag SHALL be set for all messages that are a part of logical message stream, and are not the terminal message of this stream. If the message stream is a response to `Client` request, the MORE flag SHALL be set in the REPLY_ message as well.
2. The MORE flag SHALL be cleared for all messages that are not part of the logical message stream, or are the terminal message of such stream.
3. The receiver SHALL ignore the MORE flag for all messages of message-type_ HELLO_, WELCOME_, NOOP_, REQUEST_, CANCEL_, CLOSE_ and ERROR_.

2.4.5 Protocol versioning
^^^^^^^^^^^^^^^^^^^^^^^^^

General rules
"""""""""""""

All revisions of this specification SHALL conform to following rules:

1. All revisions SHALL preserve next parts of this revision:

   a) reqirements defined for `Transport Channel`_
   b) the existence of control-frame_
   c) the position, content and meaning of first five bytes of control-frame_, ie. the signature_ and the control-byte_
   d) the existence of message token_

2. All revisions SHALL preserve next parts of all previous revisions:

   a) defined :ref:`Message types <message-type>`
   b) defined Flags_
   c) defined `Error Codes`_

Version negotiation
"""""""""""""""""""

1. Both the `Client` and the `Service` SHALL use the same protocol version for all messages transmitted as part of a single Connection_.
2. The protocol version used for the Connection_ is defined by the `Client` in his HELLO_ message sent to the `Service`.
3. The `Service` SHALL use the same protocol version as the `Client`.
4. If `Service` cannot handle Connection_ in protocol version used by the `Client`, it SHOULD respond with appropriate ERROR_ message in format defined by this revision. The `Service` MAY respond to this condition by closing the `Transport Connection` associated with the Connection_ request.
5. The `Client` using different revision of this protocol than revision 1 SHOULD be able to handle ERROR_ message in format defined by this revision that would be send as response to his HELLO_ message.
6. The `Client` SHALL eventually interpret the closing of the `Transport Channel`_ to the `Service` without response to his HELLO_ message as rejection of his request to create the Connection_.

2.5 Handling of client requests
-------------------------------

The `Client` SHALL send its requests to the `Service` as REQUEST_ messages with `Request Code`_ indicating the required functionality (an API call).

2.5.1 General rules
^^^^^^^^^^^^^^^^^^^

The handling of Client request has following general rules:

1. The `Service` MUST always respond to the REQUEST_ message in one from following formats:

   a. Send the ERROR_ message describing the error status detected by the `Service` that prevents successful completion of the request.
   b. Send the REPLY_ message as an indication of successful completion of the request, or as indication that `Service` started to fulfill the request. The actual meaning of this reply is defined by `Service API`_.
2. An ERROR_ message sent to the `Client` SHALL always end the processing of the request.
3. The fulfillment of particular request MAY require multiple messages to be sent by `Service`. In such a case, service MUST send the REPLY_ message first, before any additional message would be sent.
4. The subsequent messages after REPLY_ message SHALL be only of message-type_ DATA_, STATE_ or ERROR_.
5. The `Service API`_ for particular `Request Code`_ that requires multiple messages to be send by `Service` SHALL use one from the following methods to indicate the end of request processing to the `Client`:

   a. Using MORE_ flag in REPLY_, DATA_ and STATE_ messages sent to the `Client`. It is RECOMMENDED to use it as preferred method for organization of the message stream.
   b. Using STATE_ message with information that indicates the end of request processing.
   c. Continuous processing terminated on `Client` request by CANCEL_ message or until Connection_ is not closed.
6. The service MAY accept a new request from the client before the initial request has been fully processed. However, all parallel request messages MUST have different (unique) :ref:`Message token <message-token>` value.
7. The processing of any active request can be terminated prematurely at the client's request via the CANCEL_ message.

.. _Service API:
.. _Interface:
.. _Interfaces:

2.5.2 Service API
^^^^^^^^^^^^^^^^^

The `Service API` consists from `Interfaces` (API contracts) that consists from individual operations (functions).

1. An `Interface` SHALL have a globally unique identification (GUID). It’s RECOMMENDED to use uuid version 5 - SHA1, namespace OID.
2. An `Interface` MUST provide at least one `Operation` (function), and MAY provide up to 255 individual `Operations`.
3. An `Operation` MUST have numeric identification unique within the `Interface`, and with value in range 1..255. This identification is called `Interface operation code`.
4. The `Service` MUST assign an unique `Interface identification number` in range 1..255 to each `Interface` it provides, and announce the Interface identification along with assigned number in the data-frame of the WELCOME_ message.
5. The `Service` MUST provide at least one `Interface`, and MAY provide up to 255 individual `Interfaces`.
6. The set of `Interfaces` that `Service` provides MUST be stable, which means that all `Service` instances with the same :ref:`Agent identification` MUST provide the same set of `Interfaces` to all `Clients`.


.. _Request codes:
.. _Request Code:

2.5.3 Request codes
^^^^^^^^^^^^^^^^^^^

The `Request Code` uniquely identifies the `Service` functionality (an API call). This specification define following rules for request codes:

1. The first (more significant) byte of type-data_ field SHALL contain the `Interface identification number` assigned by `Service` to particular `Interface` it supports (see :ref:`Data frames - WELCOME <welcome-dataframe>`).
2. The second (less significant) byte of type-data_ field SHALL contain the `Interface operation code`.


.. _protocol-buffer:

2.6 Data frames
---------------

Where control-frame_ contains semantic specification of the message, individual data-frame_ parts of the message carry data associated with given API call or response.

Number, content and structure of individual `data-frames` SHALL be defined by API specification for particular message-type_ and/or `Request Code`_.

2.6.1 General rules
^^^^^^^^^^^^^^^^^^^

All API and other specifications that define data-frame_ contents SHALL conform to following rules:

1. The message SHALL have minimal necessary number of `data-frames`.
2. The total size of all `data-frames` in single message SHOULD NOT exceed 50MB.
3. Any peer MAY set a Connection_ limit on total size (in bytes) for any single message transmitted that SHALL NOT be smaller than 1MB. Such limit SHALL be announced to other peer in HELLO and WELCOME message. Such limit MAY be negotiable between peers after Connection_ is successfully established.
4. All structured data in `data-frames` defined by this specification are serialized as single `Protocol Buffers`_ message.
5. All API and other specifications that define rules for data-frame_ contents SHOULD use serialization to store structured data into data-frame_. The RECOMMENDED serialization methods are `Protocol Buffers`_ (preferred) or `Flat Buffers`_ (in case the direct access to parts of serialized data is required). It is NOT RECOMMENDED to use any verbose serialization format such as JSON or XML. The whole Service API SHOULD use only one serialization method. Serialization method MAY be negotiable between peers.

2.6.2 Common protobuf specifications
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

All Protocol Buffer definitions in this specifications build on protocol buffers defined by :ref:`3/FBDS - 5.1 Common protobuf specifications <common-protobuf>`.

All Protocol Buffer definitions in this specifications use `proto3` syntax. This syntax variant does not support required fields, and all fields are optional (basic types will have the default "empty" value when they are not serialized). However, some fields in FBSP specification are considered as mandatory (as "required" in `proto2`), and should be validated as such by receiver.

2.6.3 FBSP Data Frames for message types
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. _hello-dataframe:

HELLO data
""""""""""

.. code-block:: protobuf

   package firebird.butler;

   import "google/protobuf/any.proto";
   import "firebird/butler/fbsd.proto";

   message FBSPHelloDataframe {
     PeerIdentification           instance   = 1 ;
     AgentIdentification          client     = 2 ;
     repeated google.protobuf.Any supplement = 3 ;
   }

:instance:
  MANDATORY information about peer.

:client:
  MANDATORY information about Client.

:supplement:
  Any additional information about Client.

.. _welcome-dataframe:

WELCOME data
""""""""""""

.. code-block:: protobuf

   package firebird.butler;

   import "google/protobuf/any.proto";
   import "firebird/butler/fbsd.proto";

   message FBSPWelcomeDataframe {
     PeerIdentification           instance   = 1 ;
     AgentIdentification          service    = 2 ;
     repeated InterfaceSpec       api        = 3 ;
     repeated google.protobuf.Any supplement = 4 ;
   }

:instance:
  MANDATORY information about peer.

:service:
  MANDATORY information about Service.

:api:
  MANDATORY information about Service API.

:supplement:
  Any additional information about Service.


.. _cancel-dataframe:

CANCEL data
"""""""""""

.. code-block:: protobuf

   package firebird.butler;

   import "google/protobuf/any.proto";

   message FBSPCancelRequests {
     bytes                        token      = 1 ;
     repeated google.protobuf.Any supplement = 2 ;
   }

:token:
  MANDATORY message-token_ of the message to be cancelled.

:supplement:
  Any additional information required or supported by Service API specification for cancellation of particular message.


.. _state-dataframe:

STATE data
""""""""""

.. code-block:: protobuf

   package firebird.butler;

   import "google/protobuf/any.proto";
   import "firebird/butler/fbsd.proto";

   message FBSPStateInformation {
     StateEnum                    state      = 1 ;
     repeated google.protobuf.Any supplement = 2 ;
   }

:state:
  MANDATORY :ref:`State enumeration`

:supplement:
  Any additional state information supported by Service API specification.


.. _error-dataframe:

ERROR data
""""""""""

Each Data Frame must contain :ref:`3/FBSD - Error Description <error-description>` protobuf message.


.. _error codes:
.. _error code:

2.7 Error codes
---------------

Error codes are transmitted in type-data_ field of the ERROR_ message.

1. The `Error Code` is a 11-bit unsigned integer number encoded in upper (leftmost) bits of the type-data_ field of ERROR_ message.
2. Value 0 SHALL NOT be a valid `Error Code`. The `Error Code` is thus a value in range 1..2047.
3. The lower (rightmost) 5 bits of type-data_ field encode the message-type_ this particular error relates to (the bitmask is 31). The "zero" value represents general, out-of-band error reported by `Service`.


.. todo::
   :class: todo

   Finalize the list of error codes.

Errors indicating that particular request cannot be satisfied
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. rst-class:: long-field

:1 - Invalid Message:

  The service cannot or will not process the request due to something that is perceived to be a client error (e.g., malformed request syntax, invalid request message framing etc.).

:2 - Protocol violation:

  Received message is a valid FBSP message, but does not conform to the protocol. Typically, a message of this type or content is not allowed at a particular point in the conversation.

:3 - Bad Request:

  The Request Code in the received REQUEST_ message was not recognized as valid Service API call.

:4 - Not Implemented:

  The server does not support the functionality required to fulfill the request.

:5 - Error:

  The server encountered a condition that prevented it from fulfilling the request.

:6 - Internal Service Error:

  The server encountered an unexpected condition that prevented it from fulfilling the request.

:7 - Request Timeout:

  The server cannot process the request within the time that it was prepared to work or wait for external resource.

:8 - Too Many Requests:

  The client has sent too many requests in a given amount of time ("rate limiting").

:9 - Failed Dependency:

   The request could not be performed because the requested action depended on another action and that action failed.

:10 - Forbidden:

  The service understood the request but refuses to authorize it.

:11 - Unauthorized:

  The request has not been applied because it lacks valid authentication credentials for action or the target resource.

:12 - Not Found:

  The service did not find the target resource or is not willing to disclose that one exists.

:13 - Gone:

  The target resource is no longer available and this condition is likely to be permanent.

:14 - Conflict:

  The request could not be completed due to a conflict with the current state of the target resource. This code is used in situations where the user might be able to resolve the conflict and resubmit the request.

:15 - Payload Too Large:

  The service is refusing to process a request because the request payload is larger than the service is willing or able to process.

:16 - Insufficient Storage:

  The service is unable to store data needed to successfully complete the request.
  
:17 - Request Cancelled:

  The client's request was cancelled by CANCEL_ request.


Fatal errors indicating that connection would/should be terminated
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. rst-class:: long-field

:2000 - Service Unavailable:
  The server is currently unable to handle the request due to a temporary overload or scheduled maintenance, which will likely be alleviated after some delay.

:2001 - FBSP Version Not Supported:
  The server does not support, or refuses to support, the version of FBSP that was used in the HELLO_ message.


3. Reference Implementations
============================

The :ref:`Saturnin-SDK <saturnin-sdk>` provides the prime reference implementation for FBSP.


|
|

Appendix A. Transmission patterns
=================================

Keep alive
----------

.. aafig::

    +---------+              +----------+
    |  Sender |              | Receiver |
    +----+----+              +-----+----+
         |                         |
         X          "NOOP"         |
         X------------------------>*
         X                         |


Peer availability check
-----------------------

.. aafig::

    +---------+              +----------+
    |  Sender |              | Receiver |
    +----+----+              +-----+----+
         |                         |
         X       "NOOP/ACK-REQEST" |
         X------------------------>X
         |                         X
         |                         X
         |        "NOOP/ACK-REPLY" X
         X<------------------------X
         X                         |

Failed Client request
---------------------

.. aafig::

    +---------+              +----------+
    |  Client |              |  Service |
    +----+----+              +-----+----+
         |                         |
         X        REQUEST          |
         X------------------------>X
         |                         X
         |                         X
         |        "ERROR"          X
         X<------------------------X
         X                         |

    +---------+              +----------+
    |  Client |              |  Service |
    +----+----+              +-----+----+
         |                         |
         X        REQUEST          |
         X------------------------>X
         |                         X
         |     "STREAM TRAFFIC"    X
         *<----------------------->X
         |                         X
         |        "ERROR"          X
         X<------------------------X
         X                         |

Simple Client request
---------------------

.. aafig::

    +---------+              +----------+
    |  Client |              |  Service |
    +----+----+              +-----+----+
         |                         |
         X        REQUEST          |
         X------------------------>X
         |                         X
         |                         X
         |         REPLY           X
         X<------------------------X
         X                         |

Client request with message stream
----------------------------------

Using MORE_ flag for `Service` -> `Client` transfer:

.. aafig::

    +---------+              +----------+
    |  Client |              |  Service |
    +----+----+              +-----+----+
         |                         |
         X        REQUEST          |
         X------------------------>X
         |                         X
         |      REPLY (MORE)       X
         *<------------------------X
         |                         X
         |   "DATA/STATE (MORE)"   X
         *<------------------------X
         |                         X
         |   "DATA/STATE (MORE)"   X
         *<------------------------X
         |                         X
         |   "DATA/STATE (MORE)"   X
         *<------------------------X
         |                         X
         |   "DATA/STATE"          X
         X<------------------------X
         X                         |

Using MORE_ flag for `Client` -> `Service` transfer:

.. aafig::

    +---------+              +----------+
    |  Client |              |  Service |
    +----+----+              +-----+----+
         |                         |
         X        REQUEST          |
         X------------------------>X
         |                         X
         |          REPLY          X
         X<------------------------X
         X                         |
         X      "DATA (MORE)"      |
         X------------------------>*
         X                         |
         X      "DATA (MORE)"      |
         X------------------------>*
         X                         |
         X      "DATA (MORE)"      |
         X------------------------>*
         X                         |
         X          DATA           |
         X------------------------>X
         |                         X
         |      STATE [end]        X
         X<------------------------X
         X                         |

Using STATE_ message (only for `Service` -> `Client` transfer):

.. aafig::

    +---------+              +----------+
    |  Client |              |  Service |
    +----+----+              +-----+----+
         |                         |
         X        REQUEST          |
         X------------------------>X
         |                         X
         |         REPLY           X
         *<------------------------X
         |                         X
         |      "DATA/STATE"       X
         *<------------------------X
         |                         X
         |      "DATA/STATE"       X
         *<------------------------X
         |                         X
         |      "DATA/STATE"       X
         *<------------------------X
         |                         X
         |      STATE [end]        X
         X<------------------------X
         X                         |

Using CANCEL_ message (only for `Service` -> `Client` transfer):

.. aafig::

    +---------+              +----------+
    |  Client |              |  Service |
    +----+----+              +-----+----+
         |                         |
         X        REQUEST          |
         X------------------------>X
         |                         X
         |         REPLY           X
         *<------------------------X
         |                         X
         |      "DATA/STATE"       X
         *<------------------------X
         |                         X
         |      "DATA/STATE"       X
         *<------------------------X
         |                         X
         |      "DATA/STATE"       X
         *<------------------------X
         |                         X
         |        CANCEL           X
         *------------------------>X
         |                         X
         |         REPLY           X
         X<------------------------X
         X                         |

.. important::

   There is no guarantee that Service will not send more stream messages in time between CANCEL is sent, and REPLY to cancel request is received by the Client. However, the Service SHALL NOT send any stream message after it sends the REPLY to the CANCEL request.

Synchronous `Service` -> `Client` data transfer using ACK-REQUEST/ACK-REPLY flags:

.. aafig::

    +---------+                 +----------+
    |  Client |                 |  Service |
    +----+----+                 +-----+----+
         |                            |
         X          REQUEST           |
         X--------------------------->X
         |                            X
         |   "REPLY (ACK-REQUEST)"    X
         X<---------------------------X
         X                            |
         X    "REPLY (ACK-REPLY)"     |
         X--------------------------->X
         |                            X
         | "DATA/STATE (ACK-REQUEST)" X
         X<---------------------------X
         X                            |
         X  "DATA/STATE (ACK-REPLY)"  |
         X--------------------------->X
         |                            X
         | "DATA/STATE (ACK-REQUEST)" X
         X<---------------------------X
         X                            |
         X  "DATA/STATE (ACK-REPLY)"  |
         X--------------------------->X
         |                            X

Synchronous `Client` -> `Service` data transfer using ACK-REQUEST/ACK-REPLY flags:

.. aafig::

    +---------+                 +----------+
    |  Client |                 |  Service |
    +----+----+                 +-----+----+
         |                            |
         X          REQUEST           |
         X--------------------------->X
         |                            X
         |           REPLY            X
         X<---------------------------X
         X                            |
         X    "DATA (ACK-REQUEST)"    |
         X--------------------------->X
         |                            X
         |     "DATA (ACK-REPLY)"     X
         X<---------------------------X
         X                            |
         X    "DATA (ACK-REQUEST)"    |
         X--------------------------->X
         |                            X
         |     "DATA (ACK-REPLY)"     X
         X<---------------------------X
         X                            |

.. todo::
   :class: todo

   Describe additional transmission patterns.

|
|

.. _RFC2119: http://tools.ietf.org/html/rfc2119
.. _ZMTP: https://rfc.zeromq.org/spec:23/ZMTP
.. _ROUTER: https://rfc.zeromq.org/spec:28/REQREP/
.. _UUID: https://tools.ietf.org/html/rfc4122.html
.. _Protocol Buffers: https://developers.google.com/protocol-buffers/
.. _Flat Buffers: https://github.com/google/flatbuffers
.. |COSS-long| replace:: :doc:`/rfc/2/COSS`
.. |FBSD| replace:: :doc:`3/FBSD</rfc/3/FBSD>`
.. |FBLP| replace:: :doc:`5/FBLP</rfc/5/FBLP>`
.. |SSTP| replace:: :doc:`6/SSTP</rfc/6/SSTP>`
.. |RSCFG| replace:: :doc:`7/RSCFG</rfc/7/RSCFG>`
.. |RSCTRL| replace:: :doc:`8/RSCTRL</rfc/8/RSCTRL>`
.. _Service configuration: :doc:`7/RSCFG</rfc/7/RSCFG>`
.. _ZMQ_PROBE_ROUTER: http://api.zeromq.org/4-1:zmq-setsockopt
