# Plugin Forge: Un Asistente para Crear Plugins de QGIS

## 1. Resumen del Proyecto

**Plugin Forge** es un complemento para QGIS diseñado para simplificar y acelerar el desarrollo de otros plugins. Actúa como un asistente que, a través de una sencilla interfaz gráfica, solicita al usuario la información básica de un nuevo plugin (nombre, descripción, autor, etc.) y genera automáticamente toda la estructura de directorios y archivos base necesarios para empezar a programar.

El objetivo principal es eliminar los pasos repetitivos y propensos a errores de la configuración inicial de un plugin de QGIS.

---

## 2. Estado Actual del Proyecto (Fase 1 Completada)

Actualmente, el proyecto ha alcanzado un estado funcional estable. La funcionalidad implementada es la siguiente:

### Funcionalidades Clave:
- **Interfaz Gráfica (GUI):** Un diálogo modal, creado con Qt Designer, solicita al usuario los metadatos esenciales del nuevo plugin.
- **Generación de Estructura de Archivos:** Al confirmar los datos, el plugin crea una carpeta para el nuevo plugin y la puebla con los siguientes archivos base, personalizados con la información introducida:
  - `metadata.txt`: Con toda la información del plugin.
  - `__init__.py`: Punto de entrada que carga la clase principal.
  - `[nombre_del_plugin].py`: El archivo principal del plugin con la estructura de clase básica.
  - `[nombre_del_plugin]_dialog.py`: El controlador para el diálogo del nuevo plugin.
  - `[nombre_del_plugin]_dialog_base.ui`: Un archivo de interfaz de usuario de ejemplo para el nuevo plugin.
  - `resources.qrc`: Archivo de recursos XML para gestionar iconos y otros assets.
  - `icon.png`: Un icono por defecto, copiado del propio Plugin Forge.

### Proceso de Uso Actual:
1.  El usuario instala y activa `Plugin Forge` en QGIS.
2.  Ejecuta el asistente desde la barra de herramientas.
3.  Rellena el formulario y selecciona un directorio de salida.
4.  El plugin genera la estructura de archivos en la ubicación seleccionada.

### Limitación Conocida (Objetivo de la Fase 2):
- El archivo de recursos (`resources.qrc`) es creado, pero **no compilado**. El usuario debe ejecutar manualmente el comando `pyrcc5 -o resources.py resources.qrc` desde la terminal **OSGeo4W Shell** para que el nuevo plugin sea 100% funcional.

---

## 3. Hoja de Ruta (Roadmap)

El proyecto avanza por fases para asegurar un desarrollo incremental y estable.

### ✅ Fase 1: Generador de Esqueleto Básico (Completada)
- [x] Crear la interfaz de usuario para la recolección de datos.
- [x] Implementar la lógica para generar la estructura de carpetas y archivos.
- [x] Asegurar que el plugin generado sea válido y funcional (tras compilación manual).
- [x] Probar el flujo completo y solucionar errores iniciales (errores de metadatos, rutas, etc.).

### ⏳ Fase 2: Automatización y Mejoras (En Progreso)
- **(Punto 1 - Nuestro siguiente paso)** **Automatizar la compilación de recursos:** Integrar la ejecución del comando `pyrcc5` directamente en `PluginForge` usando los módulos `subprocess` y `sys` de Python. El objetivo es que el plugin generado sea funcional "out-of-the-box".
- **(Punto 2)** **Ofrecer Plantillas Avanzadas:** Permitir al usuario elegir entre diferentes tipos de plantillas de plugin (ej: con panel anclable, con selector de capas, que ejecute un algoritmo de procesamiento, etc.).
- **(Punto 3)** **Mejorar la Interfaz:** Añadir más opciones de personalización, como la posibilidad de que el usuario seleccione su propio icono para el nuevo plugin.

---

## 4. Historial de Decisiones y Aprendizajes Clave

- **Guardado de Prompts:** Se identificó la necesidad de guardar los prompts y las conversaciones de desarrollo para evitar la pérdida de información valiosa.
- **Entorno de Desarrollo:** Se aprendió que las herramientas de línea de comandos de QGIS (como `pyrcc5`) deben ejecutarse desde el **OSGeo4W Shell** para heredar las variables de entorno correctas (`PYTHONPATH`, `PYTHONHOME`), en lugar de un CMD estándar de Windows.
- **Control de Versiones:** Se adoptó **Git** y **GitHub** como sistema de control de versiones para gestionar el código, guardar el historial de cambios y tener una copia de seguridad robusta del proyecto.
- **Depuración de Metadatos:** Se resolvió un error de "complemento roto" causado por caracteres inválidos y tabulaciones ocultas en el archivo `metadata.txt`.
