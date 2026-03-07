
import coolname
from tomobase.data import Volume, Sinogram, Image

from ..registers import model_controllers, tilt_controllers, struct_data_controllers

from .image_controllers import VolumeController, SinogramController
from .tilt import TiltController

def get_image_controller(model):
    if isinstance(model, Volume):
        model_controllers[model.process_name] = VolumeController(model)
    elif isinstance(model, Sinogram):
        model_controllers[model.process_name] = SinogramController(model)
    else:
        raise ValueError(f"Model type {type(model)} is not supported")
    
def get_tilt_controller(model):
    tilt_controllers[coolname.generate_slug(2)] = TiltController(model)


def get_data_controller(model):
    pass
        #struct_data_controllers['Bubbly'] = model