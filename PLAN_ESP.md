[Español](./PLAN_ESP.md) - [English](./PLAN.md)

# Plan de Desarrollo del Proyecto ESP32-S3 CAM

## Descripción General

Proyecto para implementar un firmware en ESP32-S3 CAM con servidor web integrado para control y visualización de cámara, con interfaz web con tema oscuro y todas las comunicaciones en castellano.

## Requisitos del Proyecto

### 1. Lenguaje y Entorno

- Todo en castellano
- Tema oscuro para las webs
- Documentación de cada paso del TODOlist
- Trabajo con Thonny y MicroPython

### 2. Funcionalidades del Firmware

- Servidor web integrado con modo AP para configuración inicial
- Conexión a WiFi con credenciales guardadas
- Streaming de video en tiempo real
- Interfaz web de configuración avanzada

### 3. Indicador Visual

- Uso del LED RGB en el pin 48 para mostrar estados
  - AP: Azul
  - Station: Verde
  - Transmitiendo: Blanco
  - Error: Rojo

### 4. Interfaces Web

- Interfaz principal para ver video en tiempo real
- Interfaz de configuración (IP/cam) con previsualización y controles
- Información del hardware de la cámara en la interfaz de configuración

## Plan Detallado de Implementación

### 1. Investigación Inicial

- Investigar la biblioteca de cámara para ESP32-S3 en MicroPython
- Revisar ejemplos de conexión WiFi en modo dual (Station/AP)
- Estudiar cómo servir imágenes de video en tiempo real con MicroPython
- Investigar cómo obtener información del hardware de la cámara (modelo, resolución máxima, etc.)
- Revisar cómo controlar un LED RGB en MicroPython para ESP32-S3

### 2. Configurar Entorno de Desarrollo

- Configurar Thonny con MicroPython para ESP32-S3
- Verificar conexión al módulo y subida de scripts
- Crear estructura de directorios para el proyecto

### 3. Desarrollar Control de LED RGB

- Crear módulo para controlar el LED RGB en el pin 48
- Implementar códigos de colores para diferentes estados
- Integrar el control de LED en las funciones principales del sistema

### 4. Desarrollar WiFi Manager

- Crear script para detectar si hay credenciales de WiFi guardadas
- Implementar modo AP con servidor web para configuración de WiFi
- Crear interfaz web HTML/CSS/JS para configurar conexión WiFi con tema oscuro
- Implementar guardado de credenciales en archivos del ESP32
- Actualizar LED RGB a azul cuando esté en modo AP

### 5. Desarrollar Servidor Web de Video

- Crear servidor web principal que se active tras conexión WiFi
- Implementar streaming de imagen de cámara en tiempo real
- Desarrollar interfaz web para mostrar video con tema oscuro
- Actualizar LED RGB a verde cuando esté en modo Station y blanco cuando esté transmitiendo

### 6. Desarrollar Servidor Web de Configuración de Cámara

- Crear endpoint web adicional en sub-URL (IP/cam)
- Implementar previsualización de imagen de cámara en tiempo real
- Añadir controles típicos de configuración de cámara (brillo, contraste, resolución, etc.)
- Implementar actualización de parámetros de cámara en tiempo real
- Añadir sección en la interfaz web para mostrar información del hardware de la cámara (modelo, resolución máxima, etc.)

### 7. Implementar Tema Oscuro y Estilo

- Crear CSS común con tema oscuro para ambas interfaces web
- Asegurar consistencia visual entre las interfaces de configuración y visualización

### 8. Documentación del Proyecto

- Documentar cada paso del desarrollo con comentarios detallados
- Crear archivo README.md con instrucciones de instalación y uso
- Documentar el código fuente con comentarios en castellano
- Registrar cada funcionalidad implementada con descripción
- Documentar el código de colores del LED RGB
- Crear archivo Changelog.md para mantener un historial de cambios
- Crear TODOlist con posibles mejoras futuras en un archivo o sección específica

### 9. Pruebas y Validación

- Probar la funcionalidad de conexión WiFi en modo AP
- Verificar el streaming de video en tiempo real
- Validar los controles de configuración de cámara
- Probar la visualización de información del hardware
- Comprobar que los estados del LED RGB se actualizan correctamente
- Realizar pruebas de integración completa

### 10. Optimización y Refinamiento

- Optimizar el consumo de recursos del servidor web
- Refinar la interfaz de usuario para mejor experiencia
- Ajustar el rendimiento del streaming de video
- Optimizar el uso del LED RGB para no interferir con otros procesos

### 11. Preparación Final y Presentación

- Crear script de instalación completa
- Documentar posibles problemas y soluciones
- Preparar documentación final del proyecto
- Actualizar archivo Changelog.md con los cambios realizados

## Documentación Específica

### Changelog.md

Archivo para documentar los cambios de la forma habitual, siguiendo el formato:

```
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- [Lista de nuevas características]

### Changed
- [Lista de cambios realizados]

### Deprecated
- [Lista de características obsoletas]

### Removed
- [Lista de características eliminadas]

### Fixed
- [Lista de correcciones de errores]

### Security
- [Lista de mejoras de seguridad]
```

### TODOlist de Mejoras Futuras

Posibles extensiones del proyecto:

- Añadir autenticación para proteger las interfaces web
- Implementar grabación de video y almacenamiento en tarjeta SD
- Añadir detección de movimiento y notificaciones
- Implementar control remoto mediante comandos API
- Añadir funcionalidad de seguimiento de objetos
- Incorporar reconocimiento de rostros
- Desarrollar aplicación móvil para control remoto
- Implementar streaming a múltiples clientes simultáneamente
- Añadir funcionalidad de timbre inteligente con notificaciones
- Crear sistema de alertas basado en IA
- Implementar compresión de video para reducir ancho de banda
- Añadir soporte para múltiples cámaras
- Integrar con servicios de nube para almacenamiento remoto

## Estado del Proyecto

- Plan: Aprobado
- Fase: Implementación de módulos, resolución de problemas de hardware

## Problemas Identificados

- Módulo 'camera' no disponible en la instalación actual de MicroPython
- Solución temporal implementada con módulo de simulación
- Pendiente verificar versión de MicroPython con soporte de cámara

## Tareas Completadas

- ✅ Implementación de módulo de simulación de cámara
- ✅ Actualización de video_server.py para manejar módulos de cámara disponibles
- ✅ Actualización de camera_config_server.py para manejar módulos de cámara disponibles
- ✅ Actualización de main.py para verificar disponibilidad de la cámara
- ✅ Creación de archivo de información de configuración de cámara
- ✅ Creación de script de prueba con depuración detallada para cámara
- ✅ Creación de documentación para el script de prueba de cámara