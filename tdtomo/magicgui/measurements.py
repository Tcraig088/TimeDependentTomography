from typing import  Callable, Any, Union,  get_origin, get_args, Iterable, Optional
from unicodedata import name
from magicgui.widgets import Container, ComboBox, Select
from collections.abc import Iterable 

from typing import Iterable, Optional
from psygnal import Signal

from tomobase.data import ImageAbstract
from tomobase import registers

from ..registers import magic_widgets, struct_data_controllers

class MeasurementsSelectWidget(Container):
    changed = Signal(object)

    def __init__(
        self,
        *,
        value: Optional[list[Any]] = None,
        choices: Optional[Iterable[tuple[str, Any]]] = None,
        choices_getter: Optional[Callable[[], Iterable[tuple[str, Any]]]] = None,
        **kwargs,
    ):
        for k in ("nullable", "annotation", "gui_only", "bind"):
            kwargs.pop(k, None)

        self._choices_getter = choices_getter
        self._choices_loaded = False

        self.select = Select(
            label="Measurements",
            choices=list(choices or []),
            value=value or [],
        )

        super().__init__(widgets=[self.select], layout="vertical", **kwargs)

        self.select.changed.connect(self._emit_changed)
        struct_data_controllers.added.connect(self.refresh_choices)
        struct_data_controllers.removed.connect(self.refresh_choices)
        struct_data_controllers.renamed.connect(self.refresh_choices)
        struct_data_controllers.updated.connect(self.refresh_choices)


    def refresh_choices(self):
        if self._choices_getter is None:
            return

        old_value = []
        try:
            old_value = list(self.select.value)
        except Exception:
            pass

        new_choices = list(self._choices_getter())
        self.select.choices = new_choices

        if old_value:
            valid_values = [v for _, v in new_choices]
            restored = [v for v in old_value if v in valid_values]
            try:
                self.select.value = restored
            except Exception:
                pass

    def _emit_changed(self, *_):
        self.changed.emit(self.value)

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
        self._emit_changed()
        

magic_widgets['Measurement'] = (MeasurementsSelectWidget, None, {"choices_getter": lambda: [(name, ctrl.model) for name, ctrl in struct_data_controllers.items()]})