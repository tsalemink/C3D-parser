
import os
import copy
import numpy as np
import pandas as pd
import opensim as osim
import xml.etree.ElementTree as ET

from scipy.spatial.transform import Rotation

from c3d_parser.settings.logging import logger


osim_resources = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'osim_resources')
EXTERNAL_LOADS_TEMPLATE = ET.parse(os.path.join(osim_resources, 'external_loads_template.xml'))
DEFAULT_IK_TASK_SET = os.path.join(osim_resources, 'ik_task_set.xml')
osim.Logger.setLevel(osim.Logger.Level_Off)


def perform_ik(osim_file, trc_file, output_file, ik_task_set=None):
    model = osim.Model(osim_file)
    model.initSystem()

    ik_directory = os.path.dirname(output_file)
    error_file = os.path.join(ik_directory, '_ik_marker_errors.sto')

    ik_tool = osim.InverseKinematicsTool()
    ik_tool.setModel(model)
    ik_tool.setMarkerDataFileName(trc_file)
    if ik_task_set:
        ik_tool.set_IKTaskSet(osim.IKTaskSet(ik_task_set))
    else:
        ik_tool.set_IKTaskSet(osim.IKTaskSet(DEFAULT_IK_TASK_SET))
    ik_tool.setOutputMotionFileName(output_file)
    ik_tool.setResultsDir(ik_directory)
    ik_tool.set_report_errors(True)
    ik_tool.run()

    log_ik_errors(error_file)


def log_ik_errors(output_file):
    error_file = os.path.join(os.path.dirname(output_file), "_ik_marker_errors.sto")
    if not os.path.isfile(error_file):
        logger.warning(f"Could not find IK marker errors file: {error_file}.")
    storage = osim.Storage(error_file)

    rms_array = osim.ArrayDouble()
    max_array = osim.ArrayDouble()
    storage.getDataColumn("marker_error_RMS", rms_array)
    storage.getDataColumn("marker_error_max", max_array)

    rms_values = [rms_array.get(i) for i in range(rms_array.getSize())]
    max_values = [max_array.get(i) for i in range(max_array.getSize())]
    total_rmse = round((sum(v**2 for v in rms_values) / len(rms_values)) ** 0.5 * 1000, 1)
    max_error = round(max(max_values) * 1000, 1)

    logger.info(f"Total RMSE (IK): {total_rmse}mm. Max error (IK): {max_error}mm.")

    try:
        os.remove(error_file)
    except Exception as e:
        logger.warning(f"Unable to delete IK marker errors file: {error_file}. {e}")


def perform_id(osim_file, ik_file, grf_file, output_file):
    output_directory, output_file_name = os.path.split(output_file)
    external_loads_file = setup_external_loads(output_directory, grf_file)
    time_values = osim.TimeSeriesTable(ik_file).getIndependentColumn()

    model = osim.Model(osim_file)
    model.initSystem()

    id_tool = osim.InverseDynamicsTool()
    id_tool.setModel(model)
    id_tool.setCoordinatesFileName(ik_file)
    id_tool.setExternalLoadsFileName(external_loads_file)
    id_tool.setResultsDir(output_directory)
    id_tool.setOutputGenForceFileName(output_file_name)
    id_tool.setLowpassCutoffFrequency(8)
    id_tool.setStartTime(time_values[0])
    id_tool.setEndTime(time_values[-1])
    id_tool.run()

    os.remove(external_loads_file)


def setup_external_loads(output_directory, grf_file):
    grf_file_path = os.path.abspath(grf_file)
    grf_file_name = os.path.basename(grf_file)
    external_loads_file = os.path.join(output_directory, 'external_loads.xml')

    root = copy.deepcopy(EXTERNAL_LOADS_TEMPLATE.getroot())
    root.find("./ExternalLoads/datafile").text = grf_file_path
    root.find("./ExternalLoads/objects/ExternalForce[@name='externalforce_l']/data_source_name").text = grf_file_name
    root.find("./ExternalLoads/objects/ExternalForce[@name='externalforce_r']/data_source_name").text = grf_file_name

    tree = ET.ElementTree(root)
    tree.write(external_loads_file)

    return external_loads_file


def calculate_foot_progression_angles(model_file, ik_file):

    # Load model information.
    model = osim.Model(model_file)
    model.initSystem()
    coordinate_set = model.getCoordinateSet()
    n_coordinates = coordinate_set.getSize()

    # Load IK solution.
    storage = osim.Storage(ik_file)
    labels = storage.getColumnLabels()
    n_frames = storage.getSize()

    foot_progression = {"l": [], "r": []}
    for i in range(n_frames):

        # Build a state vector from the IK solution at this frame.
        time_stamp = storage.getStateVector(i).getTime()
        state = model.initSystem()
        state.setTime(time_stamp)
        ik_row = storage.getStateVector(i).getData()

        # Set body coordinates from the IK solution.
        for j in range(n_coordinates):
            coordinate = coordinate_set.get(j)
            coordinate_name = coordinate.getName()
            column_index = labels.findIndex(coordinate_name)
            if column_index >= 0:
                value = ik_row.get(column_index - 1)

                if coordinate.getMotionType() == osim.Coordinate.Rotational:
                    value = np.deg2rad(value)
                coordinate.setValue(state, value)
        model.realizePosition(state)

        # Extract foot segment rotation.
        for side in foot_progression.keys():
            foot_body = model.getBodySet().get(f"calcn_{side}")
            transform = foot_body.getTransformInGround(state)

            # Decompose rotation matrix into ZXY Euler angles.
            rotation_matrix = np.array([[transform.R().get(row, col) for col in range(3)] for row in range(3)])
            angles = Rotation.from_matrix(rotation_matrix).as_euler('ZXY')
            foot_progression_angle = np.rad2deg(angles[2])

            if side == "l":
                foot_progression_angle = -foot_progression_angle
            foot_progression[side].append(foot_progression_angle)

    data_frame = pd.DataFrame({
        "foot_progression_l": foot_progression["l"],
        "foot_progression_r": foot_progression["r"],
    })
    return data_frame
