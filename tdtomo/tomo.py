
import inspect
import magicgui
import napari
import collections.abc
from collections.abc import Iterable 


from tomobase import registers
from tomobase.log import logger
from tomobase.environment import GPUContext, proxy


from qtpy.QtWidgets import QWidget, QVBoxLayout, QMenu, QAction, QDockWidget, QLabel
from qtpy.QtCore import Qt


def _buildtomomenu(viewer, parent_menu):
    _menus = {}
    #create sorted dict from registers.categories
    sorted_categories = dict(sorted(registers.categories.items(), key=lambda item: item[1]))
    for key, value in sorted_categories.items():
        inheritor = registers.categories.get_inheritor(key)
        if inheritor[0] is None:
            _menus[key] = parent_menu.addMenu(key)
        else:
            _menus[key] = _menus[inheritor[0]].addMenu(key)
    
    for key, value in registers.processes.items():
        category = registers.categories.get_key(value.tomobase_category)
        if category in _menus:
            action = _menus[category].addAction(key)
            action.triggered.connect(lambda x, process=value: _buildprocesswidget(process, viewer))

def _buildprocesswidget(process, viewer):
    sig = inspect.signature(process)
    params = sig.parameters

    gui = magicgui.magicgui(process, call_button=True, auto_call=False)
    for name, param in params.items():
        if param.annotation in registers.image_types:
            gui[name].choices = [layer.name for layer in viewer.layers if isinstance(layer, registers.image_types[param.annotation])]
        if param.default in registers.image_types:
            gui[name].choices = [layer.name for layer in viewer.layers if isinstance(layer, registers.image_types[param.default])]
    
    viewer.window.add_dock_widget(gui, area='right')