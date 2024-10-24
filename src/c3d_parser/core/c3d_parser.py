
import os
import math
import json
import numpy as np
import pandas as pd

from scipy import signal, interpolate
from scipy.spatial.transform import Rotation

from trc import TRCData

from c3d_parser.core.c3d_patch import c3d
from c3d_parser.core.osim import perform_ik, perform_id


script_directory = os.path.dirname(os.path.abspath(__file__))
marker_maps_dir = os.path.join(script_directory, 'marker_maps')


def parse_session(files, input_directory, output_directory):
    grf_data = {}
    kinematic_data = {}
    kinetic_data = {}
    event_data = {}

    for file_name, dynamic in files.items():
        file_path = os.path.join(input_directory, file_name)
        analog_data, ik_data, id_data, events = parse_c3d(file_path, output_directory, dynamic)

        if dynamic:
            grf_data[file_name] = analog_data
            kinematic_data[file_name] = ik_data
            kinetic_data[file_name] = id_data
            event_data[file_name] = events

    normalised_grf_data = normalise_grf_data(grf_data, event_data, 'grf')
    normalised_torque_data = normalise_grf_data(grf_data, event_data, 'torque')
    normalised_kinematics = normalise_kinematics(kinematic_data, event_data)
    normalised_kinetics = normalise_kinetics(kinetic_data, event_data)

    return normalised_grf_data, normalised_torque_data, normalised_kinematics, normalised_kinetics


def parse_c3d(c3d_file, output_directory, is_dynamic):
    input_directory, c3d_file_name = os.path.split(os.path.abspath(c3d_file))
    gait_lab = os.path.basename(os.path.dirname(input_directory))
    file_name = os.path.splitext(c3d_file_name)[0]

    # De-identify the C3D data.
    de_identified_directory = os.path.join(output_directory, 'de_identified')
    if not os.path.exists(de_identified_directory):
        os.makedirs(de_identified_directory)
    de_identify_c3d(c3d_file, de_identified_directory)

    # Extract TRC data from C3D file.
    trc_data = TRCData()
    trc_data.import_from(c3d_file)
    frame_data = extract_marker_data(trc_data)

    # Harmonise TRC data.
    marker_data_rate = 100
    map_file = os.path.join(marker_maps_dir, f"{gait_lab}.json")
    with open(map_file, 'r') as file:
        marker_map = json.load(file)
    harmonise_markers(frame_data, marker_map)
    start_frame, end_frame = trim_frames(frame_data)
    filter_data(frame_data, trc_data['DataRate'])
    frame_data = resample_data(frame_data, trc_data['DataRate'], marker_data_rate)

    analog_data, ik_data, id_data, events, subject_weight = None, None, None, None, None
    if is_dynamic:
        # Extract GRF data from C3D file.
        analog_data, data_rate, events, plate_count, corners, subject_weight = extract_data(c3d_file, start_frame, end_frame)
        if analog_data is None:
            return

        # Match events to force plates.
        identify_event_plates(frame_data, events, corners)

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
        grf_file_path = os.path.join(grf_directory, f"{file_name}_grf.mot")
        write_grf(analog_data, grf_file_path)

    # Write harmonised TRC data.
    set_marker_data(trc_data, frame_data, rate=marker_data_rate)
    trc_directory = os.path.join(output_directory, 'trc')
    if not os.path.exists(trc_directory):
        os.makedirs(trc_directory)
    trc_file_path = os.path.join(trc_directory, f"{file_name}.trc")
    trc_data.save(trc_file_path)

    if is_dynamic:
        # TODO: Scale the OpenSim model.
        #   Temporarily use pre-scaled model.
        scaled_model = "C:\\Users\\tsal421\\Projects\\Gait\\OpenSim-Models\\PGM_SYDNEY_scaled.osim"

        # Perform inverse kinematics.
        ik_directory = os.path.join(output_directory, 'IK')
        if not os.path.exists(ik_directory):
            os.makedirs(ik_directory)
        ik_output = os.path.join(ik_directory, f"{file_name}_IK.mot")
        perform_ik(scaled_model, trc_file_path, ik_output)
        ik_data = read_data(ik_output)
        filter_data(ik_data, marker_data_rate, cut_off_frequency=8)

        # Perform inverse dynamics.
        id_directory = os.path.join(output_directory, 'ID')
        if not os.path.exists(id_directory):
            os.makedirs(id_directory)
        id_output = os.path.join(id_directory, f"{file_name}_ID.sto")
        perform_id(scaled_model, ik_output, grf_file_path, id_output)
        id_data = read_data(id_output)
        filter_data(id_data, marker_data_rate, cut_off_frequency=8)
        mass_adjust_units(id_data, subject_weight)

    return analog_data, ik_data, id_data, events


