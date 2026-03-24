from typing import List, TypeVar, Generic, Callable, Type, Any, Union, Tuple, get_origin, get_args
import inspect
import itertools
from magicgui.widgets import Label, FileEdit, PushButton, Table, Container, ComboBox, SliceEdit
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
from typing import Iterable, Optional, Tuple as TypingTuple
from tomobase.tiltschemes import TiltScheme

from qtpy.QtWidgets import QWidget, QVBoxLayout, QMenu, QAction, QDockWidget, QLabel
from qtpy.QtCore import Qt

from ...registers import model_controllers, layer_render_types, tilt_controllers, visualize_procedures
from ...controllers.getters import get_image_controller
from ...hooks import custom_magicgui_hook


from dataclasses import dataclass
from typing import Iterable, Optional

from psygnal import Signal

        
def build_tomography_menu(viewer, parent_menu):
    _menus = {}
    #create sorted dict from registers.categories
    sorted_categories = dict(sorted(registers.categories.items(), key=lambda item: item[1]))
    for key, value in sorted_categories.items():
        inheritor = registers.categories.get_inheritor(key)
        if inheritor[0] is None:
            _menus[key] = parent_menu.addMenu(key)
        else:
            _menus[key] = _menus[inheritor[0]].addMenu(key)
    
    for key, value in itertools.chain(registers.processes.items()):
        category = registers.categories.get_key(value.tomobase_category)
        if category in _menus:
            action = _menus[category].addAction(key)
            action.triggered.connect(lambda x, process=value: build_process_widget(process, viewer))
            
    
    for key, value in visualize_procedures.items():
        category = registers.categories.get_key(value.tomobase_category)
        if category in _menus:
            action = _menus[category].addAction(key)
            action.triggered.connect(lambda x, process=value: build_visual_widget(process, viewer))

def build_process_widget(process, viewer):
    sig = inspect.signature(process)

    # ---- threaded wrapper with same signature ----
    @functools.wraps(process)
    def threaded_process(*args, **kwargs):
        gui = threaded_process._gui  # injected after gui is created

        # 2) disable call button while running
        if gui.call_button is not None:
            gui.call_button.native.setEnabled(False)

        # (optional) set a status in napari
        viewer.status = f"Running: {process.__name__}"

        def _reenable():
            if gui.call_button is not None:
                gui.call_button.native.setEnabled(True)
            viewer.status = ""

        @thread_worker
        def work():
            # 1) runs in a background thread
            logger.debug(f"Starting process: {process.__name__} with args: {args} and kwargs: {kwargs}")
            return process(*args, **kwargs)

        worker = work()

        # returned runs on main thread
        @worker.returned.connect
        def _on_returned(result):
            process_names = [item.model.process_name for item in model_controllers.values()]
            if not isinstance(result, Iterable):
                result = [result]
            for item in result:
                logger.debug(f"Process returned: {item}")
                if type(item) in registers.image_types.values() and item.process_name not in process_names:
                    logger.debug(f"Registering new model from process: {item.process_name}")
                    get_image_controller(item)

        @worker.errored.connect
        def _on_error(err):
            # err is an Exception (or a NapariError-like wrapper depending on version)
            logger.exception("Process errored", exc_info=err)
            _reenable()

        @worker.finished.connect
        def _on_finished():
            _reenable()

        worker.start()
        return None  # important: do not block magicgui

    # force wrapper to present the same signature to magicgui
    threaded_process = custom_magicgui_hook(threaded_process)
    threaded_process.__signature__ = sig  # type: ignore[attr-defined]
    gui = magicgui.magicgui(threaded_process, call_button=True, auto_call=False, **threaded_process._magicgui)
    threaded_process._gui = gui  # inject reference so wrapper can disable the button

    viewer.window.add_dock_widget(gui, area="right")
    
    
def build_visual_widget(process, viewer):
    process = custom_magicgui_hook(process)
    gui = magicgui.magicgui(process, call_button=True, auto_call=False, **process._magicgui)