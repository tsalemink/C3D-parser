
import os
import json

from PySide6 import QtWidgets

from c3d_parser.core.c3d_parser import marker_maps_dir
from c3d_parser.view.dialogs.marker_set_import_dialog import MarkerSetImportDialog
from c3d_parser.view.ui.ui_marker_set_dialog import Ui_MarkerSetDialog


markers = ["C7", "T2", "T10", "MAN", "SACR", "ASI", "PSI", "THI", "PAT",
           "KNE", "KNEM", "KAX", "TIB", "ANK", "MED", "HEE", "TOE"]


class MarkerSetDialog(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super(MarkerSetDialog, self).__init__(parent)
        self._ui = Ui_MarkerSetDialog()
        self._ui.setupUi(self)

        self._make_connections()

    def _make_connections(self):
        self._ui.pushButtonImport.clicked.connect(self._import_marker_map)
        self._ui.pushButtonSave.clicked.connect(self._validate_marker_set)

    def save(self):
        file_name = f"{self._ui.lineEditName.text()}.json"
        file_path = os.path.join(marker_maps_dir, file_name)

        marker_mapping = {}
        for marker in markers:
            combo_box = getattr(self._ui, f"comboBox{marker}")
            value = combo_box.currentText()
            marker_mapping[marker] = value if value else None

        with open(file_path, 'w') as file:
            json.dump(marker_mapping, file, indent='\t')

    def load(self, file_path):
        with open(file_path, 'r') as file:
            marker_mapping = json.load(file)

        for key, value in marker_mapping.items():
            combo_box = getattr(self._ui, f"comboBox{key}")
            combo_box.setCurrentText(value)

    def _import_marker_map(self):
        dlg = MarkerSetImportDialog(self)
        if dlg.exec():
            self.load(dlg.get_file_path())

    def _validate_marker_set(self):
        file_name = f"{self._ui.lineEditName.text()}.json"
        file_path = os.path.join(marker_maps_dir, file_name)
        if os.path.exists(file_path):
            QtWidgets.QMessageBox.warning(self, "Warning", f"Marker Set ({file_name}) already exists.")
            return

        self.accept()
