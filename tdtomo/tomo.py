
import inspect
import magicgui
import napari
import collections.abc
from collections.abc import Iterable 


from tomobase.globals import logger, proxy, GPUContext, image_datatypes_register, TOMOBASE_TRANSFORM_CATEGORIES, TOMOBASE_PROCESSES


from qtpy.QtWidgets import QWidget, QVBoxLayout, QMenu, QAction, QDockWidget, QLabel
from qtpy.QtCore import Qt


def _buildtomomenu(viewer, parent_menu):
    
    for key, value in TOMOBASE_TRANSFORM_CATEGORIES.items():
        submenu  = parent_menu.addMenu(value.name.replace("_", " ").capitalize())
        _traverse_menu(key, submenu, value.categories)
        
def _traverse_menu(base, parent_menu, element):
    for key, value in element.items():
        if isinstance(value, dict):
            submenu  = parent_menu.addMenu(key)
            _traverse_menu(base, submenu, value)
        else:
            action = parent_menu.addAction(value)
            process = TOMOBASE_PROCESSES[base][value.upper().replace(" ", "_")]

            #action.triggered.connect(lambda x: _build_process_widget(process, viewer))
        pass
    
    
def _buildprocesswidget(process, viewer):
    sig = inspect.signature(process)
    params = sig.parameters

    gui = magicgui.magicgui(process, call_button=True, auto_call=False)
    for name, param in params.items():
        if param.annotation in image_datatypes_register:
            gui[name].choices = [layer.name for layer in viewer.layers if isinstance(layer, image_datatypes_register[param.annotation])]
        if param.default in image_datatypes_register:
            gui[name].choices = [layer.name for layer in viewer.layers if isinstance(layer, image_datatypes_register[param.default])]
    
    viewer.window.add_dock_widget(gui, area='right')