def de_identify_c3d(file_path, output_directory):
    input_directory, file_name = os.path.split(os.path.abspath(file_path))
    output_directory = os.path.abspath(output_directory)

    # Currently we prevent overwriting the input file.
    if input_directory == output_directory:
        raise IOError("Cannot overwrite input file.")

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    with open(file_path, 'rb') as handle:
        reader = c3d.Reader(handle)
        writer = reader.to_writer('copy')
        if 'SUBJECTS' in reader:
            writer.get('SUBJECTS').set_str('NAMES', '', 'Subject', 7)

    with open(os.path.join(output_directory, file_name), 'wb') as handle:
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


def harmonise_markers(frame_data, marker_mapping):
    # Harmonise marker labels.
    reversed_mapping = {value: key for key, value in marker_mapping.items() if value is not None}
    header_mapping = {header: reversed_mapping.get(header, None) for header in frame_data.columns[1:]}
    frame_data.rename(columns=header_mapping, inplace=True)

    # Filter out non-harmonised data points.
    if None in frame_data.columns:
        frame_data.drop(columns=[None], axis=1, inplace=True)


def trim_frames(frame_data, max_trim=50):
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

    # Trim incomplete frames near the beginning or end of the trial.
    first_frame = frame_data.index.min()
    start_frames = [frame_number for frame_number in incomplete_frames if frame_number < first_frame + max_trim]
    trim_start = max(start_frames) + 1 if start_frames else first_frame
    last_frame = frame_data.index.max()
    end_frames = [frame_number for frame_number in incomplete_frames if last_frame - max_trim < frame_number]
    trim_end = min(end_frames) - 1 if end_frames else last_frame

    frame_list = frame_data.index.to_list()
    complete_frames = frame_list[frame_list.index(trim_start):frame_list.index(trim_end) + 1]
    drop_frames = frame_data.index.difference(complete_frames)
    if not drop_frames.empty:
        frame_data.drop(drop_frames, inplace=True)

    remaining_frames = list(set(incomplete_frames.keys()) - set(start_frames) - set(end_frames))
    if remaining_frames:
        print(f"WARNING: Frames {remaining_frames} are incomplete.")

    return first_frame, last_frame


def filter_data(frame_data, data_rate, cut_off_frequency=6):
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


def extract_data(file_path, start_frame, end_frame):
    with open(file_path, 'rb') as handle:
        reader = c3d.Reader(handle)
        if (reader.analog_used == 0) or ('EVENT' not in reader):
            return None, None, None, None, None

        # Extract analog data
        time_increment = 1 / reader.analog_rate
        start = (start_frame - 1) / reader.point_rate
        stop = (end_frame - 1) / reader.point_rate + ((reader.analog_per_frame - 1) * time_increment)
        times = np.linspace(start, stop, reader.analog_sample_count).tolist()
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
            time = times[i][1]
            events[foot][time] = label
        for foot in events.keys():
            events[foot] = dict(sorted(events[foot].items()))

        # Get number of force plates.
        plate_count = reader.get('FORCE_PLATFORM:USED').int8_value

        # Rotate GRF data to align with global CS.
        corners = reader.get('FORCE_PLATFORM:CORNERS').float_array

        # Extract subject weight.
        subject_weight = reader.get('PROCESSING:BODYMASS').float_value

    return analog_data, reader.analog_rate, events, plate_count, corners, subject_weight


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
        mask = analog_data.iloc[:, columns[2]] > -10
        analog_data.iloc[mask, columns] = 0


