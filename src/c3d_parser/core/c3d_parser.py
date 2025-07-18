
import os
import re
import math
import json
import logging
import numpy as np
import pandas as pd

from collections import defaultdict
from scipy import signal, interpolate
from scipy.spatial.transform import Rotation

from trc import TRCData
from opensim_model_creator.Create_Model import create_model

from c3d_parser.core.c3d_patch import c3d
from c3d_parser.core.osim import perform_ik, perform_id
from c3d_parser.settings.logging import logger


script_directory = os.path.dirname(os.path.abspath(__file__))
marker_maps_dir = os.path.join(script_directory, 'marker_maps')


class ParserError(Exception):
    pass


class CancelException(Exception):
    pass


def parse_session(static_trial, dynamic_trials, input_directory, output_directory, lab, marker_diameter, static_data,
                  optimise_knee_axis, progress_tracker):

    file_path = os.path.normpath(os.path.join(input_directory, static_trial))
    frame, static_trc_path, height, weight = parse_static_trial(file_path, lab, marker_diameter, output_directory,
                                                                static_data)

    marker_data_rate = 100

    grf_data = {}
    event_data = {}
    spatiotemporal_data = {}
    foot_progression_data = {}
    kinematic_data = {}
    kinetic_data = {}

    trc_file_paths = {}
    grf_file_paths = {}
    deidentified_file_names = {}

    progress_tracker.progress.emit("Processing C3D data", "black")

    for trial_index, trial in enumerate(dynamic_trials, start=1):
        file_path = os.path.normpath(os.path.join(input_directory, trial))
        try:
            analog_data, events, foot_progression, s_t_data, trc_file_path, grf_file_path = \
                parse_dynamic_trial(file_path, lab, output_directory, trial_index, marker_data_rate, static_data)
        except ParserError as e:
            logger.error(e)
            continue

        grf_data[trial] = analog_data
        event_data[trial] = events
        spatiotemporal_data[trial] = s_t_data
        foot_progression_data[trial] = foot_progression

        trc_file_paths[trial] = trc_file_path
        grf_file_paths[trial] = grf_file_path
        deidentified_file_names[trial] = os.path.basename(trc_file_path).rsplit(".", 1)[0]

    dynamic_trc_path = list(trc_file_paths.values())[0] if dynamic_trials else ""
    osim_model = create_osim_model(static_trc_path, dynamic_trc_path, frame, height, weight,
                                   output_directory, optimise_knee_axis, progress_tracker)

    if not dynamic_trials:
        raise CancelException("No dynamic trials found.")

    progress_tracker.progress.emit("Running IK and ID", "black")

    for trial in dynamic_trials:
        ik_data, ik_output = run_ik(osim_model, trc_file_paths[trial], output_directory, marker_data_rate)
        ik_data = pd.concat([ik_data, foot_progression_data[trial]], axis=1)
        id_data = run_id(osim_model, ik_data, ik_output, grf_file_paths[trial], output_directory, marker_data_rate, event_data[trial], weight)

        kinematic_data[trial] = ik_data
        kinetic_data[trial] = id_data

    normalised_grf_data = normalise_grf_data(grf_data, event_data)
    normalised_kinematics = normalise_kinematics(kinematic_data, event_data)
    normalised_kinetics = normalise_kinetics(kinetic_data, event_data)

    return normalised_grf_data, normalised_kinematics, normalised_kinetics, spatiotemporal_data, deidentified_file_names


def parse_static_trial(c3d_file, lab, marker_diameter, output_directory, static_data):
    logger.info(f"Parsing static trial: {c3d_file}")

    output_file_name = 'static'
    c3d_file_name = os.path.basename(c3d_file)
    file_name = os.path.splitext(c3d_file_name)[0]
    de_identify_c3d(c3d_file, output_directory, output_file_name)

    # Harmonise TRC data.
    trc_data = TRCData()
    trc_data.import_from(c3d_file)
    frame_data = extract_marker_data(trc_data)
    harmonise_markers(frame_data, lab)
    rotation_matrix = get_static_rotation(frame_data)
    rotate_trc_data(frame_data, rotation_matrix)
    set_marker_data(trc_data, frame_data)
    trc_file_path = write_trc_data(trc_data, output_file_name, output_directory)

    _, _, height, weight, _, left_knee_width, right_knee_width, _, _, _, _ = static_data
    frame = add_medial_knee_markers(frame_data, left_knee_width, right_knee_width, marker_diameter)

    return frame, trc_file_path, height, weight


def parse_dynamic_trial(c3d_file, lab, output_directory, trial_index, marker_data_rate, static_data):
    logger.info(f"Parsing dynamic trial: {c3d_file}")

    output_file_name = f'dynamic_{trial_index}'
    c3d_file_name = os.path.basename(c3d_file)
    file_name = os.path.splitext(c3d_file_name)[0]
    de_identify_c3d(c3d_file, output_directory, output_file_name)

    # Harmonise TRC data.
    trc_data = TRCData()
    trc_data.import_from(c3d_file)
    frame_data = extract_marker_data(trc_data)
    harmonise_markers(frame_data, lab)

    # Extract GRF data from C3D file.
    start_frame, end_frame = trim_frames(frame_data)
    filter_data(frame_data, trc_data['DataRate'])
    frame_data = resample_data(frame_data, trc_data['DataRate'], marker_data_rate)
    analog_data, data_rate, events, plate_count, corners = extract_data(c3d_file, start_frame, end_frame)

    # Match events to force plates.
    identify_event_plates(frame_data, events, corners)
    validate_foot_strikes(events)

    # Harmonise GRF data.
    filter_data(analog_data, data_rate)
    analog_data = resample_data(analog_data, data_rate, frequency=1000)
    zero_grf_data(analog_data, plate_count)
    analog_data = calculate_force_and_couple(analog_data, plate_count)
    transform_grf_coordinates(analog_data, plate_count, corners)
    mean_centre = transform_cop(analog_data, corners)
    analog_data = concatenate_grf_data(analog_data, events, mean_centre)
    scale_grf_data(analog_data)

    # Rotate trials for +X walking direction.
    rotation_matrix = get_global_rotation(frame_data)
    rotate_trc_data(frame_data, rotation_matrix)
    rotate_grf_data(analog_data, rotation_matrix)

    # Write GRF data.
    grf_directory = os.path.join(output_directory, 'grf')
    if not os.path.exists(grf_directory):
        os.makedirs(grf_directory)
    grf_file_name = re.sub(r' +', '_', output_file_name)
    grf_file_path = os.path.join(grf_directory, f"{grf_file_name}_grf.mot")
    write_grf(analog_data, grf_file_path)

    # Write harmonised TRC data.
    set_marker_data(trc_data, frame_data, rate=marker_data_rate)
    trc_file_path = write_trc_data(trc_data, output_file_name, output_directory)

    foot_progression = calculate_foot_progression_angles(frame_data)
    resample_data(foot_progression, trc_data['DataRate'], marker_data_rate)

    s_t_data = calculate_spatiotemporal_data(frame_data, events, static_data)

    return analog_data, events, foot_progression, s_t_data, trc_file_path, grf_file_path


