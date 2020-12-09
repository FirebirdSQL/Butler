###########################################
3/FBSD - Firebird Butler Service Definition
###########################################

:domain: github.com/FirebirdSQL/Butler
:shortname: 3/FBSD
:name: Firebird Butler Service Definition
:status: draft
:editor: Pavel Císař <pcisar@users.sourceforge.net>

This document describes a specific category of software components capable of providing their services to clients working in the same or different contexts where the context may be a thread or a process. It defines common functionality and operational parameters to ensure interoperability and integration under defined working conditions.

License
=======

Copyright (c) 2018 The Firebird Butler Project.

This Specification is distributed under Creative Commons Attribution-ShareAlike 4.0 International license.

You should have received a copy of the CC BY-SA 4.0 along with this document; if not, see https://creativecommons.org/licenses/by-sa/4.0/

Change Process
==============

This Specification is a free and open standard and is governed by the Consensus-Oriented Specification System (COSS) (see "|COSS-long|").

.. note::

   All ideas and change proposals SHOULD be presented and discussed first in the `Firebird Butler forum <https://groups.google.com/d/forum/firebird-butler>`_.

Language
========

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in `RFC2119`_.

1. Goals
========

The purpose of this specification is to define software components capable of efficient asynchronous communication with other components through both tight and loose bindings in a diverse operating environments.

The main objectives are:

#. Architecture openness.
#. Maximum simplicity.
#. Reliability.
#. Isolation of individual components.
#. Ability to communicate as efficiently as possible within both a single operating environment and across different operating environments where these are process threads or processes running on the same computing system or network with different performance characteristics.
#. The ability to create a reliable, comprehensive, dynamically modifiable and expandable system composed of such components.

2. Architecture
===============

Firebird Butler `Service` is any software unit that performs an activity required by the `Client`, and where communication between the Service and the Client is solely through the exchange of messages via ZeroMQ sockets.

The `Service` MUST meet the following criteria:

#. Service MUST bind to at least one ZeroMQ `ROUTER` socket, referred to as `Service Socket`.
#. Service MAY use additional ZeroMQ sockets for internal purposes or as part of its public API, that are not `Service Sockets`, referred to as `Data Pipes`_. All such `Data Pipes` that are part of the Service public API MUST be detectable or defined using the API available through `Service Sockets`.
#. Services MUST assign an identity on `Service Socket`. If there are multiple `Service Sockets`, they MUST use the same identity. This socket identity SHALL be the same as `Unique Service Instance ID` defined by |FBSP|.
#. If Service uses multiple `Service Sockets`, all of them MUST provide the same functionality to the Clients. It means that from Client perspective there shall be no difference in service **abilities** available and **methods** how they are accessible between different `Service Sockets`. However, Service MAY have different **operational characteristics** when responsing to requests coming from different Service Sockets.
#. All messages coming through `Service Sockets` MUST be processed as |FBSP| protocol messages.
#. Service MUST correctly define its properties and APIs as a binding contract with Clients through |FBSP| protocol messages.
#. Service SHALL NOT accept Client request (i.e. API calls) through any other channel than `Service Socket`.

The `Client` is any software unit that meets the following criteria:

#. Client SHALL connect to `Service Socket` using ZeroMQ `DEALER` or `ROUTER` socket, referred to as `Client Socket`.
#. All messages coming through `Client Socket` MUST be processed as |FBSP| protocol messages.
#. Client MUST correctly define its properties as a binding contract with Service through |FBSP| protocol messages.
#. Client SHALL NOT send request (i.e. API calls) to the Service through any other channel than `Client Socket`.

.. _svc-recommendation:

2.1 Services
------------

The method of implementation of the Service is not specifically defined or limited, but the following recommendations should be taken into account:

