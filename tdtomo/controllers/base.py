
import enum
import napari
import numpy as np


import magicgui
from magicgui.widgets import Container, Label, FileEdit, PushButton, Table

import collections.abc
from collections.abc import Iterable

from qtpy.QtCore import Qt


from ..registers import model_controllers, layer_render_types

class ImageTypeController():
    def __init__(self, model):
        self.model = model
        self._compatibile_views = ['Pixel Render']
        self._views = {}
        # attach to the current viewer's layer-removed event (if available)
        self._viewer = None
        self.info_widget = Container(labels=False, layout="vertical")
        try:
            self._viewer = napari.current_viewer()
        except Exception:
            self._viewer = None
        if self._viewer is not None:
            self._viewer.layers.events.removed.connect(self._disconnect_layers)
        self.create_infoview()
    def _check_view(self, view_type: int):
        compatible_view_values = [layer_render_types[view] for view in self._compatibile_views]
        if view_type not in compatible_view_values:
             raise ValueError(f"View type {view_type} is not compatible with model type {type(self.model)}")

    
    def _disconnect_layers(self, events):
        for key, value in self._views.items():
            # check against the current viewer's layers
            layers = self._viewer.layers if self._viewer is not None else []
            if value.name in [layer.name for layer in layers]:
                self.model.data_changed.disconnect(value.refresh)
                del self._views[key]

    def _disconnect(self):
        if self._viewer is not None:
            self._viewer.layers.events.removed.disconnect(self._disconnect_layers)
        for key, value in self._views.items():
            self.model.data_changed.disconnect(value.refresh)
        self._views = {}
        
        
    def add_view(self, view_type: int):
        if view_type == layer_render_types['Pixel Render']:
            self._add_pixel_render_view()
                
    def _add_pixel_render_view(self, **kwargs):
        name = self.model.process_name + f" [{len(self._views)}]"
        self._views[name] = napari.layers.Image(self.model.data, name=name, contrast_limits=[0, np.max(self.model.data)*1.5], **kwargs)
        self._viewer.add_layer(self._views[name])
        self.model.data_changed.connect(self._views[name].refresh)
    
    def create_infoview(self):
        
        values = Container(labels=True, layout="vertical")
        values.native.layout().setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        values.append(Label(name="Sample Name:", value=self.model.sample_name))
        values.append(Label(name="Process Name:", value=self.model.process_name))
        values.append(Label(name="Pixel Size (nm):", value=self.model.pixelsize))
        self.info_widget.append(values)


        


        
        