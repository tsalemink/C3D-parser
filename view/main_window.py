
import os

from PySide6.QtWidgets import QMainWindow, QFileDialog, QListWidgetItem

from view.ui.ui_main_window import Ui_MainWindow


DEFAULT_STYLE_SHEET = ''
INVALID_STYLE_SHEET = 'background-color: rgba(239, 0, 0, 50)'


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self._ui = Ui_MainWindow()
        self._ui.setupUi(self)

        self._previous_directory = ''

        self._make_connections()

    def _make_connections(self):
        self._ui.lineEditDirectory.textChanged.connect(self._validate_directory)
        self._ui.pushButtonDirectoryChooser.clicked.connect(self._open_directory_chooser)
        self._ui.pushButtonScanDirectory.clicked.connect(self._scan_directory)

    def _validate_directory(self):
        directory = self._ui.lineEditDirectory.text()
        directory_valid = len(directory) and os.path.isdir(directory)

        self._ui.pushButtonScanDirectory.setEnabled(directory_valid)
        self._ui.lineEditDirectory.setStyleSheet(
            DEFAULT_STYLE_SHEET if directory_valid else INVALID_STYLE_SHEET)

    def _open_directory_chooser(self):
        directory = QFileDialog.getExistingDirectory(
            self, 'Select Directory', self._previous_directory)

        if directory:
            self._previous_directory = directory
            self._ui.lineEditDirectory.setText(directory)

    def _scan_directory(self):
        directory = self._ui.lineEditDirectory.text()
        self._ui.listWidget_files.clear()
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.lower().endswith('.c3d'):
                    path = os.path.relpath(os.path.join(root, file), directory)
                    self._ui.listWidget_files.addItem(QListWidgetItem(path))
