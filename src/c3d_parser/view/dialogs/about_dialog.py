
import os
import importlib

from PySide6 import QtWidgets
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from c3d_parser import __version__
from c3d_parser.settings.general import APPLICATION_NAME


class AboutDialog(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About")
        self.setMinimumSize(400, 300)

        layout = QtWidgets.QVBoxLayout(self)

        heading = QtWidgets.QLabel(f"{APPLICATION_NAME} {__version__}")
        heading.setFont(QFont("", 14, QFont.Bold))
        heading.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        layout.addWidget(heading)

        # List important dependency versions.
        packages = [
            ("OpenSim", "opensim"),
            ("opensim-model-creator", "opensim-model-creator"),
            ("articulated-ssm", "articulated-ssm")
        ]

        table = QtWidgets.QTableWidget(0, 2)
        table.verticalHeader().setVisible(False)
        table.setHorizontalHeaderLabels(["Package", "Version"])
        table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        table.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        table.setFocusPolicy(Qt.NoFocus)
        table.setRowCount(len(packages))
        for row, (display_name, import_name) in enumerate(packages):
            name_item = QtWidgets.QTableWidgetItem(display_name)
            version_item = QtWidgets.QTableWidgetItem(self.get_version(import_name))
            table.setItem(row, 0, name_item)
            table.setItem(row, 1, version_item)
        table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        layout.addWidget(table)

    def get_version(self, module_name):
        try:
            return importlib.metadata.version(module_name)
        except importlib.metadata.PackageNotFoundError:
            try:
                mod = importlib.import_module(module_name)
                return getattr(mod, "__version__", "N/A")
            except ModuleNotFoundError:
                return "N/A"
