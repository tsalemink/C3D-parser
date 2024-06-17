
import os
import math
import json
import numpy as np
import pandas as pd

from scipy import signal, interpolate
from scipy.spatial.transform import Rotation

from trc import TRCData

from c3d_patch import c3d


marker_maps_dir = os.path.abspath(os.path.join('..', 'marker_maps'))


def parse_c3d(c3d_file, output_directory):
    input_directory, c3d_file_name = os.path.split(os.path.abspath(c3d_file))
    gait_lab = os.path.basename(os.path.dirname(input_directory))
    trial_type = os.path.basename(input_directory)
    dynamic_trial = (trial_type == 'dynamic')
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
    map_file = os.path.join(marker_maps_dir, f"{gait_lab}.json")
    with open(map_file, 'r') as file:
        marker_map = json.load(file)
    harmonise_markers(frame_data, marker_map)
    start_frame, end_frame = trim_frames(frame_data)
    filter_data(frame_data, trc_data['DataRate'])
    frame_data = resample_data(frame_data, trc_data['DataRate'])

    # Write harmonised TRC data.
    set_marker_data(trc_data, frame_data)
    trc_directory = os.path.join(output_directory, 'trc')
    if not os.path.exists(trc_directory):
        os.makedirs(trc_directory)
    trc_file_path = os.path.join(trc_directory, f"{file_name}.trc")
    trc_data.save(trc_file_path)

    if dynamic_trial:
        # Extract GRF data from C3D file.
        analog_data, data_rate, events, plate_count, corners = extract_grf(c3d_file, start_frame, end_frame)
        if analog_data is None:
            return

        # Match events to force plates.
        identify_event_plates(frame_data, events, corners)

        # Harmonise GRF data.
        filter_data(analog_data, data_rate)
        analog_data = resample_data(analog_data, data_rate, frequency=1000)
        zero_grf_data(analog_data, plate_count)

        # Write GRF data.
        grf_directory = os.path.join(output_directory, 'grf')
        if not os.path.exists(grf_directory):
            os.makedirs(grf_directory)
        grf_file_path = os.path.join(grf_directory, f"{file_name}_grf.mot")
        write_grf(analog_data, grf_file_path)


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
            coordinates = frame[marker_index]
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


def extract_grf(file_path, start_frame, end_frame):
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
        transform_grf_coordinates(analog_data, plate_count, corners)

    return analog_data, reader.analog_rate, events, plate_count, corners


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


def transform_grf_coordinates(analog_data, plate_count, corners):
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

        start = 1 + (6 * i)
        for j in [start, start + 3]:
            columns = list(range(j, j + 3))
            values = analog_data.iloc[:, columns]
            transformed_values = values.apply(lambda row: np.dot(rotation_matrix, row), axis=1)
            analog_data.iloc[:, columns] = transformed_values.tolist()


def zero_grf_data(analog_data, plate_count):
    for i in range(plate_count):
        start = 1 + (6 * i)
        columns = list(range(start, start + 6))
        mask = analog_data.iloc[:, columns[2]] < 0
        analog_data.iloc[mask, columns] = 0


def identify_event_plates(frame_data, events, corners):
    for foot in events:
        drop_events = []
        for event_time, event in events[foot].items():
            event_index = frame_data[frame_data['Time'] <= event_time].index[-1]
            heel_coordinates = frame_data.at[event_index, foot[0] + 'HEE']
            for plate in range(len(corners)):
                if point_on_plate(heel_coordinates, corners[plate]):
                    events[foot][event_time] = [event, plate]
                    break
            else:
                drop_events.append(event_time)

        for event_time in drop_events:
            del events[foot][event_time]


def point_on_plate(point, corners):
    x_coordinates = [corner[0] for corner in corners]
    y_coordinates = [corner[1] for corner in corners]
    min_x, max_x = min(x_coordinates), max(x_coordinates)
    min_y, max_y = min(y_coordinates), max(y_coordinates)

    return min_x <= point[0] <= max_x and min_y <= point[1] <= max_y

