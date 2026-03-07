
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Dict, Optional, Tuple

import napari
from qtpy.QtWidgets import QAbstractItemView, QMenu, QTreeWidget, QTreeWidgetItem, QToolButton

import numpy as np
from tomobase.utils import set_numpy
from tomobase.data import BaseImageModel
from napari.qt.threading import thread_worker

InitFn = Callable[..., napari.layers.Layer]
UpdateFn = Callable[[napari.layers.Layer, Any], None]  # model is Any/BaseImageModel


@dataclass(frozen=True)
class RendererSpec:
    init: InitFn
    update: UpdateFn


class ImageTypeController:
    # registry: renderer-name -> (init, update)
    renderers: Dict[str, RendererSpec] = {}

    def __init__(self, model):
        self.model = model
        self._viewer = None
        self._layers: Dict[str, napari.layers.Layer] = {}
        self._callbacks: Dict[str, Callable[[], None]] = {}

        try:
            self._viewer = napari.current_viewer()
        except Exception:
            self._viewer = None

    def get_info_for_widget(self):
        _dict = {}
        _dict['Process Name'] = self.model.process_name
        _dict['Sample Name'] = self.model.sample_name
        _dict['Type'] = type(self.model).__name__
        _dict['Shape'] = self.model.data.shape
        _dict['Dtype'] = self.model.data.dtype
        _dict['Metadata'] = self.model.metadata
        return {self.model.process_name: _dict}


    @classmethod
    def register_renderer(cls, name: str, init: InitFn, update: UpdateFn) -> None:
        cls.renderers[name] = RendererSpec(init=init, update=update)

    def add_render(self, name: str, **kwargs) -> napari.layers.Layer:
        """Create the layer and wire it to model.data_changed."""
        if name not in self.renderers:
            raise KeyError(f"Unknown renderer '{name}'. Available: {list(self.renderers)}")

        spec = self.renderers[name]

        # 1) create/init the layer (any layer type)
        layer = spec.init(self.model, viewer=self._viewer, **kwargs)
        self._layers[layer.name] = layer

        # 2) connect update callback and keep a reference so we can disconnect later
        cb = lambda l=layer, m=self.model, u=spec.update: u(l, m)
        self._callbacks[layer.name] = cb
        self.model.data_changed.connect(cb)

        return layer

    def _on_layer_removed(self, event) -> None:
        """Disconnect updates when the user deletes a layer."""
        layer = event.value
        if layer is None:
            return

        name = layer.name
        cb = self._callbacks.pop(name, None)
        if cb is not None:
            try:
                self.model.data_changed.disconnect(cb)
            except Exception:
                pass

        self._layers.pop(name, None)

    def close(self) -> None:
        """Call when controller is destroyed/unloaded."""
        if self._viewer is not None:
            try:
                self._viewer.layers.events.removed.disconnect(self._on_layer_removed)
            except Exception:
                pass

        for name, cb in list(self._callbacks.items()):
            try:
                self.model.data_changed.disconnect(cb)
            except Exception:
                pass

        self._callbacks.clear()
        self._layers.clear()


def _compute_pixel_render(model: BaseImageModel):
    return set_numpy(model.data)

def pixel_init(model: BaseImageModel, viewer=None, **kwargs):
    layer_data = _compute_pixel_render(model)
    name = f"{model.process_name} VolRen"

    contrast_limits = kwargs.pop("contrast_limits", (0, float(np.max(layer_data) * 2.0)))
    layer = napari.layers.Image(layer_data, name=name, contrast_limits=contrast_limits, **kwargs)

    # If you want it added to viewer immediately:
    if viewer is not None:
        viewer.add_layer(layer)
    return layer

def pixel_update(layer, model: BaseImageModel):
    layer.data = _compute_pixel_render(model)
    layer.refresh()


@thread_worker
def _compute_fft(model):
    #xp = model.data.__array_namespace__()
    xp = np
    f = xp.fft.fftshift(xp.fft.fft2(model.data))
    return set_numpy(xp.log1p(xp.abs(f)))

def fft_init(model, viewer=None, **kwargs):
    name = f"{model.process_name} FFT"

    # placeholder layer so init returns a layer immediately
    placeholder = np.zeros((1, 1), dtype=np.float32)
    contrast_limits = kwargs.pop("contrast_limits", (0.0, 1.0))
    layer = napari.layers.Image(placeholder, name=name, contrast_limits=contrast_limits, **kwargs)

    if viewer is not None:
        viewer.add_layer(layer)

    worker = _compute_fft(model)

    @worker.returned.connect
    def _on_done(layer_data):
        # update the existing layer in-place
        layer.data = layer_data
        layer.contrast_limits = (0.0, float(np.max(layer_data) * 2.0))
        layer.refresh()

    worker.start()
    return layer

def fft_update(layer, model):
    # async re-compute on updates too (optional)
    worker = _compute_fft(model)

    @worker.returned.connect
    def _on_done(layer_data):
        layer.data = layer_data
        layer.contrast_limits = (0.0, float(np.max(layer_data) * 2.0))
        layer.refresh()

    worker.start()

ImageTypeController.register_renderer("Pixel Render", pixel_init, pixel_update)
ImageTypeController.register_renderer("FFT Render", fft_init, fft_update)


        
        