
import os
import json
import numpy

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

    # Initialise C3D data for harmonisation.
    with open(c3d_file, 'rb') as handle:
        reader = c3d.Reader(handle)
        writer = reader.to_writer('copy_metadata')

        frames = []
        for i, points, analog in reader.read_frames():
            frames.append((points, analog))

    # Harmonise C3D data.
    map_file = os.path.join(marker_maps_dir, f"{gait_lab}.json")
    with open(map_file, 'r') as file:
        marker_map = json.load(file)
    harmonise_markers(writer, marker_map, frames)
    writer.add_frames(frames)

    # Write the harmonised C3D file.
    harmonised_directory = os.path.join(output_directory, 'harmonised')
    if not os.path.exists(harmonised_directory):
        os.makedirs(harmonised_directory)
    with open(os.path.join(harmonised_directory, c3d_file_name), 'wb') as handle:
        writer.write(handle)


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


def harmonise_markers(c3d_writer, marker_mapping, frames):
    """
    Harmonises the marker set of a `c3d` `Writer` object according to a mapping of markers.

    param c3d_writer: The `c3d` `Writer` object to be updated.
    param marker_mapping: A dictionary mapping the trial marker set to the harmonised marker set.
    """
    # Harmonise marker labels.
    point_group = c3d_writer.get('POINT')
    harmonised_labels = []
    for param in ['LABELS', 'LABELS2']:
        if param in point_group.param_keys():
            marker_labels = point_group.get(param).string_array
            reversed_mapping = {value: key for key, value in marker_mapping.items() if value is not None}
            for index, value in numpy.ndenumerate(marker_labels):
                value = value.strip()
                if value in reversed_mapping:
                    harmonised_labels.append(reversed_mapping[value])
                else:
                    harmonised_labels.append(None)
            point_group.remove_param(param)
    c3d_writer.set_point_labels([value for value in harmonised_labels if value])

    # Remove all non-harmonised data points.
    for i in range(len(frames)):
        points, analog = frames[i]
        harmonised_points = []
        for j in range(len(points)):
            if harmonised_labels[j]:
                harmonised_points.append(points[j])
        frames[i] = numpy.array(harmonised_points), analog
