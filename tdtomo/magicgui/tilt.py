from typing import  Callable, Any, Union, Tuple, get_origin, get_args
from magicgui.widgets import Container, ComboBox, SliceEdit
from collections.abc import Iterable 

from typing import Iterable, Optional, Tuple as TypingTuple
from tomobase.tiltschemes import TiltScheme



from ..registers import magic_widgets, tilt_controllers

from dataclasses import dataclass
from typing import Iterable, Optional

from psygnal import Signal




TiltSchemeValue = Tuple[TiltScheme, slice] 

class TiltSchemeWidget(Container):
    changed = Signal(object)

    def __init__(
        self,
        *,
        value: Optional[TiltSchemeValue] = None,
        choices: Optional[Iterable[tuple[str, Any]]] = None,
        choices_getter: Optional[Callable[[], Iterable[tuple[str, Any]]]] = None,
        **kwargs,
    ):
        for k in ("nullable", "annotation", "gui_only", "bind"):
            kwargs.pop(k, None)

        self._choices_getter = choices_getter
        self._choices_loaded = False

        self.scheme = ComboBox(label="Scheme", choices=list(choices or []))
        self.sl = SliceEdit(label="Slice", value=slice(0, 10, 1))

        super().__init__(widgets=[self.scheme, self.sl], layout="vertical", **kwargs)

        self.scheme.changed.connect(self._emit_changed)
        self.sl.changed.connect(self._emit_changed)

        if value is not None:
            self.value = value

        tilt_controllers.added.connect(self.refresh_choices)
        tilt_controllers.removed.connect(self.refresh_choices)
        tilt_controllers.renamed.connect(self.refresh_choices)  
        tilt_controllers.updated.connect(self.refresh_choices)


    def refresh_choices(self):
        if self._choices_getter is None:
            return

        old_value = None
        try:
            old_value = self.scheme.value
        except Exception:
            pass

        new_choices = list(self._choices_getter())
        self.scheme.choices = new_choices

        if old_value is not None:
            try:
                self.scheme.value = old_value
            except Exception:
                pass

    def _emit_changed(self, *_):
        self.changed.emit(self.value)

    @property
    def value(self) -> TiltSchemeValue:
        return (self.scheme.value, self.sl.value)

    @value.setter
    def value(self, v: TiltSchemeValue) -> None:
        if v is None:
            return
        try:
            model, sl = v
        except Exception:
            return

        try:
            self.scheme.value = model
        except Exception:
            pass

        self.sl.value = sl
        self._emit_changed()
        
        
def _validate_tilt_widget(annotation):
    if get_origin(annotation) is Union:
        for arg in get_args(annotation):
            if get_origin(arg) is tuple:
                t_args = get_args(arg)
                if len(t_args) == 2 and t_args[0] is TiltScheme and t_args[1] is slice:
                    return True
    return False
    
magic_widgets['TiltScheme'] = (TiltSchemeWidget, _validate_tilt_widget, {"choices_getter": lambda: [(name, ctrl.model) for name, ctrl in tilt_controllers.items()]})