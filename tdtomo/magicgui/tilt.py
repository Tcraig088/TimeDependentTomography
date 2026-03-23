from typing import  Union, Tuple, get_origin, get_args, Optional, Tuple 
from magicgui.widgets import ComboBox, SliceEdit

from tomobase.tiltschemes import TiltScheme

from ..registers import magic_widgets, tilt_controllers
from .components import RegisteredComboBox

TiltSchemeValue = Tuple[TiltScheme, slice] 

class TiltSchemeWidget(RegisteredComboBox):
    def __init__(
        self,
        *,
        value: Optional[TiltSchemeValue] = None,
        **kwargs,
    ):
        for k in ("nullable", "annotation", "gui_only", "bind"):
            kwargs.pop(k, None)

        self.scheme = ComboBox(label="Scheme", choices=[])
        self.sl = SliceEdit(label="Slice", value=slice(0, 10, 1))

        super().__init__(value=value, widgets=[self.scheme, self.sl], register= tilt_controllers, **kwargs)

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

        
        
def _validate_tilt_widget(annotation):
    if get_origin(annotation) is Union:
        for arg in get_args(annotation):
            if get_origin(arg) is tuple:
                t_args = get_args(arg)
                if len(t_args) == 2 and t_args[0] is TiltScheme and t_args[1] is slice:
                    return True
    return False
    
magic_widgets['TiltScheme'] = (TiltSchemeWidget, _validate_tilt_widget)