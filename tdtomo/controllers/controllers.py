from tomobase.data import Volume, Sinogram, Image

from ..registers import model_controllers
from .volume import VolumeController
from .sinogram import SinogramController

def get_controller(model):
    if isinstance(model, Volume):
        model_controllers[model.process_name] = VolumeController(model)
    elif isinstance(model, Sinogram):
        model_controllers[model.process_name] = SinogramController(model)
    else:
        raise ValueError(f"Model type {type(model)} is not supported")