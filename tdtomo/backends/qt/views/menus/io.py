
import inspect
import magicgui
import napari
import collections.abc
from collections.abc import Iterable 


from tomobase.core.log import logger
from tomobase.core import registers

from .....domain.controllers.getters import get_image_controller
from qtpy.QtWidgets import QWidget, QVBoxLayout, QMenu, QAction, QDockWidget, QLabel
from qtpy.QtCore import Qt

def build_io_menu(viewer, parent_menu):
    phantoms_menu = parent_menu.addMenu('Phantoms')
    for key, value in registers.phantoms.items():
        action  = phantoms_menu.addAction(key)
        action.triggered.connect(lambda x, phantom=value: build_phantom_widget(phantom, viewer))
    
    
    for key, value in registers.image_types.items():
        action  = parent_menu.addAction(key)
        action.triggered.connect(lambda x, img_type=value: build_io_widget(img_type, viewer))

def build_io_widget(img_type, viewer):
    result = img_type.from_file()
    return get_image_controller(result)

def build_phantom_widget(phantom, viewer):
    widget = magicgui.magicgui(phantom, call_button=True, auto_call=False)
    viewer.window.add_dock_widget(widget, area='right')
    widget.called.connect(lambda result: get_image_controller(result))
