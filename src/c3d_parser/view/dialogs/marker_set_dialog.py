
import os
import re
import json

from PySide6 import QtWidgets

from c3d_parser.core.c3d_parser import marker_maps_dir
from c3d_parser.view.dialogs.marker_set_import_dialog import MarkerSetImportDialog
from c3d_parser.settings.general import DEFAULT_STYLE_SHEET, INVALID_STYLE_SHEET
from c3d_parser.view.ui.ui_marker_set_dialog import Ui_MarkerSetDialog


markers = ["C7", "T2", "T10", "MAN", "SACR", "ASI", "PSI", "THI", "PAT",
           "KNE", "KNEM", "KAX", "TIB", "ANK", "MED", "HEE", "TOE"]


class MarkerSetDialog(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super(MarkerSetDialog, self).__init__(parent)
        self._ui = Ui_MarkerSetDialog()
        self._ui.setupUi(self)

        self._marker_mapping = {}

        self._make_connections()
        self._validate_name()

    def _make_connections(self):
        self._ui.lineEditName.textChanged.connect(self._validate_name)
        self._ui.pushButtonImport.clicked.connect(self._import_marker_map)
        self._ui.pushButtonSave.clicked.connect(self._validate_marker_set)

    def set_marker_names(self, marker_names):
        for marker in markers:
            combo_box = getattr(self._ui, f"comboBox{marker}")
            combo_box.addItem('')
            combo_box.addItems(marker_names)
            if marker in marker_names:
                index = combo_box.findText(marker)
                combo_box.setCurrentIndex(index)

    def save(self):
        file_name = f"{self._ui.lineEditName.text()}.json"
        file_path = os.path.join(marker_maps_dir, file_name)

        with open(file_path, 'w') as file:
            json.dump(self._marker_mapping, file, indent='\t')

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

    def _validate_name(self):
        name = self._ui.lineEditName.text()
        invalid = not name or re.search(r'[<>:"/\\|?*]', name)

        if invalid:
            self._ui.lineEditName.setStyleSheet(INVALID_STYLE_SHEET)
            self._ui.pushButtonSave.setEnabled(False)
        else:
            self._ui.lineEditName.setStyleSheet(DEFAULT_STYLE_SHEET)
            self._ui.pushButtonSave.setEnabled(True)

    def _validate_marker_set(self):
        file_name = f"{self._ui.lineEditName.text()}.json"
        file_path = os.path.join(marker_maps_dir, file_name)
        if os.path.exists(file_path):
            QtWidgets.QMessageBox.warning(self, "Warning", f"Marker Set ({file_name}) already exists.")
            return

        self._marker_mapping = {}
        for marker in markers:
            combo_box = getattr(self._ui, f"comboBox{marker}")
            value = combo_box.currentText()
            self._marker_mapping[marker] = value if value else None

        missing = []
        for marker in ["ASI", "KNE", "ANK", "MED", "HEE"]:
            if self._marker_mapping[marker] is None:
                missing.append(f"\"{marker}\"")

        if self._marker_mapping["PSI"] is None and self._marker_mapping["SACR"] is None:
            missing.append('either "PSI" or "SACR"')

        if self._marker_mapping["KNEM"] is None and self._marker_mapping["KAX"] is None:
            missing.append('either "KNEM" or "KAX"')

        if missing:
            QtWidgets.QMessageBox.warning(self, "Warning", "Marker set must define:\n- " + "\n- ".join(missing))
            return

        self.accept()
