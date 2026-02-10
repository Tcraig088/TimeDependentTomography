import inspect
import magicgui
from magicgui.widgets import Container, Label

import napari
import collections.abc
from collections.abc import Iterable 

from qtpy.QtWidgets import QWidget, QVBoxLayout, QMenu, QAction, QDockWidget, QLabel
from qtpy.QtCore import Qt
from tdtomo.utils import _buildselectioninfowidgets



def _build_selection_info(layer):
    gui = Container()
    
    name = Label(value=f"Layer: {layer.name}")
    gui.native.layout().addWidget(name.native)
    
    data_type = Label(value=f"Type: {type(layer).__name__}")
    gui.native.layout().addWidget(data_type.native)

    for key, value in layer.metadata['ct metadata'].items():
        note = Label(value=f"{key}: {value}")
        gui.native.layout().addWidget(note.native)

    return gui

def _checklayertype(layer: 'napari.layers.Layer'):
    if 'ct metadata' not in layer.metadata:
        return False
    return layer

def _build_layer_info(viewer: 'napari.viewer.Viewer'):
    """Build the layer info widget for the viewer.

    Args:
        viewer (napari.viewer.Viewer): The napari viewer instance.
    """
    main_window = viewer.window._qt_window
    for child in main_window.children():
        if child.objectName() == "layer list":
            layer_list = child
            break
    
    selection = viewer.layers.selection.active
    valid_selections = []
    if selection is not None:
        if isinstance(selection, Iterable):
            for layer in selection:
                if _checklayertype(layer):
                    valid_selections.append(layer)
        else:
            if _checklayertype(selection):
                valid_selections.append(selection)
    
    gui = Container()
    gui.native.layout().addWidget(Label(value=f"Selected TDTOMO Layers: {len(valid_selections)}").native)
    for layer in valid_selections:
        subwindow = _build_selection_info(layer)
        gui.native.layout().addWidget(subwindow.native)
 
    docked_gui = viewer.window.add_dock_widget(gui.native, name='Layer Information', area='right')
    
    if layer_list is not None:
        viewer.window._qt_window.tabifyDockWidget(layer_list, docked_gui)
    return