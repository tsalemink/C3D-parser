
import os

from PySide6 import QtWidgets

from c3d_parser.settings.general import get_marker_maps_dir
from c3d_parser.view.ui.ui_marker_set_import_dialog import Ui_MarkerSetImportDialog


class MarkerSetImportDialog(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super(MarkerSetImportDialog, self).__init__(parent)
        self._ui = Ui_MarkerSetImportDialog()
        self._ui.setupUi(self)

        self.setup_combo_box()

    def setup_combo_box(self):
        marker_maps_dir = get_marker_maps_dir()
        labs = [os.path.splitext(lab)[0] for lab in os.listdir(marker_maps_dir)]
        self._ui.comboBoxMarkerSet.addItems(labs)

    def get_file_path(self):
        file_name = f"{self._ui.comboBoxMarkerSet.currentText()}.json"
        marker_maps_dir = get_marker_maps_dir()
        file_path = os.path.join(marker_maps_dir, file_name)

        return file_path
