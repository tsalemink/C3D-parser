
from PySide6 import QtWidgets

from c3d_parser.view.ui.ui_options_dialog import Ui_OptionsDialog


class OptionsDialog(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super(OptionsDialog, self).__init__(parent)
        self._ui = Ui_OptionsDialog()
        self._ui.setupUi(self)

    def load(self, options):
        self._ui.doubleSpinBoxLineWidth.setValue(options['line_width'])

    def save(self):
        options = {
            'line_width': self._ui.doubleSpinBoxLineWidth.value()
        }

        return options
