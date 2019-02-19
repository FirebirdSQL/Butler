####################
Project organization
####################


Basic project structure
=======================


Firebird Butler is an extensive project, divided into several layers and pillars.

The layers are:

1. **Specifications and other documents**
    
   This is the shared foundation of the Butler project. This document collection (in which this text is included) contains a description of the project, its parts and how they fit in with each other, the specification of the developer platform, the used communication protocols, and the recommended practices for their implementation and use. It also includes the specification of selected services implemented within the project, and other related documentation.
       
   All these documents (provided under `CC-BY-SA-4.0` license) reside in the `Butler repository <https://github.com/FirebirdSQL/Butler>`_ on GitHub. They are also accessible in HTML and other formats at `readthedocs`.
   
   The main communication channel for discussion of specifications, implementation strategies, and other issues related to the whole project or its basics is the `firebird-butler forum <https://groups.google.com/d/forum/firebird-butler>`_ on googlegroups.
   
   .. tip::
   
      There is also a low-traffic, read-only `annoucement list <https://groups.google.com/d/forum/firebird-butler-ann>`_ for delivery of information about new releases and other important events related to the project.
       
2. **Implementations of the Butler SDK**
    
   Different implementations of the development platform represent the individual pillars of the project. These pillars are typically formed around a particular programming language or development environment. Currently, due to limited resources, the project has only three pillars:
   
    1. `saturnin-sdk`_ : a reference implementation in Python
    2. `ButlerJavaSDK`_ : implementation in Java
    3. :ref:`Butler SDK for Free Pascal <butler-fpc-sdk>` : implementation in Free Pascal
     
   We hope the project's potential will attract other developers to help us deliver implementations also for Delphi, C# and other environments.
   
   Each SDK is a sub-project with its own repositories, communication channels, developers and documentation.
       
3. **Implementations of Butler Services**
    
   Implementation of :doc:`Butler services </rfc/3/FBSD>` is structured into stand-alone sub-projects because it is typically defined by the SDK used and the specific focus. Any such project can define its own standards and specifications beyond the basic :doc:`specifications for Butler Services <specifications>`. The basic specifications then provide the necessary minimum level of interoperability between Services implemented by different sub-projects.
   
   Within the Firebird Butler project, only one sub-project of this type is currently being developed - a Firebird Butler implementation in Python called `Saturnin`_. Its aim is to provide a standard solution for management of Firebird deployments of any size, structure and complexity with an emphasis on large corporate installations.
   
   However, other such projects with different focus and features can be developed both within and outside the Firebird Butler project.
   
4. **Distribution packages**
    
   Distribution bundles are the final product designed for common users. Like Linux distributions, they can include and combine various results from different Butler implementation projects to achieve different goals.
   
   Since the Firebird Butler project is only in its beginnings, no distributions are yet available.

.. _saturnin-sdk:

Saturnin SDK
============

The purpose of the *Saturnin SDK* sub-project is to provide basic tools for Python to create :doc:`Firebird Butler services </rfc/3/FBSD>` while providing a reference implementation of :doc:`Firebird Butler specifications  <specifications>`.

.. list-table:: 
   :widths: 30 70

   * - Lead developer
     - `Pavel Císař <mailto:pcisar2@gmail.com>`_
   * - GitHub home repository
     - `FirebirdSQL / saturnin-sdk <https://github.com/FirebirdSQL/saturnin-sdk>`_
   * - Documentation and other information sources
     - `readthedocs`
   * - Main communication channel
     - `saturnin-sdk forum <https://groups.google.com/d/forum/saturnin-sdk>`_ at googlegroups
     
.. _ButlerJavaSDK:

ButlerJavaSDK
=============

The purpose of the *ButlerJava SDK* sub-project is to provide basic tools for Java to create :doc:`Firebird Butler services </rfc/3/FBSD>` in accordance to :doc:`Firebird Butler specifications  <specifications>`.

.. list-table:: 
   :widths: 30 70

   * - Lead developer
     - `Sergey Nikitin <mailto:nikitinse@gmail.com>`_
   * - GitHub home repository
     - `FirebirdSQL / ButlerJavaSDK <https://github.com/FirebirdSQL/ButlerJavaSDK>`_
   * - Documentation and other information sources
     - `readthedocs`
   * - Main communication channel
     - `butlerj-sdk forum <https://groups.google.com/d/forum/butlerj-sdk>`_ at googlegroups

.. _butler-fpc-sdk:

Butler SDK for Free Pascal
==========================

The purpose of the *Butler SDK for Free Pascal* sub-project is to provide basic tools for Free Pascal and Lazarus to create :doc:`Firebird Butler services </rfc/3/FBSD>` in accordance to :doc:`Firebird Butler specifications  <specifications>`.

.. list-table:: 
   :widths: 30 70

   * - Lead developer
     - `Paul Reeves <mailto:ibbennu@gmail.com>`_
   * - GitHub home repository
     - `FirebirdSQL / butler-fpc-sdk <https://github.com/FirebirdSQL/butler-fpc-sdk>`_
   * - Documentation and other information sources
     - `readthedocs`
   * - Main communication channel
     - `butler-fpc-sdk forum <https://groups.google.com/d/forum/butler-fpc-sdk>`_ at googlegroups
     
.. _saturnin:

Saturnin
========

The purpose of the *Saturnin* sub-project is to provide Python-based standard solution, using the Saturnin SDK, for management of Firebird deployments of any size, structure and complexity with an emphasis on large corporate installations. The :doc:`main focus <introduction>` of the project is the creation of services and a platform for their deployment within an integrated solution.

.. list-table:: 
   :widths: 30 70

   * - Lead developer
     - `Pavel Císař <mailto:pcisar2@gmail.com>`_
   * - GitHub home repository
     - `FirebirdSQL / saturnin <https://github.com/FirebirdSQL/saturnin>`_
   * - Documentation and other information sources
     - `readthedocs`
   * - Main communication channel
     - `firebird-saturnin forum <https://groups.google.com/d/forum/firebird-saturnin>`_ at googlegroups
     