from typing import  Callable, Any, Union,  get_origin, get_args, Iterable, Optional
from types import UnionType
from unicodedata import name
from magicgui.widgets import Container, ComboBox
from collections.abc import Iterable 
import inspect
from typing import Iterable, Optional
from psygnal import Signal

from tomobase.data import ImageAbstract
from tomobase import registers

from ..registers import magic_widgets, model_controllers

class ImageComboBoxWidget(Container):
    changed = Signal(object)

    def __init__(
        self,
        *,
        value: Optional[ImageAbstract] = None,
        choices_getter: Optional[Callable[[], Iterable[tuple[str, Any]]]] = None,
        **kwargs,
    ):
        for k in ("nullable", "annotation", "gui_only", "bind"):
            kwargs.pop(k, None)

        self._choices_getter = choices_getter
        self.combo = ComboBox(label="", choices=[])

        super().__init__(widgets=[self.combo], layout="vertical", **kwargs)

        self.combo.changed.connect(self._emit_changed)


        self.refresh_choices()
        model_controllers.added.connect(self.refresh_choices)
        model_controllers.removed.connect(self.refresh_choices)
        model_controllers.renamed.connect(self.refresh_choices)
        model_controllers.updated.connect(self.refresh_choices)

        if value is not None:
            self.value = value

    def refresh_choices(self, *args):
        print("Refreshing image choices...")
        if self._choices_getter is None:
            return
        print("Getting new choices...")
        self.combo.choices = list(self._choices_getter())
        print(f"New choices: {self.combo.choices}, {list(self._choices_getter())}")
        self.combo.native.update()
        self.native.update()

    def _emit_changed(self, *args):
        self.changed.emit(self.value)

    @property
    def value(self) -> ImageAbstract:
        return self.combo.value

    @value.setter
    def value(self, v: ImageAbstract):
        try:
            self.combo.value = v
        except Exception:
            pass
        self._emit_changed()
        
        
def _is_none_type(x):
    return x is type(None)


def _is_union(annotation):
    return get_origin(annotation) in (Union, UnionType)


def _is_image_class(annotation):
    return inspect.isclass(annotation) and issubclass(annotation, ImageAbstract)


def _validate_image_widget(annotation):
    # plain class: ImageAbstract or subclass
    if _is_image_class(annotation):
        return True

    # Union[...] or X | Y
    if _is_union(annotation):
        args = [a for a in get_args(annotation) if not _is_none_type(a)]
        return len(args) > 0 and all(_is_image_class(a) for a in args)

    return False
    
magic_widgets['Image'] = (ImageComboBoxWidget, _validate_image_widget, {"choices_getter": lambda: [(name, ctrl.model) for name, ctrl in model_controllers.items()]})