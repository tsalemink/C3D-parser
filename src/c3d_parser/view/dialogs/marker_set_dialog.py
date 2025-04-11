
from PySide6 import QtWidgets

from c3d_parser.view.ui.ui_marker_set_dialog import Ui_MarkerSetDialog


class MarkerSetDialog(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super(MarkerSetDialog, self).__init__(parent)
        self._ui = Ui_MarkerSetDialog()
        self._ui.setupUi(self)

    # TODO: Implement.
    def save(self):
        pass
