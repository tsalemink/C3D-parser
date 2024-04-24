
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


# Patch methods.
c3d.Writer.add_frames = add_frames
c3d.Reader.parameter_blocks = parameter_blocks
c3d.Writer.parameter_blocks = parameter_blocks