def run_ik(osim_model, trc_file_path, output_directory, marker_data_rate):
    # Perform inverse kinematics.
    file_name = os.path.splitext(os.path.basename(trc_file_path))[0]
    ik_directory = os.path.join(output_directory, 'ik')
    if not os.path.exists(ik_directory):
        os.makedirs(ik_directory)
    ik_output = os.path.join(ik_directory, f"{file_name}_IK.mot")
    perform_ik(osim_model, trc_file_path, ik_output)
    ik_data = read_data(ik_output)
    filter_data(ik_data, marker_data_rate)

    return ik_data, ik_output


def run_id(osim_model, ik_data, ik_output, grf_file_path, output_directory, marker_data_rate, events, subject_mass):
    # Perform inverse dynamics.
    file_name = os.path.basename(grf_file_path).replace("_grf.mot", "")
    id_directory = os.path.join(output_directory, 'id')
    if not os.path.exists(id_directory):
        os.makedirs(id_directory)
    id_output = os.path.join(id_directory, f"{file_name}_ID.sto")
    perform_id(osim_model, ik_output, grf_file_path, id_output)
    id_data = read_data(id_output)
    filter_data(id_data, marker_data_rate)
    calculate_joint_powers(ik_data, id_data, events)
    mass_adjust_units(id_data, subject_mass)

    return id_data


def de_identify_c3d(file_path, output_directory, output_file_name):
    output_directory = os.path.join(output_directory, 'de_identified')
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    input_directory, _ = os.path.split(os.path.abspath(file_path))
    output_directory = os.path.abspath(output_directory)

    # Currently we prevent overwriting the input file.
    if input_directory == output_directory:
        raise IOError("Cannot overwrite input file.")

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    def de_identify_string_array(group_name, parameter_name, new_value='Subject'):
        if group_name in reader:
            analysis_group = writer.get(group_name)
            if parameter_name in analysis_group.param_keys():
                array_length = len(analysis_group.get(parameter_name).string_array)
                if array_length:
                    analysis_group.remove_param(parameter_name)
                    label_str, maxlen = c3d.Writer.pack_labels([new_value] * array_length)
                    analysis_group.add_str(parameter_name, '', label_str, maxlen, array_length)

    with open(file_path, 'rb') as handle:
        reader = c3d.Reader(handle)
        writer = reader.to_writer('copy')

        de_identify_string_array('SUBJECTS', 'NAMES')
        de_identify_string_array('ANALYSIS', 'SUBJECTS')

    with open(os.path.join(output_directory, output_file_name), 'wb') as handle:
        writer.write(handle)


def extract_marker_data(trc_data):
    frames = {}
    for frame_number in trc_data['Frame#']:
        time, frame = trc_data[frame_number]
        frames[frame_number] = [time, *map(np.array, frame)]
    frame_data = pd.DataFrame.from_dict(frames, orient='index')
    frame_data.columns = ['Time', *trc_data['Markers']]

    return frame_data


def set_marker_data(trc_data, frame_data, rate=100):
    # Clear existing frame data.
    for frame_number in trc_data['Frame#']:
        del trc_data[frame_number]

    trc_data['Markers'] = frame_data.columns[1:]
    trc_data['NumMarkers'] = len(trc_data['Markers'])
    trc_data['Frame#'] = []
    for frame_number, frame in frame_data.iterrows():
        frame_time, *data = frame
        trc_data['Frame#'].append(frame_number)
        trc_data[frame_number] = [frame_time, data]

    # Set additional information.
    trc_data['DataRate'] = rate
    trc_data['CameraRate'] = rate
    trc_data['NumFrames'] = frame_data.shape[0]


def write_trc_data(trc_data, file_name, output_directory):
    trc_directory = os.path.join(output_directory, 'trc')
    if not os.path.exists(trc_directory):
        os.makedirs(trc_directory)
    trc_file_path = os.path.join(trc_directory, f"{file_name}.trc")
    trc_data.save(trc_file_path, add_trailing_tab=True)

    return trc_file_path


def get_marker_map(lab):
    map_file = os.path.join(marker_maps_dir, f"{lab}.json")
    with open(map_file, 'r') as file:
        marker_mapping = json.load(file)

    return marker_mapping


def get_marker_set(lab):
    marker_mapping = get_marker_map(lab)

    singular = ['C7', 'T2', 'T10', 'MAN', 'SACR']
    marker_set = {}
    for key, value in marker_mapping.items():
        if key in singular:
            marker_set[key] = value
        else:
            marker_set[f"L{key}"] = f"L{value}" if value is not None else None
            marker_set[f"R{key}"] = f"R{value}" if value is not None else None

    return marker_set

def harmonise_markers(frame_data, lab):
    marker_set = get_marker_set(lab)

    # Harmonise marker labels.
    reversed_mapping = {value: key for key, value in marker_set.items() if value is not None}
    header_mapping = {header: reversed_mapping.get(header, None) for header in frame_data.columns[1:]}
    frame_data.rename(columns=header_mapping, inplace=True)

    # Filter out non-harmonised data points.
    if None in frame_data.columns:
        frame_data.drop(columns=[None], axis=1, inplace=True)


def trim_frames(frame_data):
    first_frame = frame_data.index.min()
    last_frame = frame_data.index.max()

    # Check for incomplete frames.
    incomplete_frames = {}
    for frame_number, frame in frame_data.iterrows():
        missing_markers = []
        for marker_index in range(1, len(frame)):
            coordinates = frame.iloc[marker_index]
            if math.isnan(coordinates[0]):
                missing_markers.append(frame_data.columns[marker_index])
        if missing_markers:
            incomplete_frames[frame_number] = missing_markers

    if len(incomplete_frames) >= 0.9 * len(frame_data):
        raise ParserError("Too many frames missing marker data. Unable to process trial.")

    # Trim incomplete frames near the beginning or end of the trial.
    trim_start = first_frame
    for frame in incomplete_frames:
        if (frame - trim_start) > 20:
            break
        trim_start = frame + 1
    trim_end = last_frame
    for frame in reversed(incomplete_frames):
        if (trim_end - frame) > 20:
            break
        trim_end = frame - 1

    if incomplete_frames:
        logger.warn(f"Some frames are missing required markers. "
                    f"Trimming trial from frame {trim_start} to frame {trim_end}.")

    frame_list = frame_data.index.to_list()
    complete_frames = frame_list[frame_list.index(trim_start):frame_list.index(trim_end) + 1]
    drop_frames = frame_data.index.difference(complete_frames)
    if not drop_frames.empty:
        frame_data.drop(drop_frames, inplace=True)

    remaining_frames = [frame for frame in incomplete_frames.keys() if trim_start <= frame <= trim_end]
    if remaining_frames:
        logger.warn(f"Frames {remaining_frames} are incomplete.")

    return trim_start, trim_end


