
import os
import logging
import numpy as np
from collections import defaultdict

from PySide6.QtCore import Qt, QSettings, QPoint, QThread, Signal, QObject, QTimer
from PySide6.QtWidgets import QApplication, QMainWindow, QMenu, QFileDialog, QListWidgetItem, QInputDialog, QMessageBox
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from c3d_parser.core.c3d_parser import parse_session, extract_static_data, extract_marker_names, read_grf, is_dynamic, marker_maps_dir,\
    CancelException, write_normalised_kinematics, write_normalised_kinetics, write_spatiotemporal_data
from c3d_parser.view.ui.ui_main_window import Ui_MainWindow
from c3d_parser.view.dialogs.options_dialog import OptionsDialog
from c3d_parser.view.dialogs.marker_set_dialog import MarkerSetDialog
from c3d_parser.settings.general import DEFAULT_STYLE_SHEET, INVALID_STYLE_SHEET, APPLICATION_NAME
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

        self._input_data_directory = ''
        self._output_data_directory = ''

        self._static_trial = None
        self._analog_data = None
        self._subject_weight = None
        self._kinematic_data = {}
        self._kinetic_data = {}
        self._events = {}

        self._line_width = 1.0

        self._setup_combo_box()
        self._setup_figures()
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

    def _setup_combo_box(self):
        labs = [os.path.splitext(lab)[0] for lab in os.listdir(marker_maps_dir)]
        self._ui.comboBoxLab.addItems(labs)

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
        self._grf_canvas.figure.tight_layout(pad=0.0, rect=[0.04, 0.06, 0.98, 0.96], h_pad=1.6, w_pad=0.2)
        self._update_grf_axes()

        self._ui.layoutGRFPlot.addWidget(self._grf_canvas)

    def _setup_kinematic_figures(self):
        self._kinematic_canvas = FigureCanvasQTAgg(Figure())
        self._kinematic_plots = []
        for i in range(3):
            for j in range(3):
                plot = self._kinematic_canvas.figure.add_subplot(3, 3, i * 3 + j + 1)
                plot.tick_params(axis='x', which='both', labelbottom=False, bottom=False)
                plot.tick_params(axis='y', which='both', labelleft=False, left=False)
                self._kinematic_plots.append(plot)
        self._kinematic_canvas.figure.tight_layout(pad=0.0, rect=[0.04, 0.06, 0.98, 0.96], h_pad=1.6, w_pad=2.0)
        self._update_kinematic_axes()

        self._ui.layoutKinematicPlot.addWidget(self._kinematic_canvas)

    def _setup_kinetic_figures(self):
        self._kinetic_canvas = FigureCanvasQTAgg(Figure())
        self._kinetic_plots = []
        for i in range(3):
            for j in range(3):
                plot = self._kinetic_canvas.figure.add_subplot(3, 3, i * 3 + j + 1)
                plot.tick_params(axis='x', which='both', labelbottom=False, bottom=False)
                plot.tick_params(axis='y', which='both', labelleft=False, left=False)
                self._kinetic_plots.append(plot)
        self._kinetic_canvas.figure.tight_layout(pad=0.0, rect=[0.04, 0.06, 0.98, 0.96], h_pad=1.6, w_pad=2.0)
        self._update_kinetic_axes()

        self._ui.layoutKineticPlot.addWidget(self._kinetic_canvas)

    def _update_grf_axes(self):
        self._plot_x.set_title(f'GRF (Anterior - Posterior)', fontsize=10, pad=4)
        self._plot_y.set_title(f'GRF (Medial - Lateral)', fontsize=10, pad=4)
        self._plot_z.set_title(f'GRF (Vertical)', fontsize=10, pad=4)

        for plot in [self._plot_x, self._plot_y, self._plot_z]:
            y_min, y_max = plot.get_ylim()
            plot.set_ylim(np.floor(y_min / 10) * 10, np.ceil(y_max / 10) * 10)
            y_min, y_max = plot.get_ylim()
            step = (y_max - y_min) / 4

            plot.axhline(y=0, color='gray', linewidth=1.0, zorder=1)
            plot.text(x=0, y=y_min, s=int(y_min), ha='right', va='center', fontsize=9)
            plot.text(x=0, y=(y_min + 2 * step), s="N", ha='right', va='center', fontsize=9)
            plot.text(x=0, y=y_max, s=int(y_max), ha='right', va='center', fontsize=9)

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

        self._ui.listWidgetFiles.include_trial.connect(self._include_trial)
        self._ui.listWidgetFiles.exclude_trial.connect(self._exclude_trial)
        self._ui.listWidgetFiles.category_changed.connect(self._update_subject_info)

    def _validate_input_directory(self):
        directory_valid = self._validate_directory()

        self._ui.listWidgetFiles.clear()
        if directory_valid:
            self._scan_directory()

            self._reset_grf_plots()
            self._reset_kinematic_plots()
            self._reset_kinetic_plots()

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
        self._open_directory_chooser(self._ui.lineEditInputDirectory, self._input_data_directory)

    def _open_output_directory_chooser(self):
        self._open_directory_chooser(self._ui.lineEditOutputDirectory, self._output_data_directory)

    def _open_directory_chooser(self, line_edit, data_directory):
        directory = QFileDialog.getExistingDirectory(
            self, 'Select Directory', data_directory)

        if directory:
            line_edit.setText(directory)

    def _scan_directory(self):
        directory = self._ui.lineEditInputDirectory.text()
        self._ui.listWidgetFiles.clear()
        for root, dirs, files in os.walk(directory):
            if output_direcory_name in dirs:
                dirs.remove(output_direcory_name)
            for file in files:
                if file.lower().endswith('.c3d'):
                    path = os.path.join(root, file)
                    category = "Dynamic" if is_dynamic(path) else "Static"
                    item = QListWidgetItem(os.path.relpath(path, directory))
                    item.setData(Qt.UserRole, category)
                    item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
                    item.setCheckState(Qt.CheckState.Checked)
                    self._ui.listWidgetFiles.addItem(item)

        self._update_subject_info()

    def _update_subject_info(self):
        static_trials = []
        for i in range(self._ui.listWidgetFiles.count()):
            item = self._ui.listWidgetFiles.item(i)
            if item.data(Qt.UserRole) == "Static":
                static_trials.append(item.text())

        if static_trials:
            static_trial = static_trials[0]
            if static_trial != self._static_trial:
                self._set_subject_info(static_trial)
                self._static_trial = static_trial

    def _set_subject_info(self, static_trial):
        input_directory = self._ui.lineEditInputDirectory.text()
        c3d_file = os.path.join(input_directory, static_trial)
        static_data = list(extract_static_data(c3d_file))

        if static_data[0] is not None:
            self._ui.doubleSpinBoxHeight.setValue(static_data[0])
        if static_data[1] is not None:
            self._ui.doubleSpinBoxWeight.setValue(static_data[1])
        if static_data[2] is not None:
            self._ui.doubleSpinBoxLeftKneeWidth.setValue(static_data[2])
        if static_data[3] is not None:
            self._ui.doubleSpinBoxRightKneeWidth.setValue(static_data[3])
        if static_data[4] is not None:
            self._ui.doubleSpinBoxLeftLegLength.setValue(static_data[4])
        if static_data[5] is not None:
            self._ui.doubleSpinBoxRightLegLength.setValue(static_data[5])

    @handle_runtime_error
    def _parse_c3d_data(self):
        input_directory = self._ui.lineEditInputDirectory.text()
        output_directory = self._ui.lineEditOutputDirectory.text()
        session_name = os.path.basename(input_directory)
        self._output_directory = os.path.join(output_directory, output_direcory_name, session_name)

        static_trials = []
        dynamic_trials = []
        for i in range(self._ui.listWidgetFiles.count()):
            item = self._ui.listWidgetFiles.item(i)
            if item.checkState() == Qt.Checked:
                if item.data(Qt.UserRole) == "Dynamic":
                    dynamic_trials.append(item.text())
                else:
                    static_trials.append(item.text())
            else:
                item.setFlags(item.flags() & ~Qt.ItemIsEnabled)
                item.setData(Qt.UserRole, "")

        if len(static_trials) == 0:
            logger.error("No static trial found. You may need to classify one manually.")
            return
        if len(static_trials) == 1:
            static_trial = static_trials[0]
        if len(static_trials) > 1:
            static_trial, ok = QInputDialog.getItem(None, "Select Static Trial", "Please select one static trial:", static_trials, 0, False)
            if not ok:
                return

        lab = self._ui.comboBoxLab.currentText()
        marker_diameter = self._ui.doubleSpinBoxMarkerDiameter.value()

        static_data = {
            'Height': self._ui.doubleSpinBoxHeight.value(),
            'Weight': self._ui.doubleSpinBoxWeight.value(),
            'Left Knee Width': self._ui.doubleSpinBoxLeftKneeWidth.value(),
            'Right Knee Width': self._ui.doubleSpinBoxRightKneeWidth.value(),
            'Left Leg Length': self._ui.doubleSpinBoxLeftLegLength.value(),
            'Right Leg Length': self._ui.doubleSpinBoxRightLegLength.value(),
        }
        missing = [key for key, value in static_data.items() if value == 0.0]
        if missing:
            QMessageBox.warning(self, "Warning", "Subject measurements missing:\n- " + "\n- ".join(missing))
            return
        static_data = list(static_data.values())

        self._ui.pushButtonParseData.setEnabled(False)

        self._progress_tracker = ProgressTracker()
        self._progress_tracker.progress.connect(self._update_progress)
        self._start_progress_animation()

        self._worker = _ExecThread(parse_session, static_trial, dynamic_trials, input_directory, self._output_directory, lab,
                                   marker_diameter, static_data, self._progress_tracker)
        self._worker.finished.connect(self._parse_finished)
        self._worker.cancelled.connect(self._parse_cancelled)
        self._worker.failed.connect(self._parse_failed)
        self._worker.start()

    @handle_runtime_error
    def _parse_finished(self, result):
        grf_data, self._kinematic_data, self._kinetic_data, self._s_t_data = result

        self._visualise_grf_data(grf_data)
        self._visualise_kinematic_data(self._kinematic_data)
        self._visualise_kinetic_data(self._kinetic_data)

        self._show_selected_trials()
        self._stop_progress_animation()
        self._progress_tracker.progress.emit("Process completed successfully", "green")

        self._ui.pushButtonParseData.setEnabled(True)
        self._ui.pushButtonHarmonise.setEnabled(True)

    def _parse_cancelled(self, e):
        logger.info(e)

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
        selected_trials = self._get_selected_trials()
        kinematic_exclusions = self._kinematic_curves.get_excluded_cycles()
        kinetic_exclusions = self._kinetic_curves.get_excluded_cycles()
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
            for name, data_segments in files_dict.items():
                colour = 'r' if foot == "Left" else 'b'
                for i, segment in enumerate(data_segments):
                    t_segment = np.linspace(0, 100, segment.shape[1])

                    for j, plot in enumerate([self._plot_x, self._plot_y, self._plot_z]):
                        line, = plot.plot(t_segment, segment[j], color=colour, linewidth=self._line_width)
                        line.set_picker(True)
                        self._grf_curves.add_curve(name, f"{foot}_{i}", line)

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
            for name, data_segments in files_dict.items():
                colour = 'r' if foot == "Left" else 'b'
                for i, segment in enumerate(data_segments):
                    t_segment = np.linspace(0, 100, segment.shape[1])

                    for j, plot in enumerate(self._kinematic_plots):
                        line, = plot.plot(t_segment, segment[j], color=colour, linewidth=self._line_width)
                        line.set_picker(True)
                        self._kinematic_curves.add_curve(name, f"{foot}_{i}", line)

        self._update_kinematic_axes()
        self._kinematic_canvas.draw()

    def _reset_kinetic_plots(self):
        self._visualise_kinetic_data({})

    def _visualise_kinetic_data(self, kinetic_data):
        for plot in self._kinetic_plots:
            plot.clear()

        for foot, files_dict in kinetic_data.items():
            for name, data_segments in files_dict.items():
                colour = 'r' if foot == "Left" else 'b'
                for i, segment in enumerate(data_segments):
                    t_segment = np.linspace(0, 100, segment.shape[1])

                    for j, plot in enumerate(self._kinetic_plots):
                        line, = plot.plot(t_segment, segment[j], color=colour, linewidth=self._line_width)
                        line.set_picker(True)
                        self._kinetic_curves.add_curve(name, f"{foot}_{i}", line)

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
            8: ('Subtalar Inversion (+) / Eversion (-)', 'Inv', 'Eve')
        }

        for i, plot in enumerate(self._kinematic_plots):
            plot.set_xlim(0, 100)
            if i == 3:
                plot.set_ylim(-30, 70)
            elif i == 6:
                plot.set_ylim(-15, 75)
            elif i in [7, 8]:
                plot.set_ylim(-50, 30)
            else:
                plot.set_ylim(-30, 30)
            plot.axhline(y=0, color='gray', linewidth=1.0, zorder=1)

            title, positive, negative = plot_labels.get(i, ("", "", ""))
            y_min, y_max = plot.get_ylim()
            step = (y_max - y_min) / 4

            plot.set_title(title, fontsize=10, pad=4)
            plot.text(x=0, y=y_min, s=int(y_min), ha='right', va='center', fontsize=9)
            plot.text(x=0, y=(y_min + 1 * step), s=negative, ha='right', va='center', fontsize=9)
            plot.text(x=0, y=(y_min + 2 * step), s="deg", ha='right', va='center', fontsize=9)
            plot.text(x=0, y=(y_min + 3 * step), s=positive, ha='right', va='center', fontsize=9)
            plot.text(x=0, y=y_max, s=int(y_max), ha='right', va='center', fontsize=9)

            plot.set_xticks([0, 20, 40, 60, 80, 100])
            plot.tick_params(axis='x', which='both', bottom=True, labelbottom=False)
            if i in [6, 7, 8]:
                plot.set_xticklabels(['0%', '20%', '40%', '60%', '80%', '100%'], fontsize=9)
                plot.tick_params(axis='x', labelbottom=True)
                plot.set_xlabel("Gait Cycle (%)", fontsize=9)

    def _update_kinetic_axes(self):
        plot_labels = {
            0: ('Hip Extensor Moment', 'Nm/kg', 'Ext', 'Flx'),
            1: ('Hip Abductor Moment', 'Nm/kg', 'Abd', 'Add'),
            2: ('Hip Rotation Moment', 'Nm/kg', 'Int', 'Ext'),
            3: ('Knee Extensor Moment', 'Nm/kg', 'Ext', 'Flx'),
            4: ('Ankle Dorsiflexor Moment', 'Nm/kg', 'Dor', 'Pla'),
            5: ('Subtalar Inverter Moment', 'Nm/kg', 'Inv', 'Eve'),
            6: ('Total Hip Power', 'W/kg', 'Gen', 'Abs'),
            7: ('Total Knee Power', 'W/kg', 'Gen', 'Abs'),
            8: ('Total Ankle Power', 'W/kg', 'Gen', 'Abs')
        }

        self._kinetic_plots[0].set_ylim(-2.0, 3.0)
        self._kinetic_plots[1].set_ylim(-1.0, 2.0)
        self._kinetic_plots[2].set_ylim(-0.5, 0.5)
        self._kinetic_plots[3].set_ylim(-1.0, 1.0)
        self._kinetic_plots[4].set_ylim(-1.5, 0.5)
        self._kinetic_plots[5].set_ylim(-0.5, 0.5)
        self._kinetic_plots[6].set_ylim(-3.0, 3.0)
        self._kinetic_plots[7].set_ylim(-3.0, 3.0)
        self._kinetic_plots[8].set_ylim(-1.0, 3.0)

        for i, plot in enumerate(self._kinetic_plots):
            plot.set_xlim(0, 100)
            plot.axhline(y=0, color='gray', linewidth=1.0, zorder=1)

            title, units, positive, negative = plot_labels.get(i, ("", "", ""))
            y_min, y_max = plot.get_ylim()
            step = (y_max - y_min) / 4

            plot.set_title(title, fontsize=10, pad=4)
            plot.text(x=0, y=y_min, s=y_min, ha='right', va='center', fontsize=9)
            plot.text(x=0, y=(y_min + 1 * step), s=negative, ha='right', va='center', fontsize=9)
            plot.text(x=0, y=(y_min + 2 * step), s=units, ha='right', va='center', fontsize=9)
            plot.text(x=0, y=(y_min + 3 * step), s=positive, ha='right', va='center', fontsize=9)
            plot.text(x=0, y=y_max, s=y_max, ha='right', va='center', fontsize=9)

            plot.set_xticks([0, 20, 40, 60, 80, 100])
            plot.tick_params(axis='x', which='both', bottom=True, labelbottom=False)
            if i in [6, 7, 8]:
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
            if item.checkState() == Qt.Checked:
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
            'output_data_directory': self._output_data_directory
        }

        return options

    def _set_options(self, options):
        self._line_width = options['line_width']
        self._input_data_directory = options['input_data_directory']
        self._output_data_directory = options['output_data_directory']

    def _show_marker_set_dialog(self):
        static_trials = []
        for i in range(self._ui.listWidgetFiles.count()):
            item = self._ui.listWidgetFiles.item(i)
            if item.checkState() == Qt.Checked:
                if item.data(Qt.UserRole) == "Static":
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
        settings.endGroup()

        settings.beginGroup('Options')
        settings.setValue('line_width', self._line_width)
        settings.setValue('input_data_directory', self._input_data_directory)
        settings.setValue('output_data_directory', self._output_data_directory)
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
        settings.endGroup()

        settings.beginGroup('Options')
        if settings.contains('line_width'):
            self._line_width = float(settings.value('line_width'))
        if settings.contains('input_data_directory'):
            self._input_data_directory = settings.value('input_data_directory')
        if settings.contains('output_data_directory'):
            self._output_data_directory = settings.value('output_data_directory')
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


