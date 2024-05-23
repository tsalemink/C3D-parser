
import os
import math
import json
import numpy as np

from scipy import signal

from trc import TRCData

from c3d_patch import c3d


marker_maps_dir = os.path.abspath(os.path.join('..', 'marker_maps'))


def parse_c3d(c3d_file, output_directory):
    input_directory, c3d_file_name = os.path.split(os.path.abspath(c3d_file))
    gait_lab = os.path.basename(input_directory)
    file_name = os.path.splitext(c3d_file_name)[0]

    # Extract TRC data from C3D file.
    trc_data = TRCData()
    trc_data.import_from(c3d_file)

    # Harmonise TRC data.
    map_file = os.path.join(marker_maps_dir, f"{gait_lab}.json")
    with open(map_file, 'r') as file:
        marker_map = json.load(file)
    markers, frames = harmonise_markers(trc_data, marker_map)
    trim_frames(frames)
    filter_markers(frames, trc_data['DataRate'])

    # Write harmonised TRC data.
    set_marker_data(trc_data, markers, frames)
    trc_directory = os.path.join(output_directory, 'trc')
    if not os.path.exists(trc_directory):
        os.makedirs(trc_directory)
    trc_file_path = os.path.join(trc_directory, f"{file_name}.trc")
    trc_data.save(trc_file_path)

    # De-identify the C3D data.
    de_identified_directory = os.path.join(output_directory, 'de_identified')
    if not os.path.exists(de_identified_directory):
        os.makedirs(de_identified_directory)
    de_identify_c3d(c3d_file, de_identified_directory)


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
        writer.get('SUBJECTS').set_str('NAMES', '', 'Subject', 7)

    with open(os.path.join(output_directory, file_name), 'wb') as handle:
        writer.write(handle)


def harmonise_markers(trc_data, marker_mapping):
    """
    Harmonises the marker set of a `TRCData` object according to a mapping of markers. Returns the
    harmonised marker-set and frame data.

    param c3d_writer: The `TRCData` object to be updated.
    param marker_mapping: A dictionary mapping the trial marker set to the harmonised marker set.
    """
    # Harmonise marker labels.
    reversed_mapping = {value: key for key, value in marker_mapping.items() if value is not None}
    harmonised_markers = [reversed_mapping[marker] if marker in reversed_mapping else None
                          for marker in trc_data['Markers']]

    # Filter out non-harmonised data points.
    harmonised_frames = {}
    for frame_number in trc_data['Frame#']:
        time, frame = trc_data[frame_number]
        harmonised_points = []
        for i in range(len(frame)):
            if harmonised_markers[i]:
                coordinates = frame[i]
                harmonised_points.append(coordinates)
        harmonised_frames[frame_number] = [time, harmonised_points]
    harmonised_markers = list(filter(None, harmonised_markers))

    return harmonised_markers, harmonised_frames


def set_marker_data(trc_data, markers, frames):
    # Clear existing frame data.
    for frame_number in trc_data['Frame#']:
        del trc_data[frame_number]

    trc_data['Markers'] = markers
    trc_data['Frame#'] = []
    for frame_number in frames.keys():
        trc_data['Frame#'].append(frame_number)
        trc_data[frame_number] = frames[frame_number]


def trim_frames(frames, max_trim=50):
    # Check for incomplete frames.
    incomplete_frames = {}
    for frame_number in frames.keys():
        frame = frames[frame_number][1]
        missing_markers = []
        for marker_index in range(len(frame)):
            coordinates = frame[marker_index]
            if math.isnan(coordinates[0]):
                missing_markers.append(marker_index)
        if missing_markers:
            incomplete_frames[frame_number] = missing_markers

    # Trim incomplete frames near the beginning or end of the trial.
    first_frame = list(frames.keys())[0]
    start_frames = [frame_number for frame_number in incomplete_frames if frame_number < first_frame + max_trim]
    trim_start = max(start_frames, default=first_frame - 1)
    while first_frame <= trim_start:
        del frames[first_frame]
        first_frame += 1
    last_frame = list(frames.keys())[-1]
    end_frames = [frame_number for frame_number in incomplete_frames if last_frame - max_trim < frame_number]
    trim_end = min(end_frames, default=last_frame + 1)
    while last_frame >= trim_end:
        del frames[last_frame]
        last_frame -= 1

    remaining_frames = list(set(incomplete_frames.keys()) - set(start_frames) - set(end_frames))
    if remaining_frames:
        print(f"WARNING: Frames {remaining_frames} are incomplete.")


def filter_markers(frames, data_rate, cut_off_frequency=6):
    # TODO: Do this part externally.
    # Convert frames to numpy array.
    frames_list = []
    for row in frames.values():
        data = row[1]
        frames_list.append(data)
    frames_array = np.array(frames_list)

    # Determine filter coefficients
    Wn = cut_off_frequency / (data_rate / 2)
    b, a = signal.butter(2, Wn)

    # Filter the marker trajectory.
    for i in range(frames_array.shape[1]):
        marker_trajectory = frames_array[:, i]
        filtered_trajectory = signal.filtfilt(b, a, marker_trajectory, axis=0)
        frames_array[:, i] = filtered_trajectory
