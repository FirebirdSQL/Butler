################################################
2/COSS - Consensus-Oriented Specification System
################################################

:domain: github.com/FirebirdSQL/Butler
:shortname: 2/COSS
:name: Consensus-Oriented Specification System
:status: stable
:editor: Pavel Císař <pcisar@users.sourceforge.net>


This document describes a consensus-oriented specification system (COSS) for building
interoperable technical specifications. COSS is based on a lightweight editorial process
that seeks to engage the widest possible range of interested parties and move rapidly to
consensus through working code.

This specification is derived from the `COSS <https://rfc.unprotocols.org/spec:2/COSS/>`_
specification used by ZeroMQ project.

This is revision 1 of the COSS specification.

License
=======

Copyright (c) 2008-16 the Editor and Contributors.
Copyright (c) 2018 The Firebird Butler Project.

This Specification is free software; you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software Foundation;
either version 3 of the License, or (at your option) any later version.

This Specification is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program;
if not, see http://www.gnu.org/licenses.

Change Process
==============

This Specification is a free and open standard and is governed by the Consensus-Oriented
Specification System (COSS) (i.e. by itself).

.. note::

   All ideas and change proposals SHOULD be presented and discussed first in
   the `Firebird Butler forum <https://groups.google.com/d/forum/firebird-butler>`_.

Language
========

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT",
"RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described
in `RFC2119`_.

Goals
=====

The primary goal of COSS is to facilitate the process of writing, proving, and improving
new technical specifications. A "technical specification" defines a protocol, a process,
an API, a use of language, a methodology, or any other aspect of a technical environment
that can usefully be documented for the purposes of technical or social interoperability.

COSS is intended to above all be economical and rapid, so that it is useful to small teams
with little time to spend on more formal processes.

Principles:

- We aim for rough consensus and running code.
- Specifications are small pieces, made by small teams.
- Specifications should have a clearly responsible editor.
- The process should be visible, objective, and accessible to anyone.
- The process should clearly separate experiments from solutions.
- The process should allow deprecation of old specifications.

Specifications should take minutes to explain, hours to design, days to write, weeks to
prove, months to become mature, and years to replace.

Specifications have no special status except that accorded by the community.

Architecture
============

COSS is designed around fast, easy to use communications tools. Primarily, COSS uses
a `git` repository for editing and publishing specifications texts. Additionally, it uses
`Sphinx`_ (or other similar system) for text processing and a `web site` for publishing
specifications texts in other formats than raw text.

- The domain is the conservancy for a set of specifications in a certain area.
- Each domain is implemented as an Internet site with fixed URI (preferably an Internet
  domain), hosting a `git repository` and optionally other communications tools.
- All specifications are stored in repository under `/rfc` directory.
- Each specification is a set of pages, together with comments, attached files, and other resources.
- All texts pages are in reStructuredText markup.
- Specifications exist as multiple pages, one page per version of the specification (see
  `Branching and Merging`_, below), with assigned unique incremental number.
- Specification text is stored in `/rfc/<number>/<shortname>.rst` file. Thus, we refer to
  a specification by specifying its number and short name.
- All related files should be stored in the same directory as the main text file.
- New versions of the same specification will have new numbers (i.e. will reside in
  different directories). The syntax for a specification reference is::

    <domain>/rfc/<number>/<shortname>.rst

  For example, this specification is `github.com/FirebirdSQL/Butler/rfc/2/COSS.rst`.
  The  short form `2/COSS` may be used when referring to the specification from other
  specifications in the same domain. The RST markup for inserting a hyperlink from
  the specification in the same domain in this case is::

    :doc:`/rfc/2/COSS`  # specification full name as link text
    :doc:`2/COSS </rfc/2/COSS>`  # specification shortname as link text

Every specification (including branches) carries a different number. Lower numbers indicate
more mature specifications, higher numbers indicate more experimental specifications.


COSS Lifecycle
==============

Every specification has an independent lifecycle that documents clearly its current status.

A specification has six possible states that reflect its maturity and contractual weight:

.. image:: /rfc/2/lifecycle.png

Raw Specifications
------------------

All new specifications are raw specifications. Changes to raw specifications can be
unilateral and arbitrary. Those seeking to implement a raw specification should ask for it
to be made a draft specification. Raw specifications have no contractual weight.

Draft Specifications
--------------------

