# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Módulo de simulación de cámara (camera_mock.py) para permitir ejecución sin hardware de cámara
- Archivo de información de configuración de cámara (camera_config_info.py)
- Manejo de disponibilidad de módulo de cámara en video_server.py y camera_config_server.py
- Script de prueba con depuración detallada para cámara (tests/camera_test_debug.py)
- Documentación del script de prueba de cámara (tests/README_CAMERA_TEST.md)

### Changed

- Actualización de main.py para verificar disponibilidad de módulo de cámara
- Actualización de video_server.py para usar módulo de cámara simulado si no está disponible el real
- Actualización de camera_config_server.py para usar módulo de cámara simulado si no está disponible el real

### Deprecated

- [Lista de características obsoletas]

### Removed

- [Lista de características eliminadas]

### Fixed

- Error "'module' object has no attribute 'init'" al iniciar la cámara
- Sistema ahora maneja correctamente la ausencia del módulo de cámara

### Security

- [Lista de mejoras de seguridad]