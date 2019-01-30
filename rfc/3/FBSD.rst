###########################################
3/FBSD - Firebird Butler Service Definition
###########################################

:domain: github.com/FirebirdSQL/Butler
:shortname: 3/FBSD
:name: Firebird Butler Service Definition
:status: raw
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
#. Service MAY use additional ZeroMQ sockets for internal purposes or as part of its public API, that are not `Service Sockets`. All such additional ZeroMQ sockets that are part of the Service public API MUST be detectable using the API available through `Service Sockets`.
#. Services MUST assign an identity on `Service Socket`. If there are multiple Service Sockets, they MUST use the same identity. This socket identity SHALL be the same as `Unique Service Instance ID` defined by |FBSP|.
#. If Service uses multiple `Service Sockets`, all of them MUST provide the same functionality to the Clients. It means that from Client perspective there shall be no difference in service **abilities** available and **methods** how they are accessible between different `Service Sockets`. However, Service MAY have different **operational** characteristics when responsing to request coming from different Service Sockets.
#. All messages coming through `Service Socket` MUST be processed as |FBSP| protocol messages.
#. Service MUST correctly define its properties and APIs as a binding contract with Clients through |FBSP| protocol messages.
#. Service SHALL NOT accept Client request through any other channel than `Service Socket`.

The `Client` is any software unit that meets the following criteria:

#. Client SHALL connect to `Service Socket` using ZeroMQ `DEALER` or `ROUTER` socket, referred to as `Client Socket`.
#. All messages coming through `Client Socket` MUST be processed as |FBSP| protocol messages.
#. Client MUST correctly define its properties as a binding contract with Service through |FBSP| protocol messages.
#. Client SHALL NOT send request to the Service through any other channel than `Client Socket`.

.. _svc-recommendation:

2.1 Services
------------

The method of implementation of the Service is not specifically defined or limited, but the following recommendations should be taken into account:

#. The Service SHOULD have exactly defined boundaries (API) and SHOULD use only ZeroMQ sockets to communicate across this boundary (i.e. use ZeroMQ as its only API). 
#. The Service could bind `Service Sockets` using any ZeroMQ transport protocol on any address. However, Service implementations SHOULD allow configuration of these parameters whenever and as much possible.
#. The Service SHOULD handle `Client` requests asynchronously.
#. The functionality provided by the Service to `Clients` via both the |FBSP| protocol and other channels SHOULD be defined by an open standard.
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

When using different ZeroMQ protocols, the following combinations can be achieved:

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
.. [2] `inproc` is the most efficient, but other protocols could be used as well, especially when the same Service Socket should be used in multiple contexts scenarios.
.. [3] `ipc` is the most effective option but may not be available on all platforms. In such a case, use of `tcp` through local loopback is the RECOMMENDED option.

Service could work with Clients using multiple scenarios at once. However, the following recommendations should be taken into account:

#. The Service SHOULD use the minimum necessary number of `Service Sockets`. 
#. The Service SHOULD use the most efficient protocol for each used scenario.

Taking into account the previous recommendations, it is advised to use one of the following recipes for combined scenarios:

.. list-table:: Client and Service Combined Scenarios
   :widths: 30 70
   :header-rows: 1
   
   * - Supported scenarios
     - Service Sockets
   * - **3.** and **4.**
     - Efficiency and Simplicity: One socket using `tcp`_ transport
   * - **2.** and **3.**
     - - Efficiency: Two sockets, one using `inproc`_ for Clients from context **2.**, and one using `ipc`_ transport for Clients from context **3.**
       - Simplicity: One socket using `tcp`_ transport for Clients from all contexts.
   * - **2.**, **3.** and **4.**
     - - Efficiency: Two sockets, one using `tcp`_ for Clients from context **3.** and **4.**, and one using `inproc`_ transport for Clients from context **2.**
       - Simplicity: One socket using `tcp`_ transport for Clients from all contexts.
   * - **2.** and **4.**
     - - Efficiency: Two sockets, one using `tcp`_ for Clients from context **4.**, and one using `inproc`_ transport for Clients from context **2.**
       - Simplicity: One socket using `tcp`_ transport for Clients from all contexts.

.. tip::

   When implementing `Services`, it is RECOMMENDED to use a procedure that allows the same service code to be used in different contexts through adapters or containers. Most typically, the Service could be implemented as a `Class`, that accepts `Service Socket` specification (`protocol` and `address`, or already bound 0MQ socket instance) as a `constructor` parameter.
   
   Alternatively, it is possible to encapsulate the service into another service that would act as a `router` or `bridge` to Clients or Services in another contexts.

3.2 Services that use other Services
------------------------------------

One of the main goals of this specification is to enable the creation of services that do not work in isolation according to the client / server schema, but function as integral components of a larger integrated entity. To achieve this goal, it is essential for services to use other available services themselves.

When implementing Services that are also Clients of other services, the following recommendations should be taken into account:

#. The Client connection to other Service SHOULD be handled asynchronously.
#. The Service SHOULD use the minimum necessary number of `Client Sockets`. This could be achieved by using a ROUTER socket for connecting to multiple, even different Services.
#. The Service SHOULD open the `Client Socket` to another service as soon as possible, preferably during its initialization, so that information about the availability and operating parameters of another service is known prior to processing the first request of the Service clients, where a Client request is a REQUEST message with a request code other than the code reserved for the |FBSP| protocol.
#. The client connection to another service SHOULD be kept open until the Service is terminated.
#. Information about client connections to other services SHOULD be part of the status information provided in accordance with :ref:`Recommendation 7, Section 2.1 <svc-recommendation>`.
#. Configuration and management of client connections to other services SHOULD be part of the remote configuration and control provided in accordance with :ref:`Recommendation 8, Section 2.1 <svc-recommendation>`.

.. important::

   For the successful creation of interconnected systems, due attention needs to be paid to the initialization and termination of Services, especially due to possible dependencies between Services. 
   
   For systems built from components made up of separate processes or network nodes, due consideration should also be given to the mechanism of continuous monitoring and maintenance of the link between Services.
   
   It is RECOMMENDED to use standardized methods and protocols for these purposes.


3.3 Security
============

FBSD does not specify any authentication, encryption or access control mechanisms, and fully relies on security measures provided by ZeroMQ, or other means.

4. Reference Implementations
============================

None at this time. In future, the :ref:`Saturnin` and :ref:`Saturnin-SDK <saturnin-sdk>` will act as the prime reference implementation for FBSD.
   
|
|

.. _RFC2119: http://tools.ietf.org/html/rfc2119
.. |COSS-long| replace:: :doc:`/rfc/2/COSS`
.. |FBSP| replace:: :doc:`4/FBSP</rfc/4/FBSP>`
.. |FBLP| replace:: :doc:`5/FBLP</rfc/5/FBLP>`
.. |SSTP| replace:: :doc:`6/SSTP</rfc/6/SSTP>`
.. |RSCFG| replace:: :doc:`7/RSCFG</rfc/7/RSCFG>`
.. |RSCTRL| replace:: :doc:`8/RSCTRL</rfc/8/RSCTRL>`
.. _inproc: http://api.zeromq.org/4-2:zmq-inproc
.. _ipc: http://api.zeromq.org/3-2:zmq-ipc
.. _tcp: http://api.zeromq.org/3-2:zmq-tcp
