
import os
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QDialog, QMessageBox

from c3d_parser.core.c3d_parser import ParserError
from c3d_parser.settings.general import get_marker_maps_dir
from c3d_parser.view.ui.ui_delete_marker_set_dialog import Ui_DeleteMarkerSetDialog


class DeleteMarkerSetDialog(QDialog):
    error_occurred = Signal(Exception)

    def __init__(self, parent=None):
        super(DeleteMarkerSetDialog, self).__init__(parent)
        self._ui = Ui_DeleteMarkerSetDialog()
        self._ui.setupUi(self)

        self._setup_combo_box()

        self._make_connections()

    def _make_connections(self):
        self._ui.pushButtonDelete.clicked.connect(self._delete_marker_set)

    def _setup_combo_box(self):
        marker_maps_dir = get_marker_maps_dir()
        labs = [os.path.splitext(lab)[0] for lab in os.listdir(marker_maps_dir)]
        self._ui.comboBoxMarkerSet.clear()
        self._ui.comboBoxMarkerSet.addItems(labs)

    def _delete_marker_set(self):
        marker_maps_dir = get_marker_maps_dir()
        selected = self._ui.comboBoxMarkerSet.currentText()

        reply = QMessageBox.question( self, "Confirm Deletion",
            "Are you sure you want to permanently delete this marker set?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.No:
            return

        match = next((f for f in os.listdir(marker_maps_dir) if os.path.splitext(f)[0] == selected), None)
        if match:
            file_path = os.path.join(marker_maps_dir, match)
            if os.path.isfile(file_path):
                try:
                    os.remove(file_path)
                    self._ui.comboBoxMarkerSet.removeItem(self._ui.comboBoxMarkerSet.currentIndex())
                except PermissionError:
                    e = ParserError(f"PermissionError: Could not delete marker set: {selected}")
                    self.error_occurred.emit(e)
