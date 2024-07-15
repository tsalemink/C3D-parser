
import os

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QFileDialog, QListWidgetItem
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from c3d_parser.core.c3d_parser import parse_c3d, read_grf
from c3d_parser.view.ui.ui_main_window import Ui_MainWindow


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
        self._setup_grf_figures()
        self._setup_kinematic_figures()
        self._setup_kinetic_figures()

    def _setup_grf_figures(self):
        self._grf_canvas = FigureCanvasQTAgg(Figure())
        self._grf_canvas.figure.suptitle('GRF Data')
        self._plot_x = self._grf_canvas.figure.add_subplot(311)
        self._plot_y = self._grf_canvas.figure.add_subplot(312)
        self._plot_z = self._grf_canvas.figure.add_subplot(313)
        self._plot_x.tick_params(axis='x', which='both', labelbottom=False)
        self._plot_y.tick_params(axis='x', which='both', labelbottom=False)
        self._grf_canvas.figure.tight_layout(pad=0.0)
        self._label_axes()

        self._ui.layoutGRFPlot.addWidget(self._grf_canvas)

    def _setup_kinematic_figures(self):
        self._kinematic_canvas = FigureCanvasQTAgg(Figure())
        self._kinematic_plots = []
        for i in range(3):
            for j in range(5):
                plot = self._kinematic_canvas.figure.add_subplot(3, 5, i * 5 + j + 1)
                plot.tick_params(axis='x', which='both', labelbottom=False, bottom=False)
                plot.tick_params(axis='y', which='both', labelleft=False, left=False)
                plot.text(-0.07, 0.5, 'deg', ha='center', va='center', transform=plot.transAxes)
                plot.set_title(f'Plot Title', fontsize=10, pad=-10)
                self._kinematic_plots.append(plot)
        self._kinematic_canvas.figure.tight_layout(pad=0.0, rect=[0, 0.03, 0.98, 0.98], h_pad=0.4, w_pad=0.2)

        self._ui.layoutKinematicPlot.addWidget(self._kinematic_canvas)

    def _setup_kinetic_figures(self):
        self._kinetic_canvas = FigureCanvasQTAgg(Figure())
        self._kinetic_plots = []
        for i in range(3):
            for j in range(4):
                plot = self._kinetic_canvas.figure.add_subplot(3, 4, i * 4 + j + 1)
                plot.tick_params(axis='x', which='both', labelbottom=False, bottom=False)
                plot.tick_params(axis='y', which='both', labelleft=False, left=False)
                if j == 3:
                    plot.text(-0.04, 0.5, 'W', ha='center', va='center', transform=plot.transAxes)
                else:
                    plot.text(-0.05, 0.5, 'Nm', ha='center', va='center', transform=plot.transAxes)
                plot.set_title(f'Plot Title', fontsize=10, pad=-10)
                self._kinetic_plots.append(plot)
        self._kinetic_canvas.figure.tight_layout(pad=0.0, rect=[0, 0.03, 0.98, 0.98], h_pad=0.4, w_pad=0.2)

        self._ui.layoutKineticPlot.addWidget(self._kinetic_canvas)

    def _label_axes(self):
        self._plot_x.set_ylabel('X', rotation='horizontal', labelpad=10, horizontalalignment='right')
        self._plot_y.set_ylabel('Y', rotation='horizontal', labelpad=10, horizontalalignment='right')
        self._plot_z.set_ylabel('Z', rotation='horizontal', labelpad=10, horizontalalignment='right')

    def _make_connections(self):
        self._ui.lineEditDirectory.textChanged.connect(self._validate_directory)
        self._ui.pushButtonDirectoryChooser.clicked.connect(self._open_directory_chooser)
        self._ui.pushButtonScanDirectory.clicked.connect(self._scan_directory)
        self._ui.pushButtonParseData.clicked.connect(self._parse_c3d_data)
        self._ui.pushButtonUpload.clicked.connect(self._upload_data)
        self._ui.listWidgetFiles.itemSelectionChanged.connect(self._update_selected_trial)
        self._ui.comboBoxChannels.currentIndexChanged.connect(self._update_visualisation)

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
            if '_output' in dirs:
                dirs.remove('_output')
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
            self._update_visualisation()

    def _update_combo_box(self):
        self._ui.comboBoxChannels.clear()
        if self._analog_data is not None:
            self._ui.comboBoxChannels.addItems(
                ["Force", "Position", "Torque"]
            )

    def _update_visualisation(self):
        channels_index = self._ui.comboBoxChannels.currentIndex()
        start = channels_index * 3 + 1
        t = self._analog_data.iloc[:, 0].values

        def update_plot(plot, column):
            left, right = self._analog_data.iloc[:, [column, column + 9]].values.T
            plot.clear()
            plot.plot(t, left, color='red', label='Left Foot')
            plot.plot(t, right, color='blue', label='Right Foot')
            plot.legend()

        update_plot(self._plot_x, start)
        update_plot(self._plot_y, start + 1)
        update_plot(self._plot_z, start + 2)

        self._label_axes()
        self._grf_canvas.draw()
