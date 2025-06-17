# -*- coding: utf-8 -*-
import os
from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QDialog, QFileDialog

# Esto crea una ruta absoluta al archivo .ui
UI_FILE = os.path.join(os.path.dirname(__file__), 'ui/plugin_forge_dialog_base.ui')
# Carga el archivo .ui para crear la clase del diálogo
FORM_CLASS, _ = uic.loadUiType(UI_FILE)

class PluginForgeDialog(QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(PluginForgeDialog, self).__init__(parent)
        self.setupUi(self)

        # Cambiamos el texto del botón OK por algo más descriptivo
        self.button_box.button(self.button_box.Ok).setText("Generar Plugin")

        # Conectar señales a slots (métodos)
        self.btnSelectDir.clicked.connect(self.select_output_directory)

    def select_output_directory(self):
        """Abre un diálogo para seleccionar una carpeta de destino."""
        dir_path = QFileDialog.getExistingDirectory(self, "Seleccionar Carpeta de Salida", "")
        if dir_path:
            self.lineEditOutputDir.setText(dir_path)