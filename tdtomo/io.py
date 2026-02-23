
import inspect
import magicgui
import napari
import collections.abc
from collections.abc import Iterable 


from tomobase.log import logger
from tomobase import registers

from .controllers.controllers import get_controller
from qtpy.QtWidgets import QWidget, QVBoxLayout, QMenu, QAction, QDockWidget, QLabel
from qtpy.QtCore import Qt

def _buildiomenu(viewer, parent_menu):
    phantoms_menu = parent_menu.addMenu('Phantoms')
    for key, value in registers.phantoms.items():
        action  = phantoms_menu.addAction(key)
        action.triggered.connect(lambda x, phantom=value: _buildphantomwidget(phantom, viewer))
    
    
    for key, value in registers.image_types.items():
        action  = parent_menu.addAction(key)
        action.triggered.connect(lambda x, img_type=value: _buildiowidget(img_type, viewer))

def _buildiowidget(img_type, viewer):
    result = img_type.from_file()
    return get_controller(result)

def _buildphantomwidget(phantom, viewer):
    widget = magicgui.magicgui(phantom, call_button=True, auto_call=False)
    viewer.window.add_dock_widget(widget, area='right')
    widget.called.connect(lambda result: get_controller(result))
