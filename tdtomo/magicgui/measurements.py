from typing import  Callable, Any, Iterable, Optional
from unicodedata import name
from magicgui.widgets import  Select
from collections.abc import Iterable 

from typing import Iterable, Optional
from psygnal import Signal



from ..registers import magic_widgets, struct_data_controllers
from .components import RegisteredComboBox

class MeasurementsSelectWidget(RegisteredComboBox):
    changed = Signal(object)

    def __init__(
        self,
        *,
        value: Optional[list[Any]] = None,
        **kwargs,
    ):
        for k in ("nullable", "annotation", "gui_only", "bind"):
            kwargs.pop(k, None)

        self.select = Select(label="",choices=[],value=value or [])

        super().__init__(value=value, widgets=[self.select], register= struct_data_controllers,  **kwargs)

    @property
    def value(self) -> list[Any]:
        try:
            return list(self.select.value)
        except Exception:
            return []

    @value.setter
    def value(self, v: Optional[list[Any]]) -> None:
        try:
            self.select.value = list(v or [])
        except Exception:
            pass

magic_widgets['Measurement'] = (MeasurementsSelectWidget, None)