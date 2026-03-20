import inspect
import itertools
from magicgui.widgets import Select


from .magicgui import *
from .registers import magic_widgets
from tomobase.log import logger

def magic_gui_dict_builder(func):
    logger.debug(f"Building magicgui dict for function {func.__name__}")
    sig = inspect.signature(func)
    func._magicgui = getattr(func, '_magicgui', {})
    logger.debug(f"Function signature: {sig}, func._magicgui before: {func._magicgui}")
    for param in sig.parameters.values():
        logger.debug(f"Processing parameter: {param.name}, annotation: {param.annotation}")
        for key, value in magic_widgets.items():
            logger.debug(f"Checking against magic widget: {key}, value: {value}")
            if value[1] is not None:
                if value[1](param.annotation):
                    logger.debug(f"Parameter {param.name} matches magic widget: {key}")
                    func._magicgui[param.name] = {
                        "widget_type": value[0],
                        **value[2]
                    }
                
            if param.name == 'measurements':
                logger.debug(f"Special case for 'measurements' parameter, annotation: {param.annotation}")
                func._magicgui[param.name] = {
                    "widget_type": value[0],
                    **value[2]
                }
    return func
