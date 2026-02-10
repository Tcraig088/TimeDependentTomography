

from enum import Enum
from tomobase.data import Sinogram, Image, Volume
from .registration import _modules
if _modules.tomondt:
    from tomondt.data import VolumeTimeSeries 

class ViewType(Enum):
    DEFAULT = 0
    SINOGRAM = 1
    IMAGE = 2
    VOLUME = 3
    VOLUME_TIME_SERIES = 4
    ORTHOSLICE = 5
    DIFFERENCEMAP = 6


class LayerController:
    def __init__(self, model, view_Type=ViewType.DEFAULT, attributes={}):
        self.model = model
        
        if self.view_type == ViewType.DEFAULT:
            if isinstance(self.model, Sinogram):
                view_type = ViewType.SINOGRAM
            elif isinstance(self.model, Image):
                view_type = ViewType.IMAGE
            elif isinstance(self.model, Volume):
                    view_type = ViewType.VOLUME
                    

        def _on_close(event):
            self.model.remove_layer(self.view.layer)
            event.accept()