def filter_data(frame_data, data_rate, cut_off_frequency=8):
    # Determine filter coefficients
    Wn = cut_off_frequency / (data_rate / 2)
    b, a = signal.butter(2, Wn)

    # Filter each marker trajectory.
    for marker in frame_data.columns[1:]:
        marker_trajectory = frame_data.loc[:, marker].values
        filtered_trajectory = signal.filtfilt(b, a, marker_trajectory, axis=0)
        frame_data.loc[:, marker] = filtered_trajectory


def resample_data(frame_data, data_rate, frequency=100):
    if data_rate == frequency:
        return frame_data

    start_time = frame_data.iloc[:, 0].iat[0]
    end_time = frame_data.iloc[:, 0].iat[-1]
    number_of_frames = int((end_time - start_time) * frequency)
    time_array = np.linspace(start_time, end_time, number_of_frames)

    resampled_frame_data = pd.DataFrame(columns=frame_data.columns)
    resampled_frame_data.iloc[:, 0] = time_array

    for column in frame_data.columns[1:]:
        trajectory = np.stack(frame_data.loc[:, column].values)

        # Resample analog data.
        if trajectory.ndim == 1:
            tck = interpolate.splrep(frame_data.iloc[:, 0].values, trajectory, s=0)
            resampled_trajectory = interpolate.splev(time_array, tck, der=0)

        # Resample marker data.
        else:
            resampled_trajectory = []
            for axis in trajectory.transpose():
                tck = interpolate.splrep(frame_data.iloc[:, 0].values, axis, s=0)
                resampled_trajectory.append(interpolate.splev(time_array, tck, der=0))
            resampled_trajectory = np.stack(resampled_trajectory).transpose()

        # Adjust frame format to support row iteration.
        flattened_array = np.empty(resampled_trajectory.shape[0], dtype=object)
        for i in range(resampled_trajectory.shape[0]):
            flattened_array[i] = resampled_trajectory[i]
        resampled_frame_data.loc[:, column] = flattened_array
        resampled_frame_data.index = pd.RangeIndex(start=1, stop=len(resampled_frame_data) + 1, step=1)

    return resampled_frame_data


def get_global_rotation(frame_data):
    r_asis = frame_data["RASI"].values
    difference = r_asis[-1] - r_asis[0]
    primary_axis = np.argmax(np.abs(difference))
    trial_direction = np.zeros(3)
    trial_direction[primary_axis] = np.sign(difference[primary_axis])

    angle = -np.arctan2(trial_direction[1], trial_direction[0])
    rotation_matrix = np.round(Rotation.from_euler('z', angle).as_matrix())

    return rotation_matrix


def get_static_rotation(frame_data):
    for l_asis, r_asis in zip(frame_data["LASI"], frame_data["RASI"]):
        if not (np.any(np.isnan(l_asis)) or np.any(np.isnan(r_asis))):
            asis_vector = l_asis - r_asis
            unit_vector = asis_vector / np.linalg.norm(asis_vector)

            angle = np.arctan2(unit_vector[0], unit_vector[1])
            rotation_matrix = Rotation.from_euler('z', angle).as_matrix()

            return rotation_matrix
    raise ParserError("ASIS markers not found. Cannot determine static trial rotation.")


def rotate_trc_data(frame_data, rotation_matrix):
    identity_matrix = np.eye(3)
    if np.array_equal(rotation_matrix, identity_matrix):
        return

    for column in frame_data.columns[1:]:
        frame_data[column] = frame_data[column].apply(
            lambda x: rotation_matrix @ np.array(x)
        )


def rotate_grf_data(analog_data, rotation_matrix):
    identity_matrix = np.eye(3)
    if np.array_equal(rotation_matrix, identity_matrix):
        return

    for i in range(1, analog_data.columns.size, 3):
        rotated_values = analog_data.iloc[:, i:i + 3].apply(
            lambda row: rotation_matrix @ row.values, axis=1
        )
        analog_data.iloc[:, i:i + 3] = np.vstack(rotated_values)


def extract_marker_names(filename):
    with open(filename, 'rb') as handle:
        reader = c3d.Reader(handle)

    # Filter out model outputs (Angles, Forces, Moments, Powers, Scalars) from point labels.
    point_group = reader.get('POINT')
    model_outputs = set()
    for param in ['ANGLES', 'FORCES', 'MOMENTS', 'POWERS', 'SCALARS']:
        if param in point_group.param_keys():
            model_outputs.update(point_group.get(param).string_array)

    point_labels = []
    if 'LABELS' in point_group.param_keys():
        filtered_labels = [None if label in model_outputs else label.strip() for label in point_group.get('LABELS').string_array]
        point_labels.extend(filtered_labels)
    i = 2
    while f'LABELS{i}' in point_group.param_keys():
        filtered_labels = [None if label in model_outputs else label.strip() for label in point_group.get(f'LABELS{i}').string_array]
        point_labels.extend(filtered_labels)
    point_labels = list(filter(None, point_labels))

    marker_names = []
    for item in point_labels:
        if item.startswith('L') and f'R{item[1:]}' in point_labels:
            marker_names.append(item[1:])
        elif not (item.startswith('L') or item.startswith('R')):
            marker_names.append(item)

    return marker_names


def extract_data(file_path, start_frame, end_frame):
    with open(file_path, 'rb') as handle:
        reader = c3d.Reader(handle)

        if reader.analog_used == 0:
            raise ParserError("No analog data found in dynamic trial.")
        if 'EVENT' not in reader:
            raise ParserError("No events found in dynamic trial.")

        # Extract analog data
        time_increment = 1 / reader.analog_rate
        start = (start_frame - 1) / reader.point_rate
        stop = end_frame / reader.point_rate - (time_increment / 2)
        times = np.arange(start, stop, time_increment).tolist()
        analog_data = {'time': times}

        labels = reader.get('ANALOG:LABELS').string_array
        analog_data.update({label: [] for label in labels})
        for i, points, analog in reader.read_frames():
            if i < start_frame or end_frame < i:
                continue

            for j, label in enumerate(analog_data):
                if j == 0:
                    continue
                analog_data[label].extend(analog[j - 1])
        analog_data = pd.DataFrame(analog_data)

        # Extract event information.
        event_group = reader.get('EVENT')
        event_count = event_group.get('USED').int8_value
        contexts = event_group.get('CONTEXTS').string_array
        labels = event_group.get('LABELS').string_array
        times = event_group.get('TIMES').float_array
        events = {'Left': {}, 'Right': {}}

        for i in range(event_count):
            foot = contexts[i].strip()
            label = labels[i].strip()
            event_time = times[i][1]
            events[foot][event_time] = label

        for foot in events.keys():
            events[foot] = dict(sorted(events[foot].items()))

        # Annotate stride numbers.
        annotated_events = {'Left': {}, 'Right': {}}
        stride_numbers = {"Left": 0, "Right": 0}
        for foot, event in events.items():
            for event_time, event_type in event.items():
                if event_type == "Foot Strike":
                    stride_numbers[foot] += 1
                stride_number = stride_numbers[foot]

                if stride_number not in annotated_events[foot]:
                    annotated_events[foot][stride_number] = {}
                annotated_events[foot][stride_number][event_time] = event_type

        # Remove events outside the trimmed frame range.
        trimmed_events = {'Left': {}, 'Right': {}}
        for foot, events in annotated_events.items():
            for stride_number, stride_events in events.items():
                for event_time, event_type in stride_events.items():
                    if start < event_time < stop:
                        if stride_number not in trimmed_events[foot]:
                            trimmed_events[foot][stride_number] = {}
                        trimmed_events[foot][stride_number][event_time] = event_type
                    else:
                        logger.warn(f"Event at {event_time}s is outside the trial's valid range "
                                    f"of time stamps ({start}s - {stop}s).")

        # Get number of force plates.
        plate_count = reader.get('FORCE_PLATFORM:USED').int8_value

        # Rotate GRF data to align with global CS.
        corners = reader.get('FORCE_PLATFORM:CORNERS').float_array

    return analog_data, reader.analog_rate, trimmed_events, plate_count, corners


