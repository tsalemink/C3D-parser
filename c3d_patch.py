
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


# Patch `add_frames` method.
c3d.Writer.add_frames = add_frames
