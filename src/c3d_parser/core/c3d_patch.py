
import c3d

import numpy as np

from c3d_parser.settings.logging import logger


# Set variables required by patch functions.
check_metadata_base = c3d.Reader._check_metadata


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


def _check_metadata(self):
    """
    For cases where the C3D headers have not been correctly set.
    """
    if self._header.scale_factor == -1.0 and self._header.scale_factor != self.point_scale:
        logger.warning(f"Header scale factor ({self._header.scale_factor}) does not match metadata ({self.point_scale}). Updating header.")
        self._header.scale_factor = self.point_scale

    check_metadata_base(self)


def add_param(self, name, **kwargs):
    """
    This method overrides `add_param` so that it can handle C3D files created in Nexus versions
    earlier than 2.0. For some reason these files cause `c3d` to crash when reading them in,
    claiming that the parameters already exist.

    When this function is called to create a parameter that already exists, it will return instead
    of raising an error.
    """
    if not isinstance(name, str):
        raise TypeError("Expected 'name' argument to be a string, was of type {}".format(type(name)))
    name = name.upper()
    if name in self._params:
        logger.warning(f"Duplicate parameters found in input file.")
        return
    self._params[name] = c3d.Param(name, self._dtypes, **kwargs)


# Patch methods.
c3d.Writer.add_frames = add_frames
c3d.Reader.parameter_blocks = parameter_blocks
c3d.Writer.parameter_blocks = parameter_blocks
c3d.Writer.set_point_labels = set_point_labels
c3d.Reader._check_metadata = _check_metadata
c3d.Group.add_param = add_param
