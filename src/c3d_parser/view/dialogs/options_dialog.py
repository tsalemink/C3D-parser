
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
        self._ui.lineEditRootInput.textChanged.connect(self._validate_data_directory)
        self._ui.lineEditRootOutput.textChanged.connect(self._validate_data_directory)
        self._ui.pushButtonRootInputChooser.clicked.connect(self._open_input_directory_chooser)
        self._ui.pushButtonRootOutputChooser.clicked.connect(self._open_output_directory_chooser)

    def load(self, options):
        self._ui.doubleSpinBoxLineWidth.setValue(options['line_width'])
        self._ui.lineEditRootInput.setText(options['input_data_directory'])
        self._ui.lineEditRootOutput.setText(options['output_data_directory'])

    def save(self):
        options = {
            'line_width': self._ui.doubleSpinBoxLineWidth.value(),
            'input_data_directory': self._ui.lineEditRootInput.text(),
            'output_data_directory': self._ui.lineEditRootOutput.text()
        }

        return options

    def _validate_data_directory(self):
        line_edit = self.sender()
        directory = line_edit.text()
        directory_valid = len(directory) and os.path.isdir(directory)
        line_edit.setStyleSheet(DEFAULT_STYLE_SHEET if directory_valid else INVALID_STYLE_SHEET)

    def _open_input_directory_chooser(self):
        self._open_directory_chooser(self._ui.lineEditRootInput)

    def _open_output_directory_chooser(self):
        self._open_directory_chooser(self._ui.lineEditRootOutput)

    def _open_directory_chooser(self, line_edit):
        current_directory = line_edit.text()
        if not os.path.isdir(current_directory):
            current_directory = ''

        directory = QtWidgets.QFileDialog.getExistingDirectory(
            self, 'Select Directory', current_directory)

        if directory:
            line_edit.setText(directory)