def extract_static_data(file_path):
    with open(file_path, 'rb') as handle:
        reader = c3d.Reader(handle)

        if 'PROCESSING' not in reader:
            logger.warn("No processing section found in static trial.")
            return None, None, None, None, None, None

        processing_group = reader.get('PROCESSING')
        height = weight = asis_width = left_knee_width = right_knee_width = None
        left_ankle_width = right_ankle_width = left_leg_length = right_leg_length = None

        if 'HEIGHT' in processing_group:
            height = reader.get('PROCESSING:Height').float_value
        if 'BODYMASS' in processing_group:
            weight = reader.get('PROCESSING:Bodymass').float_value
        if 'INTERASISDISTANCE' in processing_group:
            asis_width = reader.get('PROCESSING:InterAsisDistance').float_value
        if 'LKNEEWIDTH' in processing_group:
            left_knee_width = reader.get('PROCESSING:LKneeWidth').float_value
        if 'RKNEEWIDTH' in processing_group:
            right_knee_width = reader.get('PROCESSING:RKneeWidth').float_value
        if 'LANKLEWIDTH' in processing_group:
            left_ankle_width = reader.get('PROCESSING:LAnkleWidth').float_value
        if 'RANKLEWIDTH' in processing_group:
            right_ankle_width = reader.get('PROCESSING:RAnkleWidth').float_value
        if 'LLEGLENGTH' in processing_group:
            left_leg_length = reader.get('PROCESSING:LLegLength').float_value
        if 'RLEGLENGTH' in processing_group:
            right_leg_length = reader.get('PROCESSING:RLegLength').float_value

    return (height, weight, asis_width, left_knee_width, right_knee_width,
            left_ankle_width, right_ankle_width, left_leg_length, right_leg_length)


def read_grf(file_path):
    with open(file_path, 'r') as file:
        # Skip header.
        for _ in range(7):
            next(file)

        # Read GRF data.
        column_labels = file.readline().strip().split('\t')
        analog_data = pd.read_csv(file, sep='\t', header=None, names=column_labels)

    return analog_data


def write_grf(analog_data, file_path):
    with open(file_path, 'w') as file:
        row_count, column_count = analog_data.shape

        # Write header.
        file.write(f"{os.path.basename(file_path)}\n")
        file.write("version=1\n")
        file.write(f"nRows={row_count}\n")
        file.write(f"nColumns={column_count}\n")
        file.write("inDegrees=yes\n")
        file.write("endheader\n\n")

        # Write labels.
        for label in analog_data.columns:
            file.write(f"{label.strip()}\t")
        file.write("\n")

    # Write GRF data.
    with open(file_path, 'a') as file:
        np.savetxt(file, analog_data.values, fmt='%0.6f', delimiter='\t')


def calculate_force_and_couple(analog_data, plate_count):
    new_data = pd.DataFrame(analog_data['time'])

    for i in range(plate_count):
        start = 1 + (6 * i)
        columns = list(range(start, start + 6))
        Fx, Fy, Fz, Mx, My, Mz = analog_data.iloc[:, columns].values.T

        with np.errstate(divide='ignore', invalid='ignore'):
            CoPx = np.where(Fz != 0, -(My + Fx) / Fz, 0)
            CoPy = np.where(Fz != 0, (Mx - Fy) / Fz, 0)
        Tz = Mz - CoPx * Fy + CoPy * Fx

        new_data[f'Fx{i + 1}'] = Fx
        new_data[f'Fy{i + 1}'] = Fy
        new_data[f'Fz{i + 1}'] = Fz
        new_data[f'CoPx{i + 1}'] = CoPx
        new_data[f'CoPy{i + 1}'] = CoPy
        new_data[f'CoPz{i + 1}'] = np.zeros(len(analog_data))
        new_data[f'Tx{i + 1}'] = np.zeros(len(analog_data))
        new_data[f'Ty{i + 1}'] = np.zeros(len(analog_data))
        new_data[f'Tz{i + 1}'] = Tz

    return new_data


def transform_grf_coordinates(analog_data, plate_count, corners):
    # Rotate GRF data to align with global CS.
    for i in range(plate_count):
        plate = corners[i]
        x_vector = plate[0] - plate[1]
        y_vector = plate[0] - plate[3]
        x_unit_vector = x_vector / np.linalg.norm(x_vector)
        y_unit_vector = y_vector / np.linalg.norm(y_vector)
        force_plate_axes = [x_unit_vector, y_unit_vector]
        global_axes = [[1, 0, 0], [0, 1, 0]]
        rotation, _ = Rotation.align_vectors(force_plate_axes, global_axes)
        rotation_matrix = rotation.as_matrix()

        start = 1 + (9 * i)
        for j in [start, start + 3, start + 6]:
            columns = list(range(j, j + 3))
            values = analog_data.iloc[:, columns]
            transformed_values = values.apply(lambda row: np.dot(rotation_matrix, row), axis=1)
            analog_data.iloc[:, columns] = transformed_values.tolist()


def zero_grf_data(analog_data, plate_count):
    for i in range(plate_count):
        start = 1 + (6 * i)
        columns = list(range(start, start + 6))
        mask = analog_data.iloc[:, columns[2]] > 0
        analog_data.iloc[mask, columns] = 0


def identify_event_plates(frame_data, events, corners):

    def identify_plate(coordinates):
        for plate in range(len(corners)):
            if point_on_plate(coordinates, corners[plate]):
                events[foot][stride_number][event_time] = [event_type, plate]
                break
            else:
                events[foot][stride_number][event_time] = [event_type, None]

    for foot, foot_events in events.items():
        for stride_number, stride_events in foot_events.items():
            for event_time, event_type in stride_events.items():
                event_index = frame_data[frame_data['Time'] <= event_time].index[-1]
                if event_type == "Foot Strike":
                    heel_coordinates = frame_data.at[event_index, foot[0] + 'HEE']
                    identify_plate(heel_coordinates)
                else:
                    toe_coordinates = frame_data.at[event_index, foot[0] + 'TOE']
                    identify_plate(toe_coordinates)