#. The Service SHOULD have exactly defined boundaries (API) and SHOULD use only ZeroMQ sockets to communicate across this boundary (i.e. use ZeroMQ as its only API).
#. The Service could bind `Service Sockets` using any ZeroMQ transport protocol on any address. However, Service implementations SHOULD allow configuration of these parameters whenever and as much possible.
#. The Service SHOULD handle `Client` requests asynchronously.
#. The functionality provided by the Service to `Clients` via both the |FBSP| protocol and other channels SHOULD be defined by an open standard. See |FBDP| for examples.
#. The Service SHOULD provide some method of discovery for its access points and connection methods available to its `Clients`. This method SHOULD be defined by an open standard.
#. The Service SHOULD provide a logging information about its activities. It is RECOMMENDED to use standardized methods and protocols for this purpose. See |FBSP| for details  and |FBLP| for examples.
#. The Service SHOULD provide information about its internal state. It is RECOMMENDED to use standardized methods and protocols for this purpose. See |FBSP| for details and |SSTP| for examples.
#. The Service that provide services to `Clients` running in different process or on another Network node SHOULD support remote configuration and remote control. It is RECOMMENDED to use standardized methods and protocols for this purpose. See |FBSP| for details, and |RSCFG| and |RSCTRL| for examples.

.. important::

   Any violation of these recommendations SHOULD be clearly specified in Service documentation.

2.2. Clients
------------

The method of implementation of the Service Client is not specifically defined or limited, but the following recommendations should be taken into account:

#. The Client SHOULD handle requests to the `Service` asynchronously.

.. important::

   Any violation of these recommendations SHOULD be clearly specified in Client documentation.


3. Operation of services
========================

3.1 Context of the Service and the Client
-----------------------------------------

Both the `Service` and the `Client` can run in the same or different context, the context being the process `thread` or the separate `process`, or a separate process on another `network node`.

The following table shows the possible combinations of execution contexts and the optimal ZeroMQ communication protocols for a given combination:

.. list-table:: Client and Service Link Scenarios
   :widths: 5 40 40 15
   :header-rows: 1

   * - Scenario
     - Service Context
     - Client Context
     - ZeroMQ protocol
   * - **1.**
     - Thread `T` of Process `P` on node `N`
     - Thread `T` of Process `P` on node `N`
     - `inproc`_ [1]_
   * - **2.**
     - Thread `T1` of Process `P` on node `N`
     - Thread `T2` of Process `P` on node `N`
     - `inproc`_ [2]_
   * - **3.**
     - Thread `T` of Process `P1` on node `N`
     - Thread `T` of Process `P2` on node `N`
     - `ipc`_, `tcp`_ [3]_
   * - **4.**
     - Thread `T` of Process `P` on node `N1`
     - Thread `T` of Process `P` on node `N2`
     - `tcp`_

.. [1] This scenario requires an `ioloop` supported and shared by both, the `Client` and the `Service`. It is NOT RECOMMENDED to mix this context scenario with others.
.. [2] `inproc` is the most efficient, but other protocols could be used if inproc couldn't be used for some reson.
.. [3] `ipc` is the most effective option but may not be available on all platforms. In such a case, use of `tcp` through local loopback is the RECOMMENDED option.

Service could work with Clients using multiple scenarios at once. However, the following recommendations should be taken into account:

#. The Service SHOULD use the minimum necessary number of `Service Sockets`. The ZeroMQ library allows you to bind a socket to multiple addresses using multiple protocols. However, some ZMQ implementations may not allow this, and it may be necessary to use multiple `Service Sockets` to provide the most efficient connections for all supported scenarios.
#. The Service SHOULD use the most efficient protocol for each used/supported scenario.

.. tip::

   When implementing `Services`, it is RECOMMENDED to use a procedure that allows the same service code to be used in different contexts through adapters or containers. Most typically, the Service could be implemented as a `Class`, that accepts and uses externally defined `Service Socket` specification (`protocol` and `address`, or already bound 0MQ socket instance etc.).

   Alternatively, it is possible to encapsulate the service into another service that would act as a `router` or `bridge` to Clients or Services in another contexts.

3.2 Services that use other Services
------------------------------------

One of the main goals of this specification is to enable the creation of services that do not work in isolation according to the client / server schema, but function as integral components of a larger integrated entity. To achieve this goal, it is essential for services to use other available services themselves.

The RECOMMENDED method of integration is an indirect link between services through `Data Pipes`_, where individual services act as producers and / or consumers of data for / from other services. However, it is also possible to integrate services directly, that is, when the service as a client calls another service.

When implementing Services that are also Clients of other services, the following recommendations should be taken into account:

