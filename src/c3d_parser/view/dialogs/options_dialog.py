
import os

from PySide6.QtWidgets import QDialog, QFileDialog
from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtCore import QRegularExpression

from c3d_parser.view.ui.ui_options_dialog import Ui_OptionsDialog
from c3d_parser.settings.general import DEFAULT_STYLE_SHEET, INVALID_STYLE_SHEET


class OptionsDialog(QDialog):

    def __init__(self, parent=None):
        super(OptionsDialog, self).__init__(parent)
        self._ui = Ui_OptionsDialog()
        self._ui.setupUi(self)

        self._colour_boxes = {
            self._ui.lineEditLeftColour: self._ui.labelLeftColour,
            self._ui.lineEditRightColour: self._ui.labelRightColour,
            self._ui.lineEditSelectionColour: self._ui.labelSelectionColour
        }

        self._setup_colour_settings()
        self._disable_default_button_selection()

        self._make_connections()

    def _make_connections(self):
        self._ui.lineEditRootInput.textChanged.connect(self._validate_data_directory)
        self._ui.lineEditRootOutput.textChanged.connect(self._validate_data_directory)
        self._ui.pushButtonRootInputChooser.clicked.connect(self._open_input_directory_chooser)
        self._ui.pushButtonRootOutputChooser.clicked.connect(self._open_output_directory_chooser)

    def _setup_colour_settings(self):
        self._validator = QRegularExpressionValidator(QRegularExpression("^#[0-9A-Fa-f]{6}$"))
        self._ui.lineEditLeftColour.setValidator(self._validator)
        self._ui.lineEditLeftColour.textChanged.connect(self._colour_code_changed)
        self._ui.lineEditRightColour.setValidator(self._validator)
        self._ui.lineEditRightColour.textChanged.connect(self._colour_code_changed)
        self._ui.lineEditSelectionColour.setValidator(self._validator)
        self._ui.lineEditSelectionColour.textChanged.connect(self._colour_code_changed)

    def _colour_code_changed(self, text):
        line_edit = self.sender()
        state, _, _ = self._validator.validate(text, 0)
        if state == QRegularExpressionValidator.State.Acceptable:
            line_edit.setStyleSheet(DEFAULT_STYLE_SHEET)
            colour_box = self._colour_boxes[line_edit]
            colour_box.setStyleSheet(f"border: 1px solid black;"
                f"border-radius: 2px; background-color: {text};")
        else:
            line_edit.setStyleSheet(INVALID_STYLE_SHEET)

    def _disable_default_button_selection(self):
        self._ui.pushButtonOK.setAutoDefault(False)
        self._ui.pushButtonCancel.setAutoDefault(False)
        self._ui.pushButtonRootInputChooser.setAutoDefault(False)
        self._ui.pushButtonRootOutputChooser.setAutoDefault(False)

    def load(self, options):
        self._ui.doubleSpinBoxLineWidth.setValue(options['line_width'])
        self._ui.lineEditRootInput.setText(options['input_data_directory'])
        self._ui.lineEditRootOutput.setText(options['output_data_directory'])
        self._ui.checkBoxOptimiseKneeAxis.setChecked(options['optimise_knee_axis'])
        self._ui.lineEditLeftColour.setText(options['colour_left'])
        self._ui.lineEditRightColour.setText(options['colour_right'])
        self._ui.lineEditSelectionColour.setText(options['colour_selection'])

    def save(self):
        options = {
            'line_width': self._ui.doubleSpinBoxLineWidth.value(),
            'input_data_directory': self._ui.lineEditRootInput.text(),
            'output_data_directory': self._ui.lineEditRootOutput.text(),
            'optimise_knee_axis': self._ui.checkBoxOptimiseKneeAxis.isChecked(),
            'colour_left': self._ui.lineEditLeftColour.text(),
            'colour_right': self._ui.lineEditRightColour.text(),
            'colour_selection': self._ui.lineEditSelectionColour.text()
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

        directory = QFileDialog.getExistingDirectory(
            self, 'Select Directory', current_directory)

        if directory:
            line_edit.setText(directory)