def validate_foot_strikes(events):
    invalid_strides = {'Left': set(), 'Right': set()}
    time_ordered_strikes = {}
    for foot, foot_events in events.items():
        for stride_number, stride_events in foot_events.items():
            for event_time, (event_type, event_plate) in stride_events.items():
                if event_type == "Foot Strike":
                    time_ordered_strikes[event_time] = (foot, stride_number, event_plate)

            if len(stride_events) == 2:
                strike, off = stride_events.values()
                if strike[1] != off[1]:
                    logger.warn(f"Stride ({foot} {stride_number}) is invalid. "
                                f"Stride occurs over multiple force plates.")
                    invalid_strides[foot].add(stride_number)

            if len(stride_events) > 2:
                logger.warn(f"Stride ({foot} {stride_number}) is invalid. "
                            f"Additional events detected in stride.")
                invalid_strides[foot].add(stride_number)

    time_ordered_strikes = dict(sorted(time_ordered_strikes.items()))
    previous_strike = (None, None, None)
    for event_time, (foot, stride_number, event_plate) in time_ordered_strikes.items():
        previous_foot, previous_stride, previous_plate = previous_strike

        off_plate = None
        if previous_foot is not None:
            for event in events[previous_foot][previous_stride].values():
                if event[0] == "Foot Off":
                    off_plate = event[1]
                    break

        if event_plate == off_plate and off_plate is not None:
            logger.warn(f"Strides ({previous_foot} {previous_stride}) and ({foot} {stride_number}) "
                        f"are invalid. Consecutive strides occur on the same force plate.")
            invalid_strides[previous_foot].add(previous_stride)
            invalid_strides[foot].add(stride_number)
        previous_strike = (foot, stride_number, event_plate)

    for foot, strides in invalid_strides.items():
        for stride_number in strides:
            for event in events[foot][stride_number].values():
                event[1] = None


def point_on_plate(point, corners):
    x_coordinates = [corner[0] for corner in corners]
    y_coordinates = [corner[1] for corner in corners]
    min_x, max_x = min(x_coordinates), max(x_coordinates)
    min_y, max_y = min(y_coordinates), max(y_coordinates)

    return min_x <= point[0] <= max_x and min_y <= point[1] <= max_y


def transform_cop(analog_data, corners):
    centres = np.zeros((len(corners), 3))
    for i, plate_corners in enumerate(corners):
        centre = np.mean(plate_corners, axis=0)
        centres[i] = centre

        CoPx = analog_data.iloc[:, i * 9 + 4]
        CoPy = analog_data.iloc[:, i * 9 + 5]

        analog_data.iloc[:, i * 9 + 4] = CoPx + centre[0]
        analog_data.iloc[:, i * 9 + 5] = CoPy + centre[1]

    return np.mean(centres, axis=0)


def concatenate_grf_data(analog_data, events, mean_centre):
    columns = ["ground_force_vx", "ground_force_vy", "ground_force_vz",
               "ground_force_px", "ground_force_py", "ground_force_pz",
               "ground_torque_x", "ground_torque_y", "ground_torque_z",
               "1_ground_force_vx", "1_ground_force_vy", "1_ground_force_vz",
               "1_ground_force_px", "1_ground_force_py", "1_ground_force_pz",
               "1_ground_torque_x", "1_ground_torque_y", "1_ground_torque_z"]
    concatenated_data = pd.DataFrame(columns=['time'] + columns)
    concatenated_data['time'] = analog_data['time']
    for column in columns:
        if "px" in column:
            concatenated_data[column] = mean_centre[0]
        elif "py" in column:
            concatenated_data[column] = mean_centre[1]
        else:
            concatenated_data[column] = 0.0

    def copy_data():
        frames = range(start, end + 1)
        data = analog_data.iloc[frames, source_columns].values
        concatenated_data.iloc[frames, target_columns] = data

    for foot, foot_events in events.items():
        i = 0 if foot == "Left" else 1
        target_columns = range(i * 9 + 1, i * 9 + 10)

        for stride_number, stride_events in foot_events.items():
            if len(stride_events) >= 2:
                stride_items = list(stride_events.items())
                start_time, (_, strike_plate) = stride_items[0]
                end_time, (_, off_plate) = stride_items[1]
                if strike_plate is None or off_plate is None or strike_plate != off_plate:
                    continue
                source_columns = range(strike_plate * 9 + 1, strike_plate * 9 + 10)

                start = analog_data[analog_data['time'] <= start_time].index[-1]
                while analog_data.iloc[start, source_columns[2]] > 0:
                    start -= 1
                end = analog_data[analog_data['time'] <= end_time].index[-1]
                while analog_data.iloc[end, source_columns[2]] > 0:
                    end += 1

                new_start_time = analog_data.iloc[start]['time']
                new_end_time = analog_data.iloc[end]['time']
                if new_start_time < start_time - 0.2:
                    logger.warn(f"Interference detected on force plate at the beginning of "
                                f"stride ({foot} {stride_number}).")
                    start = analog_data[analog_data['time'] <= start_time].index[-1]
                if end_time + 0.2 < new_end_time:
                    logger.warn(f"Interference detected on force plate at the end of stride "
                                f"({foot} {stride_number}).")
                    end = analog_data[analog_data['time'] <= end_time].index[-1]

                copy_data()
                start, end = None, None

    # Change header order for OpenSim.
    concatenated_data = concatenated_data.iloc[:,
                        [0, 1, 2, 3, 4, 5, 6, 10, 11, 12, 13, 14, 15, 7, 8, 9, 16, 17, 18]]

    return concatenated_data


def scale_grf_data(analog_data):
    columns = [
        'ground_force_px', 'ground_force_py', 'ground_force_pz',
        '1_ground_force_px', '1_ground_force_py', '1_ground_force_pz',
        'ground_torque_x', 'ground_torque_y', 'ground_torque_z',
        '1_ground_torque_x', '1_ground_torque_y', '1_ground_torque_z'
    ]
    analog_data[columns] = analog_data[columns] / 1000


def is_dynamic(file_path):
    with open(file_path, 'rb') as handle:
        try:
            logging.disable()
            reader = c3d.Reader(handle)
        finally:
            logging.disable(logging.NOTSET)

        if reader.analog_used > 0 and reader.frame_count > 100:
            return True
        else:
            return False


def read_data(file_path):
    with open(file_path, 'r') as file:
        labels, data = [], []
        for line in file:
            if line.strip() == "endheader":
                while not (line := next(file).strip()):
                    continue
                labels = line.split()
                break
        for line in file:
            data.append([float(x) for x in line.strip().split()])

    return pd.DataFrame(data, columns=labels)


def mass_adjust_units(kinetic_data, subject_mass):
    kinetic_data.iloc[:, 1:] /= subject_mass


def calculate_joint_powers(kinematic_data, kinetic_data, events):
    time = kinematic_data['time'].values
    for joint in ['hip_flexion', 'knee_flexion', 'ankle_angle']:
        for leg in ['l', 'r']:
            joint_angle = kinematic_data[f'{joint}_{leg}'].values
            joint_moment = kinetic_data[f'{joint}_{leg}_moment'].values
            angular_velocity = calculate_angular_velocity(joint_angle, time)
            kinetic_data[f'{joint}_{leg}_power'] = angular_velocity * joint_moment