#. The Client connection to other Service SHOULD be handled asynchronously.
#. The Service SHOULD use the minimum necessary number of `Client Sockets`. This could be achieved by using a ROUTER socket for connecting to multiple, even different Services.
#. The Service SHOULD open the `Client Socket` to another service as soon as possible, preferably during its initialization, so that information about the availability and operating parameters of another service is known prior to processing the first request of the Service clients, where a Client request is a REQUEST message as defined by |FBSP| protocol.
#. The client connection to another service SHOULD be kept open until the Service is terminated.
#. Information about client connections to other services SHOULD be part of the status information provided in accordance with :ref:`Recommendation 7, Section 2.1 <svc-recommendation>`.
#. Configuration and management of client connections to other services SHOULD be part of the remote configuration and control provided in accordance with :ref:`Recommendation 8, Section 2.1 <svc-recommendation>`.

.. important::

   For the successful creation of interconnected systems, due attention needs to be paid to the initialization and termination of Services, especially due to possible dependencies between Services.

   For systems built from components made up of separate processes or network nodes, due consideration should also be given to the mechanism of continuous monitoring and maintenance of the link between Services.

   It is RECOMMENDED to use standardized methods and protocols for these purposes.


3.3 Security
------------

FBSD does not specify any authentication, encryption or access control mechanisms, and fully relies on security measures provided by ZeroMQ, or other means.

.. _data pipes:

4. Data Pipes
=============

A `Data Pipe` is a one-way communication channel for transferring `user data` between **exactly two** software components through message exchange via ZeroMQ sockets.

The `Data Pipe` MUST meet the following criteria:

#. The Data Pipe MUST have separately defined `input` and `output` abstract endpoints.
#. Messages that carry **user data** SHALL be accepted only from **exactly one** peer connected to `input` endpoint, and routed to **exactly one** peer connected to `output` endpoint.

|

*Basic diagram of user data transmission via Data Pipe:*

.. aafig::

    +---------------+ Pipe Input +-----------+ Pipe Output +---------------+
    | Data Producer +----------->+ Data Pipe +------------>+ Data Consumer |
    +---------------+            +-----------+             +---------------+


|

The method of implementation of the `Data Pipe` is not specifically defined or limited, but the following recommendations should be taken into account:

#. Messages SHOULD be handled asynchronously.
#. The message exchange provided by the `Data Pipe` SHOULD be defined by an open standard. See |FBDP| for example.


5. Structured data in messages
==============================

All structured user data passed trough `Data Pipes`_ or `Service Sockets` between `Services` and `Clients` SHOULD use  serialization method. The RECOMMENDED serialization methods are `Protocol Buffers`_ (preferred) or `Flat Buffers`_ (in case the direct access to parts of serialized data is required). It is NOT RECOMMENDED to use any verbose serialization format such as JSON or XML. The whole Service API SHOULD use only one serialization method. Serialization method MAY be negotiable between peers.

.. _common-protobuf:

5.1 Common protobuf specifications
----------------------------------

This specification defines set of common `Protocol Buffers`_ types and messages that SHOULD be used where applicable.

All `protobuf` specifications use `proto3` syntax. This syntax variant does not support required fields, and all fields are optional (basic types will have the default "empty" value when they are not serialized). However, some fields in FBSD specification are considered as mandatory (as "required" in `proto2`), and should be validated as such by receiver.

5.1.1 Enumeration types
^^^^^^^^^^^^^^^^^^^^^^^

.. _state enumeration:

Process State
"""""""""""""

Universal enumeration type for process state.

.. code-block:: protobuf

   package firebird.butler;

   enum StateEnum {
     option allow_alias = true ;

     STATE_UNKNOWN    = 0 ;
     STATE_READY      = 1 ;
     STATE_RUNNING    = 2 ;
     STATE_WAITING    = 3 ;
     STATE_STOPPED    = 4 ;
     STATE_FINISHED   = 5 ;
     STATE_TERMINATED = 6 ;

     // Aliases

     STATE_CREATED    = 1 ;
     STATE_BLOCKED    = 3 ;
     STATE_SUSPENDED  = 4 ;
     STATE_ABORTED    = 6 ;
   }

Address domain
""""""""""""""

Enumeration for identification of address domain (scope).

