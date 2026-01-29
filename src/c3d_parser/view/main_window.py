
import os
import mplcursors
import numpy as np
import pandas as pd
from collections import defaultdict

from PySide6.QtGui import QPen, QColor, QFontMetrics
from PySide6.QtCore import Qt, QSettings, QPoint, QThread, Signal, QObject, QTimer, QAbstractTableModel, QRect
from PySide6.QtWidgets import (QApplication, QMainWindow, QMenu, QFileDialog, QListWidgetItem, QInputDialog,
                               QMessageBox, QTableView, QLabel, QAbstractButton, QHeaderView, QStyledItemDelegate,
                               QWidget, QVBoxLayout, QHBoxLayout)
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from c3d_parser.core.c3d_parser import (parse_session, extract_static_data, extract_marker_names, is_dynamic,
    CancelException, write_normalised_kinematics, write_normalised_kinetics, write_spatiotemporal_data)
from c3d_parser.settings.general import (APPLICATION_NAME, VERSION, DEFAULT_STYLE_SHEET, INVALID_STYLE_SHEET,
                                         get_marker_maps_dir)
from c3d_parser.view.ui.ui_main_window import Ui_MainWindow
from c3d_parser.view.dialogs.options_dialog import OptionsDialog
from c3d_parser.view.dialogs.marker_set_dialog import MarkerSetDialog
from c3d_parser.view.dialogs.about_dialog import AboutDialog
from c3d_parser.view.utils import handle_runtime_error
from c3d_parser.settings.logging import logger


output_direcory_name = 'c3d_parser_output'


class _ExecThread(QThread):
    finished = Signal(tuple)
    cancelled = Signal(Exception)
    failed = Signal(Exception)

    def __init__(self, func, *args, **kwargs):
        super().__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def run(self):
        try:
            output = self.func(*self.args, **self.kwargs)
            self.finished.emit(output)
        except CancelException as e:
            self.cancelled.emit(e)
        except Exception as e:
            self.failed.emit(e)


