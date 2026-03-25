import inspect
from magicgui.widgets import Select
import copy

from ...submodules.tomobase.tomobase.backends.qt.magicgui_widgets import *
from .registers import magic_widgets
from tomobase.core.log import logger

def custom_magicgui_hook(func):
    sig = inspect.signature(func)
    func._magicgui = getattr(func, '_magicgui', {})
    for param in sig.parameters.values():
        for key, value in magic_widgets.items():
            if value[1] is not None:
                if value[1](param.annotation):
                    func._magicgui[param.name] = {"widget_type": value[0]}
                
            if param.name == 'measurements':
                func._magicgui[param.name] = {"widget_type": value[0]}
    return func


def visualize_hook(func):
    def decorator(*args, **kwargs):
        func(*args, **kwargs)
        
        func.tomobase_name = kwargs.get("name", func.__name__)
        func.is_tdtomo_visualizer = True
        func.tomobase_category = kwargs.get("category", 0)
        if func.__name__ == func.tomobase_name:
            func.tomobase_name = copy.deepcopy(func.__name__)
            func.tomobase_name = func.tomobase_name.replace('_', ' ').title()
        return func
    return decorator