.. code-block:: protobuf

   package firebird.butler;

   enum AddressDomainEnum {
     DOMAIN_UNKNOWN = 0 ; // Not a valid option, defined only to handle undefined values
     DOMAIN_LOCAL   = 1 ; // Within process (inproc)
     DOMAIN_NODE    = 2 ; // On single node (ipc or tcp loopback)
     DOMAIN_NETWORK = 3 ; // Network-wide (ip address or domain name)
   }

Transport protocol
""""""""""""""""""

Enumeration for transport protocol identification.

.. code-block:: protobuf

   package firebird.butler;

   enum TransportProtocolEnum {
     PROTOCOL_UNKNOWN = 0 ; // Not a valid option, defined only to handle undefined values
     PROTOCOL_INPROC  = 1 ;
     PROTOCOL_IPC     = 2 ;
     PROTOCOL_TCP     = 3 ;
     PROTOCOL_PGM     = 4 ;
     PROTOCOL_EPGM    = 5 ;
     PROTOCOL_VMCI    = 6 ;
   }

Socket type
"""""""""""

Enumeration for ZeroMQ socket types.

.. code-block:: protobuf

   package firebird.butler;

   enum SocketTypeEnum {
     SOCKET_TYPE_UNKNOWN = 0 ; // Not a valid option, defined only to handle undefined values
     SOCKET_TYPE_DEALER  = 1 ;
     SOCKET_TYPE_ROUTER  = 2 ;
     SOCKET_TYPE_PUB     = 3 ;
     SOCKET_TYPE_SUB     = 4 ;
     SOCKET_TYPE_XPUB    = 5 ;
     SOCKET_TYPE_XSUB    = 6 ;
     SOCKET_TYPE_PUSH    = 7 ;
     SOCKET_TYPE_PULL    = 8 ;
     SOCKET_TYPE_STREAM  = 9 ;
     SOCKET_TYPE_PAIR    = 10 ;
   }

Socket use
""""""""""

Enumeration for ZeroMQ socket usage type.

.. code-block:: protobuf

   package firebird.butler;

   enum SocketUseEnum {
     SOCKET_USE_UNKNOWN  = 0 ; // Not a valid option, defined only to handle undefined values
     SOCKET_USE_PRODUCER = 1 ; // Socket used to provide data to peers
     SOCKET_USE_CONSUMER = 2 ; // Socket used to get data prom peers
     SOCKET_USE_EXCHANGE = 3 ; // Socket used for data exchange
   }

Dependency type
"""""""""""""""

Enumeration for definition of dependency type.

.. code-block:: protobuf

   package firebird.butler;

   enum DependencyTypeEnum {
     DEPTYPE_UNKNOWN   = 0 ; // Not a valid option, defined only to handle undefined values
     DEPTYPE_REQUIRED  = 1 ; // The resource MUST be provided
     DEPTYPE_PREFERRED = 2 ; // The resource SHOULD be provided if available
     DEPTYPE_OPTIONAL  = 3 ; // The resource MAY be provided if available
   }

5.1.2 Data structures (messages)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Platform Identification
"""""""""""""""""""""""

A data structure that describes the Firebird Butler Development Platform used by Client or Service.

.. code-block:: protobuf

   package firebird.butler;

   message PlatformId {
     bytes  uid     = 1 ;
     string version = 2 ;
   }

:uid:
  MANDATORY unique platform ID. It's RECOMMENDED to use uuid version 5 - SHA1, namespace OID.

:version:
  MANDATORY platform version. MUST conform to `major[.minor[.patch[-tag]]]` pattern, where `major`, `minor` and `patch` are numbers, and `tag` is alphanumeric. It's RECOMMENDED to use `semantic versioning`_.

