import magicgui
from magicgui.widgets import Container, Label, FileEdit, PushButton, Table

from pathlib import Path
import pickle
import napari
import collections.abc
from collections.abc import Iterable 

from tomobase.data import BaseImageModel
from tomobase.log import logger
from tomobase.environment import GPUContext, proxy
from tomobase import registers
from tomobase.phantoms.nanocage import get_nanocage

from qtpy.QtWidgets import QWidget, QVBoxLayout, QMenu, QAction, QDockWidget, QLabel, QFrame, QFileDialog, QApplication, QAbstractItemView, QToolButton, QTableWidgetItem
from qtpy.QtCore import Qt

from tdtomo.views.ui.image_list import refresh_table


from ...registers import model_controllers, layer_render_types
from tomobase.data import *


info_widget = Container(labels=False,layout="vertical")


def refresh_info_widget():
    info_widget.clear()
    for key, value in model_controllers.items():
        info_widget.append(model_controllers[key].info_widget)

def build_info_widget(viewer: 'napari.viewer.Viewer'):
    """Build the workspace widget for the viewer and dock it on the left.

    This will attempt to create a FunctionGui backed by `models_widget` and set
    the default parameter value to the current `_models` dictionary. If that
    fails for any reason, it will fall back to creating the Container directly
    and docking it.
    """
    main_window = getattr(viewer.window, "_qt_window", None)
    layer_list = None
    if main_window is not None:
        for child in main_window.children():
            try:
                if child.objectName() == "layer controls":
                    layer_controls = child
                    break
            except Exception:
                continue
    
    docked_gui = viewer.window.add_dock_widget(info_widget, name='Model Info', area='left')

    model_controllers.removed.connect(refresh_info_widget)
    model_controllers.added.connect(refresh_info_widget)
    model_controllers.updated.connect(refresh_info_widget)

    refresh_info_widget()  
    if layer_controls is not None:
        try:
            viewer.window._qt_window.tabifyDockWidget(layer_controls, docked_gui)
        except Exception:
            pass
    return docked_gui