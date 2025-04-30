# Change Log
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## [2.0.0] - 2025-04-30

### Changed

- Minimal Python version raised to 3.11
- Dependency on `protobuf` changed to "~=5.29".
- Protobufs recompiled with protoc 25.1

## [1.0.0] - 2023-10-03

### Added

- Tests (pytest)

### Changed

- Requirements downgraded to protobuf>=4.23.4

## [1.0.0] - 2023-10-03

### Changed

- Update dependency to protobuf >=4.24.3
- Recompilation of protobuf definitions with libprotoc 23.4
- Build system changed from setuptools to hatch
- Package version is now defined in firebird.butler.__about__.py (__version__)

### Added

- .pyi files for protobuf modules.

## [0.5.0] - 2022-11-14

## [0.4.0] - 2022-10-18

## [0.3.1] - 2021-03-04

## [0.2.2] - 2020-02-27

## [0.2.0] - 2019-10-13

Initial release. Contains next modules with protobuf messages and nums:

- firebird.butler.fbsd_pb2 for [Firebird Butler Service Definition](https://firebird-butler.readthedocs.io/en/latest/rfc/3/FBSD.html)
- firebird.butler.fbsp_pb2 for [Firebird Butler Service Protocol](https://firebird-butler.readthedocs.io/en/latest/rfc/4/FBSP.html)
- firebird.butler.fbdp_pb2 for [Firebird Butler Data Pipe Protocol](https://firebird-butler.readthedocs.io/en/latest/rfc/9/FBDP.html)

