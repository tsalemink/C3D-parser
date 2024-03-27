
import c3d
import numpy as np


# TODO: Simplify this function.
def read_c3d(file_path):
    with open(file_path, 'rb') as handle:
        reader = c3d.Reader(handle)

        # Get units.
        units = reader.get('POINT').get('UNITS').string_value

        # Get marker labels.
        markers = {'time': []}
        count = 0
        marker_labels = ['time']
        for pl in reader.point_labels:
            lb = pl.strip()
            if len(lb) == 0:
                lb = 'M{:03d}'.format(count)
                count += 1
            marker_labels.append(lb)
            markers[lb] = []

        # Get marker data and analog data.
        analogs = []
        for i, points, analog in reader.read_frames():
            analogs.append(analog[:, 0])
            markers[marker_labels[0]].append((i-1)*(1/reader.point_rate))
            for j in range(1, len(marker_labels)):
                errors = points[j-1, 3:]
                p = points[j-1, 0:3]
                for e in errors:
                    if e == -1:
                        p = np.asarray([np.NaN, np.NaN, np.NaN])
                        break
                markers[marker_labels[j]].append(p)

        c3d_data = {'markers': markers, 'mocap': {"rates": reader.point_rate, "units": units, "header": reader.header}, "analog": analogs}
    return c3d_data