def calculate_angular_velocity(joint_angle, time):
    joint_angle_radians = np.deg2rad(joint_angle)
    return np.gradient(joint_angle_radians, time)


def normalise_grf_data(data, events):
    normalised_data = {"Left": {}, "Right": {}}
    for i in range(len(data)):
        file_name = list(data.keys())[i]
        grf_data = list(data.values())[i]
        trial_events = list(events.values())[i]

        for foot, foot_events in trial_events.items():
            column = 1 if foot == "Left" else 7
            force_data = grf_data.iloc[:, [0, *range(column, column + 3)]]

            start = None
            for stride_number, stride_events in foot_events.items():
                (event_time, (event_type, event_plate)), *_ = stride_events.items()
                frame = force_data[force_data['time'] <= event_time].index[-1]
                if event_type == "Foot Strike" and start:
                    while force_data.iloc[frame, 3] > 0:
                        frame -= 1
                    if file_name not in normalised_data[foot]:
                        normalised_data[foot][file_name] = {}
                    data_segment = force_data.iloc[start:frame, 1:]
                    start = None if event_plate is None else frame

                    # Perform side-specific transformations.
                    if "ground_force_vy" in data_segment.columns:
                        data_segment["ground_force_vy"] = -data_segment["ground_force_vy"]

                    normalised_data[foot][file_name][stride_number - 1] = data_segment.values.T

                elif event_type == "Foot Strike" and event_plate is not None:
                    while force_data.iloc[frame, 3] > 0:
                        frame -= 1
                    start = frame

    return normalised_data


def normalise_kinematics(kinematic_data, events):
    normalised_data = {"Left": {}, "Right": {}}
    for i in range(len(kinematic_data)):
        file_name = list(kinematic_data.keys())[i]
        trial_data = list(kinematic_data.values())[i]
        trial_events = list(events.values())[i]

        for foot, foot_events in trial_events.items():
            side = foot[0].lower()
            names = [
                f'pelvis_tilt',
                f'pelvis_list',
                f'pelvis_rotation',
                f'hip_flexion_{side}',
                f'hip_adduction_{side}',
                f'hip_rotation_{side}',
                f'knee_flexion_{side}',
                f'ankle_angle_{side}',
                f'subtalar_angle_{side}',
                f'foot_progression_{side}'
            ]
            data = trial_data.loc[:, ['time'] + names]

            start = None
            for stride_number, stride_events in foot_events.items():
                (event_time, (event_type, event_plate)), *_ = stride_events.items()
                if event_type == "Foot Strike" and start:
                    frame = data[data['time'] >= event_time].index[0]
                    if file_name not in normalised_data[foot]:
                        normalised_data[foot][file_name] = {}
                    data_segment = data.iloc[start:frame, 1:]

                    # Perform side-specific transformations.
                    if foot == "Left":
                        data_segment["pelvis_rotation"] = -data_segment["pelvis_rotation"]
                    if foot == "Right":
                        data_segment["pelvis_list"] = -(data_segment["pelvis_list"] - 180)
                    data_segment["pelvis_list"] -= 90

                    normalised_data[foot][file_name][stride_number - 1] = data_segment.values.T
                    start = data[data['time'] <= event_time].index[-1]
                elif event_type == "Foot Strike":
                    start = data[data['time'] <= event_time].index[-1]

    return normalised_data


def normalise_kinetics(kinetic_data, events):
    normalised_data = {"Left": {}, "Right": {}}
    for i in range(len(kinetic_data)):
        file_name = list(kinetic_data.keys())[i]
        trial_data = list(kinetic_data.values())[i]
        trial_events = list(events.values())[i]

        for foot, foot_events in trial_events.items():
            side = foot[0].lower()
            names = [
                f'hip_flexion_{side}_moment',
                f'hip_adduction_{side}_moment',
                f'hip_rotation_{side}_moment',
                f'hip_flexion_{side}_power',
                f'knee_flexion_{side}_moment',
                f'knee_adduction_{side}_moment',
                f'knee_rotation_{side}_moment',
                f'knee_flexion_{side}_power',
                f'ankle_angle_{side}_moment',
                f'subtalar_angle_{side}_moment',
                f'ankle_angle_{side}_power'
            ]
            data = trial_data.loc[:, ['time'] + names]

            start = None
            for stride_number, stride_events in foot_events.items():
                (event_time, (event_type, event_plate)), *_ = stride_events.items()

                if event_type == "Foot Strike" and start:
                    frame = data[data['time'] >= event_time].index[0]
                    if file_name not in normalised_data[foot]:
                        normalised_data[foot][file_name] = {}
                    data_segment = data.iloc[start:frame, 1:]

                    # Perform sign transformations.
                    data_segment[f"knee_adduction_{side}_moment"] = -data_segment[f"knee_adduction_{side}_moment"]
                    data_segment[f"knee_rotation_{side}_moment"] = -data_segment[f"knee_rotation_{side}_moment"]
                    data_segment[f"ankle_angle_{side}_moment"] = -data_segment[f"ankle_angle_{side}_moment"]

                    normalised_data[foot][file_name][stride_number - 1] = data_segment.values.T
                    if event_plate is not None:
                        start = data[data['time'] <= event_time].index[-1]
                    else:
                        start = None

                elif event_type == "Foot Strike":
                    if event_plate is not None:
                        start = data[data['time'] <= event_time].index[-1]

    return normalised_data


def write_normalised_kinematics(kinematic_data, selected_trials, excluded_cycles, output_directory):
    normalised_directory = os.path.join(output_directory, 'normalised')
    if not os.path.exists(normalised_directory):
        os.makedirs(normalised_directory)
    output_file = os.path.join(normalised_directory, f"combined_kinematics.csv")
    columns = ['pelvis_tilt', 'pelvis_list', 'pelvis_rotation',
               'hip_flexion', 'hip_adduction', 'hip_rotation',
               'knee_flexion', 'ankle_angle', 'subtalar_angle',
               'foot_progression']
    write_normalised_data(kinematic_data, columns, selected_trials, excluded_cycles, output_file)


def write_normalised_kinetics(kinetic_data, selected_trials, excluded_cycles, output_directory):
    normalised_directory = os.path.join(output_directory, 'normalised')
    output_file = os.path.join(normalised_directory, f"combined_kinetics.csv")
    columns = ['hip_flexion_moment', 'hip_adduction_moment', 'hip_rotation_moment',
               'hip_flexion_power', 'knee_flexion_moment', 'knee_adduction_moment',
               'knee_rotation_moment', 'knee_flexion_power', 'ankle_angle_moment',
               'subtalar_angle_moment', 'ankle_angle_power']
    write_normalised_data(kinetic_data, columns, selected_trials, excluded_cycles, output_file)


