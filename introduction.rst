###############################
Introduction to Firebird Butler
###############################


The main ideas behind the project
=================================

Itching to scratch
------------------

Managing IT infrastructure is basically a simple, two-component problem. One component is
early detection of disaster and recovery from such events. The second component is
a control system to maintain the operational parameters of the IT system within required
limits. Both components should work in synergy and both involve parts that either measure
various parameters, process or evaluate the measured values, or execute actions according
to defined logic or upon human intervention.

However, in practice it's a very challenging problem. Mostly because the requirements for
each deployment are very diverse, and evolving over time. The second pitfall is the tools
to help you solve this riddle. There are too many, and none of them is a silver bullet that
solves everything. Also, you will soon find that the more one of the components can do,
the more complex it is, and thus more prone to errors or hidden problems. You will also
often find yourself in a straitjacket, where a product does 70%-98% of what you need, but
the remaining is astonishingly hard to achieve if not simply impossible. So you will always
end with either incomplete solution, or a mash-up solution and integration issues of various
degree and severity.

Managing Firebird deployments is no different in this regard. The sole difference is that
the range of tools available specifically for this task is very small, and their help ends
at the boundary of Firebird-related issues. But Firebird is only a (small) part of the wider
picture, especially for the IT staff that has to manage a network of semi-automated
production factories spread over several countries (to name at least one real-world example).

The sad truth is, that you will always end up with a more or less custom solution (you at
least have to hack together all required parts). And the more you do yourself, the more
effective and reliable the final solution becomes.

.. admonition:: Conclusion

   The truth at the very bottom of this problem is, that we don't really need a ready-to-use
   final solution (a *Golden Product*) - we actually need a **Solution Construction Kit**.

The road to solution
--------------------

One of the key values on which the Firebird Project is built is the preservation of
the philosophy inherited (through InterBase) from Borland, which can be described as
*"clever engineering"*. One of the many examples of the realization of this philosophy was
Borland Delphi, and the way it revolutionized the development of applications using
components. While the concept was not completely new, the way it was used and implemented
was clever and innovative. The Delphi Component Library was (and still is) a great example
of a solid *"Solution Construction Kit"*. The Butler project builds on this basic idea but
tries to translate it into the context of modern times.

The IT world has changed a lot since 1995 when Delphi first appeared. Multi-platform,
multi-device, distributed, scalability - those are the key words today. Today we build
systems with such high levels of complexity, processing such astonishing  amounts of data,
that we have had to resort to AI and adaptive self-learning systems to cope with the issues
raised. Almost everything is interconnected, and what is not yet soon will be. Today's
components are no longer just classes but whole applications or systems connected through
web technologies. The software component's paradigm has transformed itself into
a service-oriented and messaging architecture. Unfortunately, due to stormy development,
two unpleasant things happened. First, linking services using web technologies (primarily
HTTP, JSON, etc.) was the result of giving priority to a path of lesser resistance rather
than the effectiveness of these technologies. This has led to the tearing of the worlds
of large and small software components. So now we have separate "component systems" for
small solutions and the big ones, with no easy way to bridge the gap.

.. admonition:: Our answer

   **The Firebird "Butler" Project** is a **serious** attempt to address this problem - in
   line with the Firebird's scalability doctrine **"from embedded to enterprise".**

   So, once again in Firebird's history [1]_, **We Boldly Go Where No Man Has Gone Before**.

.. note::

   The **Firebird Butler Development Platform** (a multi-platform library core similar to
   TComponent+TModule from Delphi VCL) is the *heart* of the Butler Project. The second
   layer built on top of it is the **Firebird Butler Service Library**, which is
   a *repository* of various (mostly Firebird-related) services. The outer layer is
   the **Firebird Butler** itself (*the product*), which should be a distribution (or set
   of purpose-tailored distributions) for direct deployment.

|

.. _butler-platform-intro:

Firebird Butler Development Platform
====================================