class ProgressTracker(QObject):
    progress = Signal(str, str)


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self._ui = Ui_MainWindow()
        self._ui.setupUi(self)

        self.setWindowTitle(f"{APPLICATION_NAME} {VERSION}")

        # Initialise user settings.
        self._line_width = 1.0
        self._input_data_directory = ''
        self._output_data_directory = ''
        self._optimise_knee_axis = True

        self._static_trial = None
        self._analog_data = None
        self._subject_weight = None
        self._kinematic_data = {}
        self._kinetic_data = {}
        self._s_t_data = {}
        self._deidentified_file_names = {}
        self._events = {}

        self._disable_spin_box_scrolling()
        self._setup_combo_boxes()
        self._setup_figures()
        self._setup_spatiotemporal_display()
        self._make_connections()
        self._load_settings()
        self._setup_progress_bar()
        self._validate_directory()

        self._grf_curves = GaitCurves(self._grf_canvas)
        self._kinematic_curves = GaitCurves(self._kinematic_canvas)
        self._kinetic_curves = GaitCurves(self._kinetic_canvas)

    def _setup_progress_bar(self):
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._animate_progress_bar)
        self._progress_text = ""
        self._dots = 0

    def _setup_combo_boxes(self):
        self._reset_lab_combo_box()

        # Force Qt to use placeholder text until sex selected.
        self._ui.comboBoxSex.setCurrentIndex(-1)

        self._ui.comboBoxLab.wheelEvent = lambda event: None
        self._ui.comboBoxSex.wheelEvent = lambda event: None

    def _disable_spin_box_scrolling(self):
        self._ui.spinBoxAge.wheelEvent = lambda event: None
        self._ui.doubleSpinBoxHeight.wheelEvent = lambda event: None
        self._ui.doubleSpinBoxBodyMass.wheelEvent = lambda event: None
        self._ui.doubleSpinBoxASISWidth.wheelEvent = lambda event: None
        self._ui.doubleSpinBoxLeftKneeWidth.wheelEvent = lambda event: None
        self._ui.doubleSpinBoxRightKneeWidth.wheelEvent = lambda event: None
        self._ui.doubleSpinBoxLeftAnkleWidth.wheelEvent = lambda event: None
        self._ui.doubleSpinBoxRightAnkleWidth.wheelEvent = lambda event: None
        self._ui.doubleSpinBoxLeftLegLength.wheelEvent = lambda event: None
        self._ui.doubleSpinBoxRightLegLength.wheelEvent = lambda event: None
        self._ui.doubleSpinBoxMarkerDiameter.wheelEvent = lambda event: None

    def _reset_lab_combo_box(self):
        current_selection = self._ui.comboBoxLab.currentText()
        marker_maps_dir = get_marker_maps_dir()
        labs = [os.path.splitext(lab)[0] for lab in os.listdir(marker_maps_dir)]
        self._ui.comboBoxLab.clear()
        self._ui.comboBoxLab.addItems(labs)

        if current_selection in labs:
            index = labs.index(current_selection)
            self._ui.comboBoxLab.setCurrentIndex(index)

    def _setup_figures(self):
        self._setup_grf_figure()
        self._setup_kinematic_figures()
        self._setup_kinetic_figures()

    def _setup_grf_figure(self):
        self._grf_canvas = FigureCanvasQTAgg(Figure())
        self._plot_x = self._grf_canvas.figure.add_subplot(311)
        self._plot_y = self._grf_canvas.figure.add_subplot(312)
        self._plot_z = self._grf_canvas.figure.add_subplot(313)
        self._plot_x.tick_params(axis='x', which='both', labelbottom=False, bottom=False)
        self._plot_y.tick_params(axis='x', which='both', labelbottom=False, bottom=False)
        self._plot_z.tick_params(axis='x', which='both', labelbottom=False, bottom=False)
        self._plot_x.tick_params(axis='y', which='both', labelleft=False, left=False)
        self._plot_y.tick_params(axis='y', which='both', labelleft=False, left=False)
        self._plot_z.tick_params(axis='y', which='both', labelleft=False, left=False)
        self._grf_canvas.figure.tight_layout(pad=0.0, rect=(0.04, 0.06, 0.98, 0.96), h_pad=2.0, w_pad=0.2)
        self._update_grf_axes()

        self._ui.layoutGRFPlot.addWidget(self._grf_canvas)

    def _setup_kinematic_figures(self):
        self._kinematic_canvas = FigureCanvasQTAgg(Figure())
        self._kinematic_plots = []
        for i in range(4):
            for j in range(1 if i == 2 else 3):
                plot = self._kinematic_canvas.figure.add_subplot(4, 3, i * 3 + j + 1)
                plot.tick_params(axis='x', which='both', labelbottom=False, bottom=False)
                plot.tick_params(axis='y', which='both', labelleft=False, left=False)
                self._kinematic_plots.append(plot)
        self._kinematic_canvas.figure.tight_layout(pad=0.0, rect=(0.04, 0.06, 0.98, 0.96), h_pad=2.0, w_pad=2.0)
        self._update_kinematic_axes()

        self._ui.layoutKinematicPlot.addWidget(self._kinematic_canvas)

    def _setup_kinetic_figures(self):
        self._kinetic_canvas = FigureCanvasQTAgg(Figure())
        self._kinetic_plots = []
        for i in range(4):
            for j in range(2 if i == 2 else 3):
                index = i * 3 + j + 1
                plot = self._kinetic_canvas.figure.add_subplot(4, 3, index)
                plot.tick_params(axis='x', which='both', labelbottom=False, bottom=False)
                plot.tick_params(axis='y', which='both', labelleft=False, left=False)
                self._kinetic_plots.append(plot)
        self._kinetic_canvas.figure.tight_layout(pad=0.0, rect=(0.04, 0.06, 0.98, 0.96), h_pad=2.0, w_pad=2.0)
        self._update_kinetic_axes()

        self._ui.layoutKineticPlot.addWidget(self._kinetic_canvas)

    def _setup_spatiotemporal_display(self):
        self._spatiotemporal_tables = []

    def _clear_spatiotemporal_data(self):
        layout = self._ui.scrollAreaSpatiotemporal.layout()

        for table in self._spatiotemporal_tables:
            layout.removeWidget(table)
            table.deleteLater()
        self._spatiotemporal_tables = []

    def _visualise_spatiotemporal_data(self):
        layout = self._ui.scrollAreaSpatiotemporal.layout()
        self._clear_spatiotemporal_data()

        # Create spatio-temporal tables.
        for trial, df in self._s_t_data.items():
            df_renamed = df.rename(index=lambda idx: f"{idx}").round(3)
            table = CustomTableView(trial)
            model = SpatiotemporalModel(df_renamed.T)
            table.setModel(model)

            layout.addWidget(table)
            self._spatiotemporal_tables.append(table)

        # Create legend.
        legend = QWidget(self._ui.tabSpatiotemporal)
        legend.setStyleSheet("border: 1px solid gray;")
        layout = QVBoxLayout(legend)
        layout.setContentsMargins(6, 6, 6, 6)
        layout.setSpacing(6)
        legend.resize(100, 50)

        for color, text in [("firebrick", "Left"), ("cornflowerblue", "Right")]:
            row_layout = QHBoxLayout()
            box = QLabel()
            box.setFixedSize(15, 15)
            box.setStyleSheet(f"background-color: {color}; border: 1px solid black;")
            label = QLabel(text)
            label.setStyleSheet("border: none;")
            row_layout.addWidget(box)
            row_layout.addWidget(label)
            layout.addLayout(row_layout)

        def reposition():
            legend.move(self._ui.tabSpatiotemporal.width() - legend.width() - 10, 10)
            legend.raise_()

        self._ui.tabSpatiotemporal.resizeEvent = lambda e: reposition()
        reposition()

    def _update_s_t_data_from_tables(self):
        for table in self._spatiotemporal_tables:
            trial_name = table.get_trial_name()
            df = table.model().get_data().copy()
            excluded = table.model().get_excluded_cycles()
            if excluded:
                df = df.drop(df.columns[list(excluded)], axis=1)
            self._s_t_data[trial_name] = df.T

    def _update_grf_axes(self):
        self._plot_x.set_title(f'GRF (Anterior - Posterior)', fontsize=10, pad=6)
        self._plot_y.set_title(f'GRF (Medial - Lateral)', fontsize=10, pad=6)
        self._plot_z.set_title(f'GRF (Vertical)', fontsize=10, pad=6)

        for plot in [self._plot_x, self._plot_y, self._plot_z]:
            y_min, y_max = plot.get_ylim()
            plot.set_ylim(np.floor(y_min / 10) * 10, np.ceil(y_max / 10) * 10)
            y_min, y_max = plot.get_ylim()
            step = (y_max - y_min) / 4

            plot.axhline(y=0, color='gray', linewidth=1.0, zorder=1)
            plot.text(x=0, y=y_min, s=f"{int(y_min)}", ha='right', va='center', fontsize=9)
            plot.text(x=0, y=(y_min + 2 * step), s="N", ha='right', va='center', fontsize=9)
            plot.text(x=0, y=y_max, s=f"{int(y_max)}", ha='right', va='center', fontsize=9)

            plot.set_xticks([0, 20, 40, 60, 80, 100])
            plot.tick_params(axis='x', which='both', bottom=True, labelbottom=False)

        self._plot_z.set_xticklabels(['0%', '20%', '40%', '60%', '80%', '100%'], fontsize=9)
        self._plot_z.tick_params(axis='x', labelbottom=True)
        self._plot_z.set_xlabel("Gait Cycle (%)", fontsize=9)

    def _make_connections(self):
        self._ui.lineEditInputDirectory.textChanged.connect(self._validate_input_directory)
        self._ui.lineEditOutputDirectory.textChanged.connect(self._validate_directory)
        self._ui.listWidgetFiles.itemChanged.connect(self._update_plot_visibility)
        self._ui.pushButtonInputDirectoryChooser.clicked.connect(self._open_input_directory_chooser)
        self._ui.pushButtonOutputDirectoryChooser.clicked.connect(self._open_output_directory_chooser)
        self._ui.pushButtonParseData.clicked.connect(self._parse_c3d_data)
        self._ui.pushButtonHarmonise.clicked.connect(self._harmonise_data)
        self._ui.actionQuit.triggered.connect(self._quit_application)
        self._ui.actionReloadInput.triggered.connect(self._validate_input_directory)
        self._ui.actionOptions.triggered.connect(self._show_options_dialog)
        self._ui.actionCustomMarkerSet.triggered.connect(self._show_marker_set_dialog)
        self._ui.actionAbout.triggered.connect(self._show_about_dialog)

        self._ui.listWidgetFiles.include_trial.connect(self._include_trial)
        self._ui.listWidgetFiles.exclude_trial.connect(self._exclude_trial)
        self._ui.listWidgetFiles.include_kinetics.connect(self._include_kinetics)
        self._ui.listWidgetFiles.exclude_kinetics.connect(self._exclude_kinetics)
        self._ui.listWidgetFiles.include_left.connect(self._include_left)
        self._ui.listWidgetFiles.exclude_left.connect(self._exclude_left)
        self._ui.listWidgetFiles.include_right.connect(self._include_right)
        self._ui.listWidgetFiles.exclude_right.connect(self._exclude_right)
        self._ui.listWidgetFiles.category_changed.connect(self._update_subject_info)

    def _validate_input_directory(self):
        directory_valid = self._validate_directory()

        self._ui.listWidgetFiles.clear()
        if directory_valid:
            self._scan_directory()

            self._reset_grf_plots()
            self._reset_kinematic_plots()
            self._reset_kinetic_plots()
            self._clear_spatiotemporal_data()

    def _validate_directory(self):
        input_directory = self._ui.lineEditInputDirectory.text()
        input_directory_valid = len(input_directory) and os.path.isdir(input_directory)
        self._ui.lineEditInputDirectory.setStyleSheet(DEFAULT_STYLE_SHEET if input_directory_valid else INVALID_STYLE_SHEET)

        output_directory = self._ui.lineEditOutputDirectory.text()
        output_directory_valid = len(output_directory) and os.path.isdir(output_directory)
        self._ui.lineEditOutputDirectory.setStyleSheet(DEFAULT_STYLE_SHEET if output_directory_valid else INVALID_STYLE_SHEET)

        self._ui.pushButtonParseData.setEnabled(input_directory_valid and output_directory_valid)
        self._ui.pushButtonHarmonise.setEnabled(False)

        return input_directory_valid

    def _open_input_directory_chooser(self):
        line_edits = [self._ui.lineEditInputDirectory, self._ui.lineEditOutputDirectory]
        self._open_directory_chooser(line_edits, self._input_data_directory)

    def _open_output_directory_chooser(self):
        line_edits = [self._ui.lineEditOutputDirectory]
        self._open_directory_chooser(line_edits, self._output_data_directory)

    def _open_directory_chooser(self, line_edits, data_directory):
        directory = QFileDialog.getExistingDirectory(
            self, 'Select Directory', data_directory)

        if directory:
            for line_edit in line_edits:
                line_edit.setText(directory)

    def _scan_directory(self):
        self._clear_subject_info()

        directory = self._ui.lineEditInputDirectory.text()
        self._ui.listWidgetFiles.clear()
        self._static_trial = None
        for root, dirs, files in os.walk(directory):
            if output_direcory_name in dirs:
                dirs.remove(output_direcory_name)
            for file in files:
                if file.lower().endswith('.c3d'):
                    path = os.path.join(root, file)
                    category = "Dynamic" if is_dynamic(path) else "Static"
                    item = QListWidgetItem(os.path.relpath(path, directory))
                    item.setData(Qt.ItemDataRole.UserRole, category)
                    item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
                    item.setCheckState(Qt.CheckState.Checked)
                    self._ui.listWidgetFiles.addItem(item)

        self._update_subject_info()

    def _update_subject_info(self):
        static_trials = []
        for i in range(self._ui.listWidgetFiles.count()):
            item = self._ui.listWidgetFiles.item(i)
            if item.data(Qt.ItemDataRole.UserRole) == "Static":
                static_trials.append(item.text())

        if static_trials:
            static_trial = static_trials[0]
            if static_trial != self._static_trial:
                self._set_subject_info(static_trial)
                self._static_trial = static_trial

    def _clear_subject_info(self):
        self._ui.comboBoxSex.setCurrentIndex(-1)
        self._ui.spinBoxAge.setValue(0)
        self._ui.doubleSpinBoxHeight.setValue(0)
        self._ui.doubleSpinBoxBodyMass.setValue(0)
        self._ui.doubleSpinBoxASISWidth.setValue(0)
        self._ui.doubleSpinBoxLeftKneeWidth.setValue(0)
        self._ui.doubleSpinBoxRightKneeWidth.setValue(0)
        self._ui.doubleSpinBoxLeftAnkleWidth.setValue(0)
        self._ui.doubleSpinBoxRightAnkleWidth.setValue(0)
        self._ui.doubleSpinBoxLeftLegLength.setValue(0)
        self._ui.doubleSpinBoxRightLegLength.setValue(0)

    def _set_subject_info(self, static_trial):
        input_directory = self._ui.lineEditInputDirectory.text()
        c3d_file = os.path.join(input_directory, static_trial)
        static_data = list(extract_static_data(c3d_file))

        if static_data[0] is not None:
            self._ui.doubleSpinBoxHeight.setValue(static_data[0])
        if static_data[1] is not None:
            self._ui.doubleSpinBoxBodyMass.setValue(static_data[1])
        if static_data[2] is not None:
            self._ui.doubleSpinBoxASISWidth.setValue(static_data[2])
        if static_data[3] is not None:
            self._ui.doubleSpinBoxLeftKneeWidth.setValue(static_data[3])
        if static_data[4] is not None:
            self._ui.doubleSpinBoxRightKneeWidth.setValue(static_data[4])
        if static_data[5] is not None:
            self._ui.doubleSpinBoxLeftAnkleWidth.setValue(static_data[5])
        if static_data[6] is not None:
            self._ui.doubleSpinBoxRightAnkleWidth.setValue(static_data[6])
        if static_data[7] is not None:
            self._ui.doubleSpinBoxLeftLegLength.setValue(static_data[7])
        if static_data[8] is not None:
            self._ui.doubleSpinBoxRightLegLength.setValue(static_data[8])

    @handle_runtime_error
    def _parse_c3d_data(self):
        input_directory = self._ui.lineEditInputDirectory.text()
        output_directory = self._ui.lineEditOutputDirectory.text()
        session_name = os.path.basename(input_directory)
        self._output_directory = os.path.join(output_directory, output_direcory_name)

        if os.path.exists(self._output_directory):
            reply = QMessageBox.warning(self, "Warning",
                                        "The selected output directory already contains results. "
                                        "Do you wish to overwrite these files?",
                                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                        QMessageBox.StandardButton.No)
            if reply != QMessageBox.StandardButton.Yes:
                return

        static_trials = []
        dynamic_trials = []
        for i in range(self._ui.listWidgetFiles.count()):
            item = self._ui.listWidgetFiles.item(i)
            if item.checkState() == Qt.CheckState.Checked:
                if item.data(Qt.ItemDataRole.UserRole) == "Dynamic":
                    dynamic_trials.append(item.text())
                else:
                    static_trials.append(item.text())
            else:
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEnabled)
                item.setData(Qt.ItemDataRole.UserRole, "")

        if len(static_trials) == 0:
            logger.error("No static trial found. You may need to classify one manually.")
            return
        elif len(static_trials) == 1:
            static_trial = static_trials[0]
        else:
            static_trial, ok = QInputDialog.getItem(None, "Select Static Trial", "Please select one static trial:", static_trials, 0, False)
            if not ok:
                return

        lab = self._ui.comboBoxLab.currentText()
        marker_diameter = self._ui.doubleSpinBoxMarkerDiameter.value()

        static_data = {
            "Sex": self._ui.comboBoxSex.currentText(),
            "Age": self._ui.spinBoxAge.value(),
            'Height': self._ui.doubleSpinBoxHeight.value(),
            'Weight': self._ui.doubleSpinBoxBodyMass.value(),
            'ASIS Width': self._ui.doubleSpinBoxASISWidth.value(),
            'Left Knee Width': self._ui.doubleSpinBoxLeftKneeWidth.value(),
            'Right Knee Width': self._ui.doubleSpinBoxRightKneeWidth.value(),
            'Left Ankle Width': self._ui.doubleSpinBoxLeftAnkleWidth.value(),
            'Right Ankle Width': self._ui.doubleSpinBoxRightAnkleWidth.value(),
            'Left Leg Length': self._ui.doubleSpinBoxLeftLegLength.value(),
            'Right Leg Length': self._ui.doubleSpinBoxRightLegLength.value(),
        }

        missing = [key for key, value in static_data.items() if not value]
        if 'Left Leg Length' in missing or 'Right Leg Length' in missing:
            reply = QMessageBox.warning(self, "Warning", "Leg length measurements missing. You can continue "
                        "without these values but will be unable to calculate the following spatio-temporal results:"
                        "\n- Normalised Stride Length\n- Normalised Step Length\n- Normalised Gait Speed",
                        QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel,
                        QMessageBox.StandardButton.Ok)
            if reply == QMessageBox.StandardButton.Cancel:
                return
            missing = [key for key in missing if key not in ('Left Leg Length', 'Right Leg Length')]
        if missing:
            QMessageBox.warning(self, "Warning", "Subject measurements missing:\n- " + "\n- ".join(missing))
            return

        if static_data['Height'] < 300:
            QMessageBox.warning(self, "Warning", "Please ensure subject height is in mm.")
            return

        optimise_knee_axis = self._optimise_knee_axis
        if not dynamic_trials:
            reply = QMessageBox.information(self, "No Dynamic Trials",
                                    "No dynamic trials identified in input directory. Do you still want to "
                                    "create the model? (knee-axis optimisation will be unavailable)",
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                    QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                optimise_knee_axis = False
            else:
                return

        self._ui.pushButtonParseData.setEnabled(False)

        self._progress_tracker = ProgressTracker()
        self._progress_tracker.progress.connect(self._update_progress)
        self._start_progress_animation()

        self._worker = _ExecThread(parse_session, static_trial, dynamic_trials, input_directory,
                                   self._output_directory, lab, marker_diameter, static_data,
                                   optimise_knee_axis, self._progress_tracker)
        self._worker.finished.connect(self._parse_finished)
        self._worker.cancelled.connect(self._parse_cancelled)
        self._worker.failed.connect(self._parse_failed)
        self._worker.start()

    @handle_runtime_error
    def _parse_finished(self, result):
        grf_data, self._kinematic_data, self._kinetic_data, self._s_t_data, self._deidentified_file_names = result

        self._visualise_grf_data(grf_data)
        self._visualise_kinematic_data(self._kinematic_data)
        self._visualise_kinetic_data(self._kinetic_data)
        self._visualise_spatiotemporal_data()

        self._show_selected_trials()
        self._stop_progress_animation()
        self._progress_tracker.progress.emit("Process completed successfully", "green")

        self._ui.pushButtonParseData.setEnabled(True)
        self._ui.pushButtonHarmonise.setEnabled(True)

    def _parse_cancelled(self, e):
        logger.info(e)

        self._stop_progress_animation()
        self._progress_tracker.progress.emit("Completed", "green")

        self._ui.pushButtonParseData.setEnabled(True)

    @handle_runtime_error
    def _parse_failed(self, e):
        self._ui.pushButtonParseData.setEnabled(True)

        raise e

    def _start_progress_animation(self):
        self._timer.start(500)

    def _stop_progress_animation(self):
        self._timer.stop()

    def _animate_progress_bar(self):
        self._dots = (self._dots + 1) % 4
        self._ui.labelProgress.setText(f"{self._progress_text}{'.' * self._dots}")

    def _update_progress(self, message, color):
        self._ui.labelProgress.setText(message)
        self._progress_text = message
        self._dots = 0
        self._ui.labelProgress.setStyleSheet(f"color: {color};")

    @handle_runtime_error
    def _harmonise_data(self):
        selected = self._get_selected_trials()
        selected_trials = {key: value for key, value in self._deidentified_file_names.items() if key in selected}
        kinematic_exclusions = self._kinematic_curves.get_excluded_cycles()
        kinetic_exclusions = self._kinetic_curves.get_excluded_cycles()
        self._update_s_t_data_from_tables()
        write_normalised_kinematics(self._kinematic_data, selected_trials, kinematic_exclusions, self._output_directory)
        write_normalised_kinetics(self._kinetic_data, selected_trials, kinetic_exclusions, self._output_directory)
        write_spatiotemporal_data(self._s_t_data, selected_trials, self._output_directory)

    def _reset_grf_plots(self):
        self._plot_x.clear()
        self._plot_y.clear()
        self._plot_z.clear()

        self._update_grf_axes()
        self._grf_canvas.draw()

    def _visualise_grf_data(self, grf_data):
        self._plot_x.clear()
        self._plot_y.clear()
        self._plot_z.clear()

        for foot, files_dict in grf_data.items():
            colour = 'r' if foot == "Left" else 'b'
            for name, cycles in files_dict.items():
                for cycle_number, cycle_data in cycles.items():
                    t_segment = np.linspace(0, 100, cycle_data.shape[1])

                    for j, plot in enumerate([self._plot_x, self._plot_y, self._plot_z]):
                        line, = plot.plot(t_segment, cycle_data[j], color=colour, linewidth=self._line_width)
                        line.set_picker(True)
                        self._grf_curves.add_curve(name, f"{foot}_{cycle_number}", line)

        for plot in [self._plot_x, self._plot_y, self._plot_z]:
            plot.margins(x=0)

        self._update_grf_axes()
        self._grf_canvas.draw()

    def _reset_kinematic_plots(self):
        self._visualise_kinematic_data({})

    def _visualise_kinematic_data(self, kinematic_data):
        for plot in self._kinematic_plots:
            plot.clear()

        for foot, files_dict in kinematic_data.items():
            colour = 'r' if foot == "Left" else 'b'
            for name, cycles in files_dict.items():
                for cycle_number, cycle_data in cycles.items():
                    t_segment = np.linspace(0, 100, cycle_data.shape[1])

                    for j, plot in enumerate(self._kinematic_plots):
                        line, = plot.plot(t_segment, cycle_data[j], color=colour, linewidth=self._line_width)
                        line.set_picker(True)
                        self._kinematic_curves.add_curve(name, f"{foot}_{cycle_number}", line)

        self._update_kinematic_axes()
        self._kinematic_canvas.draw()

    def _reset_kinetic_plots(self):
        self._visualise_kinetic_data({})

    def _visualise_kinetic_data(self, kinetic_data):
        for plot in self._kinetic_plots:
            plot.clear()

        for foot, files_dict in kinetic_data.items():
            colour = 'r' if foot == "Left" else 'b'
            for name, cycles in files_dict.items():
                for cycle_number, cycle_data in cycles.items():
                    t_segment = np.linspace(0, 100, cycle_data.shape[1])

                    for j, plot in enumerate(self._kinetic_plots):
                        line, = plot.plot(t_segment, cycle_data[j], color=colour, linewidth=self._line_width)
                        line.set_picker(True)
                        self._kinetic_curves.add_curve(name, f"{foot}_{cycle_number}", line)

        self._update_kinetic_axes()
        self._kinetic_canvas.draw()

    def _update_kinematic_axes(self):
        plot_labels = {
            0: ('Pelvic Anterior (+) / Posterior (-) Tilt', 'Ant', 'Pos'),
            1: ('Pelvic Up (+) / Down (-) Obliquity', 'Up', 'Down'),
            2: ('Pelvic Internal (+) / External (-) Rotation', 'Int', 'Ext'),
            3: ('Hip Flexion (+) / Extension (-)', 'Flex', 'Ext'),
            4: ('Hip Abduction (+) / Adduction (-)', 'Add', 'Abd'),
            5: ('Hip Internal (+) / External (-) Rotation', 'Int', 'Ext'),
            6: ('Knee Flexion (-) / Extension (+)', 'Flex', 'Ext'),
            7: ('Ankle Dorsiflexion (+) / Plantarflexion (-)', 'Dor', 'Pla'),
            8: ('Subtalar Inversion (+) / Eversion (-)', 'Inv', 'Eve'),
            9: ('Foot Progression', 'Int', 'Ext')
        }

        for i, plot in enumerate(self._kinematic_plots):
            plot.set_xlim(0, 100)
            if i == 3:
                plot.set_ylim(-30, 70)
            elif i == 6:
                plot.set_ylim(-15, 75)
            elif i in [7, 8]:
                plot.set_ylim(-50, 30)
            elif i == 9:
                plot.set_ylim(-60, 30)
            else:
                plot.set_ylim(-30, 30)
            plot.axhline(y=0, color='gray', linewidth=1.0, zorder=1)

            title, positive, negative = plot_labels.get(i, ("", "", ""))
            y_min, y_max = plot.get_ylim()
            step = (y_max - y_min) / 4

            plot.set_title(title, fontsize=10, pad=6)
            plot.text(x=0, y=y_min, s=int(y_min), ha='right', va='center', fontsize=9)
            plot.text(x=0, y=(y_min + 1 * step), s=negative, ha='right', va='center', fontsize=9)
            plot.text(x=0, y=(y_min + 2 * step), s="deg", ha='right', va='center', fontsize=9)
            plot.text(x=0, y=(y_min + 3 * step), s=positive, ha='right', va='center', fontsize=9)
            plot.text(x=0, y=y_max, s=int(y_max), ha='right', va='center', fontsize=9)

            plot.set_xticks([0, 20, 40, 60, 80, 100])
            plot.tick_params(axis='x', which='both', bottom=True, labelbottom=False)
            if i in [7, 8, 9]:
                plot.set_xticklabels(['0%', '20%', '40%', '60%', '80%', '100%'], fontsize=9)
                plot.tick_params(axis='x', labelbottom=True)
                plot.set_xlabel("Gait Cycle (%)", fontsize=9)

    def _update_kinetic_axes(self):
        plot_labels = {
            0: ('Hip Extensor Moment', 'Nm/kg', 'Ext', 'Flx'),
            1: ('Hip Abductor Moment', 'Nm/kg', 'Abd', 'Add'),
            2: ('Hip Rotator Moment', 'Nm/kg', 'Int', 'Ext'),
            3: ('Knee Extensor Moment', 'Nm/kg', 'Ext', 'Flx'),
            4: ('Knee Abductor Moment', 'Nm/kg', 'Abd', 'Add'),
            5: ('Knee Rotator Moment', 'Nm/kg', 'Int', 'Ext'),
            6: ('Ankle Dorsiflexor Moment', 'Nm/kg', 'Pla', 'Dor'),
            7: ('Subtalar Inverter Moment', 'Nm/kg', 'Inv', 'Eve'),
            8: ('Hip Power (Sagittal)', 'W/kg', 'Gen', 'Abs'),
            9: ('Knee Power (Sagittal)', 'W/kg', 'Gen', 'Abs'),
            10: ('Ankle Power (Sagittal)', 'W/kg', 'Gen', 'Abs')
        }

        self._kinetic_plots[0].set_ylim(-2.0, 3.0)      # Hip Extensor
        self._kinetic_plots[1].set_ylim(-1.0, 2.0)      # Hip Abductor
        self._kinetic_plots[2].set_ylim(-0.5, 0.5)      # Hip Rotator
        self._kinetic_plots[3].set_ylim(-1.0, 1.0)      # Knee Extensor
        self._kinetic_plots[4].set_ylim(-1.0, 1.0)      # Knee Abductor
        self._kinetic_plots[5].set_ylim(-0.5, 0.5)      # Knee Rotator
        self._kinetic_plots[6].set_ylim(-1.0, 3.0)      # Ankle Dorsiflexor
        self._kinetic_plots[7].set_ylim(-0.5, 0.5)      # Subtalar Inverter
        self._kinetic_plots[8].set_ylim(-3.0, 3.0)      # Total Hip
        self._kinetic_plots[9].set_ylim(-3.0, 3.0)      # Total Knee
        self._kinetic_plots[10].set_ylim(-2.0, 5.0)     # Total Ankle

        for i, plot in enumerate(self._kinetic_plots):
            plot.set_xlim(0, 100)
            plot.axhline(y=0, color='gray', linewidth=1.0, zorder=1)

            title, units, positive, negative = plot_labels.get(i, ("", "", "", ""))
            y_min, y_max = plot.get_ylim()
            step = (y_max - y_min) / 4

            plot.set_title(title, fontsize=10, pad=6)
            plot.text(x=0, y=y_min, s=y_min, ha='right', va='center', fontsize=9)
            plot.text(x=0, y=(y_min + 1 * step), s=negative, ha='right', va='center', fontsize=9)
            plot.text(x=0, y=(y_min + 2 * step), s=units, ha='right', va='center', fontsize=9)
            plot.text(x=0, y=(y_min + 3 * step), s=positive, ha='right', va='center', fontsize=9)
            plot.text(x=0, y=y_max, s=y_max, ha='right', va='center', fontsize=9)

            plot.set_xticks([0, 20, 40, 60, 80, 100])
            plot.tick_params(axis='x', which='both', bottom=True, labelbottom=False)
            if i in [8, 9, 10]:
                plot.set_xticklabels(['0%', '20%', '40%', '60%', '80%', '100%'], fontsize=9)
                plot.tick_params(axis='x', labelbottom=True)
                plot.set_xlabel("Gait Cycle (%)", fontsize=9)

    def _update_plot_visibility(self, item):
        visible = item.checkState() == Qt.CheckState.Checked
        for curves in [self._grf_curves, self._kinematic_curves, self._kinetic_curves]:
            curves.set_file_visibility(item.text(), visible)

    def _show_selected_trials(self):
        for i in range(self._ui.listWidgetFiles.count()):
            item = self._ui.listWidgetFiles.item(i)
            self._update_plot_visibility(item)

    def _get_selected_trials(self):
        selected_trials = []
        for i in range(self._ui.listWidgetFiles.count()):
            item = self._ui.listWidgetFiles.item(i)
            if item.checkState() == Qt.CheckState.Checked:
                selected_trials.append(item.text())
        return selected_trials

    def _show_options_dialog(self):
        dlg = OptionsDialog(self)
        dlg.load(self._get_options())
        if dlg.exec():
            self._set_options(dlg.save())
            self._update_curves()

    def _get_options(self):
        options = {
            'line_width': self._line_width,
            'input_data_directory': self._input_data_directory,
            'output_data_directory': self._output_data_directory,
            'optimise_knee_axis': self._optimise_knee_axis
        }

        return options

    def _set_options(self, options):
        self._line_width = options['line_width']
        self._input_data_directory = options['input_data_directory']
        self._output_data_directory = options['output_data_directory']
        self._optimise_knee_axis = options['optimise_knee_axis']

    def _show_marker_set_dialog(self):
        static_trials = []
        for i in range(self._ui.listWidgetFiles.count()):
            item = self._ui.listWidgetFiles.item(i)
            if item.checkState() == Qt.CheckState.Checked:
                if item.data(Qt.ItemDataRole.UserRole) == "Static":
                    static_trials.append(item.text())

        marker_names = []
        if static_trials:
            input_directory = self._ui.lineEditInputDirectory.text()
            c3d_file = os.path.join(input_directory, static_trials[0])
            marker_names = extract_marker_names(c3d_file)

        dlg = MarkerSetDialog(self)
        dlg.set_marker_names(marker_names)
        if dlg.exec():
            dlg.save()
            self._reset_lab_combo_box()

    def _show_about_dialog(self):
        dlg = AboutDialog(self)
        dlg.setModal(True)
        dlg.exec()

    def _update_curves(self):
        for curves in [self._grf_curves, self._kinematic_curves, self._kinetic_curves]:
            curves.update_line_width(self._line_width)

    def _save_settings(self):
        settings = QSettings()

        settings.beginGroup('MainWindow')
        settings.setValue('size', self.size())
        settings.setValue('pos', self.pos())
        settings.setValue('is_maximized', self.isMaximized())
        settings.setValue('lab', self._ui.comboBoxLab.currentText())
        settings.setValue('marker_diameter', self._ui.doubleSpinBoxMarkerDiameter.value())
        settings.endGroup()

        settings.beginGroup('Options')
        settings.setValue('line_width', self._line_width)
        settings.setValue('input_data_directory', self._input_data_directory)
        settings.setValue('output_data_directory', self._output_data_directory)
        settings.setValue('optimise_knee_axis', self._optimise_knee_axis)
        settings.endGroup()

    def _load_settings(self):
        settings = QSettings()

        settings.beginGroup('MainWindow')
        if settings.contains('size'):
            self.resize(settings.value('size'))
        if settings.contains('pos'):
            self.move(settings.value('pos'))
        if settings.contains('is_maximized'):
            if settings.value('is_maximized', 'true') == 'true':
                self.showMaximized()
        if settings.contains('lab'):
            self._ui.comboBoxLab.setCurrentText(settings.value('lab'))
        if settings.contains('marker_diameter'):
            self._ui.doubleSpinBoxMarkerDiameter.setValue(float(settings.value('marker_diameter')))
        settings.endGroup()

        settings.beginGroup('Options')
        if settings.contains('line_width'):
            self._line_width = float(settings.value('line_width'))
        if settings.contains('input_data_directory'):
            self._input_data_directory = settings.value('input_data_directory')
        if settings.contains('output_data_directory'):
            self._output_data_directory = settings.value('output_data_directory')
        if settings.contains('optimise_knee_axis'):
            self._optimise_knee_axis = settings.value('optimise_knee_axis') == 'true'
        settings.endGroup()

    def _quit_application(self):
        self._save_settings()
        QApplication.quit()

    def closeEvent(self, event):
        if self.sender() is None:
            self._quit_application()

    def _include_trial(self, file_name):
        for curves in [self._grf_curves, self._kinematic_curves, self._kinetic_curves]:
            curves.include_trial(file_name)

    def _exclude_trial(self, file_name):
        for curves in [self._grf_curves, self._kinematic_curves, self._kinetic_curves]:
            curves.exclude_trial(file_name)

    def _include_kinetics(self, file_name):
        self._kinetic_curves.include_trial(file_name)

    def _exclude_kinetics(self, file_name):
        self._kinetic_curves.exclude_trial(file_name)

    def _include_left(self, file_name):
        for curves in [self._grf_curves, self._kinematic_curves, self._kinetic_curves]:
            curves.include_side(file_name, "Left")

    def _exclude_left(self, file_name):
        for curves in [self._grf_curves, self._kinematic_curves, self._kinetic_curves]:
            curves.exclude_side(file_name, "Left")

    def _include_right(self, file_name):
        for curves in [self._grf_curves, self._kinematic_curves, self._kinetic_curves]:
            curves.include_side(file_name, "Right")

    def _exclude_right(self, file_name):
        for curves in [self._grf_curves, self._kinematic_curves, self._kinetic_curves]:
            curves.exclude_side(file_name, "Right")


class GaitCurves(defaultdict):

    def __init__(self, canvas):
        super().__init__(lambda: defaultdict(list))

        self._canvas = canvas
        self._canvas.mpl_connect('pick_event', lambda event: self.toggle_cycle(event))
        self._canvas.mpl_connect('button_press_event', lambda event: self.show_curve_menu(event))

        self._selected_curves = []
        self._excluded_cycles = set()

        self._cursors = {}

    def add_curve(self, file_name, cycle, curve):
        self[file_name][cycle].append(curve)

    def get_curves(self, file_name, cycle):
        return self[file_name][cycle]

    def set_file_visibility(self, file_name, visible):
        cycles = self[file_name]
        for cycle, lines in cycles.items():
            for line in lines:
                line.set_visible(visible)
                line.set_picker(visible)

        self._canvas.draw()

    def toggle_cycle(self, event):
        if event.mouseevent.button == 3:
            return

        def create_hover_callback(trial, cycle_id):
            def on_hover(selection):
                selection.annotation.set_text(f"Trial: {trial}\nCycle: {cycle_id}")
                patch = selection.annotation.get_bbox_patch()
                patch.set_alpha(0.8)
                patch.set_facecolor("white")
                patch.set_boxstyle("round,pad=0.3,rounding_size=0.15")
            return on_hover

        line = event.artist
        for file_name, cycles in self.items():
            for cycle, lines in cycles.items():
                if line in lines:
                    identifier = (file_name, cycle)
                    if identifier in self._selected_curves:
                        self._selected_curves.remove(identifier)
                        colour = 'red' if "Left" in cycle else 'blue'
                        z_order = 2

                        # Remove hover cursor from selected curve.
                        if identifier in self._cursors:
                            cursor = self._cursors.pop(identifier)
                            cursor.remove()

                    else:
                        self._selected_curves.append(identifier)
                        colour = 'green'
                        z_order = 3

                        # Add hover cursor to selected curve.
                        cursor = mplcursors.cursor(self[file_name][cycle], hover=mplcursors.HoverMode.Transient)
                        cursor.connect("add", create_hover_callback(file_name, cycle))
                        self._cursors[identifier] = cursor

                    for line in self[file_name][cycle]:
                        line.set_color(colour)
                        line.set_zorder(z_order)

        self._canvas.draw()

    def show_curve_menu(self, event):
        if event.button == 3:
            context_menu = QMenu()

            include_action = context_menu.addAction("Include Selected Cycles")
            exclude_action = context_menu.addAction("Exclude Selected Cycles")
            include_action.triggered.connect(self.include_curves)
            exclude_action.triggered.connect(self.exclude_curves)
            context_menu.addSeparator()

            include_all_action = context_menu.addAction("Include All Cycles")
            exclude_all_action = context_menu.addAction("Exclude All Cycles")
            include_all_action.triggered.connect(self.include_all)
            exclude_all_action.triggered.connect(self.exclude_all)
            context_menu.addSeparator()

            clear_selected_action = context_menu.addAction("Clear Selected")
            clear_selected_action.triggered.connect(self.clear_selected)

            point = QPoint(event.x, self._canvas.figure.bbox.height - event.y)
            context_menu.exec_(self._canvas.mapToGlobal(point))

    def include_curves(self):
        self._excluded_cycles.difference_update(self._selected_curves)
        for file_name, cycle in self._selected_curves:
            colour = 'red' if "Left" in cycle else 'blue'
            for line in self[file_name][cycle]:
                line.set_linestyle('solid')
                line.set_color(colour)
                line.set_zorder(2)
        self._selected_curves = []

        self._canvas.draw()

    def include_all(self):
        for file_name, cycles in self.items():
            self.include_trial(file_name)
        self._selected_curves = []

    def include_trial(self, file_name):
        for cycle in self[file_name].keys():
            colour = 'red' if "Left" in cycle else 'blue'
            self._include_cycle(file_name, cycle, colour)
        self._canvas.draw()

    def include_side(self, file_name, side):
        colour = 'red' if side == "Left" else 'blue'
        for cycle in self[file_name].keys():
            if side in cycle:
                self._include_cycle(file_name, cycle, colour)
        self._canvas.draw()

    def _include_cycle(self, file_name, cycle, colour):
        self._excluded_cycles.difference_update([(file_name, cycle), ])
        for line in self[file_name][cycle]:
            line.set_linestyle('solid')
            line.set_color(colour)
            line.set_zorder(2)

    def update_line_width(self, line_width):
        for cycles in self.values():
            for lines in cycles.values():
                for line in lines:
                    line.set_linewidth(line_width)

        self._canvas.draw()

    def exclude_curves(self):
        self._excluded_cycles.update(self._selected_curves)
        for file_name, cycle in self._selected_curves:
            colour = 'red' if "Left" in cycle else 'blue'
            for line in self[file_name][cycle]:
                line.set_linestyle('dotted')
                line.set_color(colour)
                line.set_zorder(1)
        self._selected_curves = []

        self._canvas.draw()

    def exclude_all(self):
        for file_name, cycles in self.items():
            self.exclude_trial(file_name)
        self._selected_curves = []

    def exclude_trial(self, file_name):
        for cycle in self[file_name].keys():
            colour = 'red' if "Left" in cycle else 'blue'
            self._exclude_cycle(file_name, cycle, colour)
        self._canvas.draw()

    def exclude_side(self, file_name, side):
        colour = 'red' if side == "Left" else 'blue'
        for cycle in self[file_name].keys():
            if side in cycle:
                self._exclude_cycle(file_name, cycle, colour)
        self._canvas.draw()

    def _exclude_cycle(self, file_name, cycle, colour):
        self._excluded_cycles.update([(file_name, cycle)], )
        for line in self[file_name][cycle]:
            line.set_linestyle('dotted')
            line.set_color(colour)
            line.set_zorder(1)

    def get_excluded_cycles(self):
        return self._excluded_cycles

    def clear_selected(self):
        for (file_name, cycle) in self._selected_curves:
            colour = 'red' if "Left" in cycle else 'blue'
            for line in self[file_name][cycle]:
                line.set_color(colour)
                line.set_zorder(2)
        self._selected_curves = []

        self._canvas.draw()


class SpatiotemporalModel(QAbstractTableModel):
    def __init__(self, df: pd.DataFrame, parent=None):
        super().__init__(parent)
        self._df = df
        self._excluded_cycles = set()

    def rowCount(self, parent=None):
        return len(self._df.index)

    def columnCount(self, parent=None):
        return len(self._df.columns) + 1

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None
        if role == Qt.ItemDataRole.DisplayRole:
            if index.column() == len(self._df.columns):
                return ""
            value = self._df.iat[index.row(), index.column()]
            if pd.isna(value):
                return ""
            return str(value)
        elif role == Qt.ItemDataRole.ForegroundRole:
            if index.column() in self._excluded_cycles:
                return QColor("lightgrey")
        return None

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role != Qt.ItemDataRole.DisplayRole:
            return None
        if orientation == Qt.Orientation.Horizontal:
            if section == len(self._df.columns):
                return ""
            return str(self._df.columns[section])
        else:
            return str(self._df.index[section])

    def flags(self, index):
        default_flags = super().flags(index)
        if index.column() >= self.columnCount() - 1:
            return default_flags & ~Qt.ItemFlag.ItemIsSelectable
        return default_flags

    def exclude_cycles(self, exclusions):
        self._excluded_cycles.update(exclusions)

    def include_cycles(self, inclusions):
        self._excluded_cycles.difference_update(inclusions)

    def get_data(self):
        return self._df

    def get_excluded_cycles(self):
        return self._excluded_cycles


class SpatiotemporalTableDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        super().paint(painter, option, index)
        model = index.model()
        rect = option.rect

        if index.column() == model.columnCount() - 1:
            painter.save()

            data = index.model().get_data()
            columns = [i for i in range(data.shape[1]) if i not in model.get_excluded_cycles()]

            def draw_box(min_value, max_value, mean, total, side=None):
                if pd.isna(mean) or pd.isna(total):
                    return

                margin = 4
                y_offset = 0
                whisker_width = 2
                box_width = int(rect.width() * (mean / total))
                box_height = (rect.height() - 2 * margin) // (2 if side else 1)
                if side == 'left':
                    colour = QColor("firebrick")
                elif side == 'right':
                    colour = QColor("cornflowerblue")
                    y_offset = box_height
                else:
                    colour = QColor("mediumpurple")
                    whisker_width = 4
                cell_left = rect.left() + 1

                # Draw box.
                box_rect = QRect(rect.left() + 1, rect.top() + margin + y_offset, box_width, box_height)
                painter.fillRect(box_rect, colour)

                # Draw whiskers.
                if side:
                    left = cell_left + (rect.width() * (min_value / total)) - 1
                    right = cell_left + (rect.width() * (max_value / total))
                    pen = QPen(QColor("black"))
                    painter.setPen(pen)
                    centre_y = box_rect.center().y()
                    painter.drawLine(left, centre_y + whisker_width, left, centre_y - whisker_width)
                    painter.drawLine(right, centre_y + whisker_width, right, centre_y - whisker_width)
                    painter.drawLine(left, centre_y, right, centre_y)

            # Calculate slightly-arbitrary max value for meter metrics.
            max_value = data.iloc[:2, :].max().max() + 0.40
            if index.row() in [5, 6, 7, 8]:
                max_value = 100
            else:
                if index.row() == 9:
                    max_value = 3.0
                elif index.row() == 10:
                    max_value = 1.5
                elif index.row() == 11:
                    max_value = 240

            left_columns = [i for i in columns if "Left" in data.columns[i]]
            right_columns = [i for i in columns if "Right" in data.columns[i]]
            left_values = data.iloc[index.row(), left_columns]
            right_values = data.iloc[index.row(), right_columns]

            if not left_values.empty:
                l_min, l_max, l_mean = left_values.min(), left_values.max(), left_values.mean()
                draw_box(l_min, l_max, l_mean, max_value, side='left')
            if not right_values.empty:
                r_min, r_max, r_mean = right_values.min(), right_values.max(), right_values.mean()
                draw_box(r_min, r_max, r_mean, max_value, side='right')

            painter.restore()

        pen = QPen(QColor("black"))
        painter.setPen(pen)

        if index.row() == model.rowCount() - 1:
            painter.drawLine(rect.bottomLeft(), rect.bottomRight())

        if index.column() == model.columnCount() - 1:
            painter.drawLine(rect.topRight(), rect.bottomRight())


class CustomTableView(QTableView):
    def __init__(self, trial_name, parent=None):
        super().__init__(parent)

        self._trial_name = trial_name
        self._corner_label = QLabel(self)
        self._corner_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setHorizontalHeader(CustomHeaderView(Qt.Orientation.Horizontal))

        font = self._corner_label.font()
        font.setBold(True)
        font.setPointSize(10)
        self._corner_label.setFont(font)

        self.setShowGrid(False)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.setStyleSheet("""
            QTableView { selection-color: black; } 
            QHeaderView::section { border-top: 1px solid black; border-left: 1px solid black; }
            QHeaderView::section:vertical { padding-left: 6px; } 
            QTableView::item { border-top: 1px solid black; border-left: 1px solid black; }
        """)
        self.verticalHeader().setStyleSheet("""
            border-left: 0px; border-right: 0px; border-top: 0px; border-bottom: 1px solid black;
        """)

        delegate = SpatiotemporalTableDelegate()
        self.setItemDelegate(delegate)

        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self._show_context_menu)
        self.horizontalHeader().setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.horizontalHeader().customContextMenuRequested.connect(self._show_context_menu)
        self.verticalHeader().setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.verticalHeader().customContextMenuRequested.connect(self._show_context_menu)

    def setModel(self, model):
        super().setModel(model)

        self._resize_table()
        self._update_corner_text()

    def _resize_table(self):
        self.resizeRowsToContents()
        table_height = self.verticalHeader().length() + self.horizontalHeader().height() + 2
        self.setMinimumHeight(table_height)
        self.setMaximumHeight(table_height)

        self.verticalHeader().setFixedWidth(240)
        self.horizontalHeader().setDefaultSectionSize(60)
        last_col = self.model().columnCount() - 1
        self.setColumnWidth(last_col, 240)

        table_width = self.horizontalHeader().length() + self.verticalHeader().width() + 2
        self.setMinimumWidth(table_width)
        self.setMaximumWidth(table_width)

        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        self.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)

    def _update_corner_text(self):
        corner_buttons = self.findChildren(QAbstractButton, options=Qt.FindChildOption.FindDirectChildrenOnly)
        if corner_buttons:
            width = self.verticalHeader().width()
            height = self.horizontalHeader().height()
            corner_buttons[0].setGeometry(0, 0, width, height)

            fm = QFontMetrics(self._corner_label.font())
            elided = fm.elidedText(self._trial_name, Qt.TextElideMode.ElideLeft, width)

            self._corner_label.setText(elided)
            self._corner_label.setGeometry(0, 0, width, height)
            self._corner_label.show()

    def _show_context_menu(self, pos):
        context_menu = QMenu()

        include_action = context_menu.addAction("Include Selected Cycles")
        exclude_action = context_menu.addAction("Exclude Selected Cycles")
        include_action.triggered.connect(self._include_cycles)
        exclude_action.triggered.connect(self._exclude_cycles)
        context_menu.addSeparator()

        include_all_action = context_menu.addAction("Include All Cycles")
        exclude_all_action = context_menu.addAction("Exclude All Cycles")
        include_all_action.triggered.connect(self._include_all)
        exclude_all_action.triggered.connect(self._exclude_all)
        context_menu.addSeparator()

        sender = self.sender()
        if isinstance(sender, QHeaderView):
            global_pos = self.mapToGlobal(sender.mapToParent(pos))
        else:
            global_pos = self.viewport().mapToGlobal(pos)
        context_menu.exec(global_pos)

    def _get_selected_columns(self):
        selection_model = self.selectionModel()
        selected_indexes = selection_model.selectedIndexes()
        selected_columns = {idx.column() for idx in selected_indexes}
        for idx in selected_indexes:
            selection_model.select(idx, selection_model.SelectionFlag.Deselect)

        return selected_columns

    def _include_cycles(self):
        selected_columns = self._get_selected_columns()
        self.model().include_cycles(selected_columns)

        self.viewport().update()

    def _exclude_cycles(self):
        selected_columns = self._get_selected_columns()
        self.model().exclude_cycles(selected_columns)

        self.viewport().update()

    def _include_all(self):
        all_columns = set(range(self.model().columnCount()))
        self.model().include_cycles(all_columns)

        self.viewport().update()

    def _exclude_all(self):
        all_columns = set(range(self.model().columnCount() - 1))
        self.model().exclude_cycles(all_columns)

        self.viewport().update()

    def get_trial_name(self):
        return self._trial_name


class CustomHeaderView(QHeaderView):
    def __init__(self, orientation, parent=None):
        super().__init__(orientation, parent)
        self.setSectionsClickable(True)
        self.setHighlightSections(True)

    def paintSection(self, painter, rect, logical_index):
        if logical_index == self.model().columnCount() - 1:
            painter.save()
            painter.setPen(self.palette().color(self.foregroundRole()))
            painter.drawLine(rect.topLeft(), rect.bottomLeft())
            painter.restore()
        else:
            super().paintSection(painter, rect, logical_index)