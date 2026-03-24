import magicgui
from magicgui.widgets import Container, Label

import napari
import collections.abc
from collections.abc import Iterable 

from tomobase.core.log import logger
from tomobase.core.environment import GPUContext, proxy



from qtpy.QtWidgets import QWidget, QVBoxLayout, QMenu, QAction, QDockWidget, QLabel
from qtpy.QtCore import Qt

def build_context_widget(viewer: 'napari.viewer.Viewer'):
    """Build the context widget for the viewer.

    Args:
        viewer (napari.viewer.Viewer): The napari viewer instance.
    """
    
    gui = magicgui.magicgui(proxy.set_context, 
                            call_button=False, 
                            auto_call=True, 
                            context={"choices": list(GPUContext), 'value':proxy.context},
                            device={"value":proxy.device, 'min':0, 'max':20})
                            
    viewer.window.add_dock_widget(gui, name='Context', area='right')