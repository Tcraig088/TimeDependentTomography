from typing import List, TypeVar, Generic, Callable, Type, Any, Union
import inspect
import magicgui
import napari
import collections.abc
from collections.abc import Iterable 
import inspect
import functools
from napari.qt.threading import thread_worker

from tomobase.core import registers
from tomobase.core.log import logger
from tomobase.core.environment import GPUContext, proxy


from qtpy.QtWidgets import QWidget, QVBoxLayout, QMenu, QAction, QDockWidget, QLabel
from qtpy.QtCore import Qt

from ...controllers.getters import get_tilt_controller


def build_tilt_widget(tiltscheme, viewer):
    gui = magicgui.magicgui(tiltscheme, call_button=True, auto_call=False)
    viewer.window.add_dock_widget(gui, area='right')
    gui.called.connect(lambda result: get_tilt_controller(result))
    

def build_tilting_menu(viewer, parent_menu):
    _menus = {}
    for key, value in registers.tiltschemes.items():
        action = parent_menu.addAction(key)
        action.triggered.connect(lambda x, tiltscheme=value: build_tilt_widget(tiltscheme, viewer))
        