Vendor Identification
"""""""""""""""""""""

A data structure that identifies a vendor of Client or Service.

.. code-block:: protobuf

   package firebird.butler;

   message VendorId {
     bytes uid = 1 ;
   }

:uid:
  MANDATORY unique vendor ID. It's RECOMMENDED to use uuid version 5 - SHA1, namespace OID.

.. _agent identification:

Agent Identification
""""""""""""""""""""

A data structure that describes the identity of the Client or Service.

.. code-block:: protobuf

   package firebird.butler;

   import "google/protobuf/any.proto";

   message AgentIdentification {
     bytes                        uid            = 1 ;
     string                       name           = 2 ;
     string                       version        = 3 ;
     VendorId                     vendor         = 4 ;
     PlatformId                   platform       = 5 ;
     string                       classification = 6 ;
     repeated google.protobuf.Any supplement     = 7 ;
   }

:uid:
  MANDATORY unique Agent ID. It's RECOMMENDED to use uuid version 5 - SHA1, namespace OID.

:name:
  MANDATORY agent name assigned by vendor. It's RECOMMENDED that `uid` and `name` make a stable pair, i.e. there should not be agents from the single vendor that have the same name but different uid and vice versa.

:version:
  MANDATORY agent version. MUST conform to `major[.minor[.patch[-tag]]]` pattern, where `major`, `minor` and `patch` are numbers, and `tag` is alphanumeric. It's RECOMMENDED to use `semantic versioning`_.

:vendor:
  MANDATORY `Vendor identification`_.

:platform:
  MANDATORY `Platform identification`_.

:classification:
  Agent classification. It's RECOMMENDED to use `domain/category` schema, for example *database/backup*.

:supplement:
  Any additional information about Agent.

Peer Identification
"""""""""""""""""""

A data structure that describes the peer within the Connection.

.. code-block:: protobuf

   package firebird.butler;

   import "google/protobuf/any.proto";

   message PeerIdentification {
     bytes                        uid        = 1 ;
     uint32                       pid        = 2 ;
     string                       host       = 3 ;
     repeated google.protobuf.Any supplement = 4 ;
   }

:uid:
  MANDATORY unique peer ID. It's RECOMMENDED to use uuid version 1.

:pid:
  MANDATORY process ID (PID of peer's process).

:host:
  MANDATORY host (network node) identification. It could be an IP (v4/v6) address, or a hostname that must be resolvable to an IP address. Peers that run on the same network node MUST have the same address/hostname.

:supplement:
  Any additional information about peer.

Interface Specification
"""""""""""""""""""""""

A data structure that describes an Interface used by Service API.

.. code-block:: protobuf

   package firebird.butler;

   message InterfaceSpec {
     uint32 number    = 1 ;
     bytes  interface = 2 ;
   }

:number:
  MANDATORY Interface Identification Number assigned by Service.

:interface:
  MANDATORY Iterface UID.

.. _error-description:

Error Description
"""""""""""""""""

A data structure that describes an error.

.. code-block:: protobuf

   package firebird.butler;

   import "google/protobuf/struct.proto";

   message ErrorDescription {
     uint64                 code        = 1 ;
     string                 description = 2 ;
     google.protobuf.Struct context     = 3 ;
     google.protobuf.Struct annotation  = 4 ;
   }


:code:
  Service-specific error code.

:description:
  MANDATORY short text description of the error.

:context:
  Structured error context information. The context is for information that accurately identifies the source of the error by the `Client`.

:annotation:
  Additional structured error information. Annotations are intended for debugging and other internal purposes and MAY be ignored by the `Client`.


6. Reference Implementations
============================

The :ref:`Saturnin` and :ref:`Saturnin-SDK <saturnin-sdk>` projects act as the prime reference implementation for FBSD.

|
|

.. _RFC2119: http://tools.ietf.org/html/rfc2119
.. |COSS-long| replace:: :doc:`/rfc/2/COSS`
.. |FBSP| replace:: :doc:`4/FBSP</rfc/4/FBSP>`
.. |FBLP| replace:: :doc:`5/FBLP</rfc/5/FBLP>`
.. |SSTP| replace:: :doc:`6/SSTP</rfc/6/SSTP>`
.. |RSCFG| replace:: :doc:`7/RSCFG</rfc/7/RSCFG>`
.. |RSCTRL| replace:: :doc:`8/RSCTRL</rfc/8/RSCTRL>`
.. |FBDP| replace:: :doc:`9/FBDP</rfc/9/FBDP>`
.. _inproc: http://api.zeromq.org/4-2:zmq-inproc
.. _ipc: http://api.zeromq.org/3-2:zmq-ipc
.. _tcp: http://api.zeromq.org/3-2:zmq-tcp
.. _Protocol Buffers: https://developers.google.com/protocol-buffers/
.. _Flat Buffers: https://github.com/google/flatbuffers
.. _semantic versioning: https://semver.org/