def write_normalised_data(data, column_names, selected_trials, excluded_cycles, output_file):
    with open(output_file, 'w') as file:
        file.write(','.join(["Trial", "Side", "Cycle-Number", "Frame"] + column_names) + '\n\n\n')

        for foot, files_dict in data.items():
            for file_name, cycles in files_dict.items():
                if file_name not in selected_trials:
                    continue

                for cycle_number, cycle_data in cycles.items():
                    cycle = f"{foot}_{cycle_number}"
                    cycle_identifier = (file_name, cycle)
                    if cycle_identifier in excluded_cycles:
                        continue

                    x_original = np.linspace(0, 1, cycle_data.shape[1])
                    x_new = np.linspace(0, 1, 101)
                    normalised_segment = np.zeros((cycle_data.shape[0], 101))
                    for j in range(cycle_data.shape[0]):
                        normalised_segment[j] = np.interp(x_new, x_original, cycle_data[j])
                    normalised_segment = normalised_segment.round(6)

                    for x in range(1, 102):
                        trial = selected_trials[file_name] if x == 1 else ""
                        side = foot if x == 1 else ""
                        stride = cycle_number if x == 1 else ""
                        row_data = [trial, side, stride, x] + normalised_segment[:, x - 1].tolist()
                        file.write(','.join(str(value) for value in row_data) + '\n')
                    file.write('\n\n')


def calculate_spatiotemporal_data(frame_data, events, static_data):
    stride_lengths = {"Left": {}, "Right": {}}
    step_lengths = {"Left": {}, "Right": {}}
    step_widths = {"Left": {}, "Right": {}}
    phases = {"Left": {}, "Right": {}}
    strike_count = 0

    _, _, _, _, _, _, _, _, _, left_leg_length, right_leg_length = static_data
    left_leg_length /= 1000
    right_leg_length /= 1000
    leg_lengths = {"Left": left_leg_length, "Right": right_leg_length}

    time_ordered_events = defaultdict(dict)
    for foot, foot_events in events.items():
        for stride_number, stride_events in foot_events.items():
            for event_time, (event_type, event_plate) in stride_events.items():
                time_ordered_events[event_time][foot] = [event_type, stride_number]

    opposite_side = {"Left": "Right", "Right": "Left"}
    strike_position = {"Left": None, "Right": None}
    foot_events = {"Left": None, "Right": None}
    stride_numbers = {"Left": 0, "Right": 0}
    for event_time in sorted(time_ordered_events):
        for foot, (event_type, stride_number) in time_ordered_events[event_time].items():
            stride_numbers[foot] = stride_number
            opposite_foot = opposite_side[foot]
            if event_type == "Foot Strike":
                strike_count += 1
                event_index = frame_data[frame_data['Time'] <= event_time].index[-1]
                heel_coordinates = frame_data.at[event_index, foot[0] + 'HEE']

                # Calculate length of stride.
                if strike_position[foot] is not None:
                    stride_length = heel_coordinates[0] - strike_position[foot][0]  # type: ignore
                    stride_lengths[foot][stride_number - 1] = stride_length / 1000
                strike_position[foot] = heel_coordinates

                # Calculate length and width of step.
                if strike_position[opposite_side[foot]] is not None:
                    previous_coordinates = strike_position[opposite_foot]

                    step_length = heel_coordinates[0] - previous_coordinates[0]     # type: ignore
                    step_lengths[opposite_foot][stride_numbers[opposite_foot]] = step_length / 1000

                    step_width = abs(heel_coordinates[1] - previous_coordinates[1])     # type: ignore
                    step_widths[opposite_foot][stride_numbers[opposite_foot]] = step_width / 1000

            # Calculate stance and swing phases.
            if stride_number not in phases[foot]:
                phases[foot][stride_number] = {}
            if foot_events[foot] is not None:
                time_interval = event_time - foot_events[foot]
                if event_type == "Foot Strike":
                    phases[foot][stride_number - 1]["Swing"] = time_interval
                elif event_type == "Foot Off":
                    phases[foot][stride_number]["Stance"] = time_interval
            foot_events[foot] = event_time

            # Calculate single and double support phases.
            if stride_numbers[opposite_foot] not in phases[opposite_foot]:
                phases[opposite_foot][stride_numbers[opposite_foot]] = {}
            if foot_events[opposite_foot] is not None:
                time_interval = event_time - foot_events[opposite_foot]
                if event_type == "Foot Strike":
                    phases[opposite_foot][stride_numbers[opposite_foot]]["Single-Support"] = time_interval
                elif event_type == "Foot Off":
                    phases[opposite_foot][stride_numbers[opposite_foot]]["Double-Support"] = time_interval

    s_t_data = {}

    # Calculate normalised lengths.
    normalised_stride_lengths = {side: {k: v / leg_lengths[side] for k, v in stride_lengths[side].items()}
                                 for side in stride_lengths}
    normalised_step_lengths = {side: {k: v / leg_lengths[side] for k, v in step_lengths[side].items()}
                               for side in step_lengths}

    # Assign lengths and widths.
    s_t_data["Stride Length (m)"] = stride_lengths
    s_t_data["Normalised Stride Length (m)"] = normalised_stride_lengths
    s_t_data["Step Length (m)"] = step_lengths
    s_t_data["Normalised Step Length (m)"] = normalised_step_lengths
    s_t_data["Step Width (m)"] = step_widths

    # Determine phase percentages.
    stance_phases = {"Left": {}, "Right": {}}
    swing_phases = {"Left": {}, "Right": {}}
    single_support_phases = {"Left": {}, "Right": {}}
    double_support_phases = {"Left": {}, "Right": {}}
    for side, cycles in phases.items():
        for cycle_number, cycle in cycles.items():
            if "Stance" in cycle and "Swing" in cycle:
                total_time = cycle["Stance"] + cycle["Swing"]
                stance_phases[side][cycle_number] = (cycle["Stance"] / total_time) * 100
                swing_phases[side][cycle_number] = (cycle["Swing"] / total_time) * 100

            if "Single-Support" in cycle and "Double-Support" in cycle:
                total_time = cycle["Single-Support"] + cycle["Double-Support"]
                single_support_phases[side][cycle_number] = (cycle["Single-Support"] / total_time) * 100
                double_support_phases[side][cycle_number] = (cycle["Double-Support"] / total_time) * 100

    # Assign phase percentages.
    s_t_data["Stance Phase %"] = stance_phases
    s_t_data["Swing Phase %"] = swing_phases
    s_t_data["Single Support Phase %"] = single_support_phases
    s_t_data["Double Support Phase %"] = double_support_phases

    average_leg_length = (left_leg_length + right_leg_length) / 2
    start_time, end_time = None, None
    for event_time in sorted(time_ordered_events):
        for event_type, _ in time_ordered_events[event_time].values():
            if event_type == "Foot Strike":
                if start_time is None:
                    start_time = event_time
                end_time = event_time
    total_time = end_time - start_time

    # Calculate gait-speed and cadence.
    total_distance = calculate_distance_covered(frame_data, start_time, end_time)
    gait_speed = (total_distance / total_time) / 1000
    normalised_gait_speed = gait_speed / math.sqrt(9.81 * average_leg_length)
    cadence = ((strike_count - 1) / total_time) * 60

    # Calculate foot progression.
    foot_angles = calculate_foot_progression(frame_data, time_ordered_events)
    s_t_data["Foot Progression (deg)"] = foot_angles

    data_frame = convert_to_data_frame(s_t_data)

    # Calculate averages and other trial-specific measurements.
    data_frame.loc['average'] = data_frame.mean()
    data_frame.loc['average', ["Gait Speed (m/s)", "Normalised Gait Speed (m/s)", "Cadence (steps/min)"]] = [
        gait_speed, normalised_gait_speed, cadence
    ]

    return data_frame


