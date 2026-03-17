from tomobase.data import Volume
import enum

import napari
import numpy as np

from ...registers import model_controllers, layer_render_types
from .base import ImageTypeController

class VolumeNDtController(ImageTypeController):
    def __init__(self, model):
        super().__init__(model)

        


        
        