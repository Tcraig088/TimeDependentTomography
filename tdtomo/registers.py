from typing import Tuple, Callable, Any, Dict, Union
from qtpy.QtCore import QObject, Signal

from tomobase import registers
from tomobase.log import logger


class ModuleDict():
    """
    Singleton class to check if submodules are available or not.

    Attributes:
    tomobase (bool): True if tomobase is available, False otherwise.
    tomoacquire (bool): True if tomoacquire is available, False otherwise.
    
    """
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ModuleDict, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        self._tomobase_checked = False
        self._tomobase_available = False
        self._tomoacquire_checked = False
        self._tomoacquire_available = False
        self._tomondt_checked = False
        self._tomondt_available = False
    
    @property    
    def tomobase(self):
        if not self._tomobase_checked:
            try:
                import tomobase
                self._tomobase_available = True
            except ModuleNotFoundError:
                self._tomobase_available = False
                logger.error("tomobase module not found.")
            except Exception as e:
                self._tomobase_available = False
                logger.error(e)
        self._tomobase_checked = True
        return self._tomobase_available
    
    @property
    def tomoacquire(self):
        if not self._tomoacquire_checked:
            try:
                import tomoacquire
                self._tomoacquire_available = True
            except Exception as e:
                self._tomoacquire_available = False
                logger.error(e)
        self._tomoacquire_checked = True
        return self._tomoacquire_available
    
    @property
    def tomondt(self):
        if not self._tomondt_checked:
            try:
                import tomondt
                self._tomondt_available = True
            except Exception as e:
                self._tomondt_available = False
                logger.error(e)
        self._tomondt_checked = True
        return self._tomondt_available
            
_modules = ModuleDict()


model_controllers = registers.Registry(str, object)
data_controllers = registers.Registry(str, object)
tilt_controllers = registers.Registry(str, object)
struct_data_controllers = registers.Registry(str, object)

plot_render_types = registers.Registry(str, int)
plot_render_types['xy'] = 0 

layer_render_types = registers.Registry(str, int)
layer_render_types['Pixel Render'] = 0
layer_render_types['FFT Render'] = 1

magic_widgets = registers.Registry(str, object)