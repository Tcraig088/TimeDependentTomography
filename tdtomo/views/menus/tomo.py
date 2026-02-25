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

from tomobase import registers
from tomobase.log import logger
from tomobase.environment import GPUContext, proxy
from typing import Iterable, Optional, Tuple as TypingTuple
from tomobase.tiltschemes import TiltScheme

from qtpy.QtWidgets import QWidget, QVBoxLayout, QMenu, QAction, QDockWidget, QLabel
from qtpy.QtCore import Qt

from ...registers import model_controllers, layer_render_types, tilt_controllers
from ...controllers.getters import get_image_controller



from dataclasses import dataclass
from typing import Iterable, Optional

from psygnal import Signal


TiltSchemeValue = Tuple[TiltScheme, slice]   # (model, slice)


class TiltSchemeWidget(Container):
    changed = Signal(object)

    def __init__(
        self,
        *,
        value: Optional[TiltSchemeValue] = None,
        choices: Iterable[tuple[str, Any]],
        **kwargs,
    ):
        # magicgui may pass these depending on version; ignore them safely
        for k in ("nullable", "annotation", "gui_only", "bind"):
            kwargs.pop(k, None)

        # choices are (label, model) pairs; ComboBox.value will be the model
        self.scheme = ComboBox(label="Scheme", choices=list(choices))
        self.sl = SliceEdit(label="Slice", value=slice(0, 10, 1))

        super().__init__(widgets=[self.scheme, self.sl], layout="vertical", **kwargs)

        self.scheme.changed.connect(self._emit_changed)
        self.sl.changed.connect(self._emit_changed)

        if value is not None:
            self.value = value

    def _emit_changed(self, *_):
        self.changed.emit(self.value)

    @property
    def value(self) -> TiltSchemeValue:
        # scheme.value is the *model*
        return (self.scheme.value, self.sl.value)

    @value.setter
    def value(self, v: TiltSchemeValue) -> None:
        if v is None:
            return
        try:
            model, sl = v
        except Exception:
            return

        # Set by VALUE (model). This works even though labels are strings.
        # If the model isn't present, leave scheme unchanged.
        try:
            self.scheme.value = model
        except Exception:
            # Some backends raise if model not in choices; ignore.
            pass

        self.sl.value = sl
        self._emit_changed()
        
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
    
    for key, value in registers.processes.items():
        category = registers.categories.get_key(value.tomobase_category)
        if category in _menus:
            action = _menus[category].addAction(key)
            action.triggered.connect(lambda x, process=value: build_process_widget(process, viewer))

def build_process_widget(process, viewer):
    sig = inspect.signature(process)
    params = sig.parameters

    _dict = {}
    for name, param in params.items():
        if param.annotation in registers.image_types.values():
            _dict[name] = {
                "choices": [
                    (n, v.model)
                    for n, v in model_controllers.items()
                    if isinstance(v.model, registers.image_types[param.annotation.__name__])
                ]
            }

        # Union[...] of image types
        if hasattr(param.annotation, "__origin__") and param.annotation.__origin__ is Union and all(isinstance(t, type) and t.__name__ in registers.image_types for t in param.annotation.__args__):
            types = param.annotation.__args__
            _dict[name] = {
                "choices": [
                    (n, v.model)
                    for n, v in model_controllers.items()
                    if any(isinstance(v.model, registers.image_types[t.__name__]) for t in types)
                ]
            }
        # Union includes a Tuple with TiltScheme (use get_origin/get_args for reliability)
        if get_origin(param.annotation) is Union:
            for arg in get_args(param.annotation):
                # typing.Tuple[...] has origin `tuple`
                if get_origin(arg) is tuple:
                    t_args = get_args(arg)
                    if len(t_args) == 2 and t_args[0] is TiltScheme and t_args[1] is slice:
                        _dict[name] = {
                            "widget_type": TiltSchemeWidget,
                            "choices": [
                                (n, v.model)
                                for n, v in tilt_controllers.items()
                            ]
                        }
                elif isinstance(arg, type) and arg.__name__ in registers.image_types:
                    _dict[name] = {
                        "choices": [
                            (n, v.model)
                            for n, v in model_controllers.items()
                            if isinstance(v.model, registers.image_types[arg.__name__])
                        ]
                    }
                    

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
    threaded_process.__signature__ = sig  # type: ignore[attr-defined]

    gui = magicgui.magicgui(threaded_process, call_button=True, auto_call=False, **_dict)
    threaded_process._gui = gui  # inject reference so wrapper can disable the button

    viewer.window.add_dock_widget(gui, area="right")