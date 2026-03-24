import pathlib
import numpy as np
import napari 
from tomobase.data import Volume, Sinogram
from skimage.measure import marching_cubes

from tomondt.data import VolumeTimeSeries

from tomobase.core.log import logger
from ..controllers.getters import get_image_controller

def read_volume(path):
    """Read a volume from disk."""
    if isinstance(path, str):
        path = pathlib.Path(path)

    return _read_volume

def _read_volume(path):
    vol = Volume.read(path)
    get_image_controller(vol)
    dummy = np.zeros((64, 64, 64), dtype=np.float32)
    z, y, x = np.indices(dummy.shape)
    mask = (z - 32)**2 + (y - 32)**2 + (x - 32)**2 < 15**2
    return [(mask, {"name": "Dummy"}, 'image')]


def read_sinogram(path):
    """Read a volume from disk."""
    if isinstance(path, str):
        path = pathlib.Path(path)

    return _read_sinogram

def _read_sinogram(path):
    vol = Sinogram.read(path)
    get_image_controller(vol)
    dummy = np.zeros((64, 64, 64), dtype=np.float32)
    z, y, x = np.indices(dummy.shape)
    mask = (z - 32)**2 + (y - 32)**2 + (x - 32)**2 < 15**2
    return [(mask, {"name": "Dummy"}, 'image')]


def read_vndt(path):
    """Read a volume from disk."""
    if isinstance(path, str):
        path = pathlib.Path(path)

    return _read_vndt

def _read_vndt(path):
    logger.info(f"Reading VolumeTimeSeries from {path}")
    vol = VolumeTimeSeries.read(path)
    get_image_controller(vol)
    dummy = np.zeros((64, 64, 64), dtype=np.float32)
    z, y, x = np.indices(dummy.shape)
    mask = (z - 32)**2 + (y - 32)**2 + (x - 32)**2 < 15**2
    return [(mask, {"name": "Dummy"}, 'image')]