def identify_event_plates(frame_data, events, corners):
    for foot in events:
        for event_time, event in events[foot].items():
            event_index = frame_data[frame_data['Time'] <= event_time].index[-1]
            heel_coordinates = frame_data.at[event_index, foot[0] + 'HEE']
            for plate in range(len(corners)):
                if point_on_plate(heel_coordinates, corners[plate]):
                    events[foot][event_time] = [event, plate]
                    break
            else:
                events[foot][event_time] = [event, None]


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

    for i in range(len(events)):
        foot = list(events)[i]
        target_columns = range(i * 9 + 1, i * 9 + 10)

        start, end = None, None
        for event in events[foot]:
            event_type = events[foot][event][0]
            event_plate = events[foot][event][1]
            if event_plate is None:
                continue
            frame = analog_data[analog_data['time'] <= event].index[-1]
            source_columns = range(event_plate * 9 + 1, event_plate * 9 + 10)

            if event_type == "Foot Strike":
                while analog_data.iloc[frame, source_columns[2]] > 0:
                    frame -= 1
                start = frame
            elif event_type == "Foot Off":
                while analog_data.iloc[frame, source_columns[2]] > 0:
                    frame += 1
                end = frame

                if start is None:
                    start = analog_data.index[0]
                copy_data()
                start, end = None, None

        if start:
            end = analog_data.index[-1]
            copy_data()

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
        reader = c3d.Reader(handle)
        if reader.analog_used > 0:
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


def normalise_grf_data(data, events, data_type):
    normalised_data = {"Left": {}, "Right": {}}
    for i in range(len(data)):
        file_name = list(data.keys())[i]
        grf_data = list(data.values())[i]
        trial_events = list(events.values())[i]

        for foot, foot_events in trial_events.items():
            column = 1 if foot == "Left" and data_type == "grf" else \
                13 if foot == "Left" else 7 if data_type == "grf" else 16
            force_data = grf_data.iloc[:, [0, *range(column, column + 3)]]

            start = None
            for event_time, (event_type, event_plate) in foot_events.items():
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
                    data_segment = force_data.iloc[start:frame, 1:]

                    # Perform side-specific transformations.
                    if "ground_force_vy" in data_segment.columns:
                        data_segment["ground_force_vy"] = -data_segment["ground_force_vy"]

                    normalised_data[foot][file_name].append(data_segment.values.T)
                    start = None

    return normalised_data


def normalise_kinematics(kinematic_data, events):
    normalised_data = {"Left": {}, "Right": {}}
    for i in range(len(kinematic_data)):
        file_name = list(kinematic_data.keys())[i]
        trial_data = list(kinematic_data.values())[i]
        trial_events = list(events.values())[i]

        for foot, foot_events in trial_events.items():
            pelvis_kinematics = ['pelvis_tilt', 'pelvis_list', 'pelvis_rotation']
            other_kinematics = ['hip_flexion', 'hip_adduction', 'hip_rotation',
                                'knee_angle', 'ankle_angle', 'subtalar_angle']
            for i, name in enumerate(other_kinematics):
                other_kinematics[i] = f"{name}_{foot[0].lower()}"
            data = trial_data.loc[:, ['time'] + pelvis_kinematics + other_kinematics]

            start = None
            for event_time, event in foot_events.items():
                if event[0] == "Foot Strike" and start:
                    frame = data[data['time'] >= event_time].index[0]
                    if file_name not in normalised_data[foot]:
                        normalised_data[foot][file_name] = []
                    data_segment = data.iloc[start:frame, 1:]

                    # Perform side-specific transformations.
                    if foot == "Left":
                        data_segment["pelvis_rotation"] = -data_segment["pelvis_rotation"]
                        data_segment["hip_adduction_l"] = -data_segment["hip_adduction_l"]
                        data_segment["hip_rotation_l"] = -data_segment["hip_rotation_l"]
                        data_segment["knee_angle_l"] = -data_segment["knee_angle_l"]
                    if foot == "Right":
                        data_segment["pelvis_list"] = -(data_segment["pelvis_list"] - 180)
                        data_segment["knee_angle_r"] = -data_segment["knee_angle_r"]
                    data_segment["pelvis_list"] -= 90

                    normalised_data[foot][file_name].append(data_segment.values.T)
                    start = None
                elif event[0] == "Foot Strike":
                    start = data[data['time'] <= event_time].index[-1]

    return normalised_data


