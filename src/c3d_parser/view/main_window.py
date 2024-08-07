
import os
import numpy as np

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QFileDialog, QListWidgetItem
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from c3d_parser.core.c3d_parser import parse_c3d, read_grf, is_dynamic
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
        self._grf_data = {}
        self._kinematic_data = {}
        self._events = {}
        self._plot_lines = {}

        self._setup_figures()
        self._make_connections()

    def _setup_figures(self):
        self._setup_grf_figure()
        self._setup_torque_figure()
        self._setup_kinematic_figures()
        self._setup_kinetic_figures()

    def _setup_grf_figure(self):
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

    def _setup_torque_figure(self):
        self._torque_canvas = FigureCanvasQTAgg(Figure())
        self._torque_canvas.figure.suptitle('Torque Data')
        self._plot_torque = self._torque_canvas.figure.add_subplot(111)
        self._torque_canvas.figure.tight_layout(pad=0.0)

        self._ui.layoutTorquePlot.addWidget(self._torque_canvas)

    def _setup_kinematic_figures(self):
        self._kinematic_canvas = FigureCanvasQTAgg(Figure())
        self._kinematic_plots = []
        for i in range(3):
            for j in range(3):
                if i == 2 and j == 1:
                    break
                plot = self._kinematic_canvas.figure.add_subplot(3, 3, i * 3 + j + 1)
                plot.tick_params(axis='x', which='both', labelbottom=False, bottom=False)
                plot.tick_params(axis='y', which='both', labelleft=False, left=False)
                plot.text(-0.07, 0.5, 'deg', ha='center', va='center', transform=plot.transAxes)
                plot.set_title(f'Plot Title', fontsize=10, pad=-10)
                self._kinematic_plots.append(plot)
        self._kinematic_canvas.figure.tight_layout(pad=0.0, rect=[0, 0.03, 0.98, 0.98], h_pad=0.4, w_pad=0.2)

        self._ui.layoutKinematicPlot.addWidget(self._kinematic_canvas)

    def _setup_kinetic_figures(self):
        pass

    def _label_axes(self):
        self._plot_x.set_ylabel('X', rotation='horizontal', labelpad=10, horizontalalignment='right')
        self._plot_y.set_ylabel('Y', rotation='horizontal', labelpad=10, horizontalalignment='right')
        self._plot_z.set_ylabel('Z', rotation='horizontal', labelpad=10, horizontalalignment='right')

    def _make_connections(self):
        self._ui.lineEditDirectory.textChanged.connect(self._validate_directory)
        self._ui.listWidgetFiles.itemChanged.connect(self._update_plot_visibility)
        self._ui.pushButtonDirectoryChooser.clicked.connect(self._open_directory_chooser)
        self._ui.pushButtonScanDirectory.clicked.connect(self._scan_directory)
        self._ui.pushButtonParseData.clicked.connect(self._parse_c3d_data)
        self._ui.pushButtonUpload.clicked.connect(self._upload_data)

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
                    path = os.path.join(root, file)
                    category = "Dynamic" if is_dynamic(path) else "Static"
                    item = QListWidgetItem(os.path.relpath(path, directory))
                    item.setData(Qt.UserRole, category)
                    item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
                    item.setCheckState(Qt.CheckState.Checked)
                    self._ui.listWidgetFiles.addItem(item)

        self._ui.pushButtonParseData.setEnabled(True)

    def _parse_c3d_data(self):
        self._grf_data = {}
        self._kinematic_data = {}
        for i in range(self._ui.listWidgetFiles.count()):
            item = self._ui.listWidgetFiles.item(i)
            dynamic = item.data(Qt.UserRole) == "Dynamic"
            directory = self._ui.lineEditDirectory.text()
            file_path = os.path.join(directory, item.text())
            output_directory = os.path.join(directory, '_output')
            analog_data, ik_data, events = parse_c3d(file_path, output_directory, dynamic)
            if dynamic:
                self._grf_data[item.text()] = analog_data
                self._kinematic_data[item.text()] = ik_data
                self._events[item.text()] = events

        self._visualise_grf_data()
        self._visualise_torque_data()
        self._visualise_kinematic_data()

    def _upload_data(self):
        pass

    def _visualise_grf_data(self):
        t, grf_data = self._extract_data("grf")
        self._plot_grf_data(t, grf_data)

    def _visualise_torque_data(self):
        t, torque_data = self._extract_data("torque")
        self._plot_torque_data(t, torque_data)

    def _extract_data(self, data_type):
        normalised_data = {"Left": {}, "Right": {}}
        for i in range(len(self._grf_data)):
            file_name = list(self._grf_data.keys())[i]
            grf_data = list(self._grf_data.values())[i]
            grf_events = list(self._events.values())[i]

            for foot, events in grf_events.items():
                column = 1 if foot == "Left" and data_type == "grf" else \
                    13 if foot == "Left" else 7 if data_type == "grf" else 16
                force_data = grf_data.iloc[:, [0, *range(column, column + 3)]]

                start = None
                for event_time, (event_type, event_plate) in events.items():
                    if event_plate is None:
                        continue
                    frame = force_data[force_data['time'] <= event_time].index[-1]
                    if event_type == "Foot Strike":
                        while force_data.iloc[frame, 3] > 0:
                            frame -= 1
                        start = frame
                    elif event_type == "Foot Off" and start:
                        while force_data.iloc[frame, 3] > 0:
                            frame += 1
                        if file_name not in normalised_data[foot]:
                            normalised_data[foot][file_name] = []
                        normalised_data[foot][file_name].append(force_data.iloc[start:frame, 1:].values.T)
                        start = None

        max_length = max(array.shape[1] for arrays_dict in normalised_data.values()
                         for arrays in arrays_dict.values() for array in arrays)
        t = np.linspace(0, 100, max_length)

        return t, normalised_data

    def _plot_grf_data(self, time_array, grf_data):
        self._plot_x.clear()
        self._plot_y.clear()
        self._plot_z.clear()

        for foot, files_dict in grf_data.items():
            for i, (name, data_segments) in enumerate(files_dict.items()):
                colour = 'r' if foot == "Left" else 'b'
                for j, segment in enumerate(data_segments):
                    t_segment = time_array[:segment.shape[1]]
                    if foot == "Left":
                        segment[1] = -segment[1]

                    line_x, = self._plot_x.plot(t_segment, segment[0], color=colour, linewidth=1.0)
                    line_y, = self._plot_y.plot(t_segment, segment[1], color=colour, linewidth=1.0)
                    line_z, = self._plot_z.plot(t_segment, segment[2], color=colour, linewidth=1.0)

                    if name not in self._plot_lines:
                        self._plot_lines[name] = []
                    self._plot_lines[name].extend([line_x, line_y, line_z])

        self._label_axes()
        self._grf_canvas.draw()

    def _plot_torque_data(self, time_array, torque_data):
        self._plot_torque.clear()

        for foot, files_dict in torque_data.items():
            for name, data_segments in files_dict.items():
                colour = 'r' if foot == "Left" else 'b'
                for segment in data_segments:
                    t_segment = time_array[:segment.shape[1]]
                    line_torque, = self._plot_torque.plot(t_segment, segment[2], color=colour, linewidth=1.0)
                    self._plot_lines[name].extend([line_torque])

        self._torque_canvas.draw()

    def _visualise_kinematic_data(self):
        normalised_data = {"Left": {}, "Right": {}}
        for i in range(len(self._kinematic_data)):
            file_name = list(self._kinematic_data.keys())[i]
            kinematic_data = list(self._kinematic_data.values())[i]
            grf_events = list(self._events.values())[i]

            for foot, events in grf_events.items():
                columns = range(7, 11) if foot == "Left" else range(11, 15)
                data = kinematic_data.iloc[:, [0, 1, 2, 3] + list(columns)]

                start = None
                for event_time, event in events.items():
                    if event[0] == "Foot Strike" and start:
                        frame = data[data['time'] >= event_time].index[0]
                        if file_name not in normalised_data[foot]:
                            normalised_data[foot][file_name] = []
                        normalised_data[foot][file_name].append(data.iloc[start:frame, 1:].values.T)
                        start = None
                    elif event[0] == "Foot Strike":
                        start = data[data['time'] <= event_time].index[-1]

        max_length = max(array.shape[1] for arrays_dict in normalised_data.values()
                         for arrays in arrays_dict.values() for array in arrays)
        t = np.linspace(0, 100, max_length)

        self._plot_kinematic_data(t, normalised_data)

    # TODO: Add titles and axis labels. Format the plots.
    def _plot_kinematic_data(self, time_array, kinematic_data):
        for plot in self._kinematic_plots:
            plot.clear()

        for foot, files_dict in kinematic_data.items():
            for i, (name, data_segments) in enumerate(files_dict.items()):
                colour = 'r' if foot == "Left" else 'b'
                for segment in data_segments:
                    t_segment = np.linspace(0, 100, segment.shape[1])

                    if foot == "Right":
                        segment[0] = -(segment[0] - 180)
                    elif foot == "Left":
                        segment[1] = -segment[1]
                        segment[3] = -segment[3]
                        segment[4] = -segment[4]

                    plot_indices = [2, 0, 1, 5, 3, 4, 6]
                    for i, index in enumerate(plot_indices):
                        line, = self._kinematic_plots[i].plot(t_segment, segment[index], color=colour, linewidth=1.0)
                        self._plot_lines[name].append(line)

        self._kinematic_canvas.draw()

    def _update_plot_visibility(self, item):
        lines = self._plot_lines.get(item.text(), [])
        visible = item.checkState() == Qt.CheckState.Checked
        for line in lines:
            line.set_visible(visible)
        self._grf_canvas.draw()
        self._torque_canvas.draw()
        self._kinematic_canvas.draw()
