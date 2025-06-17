# -*- coding: utf-8 -*-
import os
import shutil  # Necesario para copiar archivos (nuestro icono)

from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QDialog
from qgis.core import Qgis  # Para los niveles de los mensajes (Success, Critical)

# Importar la clase del diálogo que hemos creado
from .plugin_forge_dialog import PluginForgeDialog
from . import resources  # Importante para que los recursos (icono) se carguen

class PluginForge:
    def __init__(self, iface):
        self.iface = iface
        self.plugin_dir = os.path.dirname(__file__)
        self.actions = []
        self.menu = u"&Plugin Forge"
        self.dialog = None

    def tr(self, message):
        return QCoreApplication.translate('PluginForge', message)

    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        parent=None):
        
        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if add_to_toolbar:
            self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToMenu(self.menu, action)

        self.actions.append(action)
        return action

    def initGui(self):
        """Crea la entrada de menú y el icono de la barra de herramientas."""
        icon_path = ':/plugins/plugin_forge/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Asistente para Crear Plugins'),
            callback=self.run,
            parent=self.iface.mainWindow())

    def unload(self):
        """Elimina los elementos de la interfaz al desactivar el plugin."""
        for action in self.actions:
            self.iface.removePluginMenu(u"&Plugin Forge", action)
            self.iface.removeToolBarIcon(action)

    def run(self):
        """Función principal que se ejecuta al pulsar el botón."""
        if self.dialog is None:
            self.dialog = PluginForgeDialog()

        result = self.dialog.exec_()
        
        if result == QDialog.Accepted:
            # --- ¡Aquí ocurre la magia! ---
            plugin_name = self.dialog.lineEditPluginName.text()
            description = self.dialog.lineEditDescription.text()
            author = self.dialog.lineEditAuthor.text()
            email = self.dialog.lineEditEmail.text()
            output_dir = self.dialog.lineEditOutputDir.text()

            # Validar que los campos no estén vacíos
            if not all([plugin_name, description, author, email, output_dir]):
                self.iface.messageBar().pushMessage("Error", "Todos los campos son obligatorios.", level=Qgis.Critical, duration=5)
                return

            try:
                # Llamamos a nuestra nueva función para generar la estructura
                self.generate_plugin_structure(plugin_name, description, author, email, output_dir)
                self.iface.messageBar().pushMessage(
                    "Éxito", 
                    f"Plugin '{plugin_name}' creado en la carpeta de salida.", 
                    level=Qgis.Success, 
                    duration=10)
            except Exception as e:
                self.iface.messageBar().pushMessage("Error de Generación", f"No se pudo crear el plugin: {e}", level=Qgis.Critical, duration=10)

    def generate_plugin_structure(self, plugin_name, description, author, email, output_dir):
        """
        Genera la estructura de directorios y archivos para el nuevo plugin.
        """
        # 1. Preparar nombres
        module_name = plugin_name.lower().replace(' ', '_').replace('-', '_')
        class_name = plugin_name.replace(' ', '').replace('-', '')

        # 2. Crear el directorio principal del plugin
        plugin_path = os.path.join(output_dir, module_name)
        os.makedirs(plugin_path, exist_ok=True)

        # 3. Crear los archivos a partir de plantillas de texto (usando f-strings)

        # --- metadata.txt ---
        metadata_content = f"""
[general]
name={plugin_name}
qgisMinimumVersion=3.16
description={description}
version=0.1
author={author}
email={email}
about=Este es un plugin de ejemplo generado por Plugin Forge.

[python]
plugin_module={module_name}
class_name={class_name}
"""
        with open(os.path.join(plugin_path, 'metadata.txt'), 'w', encoding='utf-8') as f:
            f.write(metadata_content.strip())

        # --- __init__.py ---
        init_content = f"""
def classFactory(iface):
    from .{module_name} import {class_name}
    return {class_name}(iface)
"""
        with open(os.path.join(plugin_path, '__init__.py'), 'w', encoding='utf-8') as f:
            f.write(init_content.strip())

        # --- {module_name}.py (archivo principal) ---
        main_plugin_content = f"""
import os
from qgis.PyQt.QtCore import QCoreApplication
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction
from . import resources
from .{module_name}_dialog import {class_name}Dialog

class {class_name}:
    def __init__(self, iface):
        self.iface = iface
        self.plugin_dir = os.path.dirname(__file__)
        self.actions = []
        self.menu = self.tr(u'&{plugin_name}')
        self.toolbar = self.iface.addToolBar(u'{plugin_name}')
        self.toolbar.setObjectName(u'{class_name}Toolbar')

    def tr(self, message):
        return QCoreApplication.translate('{class_name}', message)

    def add_action(self, icon_path, text, callback, parent=None):
        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        self.iface.addPluginToMenu(self.menu, action)
        self.toolbar.addAction(action)
        self.actions.append(action)
        return action

    def initGui(self):
        icon_path = ':/plugins/{module_name}/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Ejecutar {plugin_name}'),
            callback=self.run,
            parent=self.iface.mainWindow())

    def unload(self):
        for action in self.actions:
            self.iface.removePluginMenu(self.tr(u'&{plugin_name}'), action)
            self.iface.removeToolBarIcon(action)
        del self.toolbar

    def run(self):
        dialog = {class_name}Dialog()
        dialog.exec_()
"""
        with open(os.path.join(plugin_path, f'{module_name}.py'), 'w', encoding='utf-8') as f:
            f.write(main_plugin_content.strip())

        # --- {module_name}_dialog.py ---
        dialog_py_content = f"""
import os
from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QDialog

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), '{module_name}_dialog_base.ui'))

class {class_name}Dialog(QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        super({class_name}Dialog, self).__init__(parent)
        self.setupUi(self)
"""
        with open(os.path.join(plugin_path, f'{module_name}_dialog.py'), 'w', encoding='utf-8') as f:
            f.write(dialog_py_content.strip())

        # --- {module_name}_dialog_base.ui (un archivo de interfaz básico) ---
        dialog_ui_content = """<ui version="4.0">
<class>Dialog</class>
<widget class="QDialog" name="Dialog"><property name="geometry"><rect><x>0</x><y>0</y><width>400</width><height>130</height></rect></property><property name="windowTitle"><string>Dialog</string></property><layout class="QVBoxLayout" name="verticalLayout"><item><widget class="QLabel" name="label"><property name="text"><string>¡Hola! Este es tu nuevo plugin.</string></property><property name="alignment"><set>Qt::AlignCenter</set></property></widget></item><item><widget class="QDialogButtonBox" name="buttonBox"><property name="orientation"><enum>Qt::Horizontal</enum></property><property name="standardButtons"><set>QDialogButtonBox::Cancel|QDialogButtonBox::Ok</set></property></widget></item></layout></widget>
<resources/>
<connections>
<connection><sender>buttonBox</sender><signal>accepted()</signal><receiver>Dialog</receiver><slot>accept()</slot></connection>
<connection><sender>buttonBox</sender><signal>rejected()</signal><receiver>Dialog</receiver><slot>reject()</slot></connection>
</connections>
</ui>"""
        with open(os.path.join(plugin_path, f'{module_name}_dialog_base.ui'), 'w', encoding='utf-8') as f:
            f.write(dialog_ui_content.strip())

        # --- resources.qrc ---
        resources_qrc_content = f"""
<RCC>
    <qresource prefix="/plugins/{module_name}">
        <file>icon.png</file>
    </qresource>
</RCC>
"""
        with open(os.path.join(plugin_path, 'resources.qrc'), 'w', encoding='utf-8') as f:
            f.write(resources_qrc_content.strip())
        
        # 4. Copiar el icono por defecto
        source_icon_path = os.path.join(self.plugin_dir, 'icon.png')
        dest_icon_path = os.path.join(plugin_path, 'icon.png')
        if os.path.exists(source_icon_path):
            shutil.copy(source_icon_path, dest_icon_path)