def calculate_distance_covered(frame_data, start_time=None, end_time=None):
    start_frame = frame_data.index[0] if start_time is None \
        else frame_data[frame_data['Time'] >= start_time].index[0]
    end_frame = frame_data.index[-1] if end_time is None \
        else frame_data[frame_data['Time'] <= end_time].index[-1]

    start_pos = frame_data.loc[start_frame, ['LASI', 'RASI']].mean()
    end_pos = frame_data.loc[end_frame, ['LASI', 'RASI']].mean()
    walking_direction = end_pos[:2] - start_pos[:2]
    walking_direction /= np.linalg.norm(walking_direction)

    distance_vector = end_pos - start_pos
    distance_travelled = np.dot(distance_vector[:2], walking_direction)

    return distance_travelled


def calculate_walking_direction(frame_data):
    start_pos = frame_data[['LASI', 'RASI']].iloc[0].mean(axis=0)
    end_pos = frame_data[['LASI', 'RASI']].iloc[-1].mean(axis=0)
    walking_direction = end_pos[:2] - start_pos[:2]
    walking_direction /= np.linalg.norm(walking_direction)

    return walking_direction


def calculate_foot_progression_angles(frame_data):
    walking_direction = calculate_walking_direction(frame_data)
    walking_angle = np.arctan2(walking_direction[1], walking_direction[0])

    foot_progression = pd.DataFrame()
    for foot in ['Left', 'Right']:
        side = foot[0]
        heel_xy = np.stack(frame_data[f"{side}HEE"].values)[:, :2]
        toe_xy = np.stack(frame_data[f"{side}TOE"].values)[:, :2]

        foot_vectors = toe_xy - heel_xy
        foot_unit_vectors = foot_vectors / np.linalg.norm(foot_vectors, axis=1, keepdims=True)
        foot_angles = np.arctan2(foot_unit_vectors[:, 1], foot_unit_vectors[:, 0])
        angles = np.degrees(foot_angles - walking_angle)

        if foot == 'Left':
            angles = -angles

        foot_progression[f'foot_progression_{side.lower()}'] = angles

    return foot_progression


def calculate_foot_progression(frame_data, time_ordered_events):
    walking_direction = calculate_walking_direction(frame_data)

    foot_angles = {"Left": {}, "Right": {}}
    foot_events = {"Left": None, "Right": None}
    for event_time in sorted(time_ordered_events):
        for foot, (event_type, stride_number) in time_ordered_events[event_time].items():
            if foot_events[foot] is not None:
                if event_type == "Foot Off":
                    mid_stance_time = (foot_events[foot] + event_time) / 2  # type: ignore
                    frame = frame_data[frame_data['Time'] >= mid_stance_time].index[0]
                    heel_position = frame_data.loc[frame, f"{foot[0]}HEE"]
                    toe_position = frame_data.loc[frame, f"{foot[0]}TOE"]
                    foot_vector = toe_position[:2] - heel_position[:2]
                    foot_vector /= np.linalg.norm(foot_vector)

                    foot_angle = np.arctan2(foot_vector[1], foot_vector[0])
                    walking_angle = np.arctan2(walking_direction[1], walking_direction[0])
                    angle = np.degrees(foot_angle - walking_angle)
                    if foot == 'Right':
                        angle = -angle

                    foot_angles[foot][stride_number] = normalise_angle(angle)

            foot_events[foot] = event_time

    return foot_angles


def normalise_angle(angle):
    if angle < -180:
        angle += 360
    elif angle > 180:
        angle -= 360
    return angle


def write_spatiotemporal_data(data, selected_trials, output_directory):
    normalised_directory = os.path.join(output_directory, 'normalised')
    output_file = os.path.join(normalised_directory, f"spattemp.csv")

    combined_data_frame = pd.concat([df.rename(index=lambda idx: f"{selected_trials[trial]} {idx}")
         for trial, df in data.items() if trial in selected_trials])
    combined_data_frame.round(3).to_csv(output_file)


def convert_to_data_frame(s_t_data):
    row_dict = {}
    for measurement, data_both_side in s_t_data.items():
        for side, data_one_side in data_both_side.items():
            for cycle_number, value in data_one_side.items():
                row_label = f"({side}-{cycle_number})"
                if row_label not in row_dict:
                    row_dict[row_label] = {}
                row_dict[row_label][measurement] = value
    data_frame = pd.DataFrame.from_dict(row_dict, orient='index')

    return data_frame


def add_medial_knee_markers(frame_data, left_knee_width, right_knee_width, marker_diameter=14):
    """
    This function takes a pandas.DataFrame of TRC data, extracts a single frame from the data
    and adds the medial knee markers if they are missing. It returns the frame as a pandas.Series.

    The ``padding`` argument should include skin-padding as well as the thickness of the
    baseplate used to attach the markers.
    """
    frame = frame_data.iloc[len(frame_data) // 2].copy()

    medial_padding = 6
    lateral_padding = 4

    for side in ['L', 'R']:
        medial_label = f'{side}KNEM'
        if medial_label not in frame.index:
            if left_knee_width is None or right_knee_width is None:
                raise ParserError("No knee-width values found in static trial. Unable to add medial knee markers.")

            axis_marker = frame[f'{side}KAX']
            lateral_marker = frame[f'{side}KNE']
            axix_vector = lateral_marker - axis_marker
            magnitude = np.sqrt((np.array(axix_vector) ** 2.0).sum(-1))
            knee_axis = np.divide(axix_vector, magnitude)

            # Adjust knee width to account for marker-radius, skin-padding.
            knee_width = left_knee_width if side == 'L' else right_knee_width
            knee_width = knee_width + marker_diameter + medial_padding + lateral_padding
            medial_marker = lateral_marker + knee_width * knee_axis
            frame[medial_label] = medial_marker

    return frame


def create_osim_model(static_trc, dynamic_trc, static_marker_data, height, weight,
                      output_directory, optimise_knee_axis, progress_tracker):

    # Assume height in cm and convert to m.
    height /= 1000

    static_marker_data = static_marker_data.drop("Time").to_dict()
    rotation_matrix = np.array([[1, 0, 0], [0, 0, 1], [0, -1, 0]])
    static_marker_data = {k: np.dot(rotation_matrix, v) for k, v in static_marker_data.items()}

    model_path = create_model(static_trc, dynamic_trc, output_directory, static_marker_data, weight, height,
                              optimise_knee_axis=optimise_knee_axis, progress_tracker=progress_tracker)

    return model_path