In Delphi, the VCL components interact through direct method calls (connected to `event`
attributes). Other systems (like Qt) use slightly different connection mechanisms, but
the principle remains the same. The connection between components is predominantly stable,
calls are synchronous, and predominantly stateful. The world of distributed services uses
mostly unstable TCP/IP connections and stateless calls that are often asynchronous.

So, is it even possible to bridge the gap between the worlds of small, in-process components
and big, distributed ones? The answer is YES, if the focus is on a technical solution that
subsumes the key properties for each and can easily live in both worlds.

Let's look at the key properties closely.

Direct method calls vs. TCP/IP
----------------------------------

Direct method calls are most effective, but while they are easy within single thread, they
are impossible between threads or processes. The closest thing to it that you can do is
remote procedure calling (RPC). Although RPC is easy today, it's also a killer of performance
and scalability, especially when it is synchronous.

Raw TCP/IP communication is easy today, and the same applies for using it in the context
of web-related technologies (HTTP etc.). But using it for communication between threads
(or even between objects in a single thread) is cumbersome and not very effective.
The advantage is that you can easily go asynchronous.

So it's clear that if you want scaleable solution, you have to give up the direct method
calls, and resort to sending messages. However, you would need a message delivery system
that is equally efficient for in-process, inter-process and network communication. In such
a case the loss of direct calls may be an advantage rather than an obstacle (you can do
more reliable parallel execution this way, even within a single thread).

.. admonition:: Our approach

   The Butler Project chose ZeroMQ_ as the core solution for messaging. More about it later.

Tight vs. loose coupling
------------------------

In a distributed environment, connecting between components via signals or event attributes
and calling methods directly is equivalent to a stable TCP/IP connection - the connection
is always present and open and you can always make a call. Tight coupling between connected
components enables the most effective ways to do things. Doing the same with TCP/IP within
single application is easy, since the connection can unlikely break by itself. However,
it is not so simple for connections between processes or over a network - they can break
any time. Because nodes can disappear from the network, it's not always possible to achieve
tight coupling efficiently and reliably over a network. That is why network services mostly
use stateless protocols and communication. In the current state of affairs, the services are
loosely coupled when integrated using some Service Integration Solution, such as  Zato_,
or by direct communication between the services.

The truth is, that using loose coupling is a hard tradeoff. It makes no sense to stick to
it for deployments on a single computer nor for small or reliable corporate networks. It's
a "better" solution only for integrations over unreliable or external sources, or with
services that can't do better. These integration solutions merely opt for implementation
simplicity over effectiveness, providing classic examples of one-size-fits-all syndrome
gone wrong.

.. admonition:: Our approach

   Our Firebird Butler Development Platform will allow the creation of services with
   **both** tight and loose integration, with preference for tightness.

   The **Firebird Butler product** will be basically an application. A LEGO-style
   application where you can stick various building blocks together in various ways, even
   distributed over a network, but it could be still viewed as single application/system.
   With both tight and loose coupling supported, it should be possible to have simplified
   builds for single execution as well as distributed builds encompassing a set of separate
   processes running on several nodes of the network.

Synchronous vs. asynchronous
----------------------------

Synchronous communication is easier, but doesn't scale well. To perform complex processing
of large amounts of data effectively, it's necessary to utilize CPU and other resources as
much as possible, typically with parallel and/or asynchronous processing. However, there
are many ways how to go parallel and asynchronous, and each style has its own strong and
weak points. Also, each programming language has it's own specific way to do it.

.. admonition:: Our approach

   The basis of the Firebird Butler Development Platform design is asynchronous
   communication between Butler Services, but without strictly defining its exact
   implementation. Various Butler Platform implementations could offer various (and even
   multiple) strategies for implementing Butler Services. However, services implemented in
   different ways and languages should be still able to interact with one another.

ZeroMQ
----------

ZeroMQ is an elegant, small yet powerful library that handles the messaging fundamentals
while allowing users to build various messaging architectures. The interface is based on
the Berkeley sockets API, with `additional functionality <http://zeromq.org/docs:features>`_.

