from typing import  Union,  get_origin, get_args, Optional
from types import UnionType
from magicgui.widgets import ComboBox
import inspect

from tomobase.data import ImageAbstract
from ..registers import magic_widgets, model_controllers
from .components import RegisteredComboBox

class ImageComboBoxWidget(RegisteredComboBox):
    def __init__(
        self,
        *,
        value: Optional[ImageAbstract] = None,
        **kwargs,
    ):
        for k in ("nullable", "annotation", "gui_only", "bind"):
            kwargs.pop(k, None)

        self.register = model_controllers
        self.dropbox = ComboBox(label="", choices=[])

        super().__init__(value=value, widgets=[self.dropbox], register=model_controllers, **kwargs)

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
    
magic_widgets['Image'] = (ImageComboBoxWidget, _validate_image_widget)