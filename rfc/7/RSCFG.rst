###############################################
7/RSCFG - Remote Service Configuration Protocol
###############################################

:domain: github.com/FirebirdSQL/Butler
:shortname: 7/RSCFG
:name: Remote Service Configuration Protocol
:status: raw
:editor: Pavel Císař <pcisar@users.sourceforge.net>

Remote Service Configuration Protocol (RSCFG) specifies a uniform method for configuring Firebird Butler Service operating parameters through Client requests passed via |FBSP| protocol.

License
=======

Copyright (c) 2018 The Firebird Butler Project.

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
#. :doc:`/rfc/4/FBSP`
#. :doc:`/rfc/5/FBLP`
#. :doc:`/rfc/6/SSTP`
#. :doc:`/rfc/8/RSCTRL`

1. Goals
========

The purpose of this specification is to define unified data format, and formal rules for exchanging configuration information between Butler Service and its Client. Its goals are:

#. Define unified, flexible and extensible data format for `Service` configuration information, suitable for diagnostic and control purposes.
#. Define serialization format for such configuration information suitable for transmission in |FBSP| `Data Frames`.
#. Define a base API for transmitting such configuration information between the :doc:`Firebird Butler Service </rfc/3/FBSD>` and the `Client`.
#. Define a base API for remote `Service` configuration by its `Client`.

2. Implementation
=================

.. todo:: 
   :class: todo

   Specification body.

|
|

.. _RFC2119: http://tools.ietf.org/html/rfc2119
.. |COSS-long| replace:: :doc:`/rfc/2/COSS`
.. |FBSD| replace:: :doc:`3/FBSD</rfc/3/FBSD>`
.. |FBSP| replace:: :doc:`4/FBSP</rfc/4/FBSP>`
.. |FBLP| replace:: :doc:`5/FBLP</rfc/5/FBLP>`
.. |SSTP| replace:: :doc:`6/SSTP</rfc/6/SSTP>`
.. |RSCTRL| replace:: :doc:`8/RSCTRL</rfc/8/RSCTRL>`

