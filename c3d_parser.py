
import os
import math
import json
import numpy as np
import pandas as pd

from scipy import signal, interpolate

from trc import TRCData

from c3d_patch import c3d


marker_maps_dir = os.path.abspath(os.path.join('..', 'marker_maps'))


def parse_c3d(c3d_file, output_directory):
    input_directory, c3d_file_name = os.path.split(os.path.abspath(c3d_file))
    gait_lab = os.path.basename(input_directory)
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
    trim_frames(frame_data)
    filter_markers(frame_data, trc_data['DataRate'])
    frame_data = resample_markers(frame_data, trc_data['DataRate'])

    # Write harmonised TRC data.
    set_marker_data(trc_data, frame_data)
    trc_directory = os.path.join(output_directory, 'trc')
    if not os.path.exists(trc_directory):
        os.makedirs(trc_directory)
    trc_file_path = os.path.join(trc_directory, f"{file_name}.trc")
    trc_data.save(trc_file_path)


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


def filter_markers(frame_data, data_rate, cut_off_frequency=6):
    # Determine filter coefficients
    Wn = cut_off_frequency / (data_rate / 2)
    b, a = signal.butter(2, Wn)

    # Filter each marker trajectory.
    for marker in frame_data.columns[1:]:
        marker_trajectory = frame_data.loc[:, marker].values
        filtered_trajectory = signal.filtfilt(b, a, marker_trajectory, axis=0)
        frame_data.loc[:, marker] = filtered_trajectory


def resample_markers(frame_data, data_rate, frequency=100):
    if data_rate == 100:
        return frame_data

    start_time = frame_data['Time'].iat[0]
    end_time = frame_data['Time'].iat[-1]
    number_of_frames = int((end_time - start_time) * frequency)
    time_array = np.linspace(start_time, end_time, number_of_frames)

    resampled_frame_data = pd.DataFrame(columns=frame_data.columns)
    resampled_frame_data['Time'] = time_array

    # Resample each marker trajectory.
    for marker in frame_data.columns[1:]:
        marker_trajectory = np.stack(frame_data.loc[:, marker].values)

        resampled_trajectory = []
        for axis in marker_trajectory.transpose():
            tck = interpolate.splrep(frame_data['Time'].values, axis, s=0)
            resampled_trajectory.append(interpolate.splev(time_array, tck, der=0))
        resampled_trajectory = np.stack(resampled_trajectory).transpose()

        # Adjust frame format to support row iteration.
        flattened_array = np.empty(resampled_trajectory.shape[0], dtype=object)
        for i in range(resampled_trajectory.shape[0]):
            flattened_array[i] = resampled_trajectory[i]
        resampled_frame_data.loc[:, marker] = flattened_array

    return resampled_frame_data