def normalise_kinetics(kinetic_data, events):
    normalised_data = {"Left": {}, "Right": {}}
    for i in range(len(kinetic_data)):
        file_name = list(kinetic_data.keys())[i]
        trial_data = list(kinetic_data.values())[i]
        trial_events = list(events.values())[i]

        for foot, foot_events in trial_events.items():
            moment_names = ['hip_flexion', 'hip_adduction', 'hip_rotation',
                            'knee_angle', 'ankle_angle', 'subtalar_angle']
            for i, name in enumerate(moment_names):
                moment_names[i] = f"{name}_{foot[0].lower()}_moment"
            data = trial_data.loc[:, ['time'] + moment_names]

            start = None
            for event_time, event in foot_events.items():
                if event[0] == "Foot Strike" and start:
                    frame = data[data['time'] >= event_time].index[0]
                    if file_name not in normalised_data[foot]:
                        normalised_data[foot][file_name] = []
                    data_segment = data.iloc[start:frame, 1:]

                    # Perform side-specific transformations.
                    if foot == "Right":
                        data_segment["hip_adduction_r_moment"] = -data_segment["hip_adduction_r_moment"] + 1

                    normalised_data[foot][file_name].append(data_segment.values.T)
                    start = None
                elif event[0] == "Foot Strike":
                    start = data[data['time'] <= event_time].index[-1]

    return normalised_data


def write_normalised_kinematics(kinematic_data, selected_trials, output_directory):
    normalised_directory = os.path.join(output_directory, 'normalised')
    if not os.path.exists(normalised_directory):
        os.makedirs(normalised_directory)
    output_file = os.path.join(normalised_directory, f"combined_kinematics.csv")
    columns = ["pelvis_list", "pelvis_rotation", "pelvis_tilt",
               "hip_adduction", "hip_rotation", "hip_flexion",
               "knee_angle", "ankle_angle", "subtalar_angle"]
    write_normalised_data(kinematic_data, columns, selected_trials, output_file)


def write_normalised_kinetics(kinetic_data, selected_trials, output_directory):
    normalised_directory = os.path.join(output_directory, 'normalised')
    output_file = os.path.join(normalised_directory, f"combined_kinetics.csv")
    columns = ["hip_adduction_moment", "hip_rotation_moment", "hip_flexion_moment",
               "knee_angle_moment", "ankle_angle_moment", "subtalar_angle_moment"]
    write_normalised_data(kinetic_data, columns, selected_trials, output_file)


def write_normalised_data(data, column_names, selected_trials, output_file):
    with open(output_file, 'w') as file:
        file.write(','.join(["Frame"] + column_names) + '\n\n\n')

        for foot, files_dict in data.items():
            for name, data_segments in files_dict.items():
                if name not in selected_trials:
                    continue
                for segment in data_segments:
                    x_original = np.linspace(0, 1, segment.shape[1])
                    x_new = np.linspace(0, 1, 100)
                    normalised_segment = np.zeros((segment.shape[0], 100))
                    for i in range(segment.shape[0]):
                        normalised_segment[i] = np.interp(x_new, x_original, segment[i])

                    for x in range(1, 101):
                        row_data = [x] + normalised_segment[:, x - 1].tolist()
                        file.write(','.join(f'{value:.6f}' for value in row_data) + '\n')
                    file.write('\n\n')
