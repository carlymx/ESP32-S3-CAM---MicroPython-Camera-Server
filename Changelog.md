[Español](./Changelog_ESP.md) - [English](Changelog.md)

# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Camera simulation module (camera_mock.py) to allow execution without camera hardware
- Camera configuration information file (camera_config_info.py)
- Camera module availability handling in video_server.py and camera_config_server.py
- Detailed debugging test script for camera (tests/camera_test_debug.py)
- Camera test script documentation (tests/README_CAMERA_TEST.md)

### Changed

- Update of main.py to verify camera module availability
- Update of video_server.py to use simulated camera module if real one is not available
- Update of camera_config_server.py to use simulated camera module if real one is not available

### Deprecated

- [List of deprecated features]

### Removed

- [List of removed features]

### Fixed

- Error "'module' object has no attribute 'init'" when starting camera
- System now correctly handles absence of camera module

### Security

- [List of security improvements]