When raw specifications can be demonstrated, they become draft specifications. Changes to
draft specifications should be done in consultation with users. Draft specifications are
contracts between the editors and implementers.

Stable Specifications
---------------------

When draft specifications are used by third parties, they become stable specifications.
Changes to stable specifications should be restricted to cosmetic ones, errata and
clarifications. Stable specifications are contracts between editors, implementers,
and end-users.

Deprecated Specifications
-------------------------

When stable specifications are replaced by newer draft specifications, they become
deprecated specifications. Deprecated specifications should not be changed except to
indicate their replacements, if any. Deprecated specifications are contracts between
editors, implementers and end-users.

Retired Specifications
----------------------

When deprecated specifications are no longer used in products, they become retired
specifications. Retired specifications are part of the historical record. They should not
be changed except to indicate their replacements, if any. Retired specifications have no
contractual weight.

Deleted Specifications
----------------------

Deleted specifications are those that have not reached maturity (stable) and were discarded.
They should not be used and are only kept for their historical value. Only Raw and Draft
specifications can be deleted.

Editorial control
=================

A specification MUST have a single responsible editor, the only person who SHALL change
the status of the specification through the lifecycle stages.

A specification MAY also have additional contributors who contribute changes to it. It is
RECOMMENDED to use the C4 process to maximize the scale and diversity of contributions.

The editor is responsible for accurately maintaining the state of specifications and for
handling all comments on the specification.

Branching and Merging
=====================

Any member of the domain MAY branch a specification at any point. This is done by copying
the existing text, and creating a new specification with the same name and content, but
a new number. The ability to branch a specification is necessary in these circumstances:

- To change the responsible editor for a specification, with or without the cooperation
  of the current responsible editor.
- To rejuvenate a specification that is stable but needs functional changes. This is
  the proper way to make a new version of a specification that is in stable or deprecated
  status.
- To resolve disputes between different technical opinions.

The responsible editor of a branched specification is the person who makes the branch.

Branches, including added contributions, are derived works and thus licensed under the same
terms as the original specification. This means that contributors are guaranteed the right
to merge changes made in branches back into their original specifications.

Technically speaking, a branch is a different specification, even if it carries the same
name. Branches have no special status except that accorded by the community.

Conflict resolution
===================

COSS resolves natural conflicts between teams and vendors by allowing anyone to define
a new specification. There is no editorial control process except that practised by
the editor of a new specification. The administrators of a domain (moderators) may choose
to interfere in editorial conflicts, and may suspend or ban individuals for behaviour they
consider inappropriate.

Conventions
===========

Where possible editors and contributors are encouraged to:

- Refer to and build on existing work when possible, especially IETF specifications.
- Contribute to existing specifications rather than reinvent their own.
- Use collaborative branching and merging as a tool for experimentation.

Appendix A. Color Coding
========================

It is RECOMMENDED to use color coding to indicate specification's status. Color coded
specifications SHOULD use the following color scheme:

- |raw|
- |draft|
- |stable|
- |deprecated|
- |retired|
- |deleted|

Appendix B. Metainformation
===========================

It is RECOMMENDED that specification metadata is specified as a YAML header (where possible)
or a separate YAML file. This will enable programmatic access to specification metadata.

.. list-table::
   :widths: 20 20 20 40
   :header-rows: 1

   * - Key
     - Value
     - Type
     - Example
   * - domain
     - specification domain
     - string
     - rfc.unprotocols.org
   * - shortname
     - short name
     - string
     - 2/COSS
   * - name
     - full name
     - string
     - Consensus-Oriented Specification System
   * - status
     - status
     - string
     - draft
   * - editor
     - editor name/email
     - string
     - Yurii Rashkovskii yrashk@gmail.com
   * - contributors
     - contributors
     - list
     - Pieter Hintjens ph@imatix.com, André Rebentisch andre@openstandards.de, Alberto Barrionuevo abarrio@opentia.es, Chris Puttick chris.puttick@thehumanjourney.net

.. _RFC2119: http://tools.ietf.org/html/rfc2119
.. _Sphinx: http://www.sphinx-doc.org
.. |raw| image:: /rfc/2/raw.svg
.. |draft| image:: /rfc/2/draft.svg
.. |stable| image:: /rfc/2/stable.svg
.. |deprecated| image:: /rfc/2/deprecated.svg
.. |retired| image:: /rfc/2/retired.svg
.. |deleted| image:: /rfc/2/deleted.svg