It provides services and patterns to do brokered or broker-less systems, sync and async
messaging, various request/reply conversations, push/pull pipes, publisher/subscriber
multicasts, workload pipelines, authentication, CURVE security, and various protocols
(tcp, ipc, inproc, pgm/epgm, vmci). It significantly simplifies the development of viable
custom systems with load balancing, high availability or reliability features, dynamic
mashups, cloud architectures etc. It does not do these things for you, as other systems
try to do, but you can do it yourself reliably without too much effort, in a way and to
the extent that fits your needs. And as a cherry on top, ZeroMQ helps with reliable
multi-thread applications using inproc sockets for fast and safe pipelines, or multi-process
ones with ipc sockets.

Of course it's not perfect.  It will have limits, issues and dark corners like any piece
of software out there, but we think that it provides everything we would need at a level
that is good enough.

You can learn more about ZeroMQ_ from the excellent ZGuide_, that includes many
`examples in about 30 programming languages <https://github.com/booksbyus/zguide/tree/master/examples>`_.

ZeroMQ comes with the low-level C API. High-level bindings exist in 40+ languages
including `Python <https://github.com/zeromq/pyzmq>`_,
`Delphi <https://github.com/grijjy/DelphiZeroMQ>`_,
`FreePascal <https://github.com/DJMaster/zeromq-fpc>`_, Java, PHP, Ruby, C, C++, C#,
Erlang, Perl, and `more <http://zeromq.org/bindings:_start>`_. It also comes in a pure
Java stack called JeroMQ_, and a pure C# stack called NetMQ_. These are both official
projects and supported by the ZeroMQ community.

Some organizations that we know use it are: AT&T, Cisco, EA, Los Alamos Labs, NASA, Weta
Digital, Zynga, Spotify, Samsung Electronics, IBM, Microsoft, and CERN.

Platform specification
----------------------

The Firebird Butler Development Platform defines basic features of Butler Services and
messaging protocols. For example, it describes the following:

- service registration and discovery
- communication negotiation (security, protocol version, communication channels, data
  format, sync/async patterns etc.)
- feature and configuration discovery
- service control
- message exchange methods (request/reply, push/pull, produce/subscribe etc.)

The specification DOES NOT describe how individual services should do their jobs. For
example if you are looking to create a service that does database backups, the specification
defines how one should find it, connect to it, negotiate communication details (common
patterns), discover its features, exchange messages, error handling and codes, some common
messaging patterns like presence verification (ping), addressing, control messages etc.
But what messages, data and formats your service uses to do its job, what features it
would have and how it would do its work is up to you. You can create a dumb backup service
that is just a thin wrapper around the backup provided by Firebird service API that can
handle only one database at a time and does not report back, or you can create a complex
backup service that can handle many databases simultaneously, on a regular basis
(has a scheduler), uses a global resource registry for server, database and backup
specification, uses a logging service, can do proximity-based load balancing to fellow
backup services and will send information about its status and progress to some messaging
pipe, and **either service would be a first-class well-behaving citizen in a Butler deployment**.

Platform implementation
-----------------------

Platform :doc:`specifications <specifications>` (a set of RFC documents) are blueprints
for Platform implementation in various programming languages. The **reference implementation**
is in the Python programming language, but within the Butler project, we would also like
to provide implementations for C#, Java, Delphi, and Free Pascal. However, the Firebird
Project has **currently** resources only for implementations in :ref:`Python <saturnin>`,
:ref:`Java <ButlerJavaSDK>` and :ref:`Free Pascal <butler-fpc-sdk>`.

Because a platform specification does not define exact API or implementation details,
the individual implementations may vary in their design, architecture, features and API
provided for the service developers. There could be even multiple implementations in the
same programming language that provide different features or architecture (for example,
Python implementation for Python that uses "traditional" thread/process approach or another
one that takes advantage from async processing language features, or different async
libraries like `trio`, `curio`,  `twisted` or `asyncio`).

.. note::

   Applications and Butler Services created using **any** platform implementation will be
   able to bind and communicate with any Butler service, regardless of the platform on
   which it is implemented. However, individual platform implementations could provide
   additional integration options and features for applications and services that use the
   same platform implementation, beyond the options and features defined by the Butler
   Platform specification.

