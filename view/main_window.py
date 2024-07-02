
import os

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QFileDialog, QListWidgetItem
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from c3d_parser import parse_c3d, read_grf
from view.ui.ui_main_window import Ui_MainWindow


DEFAULT_STYLE_SHEET = ''
INVALID_STYLE_SHEET = 'background-color: rgba(239, 0, 0, 50)'


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self._ui = Ui_MainWindow()
        self._ui.setupUi(self)

        self._previous_directory = ''
        self._analog_data = None

        self._setup_figures()
        self._make_connections()

    def _setup_figures(self):
        figure_left = Figure(figsize=(5, 3))
        figure_left.suptitle('Left Foot')
        self._canvas_left = FigureCanvasQTAgg(figure_left)
        self._ui.verticalLayoutPlot.addWidget(self._canvas_left)
        self._plot_left = figure_left.add_subplot(111)
        figure_left.tight_layout(pad=0.0)

        figure_right = Figure(figsize=(5, 3))
        figure_right.suptitle('Right Foot')
        self._canvas_right = FigureCanvasQTAgg(figure_right)
        self._ui.verticalLayoutPlot.addWidget(self._canvas_right)
        self._plot_right = figure_right.add_subplot(111)
        figure_right.tight_layout(pad=0.0)

    def _make_connections(self):
        self._ui.lineEditDirectory.textChanged.connect(self._validate_directory)
        self._ui.pushButtonDirectoryChooser.clicked.connect(self._open_directory_chooser)
        self._ui.pushButtonScanDirectory.clicked.connect(self._scan_directory)
        self._ui.pushButtonParseData.clicked.connect(self._parse_c3d_data)
        self._ui.pushButtonUpload.clicked.connect(self._upload_data)
        self._ui.listWidgetFiles.itemSelectionChanged.connect(self._update_selected_trial)
        self._ui.comboBoxChannels.currentIndexChanged.connect(self._update_plot)

    def _validate_directory(self):
        directory = self._ui.lineEditDirectory.text()
        directory_valid = len(directory) and os.path.isdir(directory)

        self._ui.listWidgetFiles.clear()
        self._ui.pushButtonParseData.setEnabled(False)
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
        self._ui.listWidgetFiles.clear()
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.lower().endswith('.c3d'):
                    path = os.path.relpath(os.path.join(root, file), directory)
                    item = QListWidgetItem(path)
                    item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
                    item.setCheckState(Qt.CheckState.Checked)
                    self._ui.listWidgetFiles.addItem(item)

        self._ui.pushButtonParseData.setEnabled(True)

    def _parse_c3d_data(self):
        for i in range(self._ui.listWidgetFiles.count()):
            item = self._ui.listWidgetFiles.item(i)
            if item.checkState() == Qt.CheckState.Unchecked:
                continue

            directory = self._ui.lineEditDirectory.text()
            file_path = os.path.join(directory, item.text())
            output_directory = os.path.join(directory, '_output')
            parse_c3d(file_path, output_directory)

    def _upload_data(self):
        pass

    def _update_selected_trial(self):
        selected_item = self._ui.listWidgetFiles.currentItem()
        if selected_item is not None:
            directory = self._ui.lineEditDirectory.text()
            grf_directory = os.path.join(directory, '_output', 'grf')
            name = os.path.splitext(os.path.basename(selected_item.text()))[0]
            file_path = os.path.join(grf_directory, name + '_grf.mot')

            if os.path.isfile(file_path):
                self._analog_data = read_grf(file_path)
            else:
                self._analog_data = None
            self._update_combo_box()
            self._update_plot()

    def _update_combo_box(self):
        self._ui.comboBoxChannels.clear()
        if self._analog_data is not None:
            self._ui.comboBoxChannels.addItems(
                ["Force", "Position", "Torque"]
            )

    def _update_plot(self):
        channels_index = self._ui.comboBoxChannels.currentIndex()
        start = channels_index * 3 + 1
        columns_left = range(start, start + 3)
        columns_right = range(start + 9, start + 12)
        t = self._analog_data.iloc[:, 0].values

        self._plot_left.clear()
        x, y, z = self._analog_data.iloc[:, columns_left].values.T
        self._plot_left.plot(t, x, color='red', label='x')
        self._plot_left.plot(t, y, color='green', label='y')
        self._plot_left.plot(t, z, color='blue', label='z')
        self._plot_left.set_xlim([t[0], t[-1]])
        self._plot_left.legend()
        self._canvas_left.draw()

        self._plot_right.clear()
        x, y, z = self._analog_data.iloc[:, columns_right].values.T
        self._plot_right.plot(t, x, color='red', label='x')
        self._plot_right.plot(t, y, color='green', label='y')
        self._plot_right.plot(t, z, color='blue', label='z')
        self._plot_right.set_xlim([t[0], t[-1]])
        self._plot_right.legend()
        self._canvas_right.draw()
