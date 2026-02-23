from tomobase.data import Volume
import enum

import napari
import numpy as np

from ..registers import model_controllers, layer_render_types
from .base import ImageTypeController

class SinogramController(ImageTypeController):
    def __init__(self, model):
        super().__init__(model)
        self._compatibile_views = ['Pixel Render']
        self.add_view(layer_render_types['Pixel Render'])
        
    def add_view(self, view_type: int):
        self._check_view(view_type)
        super().add_view(view_type)
        


        
        