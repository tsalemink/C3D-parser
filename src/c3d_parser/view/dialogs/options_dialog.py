
import os

from PySide6 import QtWidgets

from c3d_parser.view.ui.ui_options_dialog import Ui_OptionsDialog
from c3d_parser.settings.general import DEFAULT_STYLE_SHEET, INVALID_STYLE_SHEET


class OptionsDialog(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super(OptionsDialog, self).__init__(parent)
        self._ui = Ui_OptionsDialog()
        self._ui.setupUi(self)

        self._make_connections()

    def _make_connections(self):
        self._ui.lineEditDataDirectory.textChanged.connect(self._validate_data_directory)
        self._ui.pushButtonDataDirectoryChooser.clicked.connect(self._open_directory_chooser)

    def load(self, options):
        self._ui.doubleSpinBoxLineWidth.setValue(options['line_width'])
        self._ui.lineEditDataDirectory.setText(options['data_directory'])

    def save(self):
        options = {
            'line_width': self._ui.doubleSpinBoxLineWidth.value(),
            'data_directory': self._ui.lineEditDataDirectory.text()
        }

        return options

    def _validate_data_directory(self):
        directory = self._ui.lineEditDataDirectory.text()
        directory_valid = len(directory) and os.path.isdir(directory)
        self._ui.lineEditDataDirectory.setStyleSheet(DEFAULT_STYLE_SHEET if directory_valid else INVALID_STYLE_SHEET)

    def _open_directory_chooser(self):
        current_directory = self._ui.lineEditDataDirectory.text()
        if not os.path.isdir(current_directory):
            current_directory = ''

        directory = QtWidgets.QFileDialog.getExistingDirectory(
            self, 'Select Directory', current_directory)

        if directory:
            self._ui.lineEditDataDirectory.setText(directory)
