
import os
import json

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
    trc_data['Markers'] = markers
    for frame_number in trc_data['Frame#']:
        trc_data[frame_number] = frames[frame_number]