|

Firebird Butler Services
========================

A Butler Service is basically a piece of software that uses `ZeroMQ socket` and
:doc:`Firebird Butler Service Protocol </rfc/4/FBSP>` for communication over this ZeroMQ
channel. A service could use multiple ZeroMQ sockets for various purposes, but only one
primary socket is required to support the Butler Service protocol.

**Butler Services could do anything**, but a well designed service does only one task, or
a small set of closely related tasks within single category. While respecting the rule
of simplicity, services can be divided into several basic types:

- `Measuring` services, that collect and pass on data. For example it may collect data
  from monitoring tables.
- `Processing` services, that take data on input, do something (on them) and have some
  data on output. This general category includes services that perform analytics, data
  transformation, brokers, bridges, routers, aggregators, load balancers etc.
- `Provider` services, that do things on request. For example perform a database backup.
- `Control` services, that manage other services.


Planned services
----------------

.. note::

   The following overview contains only services that we currently consider to be the core
   of the Firebird Butler (product). They represent a road map for developing the first
   version within the :ref:`Saturnin Core` sub-project.

*Measuring* services
^^^^^^^^^^^^^^^^^^^^

At first we want to take advantage of existing Firebird features (API, monitoring tables,
trace service, user queries etc.) to provide data about transactions, connections, queries,
security, configuration, resources, availability, operational information (logs, gstat
output etc.). Consequently, we assume that additional user requirements for new information
sources or formats will be met in collaboration with the Firebird engine developers.

*Processing* services
^^^^^^^^^^^^^^^^^^^^^

We plan to create **at least** the following set of services in this category:

- User-defined state machine analytics on measured data to trigger actions or emit signals
- Export of metrics to the Graphite_ open source monitoring product (primarily as metrics
  storage and a visualization solution)
- Import connector for the python-diamond_ open source daemon that collects system metrics
  such as cpu, memory, network, i/o, load, disk etc.
- Notification service to send reports and alerts via e-mail and other means.
- Logging service, to collect log entries from other services.

*Provider* services
^^^^^^^^^^^^^^^^^^^
We plan to create **at least** the following set of services in this category:

- Registry service for services and other resources, as a solution for central configuration needs.
- Scheduler service to run jobs on a regular basis
- Extensible storage service (it will provide at least file-based storage)
- Services for Firebird-related tasks like: backup & restore (gbak and nbackup), sweep and
  other tasks provided by gfix, cancellation of connections and transactions, user defined
  SQL commands and scripts
- Service to run user defined action -> external program or script

*Control* services
^^^^^^^^^^^^^^^^^^

We plan to create **at least** the following set of services in this category:

- General control service that uses Butler protocol specification to keep track of the state
  and configuration of registered running services, could emit signals and other
  information messages about it, and provide management service activities within the scope
  defined by the Butler protocol.
- A command-line tool to interact with this control service.

|

Where to go next
================

* The Firebird "Butler" Project :doc:`structure and organization <organization>`
* The Firebird Butler :doc:`Specifications <specifications>`
* The `Firebird Project`_ main website

|
|

.. [1] Do you know that *InterBase* (the progenitor of the *Firebird RDBMS*) pioneered several technology concepts like  *Multi-version Concurrency Control* (MVCC_) or BLOBs_?


.. _IBPhoenix: http://www.ibphoenix.com
.. _Firebird: http://www.firebirdsql.org
.. _Firebird Project: http://www.firebirdsql.org
.. _Zato: https://zato.io/
.. _ZeroMQ: http://zeromq.org/
.. _ZGuide: http://zguide.zeromq.org/
.. _JeroMQ: https://github.com/zeromq/jeromq
.. _NetMQ: https://github.com/zeromq/netmq
.. _Graphite: https://graphiteapp.org/
.. _python-diamond: https://github.com/python-diamond/Diamond
.. _MVCC: https://en.wikipedia.org/wiki/Multiversion_concurrency_control
.. _BLOBs: http://www.ibphoenix.com/resources/documents/history/doc_299
