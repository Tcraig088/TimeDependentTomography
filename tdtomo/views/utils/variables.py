import magicgui
from magicgui.widgets import Container, Label

import napari
import collections.abc
from collections.abc import Iterable 


from tomobase.globals import logger, proxy, GPUContext, image_datatypes_register


from qtpy.QtWidgets import QWidget, QVBoxLayout, QMenu, QAction, QDockWidget, QLabel
from qtpy.QtCore import Qt

def variables_widget(table:dict[str, int]):
    pass

def _build_variables_widget(viewer: 'napari.viewer.Viewer'):
    """Build the workspace widget for the viewer.
    Args:
        viewer (napari.viewer.Viewer): The napari viewer instance.
    """
    main_window = viewer.window._qt_window
    for child in main_window.children():
        if child.objectName() == "layer list":
            layer_list = child
            break


    gui = magicgui.magicgui(variables_widget, call_button=True)
    docked_gui = viewer.window.add_dock_widget(gui, name='variables list', area='left')
    
    if layer_list is not None:
        viewer.window._qt_window.tabifyDockWidget(layer_list, docked_gui)
    return