class GaitCurves(defaultdict):

    def __init__(self, canvas):
        super().__init__(lambda: defaultdict(list))

        self._canvas = canvas
        self._canvas.mpl_connect('pick_event', lambda event: self.toggle_cycle(event))
        self._canvas.mpl_connect('button_press_event', lambda event: self.show_curve_menu(event))

        self._selected_curves = []
        self._excluded_cycles = set()

    def add_curve(self, file_name, cycle, curve):
        self[file_name][cycle].append(curve)

    def get_curves(self, file_name, cycle):
        return self[file_name][cycle]

    def set_file_visibility(self, file_name, visible):
        cycles = self[file_name]
        for cycle, lines in cycles.items():
            for line in lines:
                line.set_visible(visible)

        self._canvas.draw()

    def toggle_cycle(self, event):
        if event.mouseevent.button == 3:
            return

        line = event.artist
        for file_name, cycles in self.items():
            for cycle, lines in cycles.items():
                if line in lines:
                    identifier = (file_name, cycle)
                    if identifier in self._selected_curves:
                        self._selected_curves.remove(identifier)
                        colour = 'red' if "Left" in cycle else 'blue'
                        z_order = 2
                    else:
                        self._selected_curves.append(identifier)
                        colour = 'green'
                        z_order = 3

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

        self._canvas.draw()

    def include_all(self):
        for file_name, cycles in self.items():
            self.include_trial(file_name)
        self._selected_curves = []

    def include_trial(self, file_name):
        for cycle, lines in self[file_name].items():
            self._excluded_cycles.difference_update([(file_name, cycle), ])
            colour = 'red' if "Left" in cycle else 'blue'
            for line in lines:
                line.set_linestyle('solid')
                line.set_color(colour)
                line.set_zorder(2)

        self._canvas.draw()

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
        for cycle, lines in self[file_name].items():
            self._excluded_cycles.update([(file_name, cycle)], )
            colour = 'red' if "Left" in cycle else 'blue'
            for line in lines:
                line.set_linestyle('dotted')
                line.set_color(colour)
                line.set_zorder(1)

        self._canvas.draw()

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
