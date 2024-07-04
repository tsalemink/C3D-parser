
import c3d

import numpy as np


def add_frames(self, frames, index=None):
    """
    This method patches a bug present in v0.5.2 which is causing the `from_reader` method to fail.
    """
    sh = np.array(frames, dtype=object).shape
    # Single frame
    if len(sh) != 2:
        frames = np.array([frames], dtype=object)
        sh = np.shape(frames)
    # Sequence of invalid shape
    if sh[1] != 2:
        raise ValueError(
            'Expected frame input to be sequence of point and analog pairs on form (-1, 2). ' +
            'Input was of shape {}.'.format(str(sh)))

    if index is not None:
        self._frames[index:index] = frames
    else:
        self._frames.extend(frames)


def parameter_blocks(self):
    """
    This method patches a bug present in v0.5.2 which is causing the number of bytes in the
    parameter section to be incorrectly calculated.
    """
    byte_count = 4. + sum(g.binary_size() for g in self.group_values())
    return int(np.ceil(byte_count / 512))


def set_point_labels(self, labels, name='LABELS'):
    """
    This method adds an additional `name` parameter to the `set_point_labels` method - to support
    alternative label group names.
    """
    label_str, label_max_size = c3d.Writer.pack_labels(labels)
    self.point_group.add_str(name, 'Point labels.', label_str, label_max_size, len(labels))


# Patch methods.
c3d.Writer.add_frames = add_frames
c3d.Reader.parameter_blocks = parameter_blocks
c3d.Writer.parameter_blocks = parameter_blocks
c3d.Writer.set_point_labels = set_point_labels
