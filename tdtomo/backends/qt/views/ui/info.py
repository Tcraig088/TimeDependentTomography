from xml.parsers.expat import model

import magicgui
from magicgui.widgets import Container, Label, FileEdit, PushButton, Table

from pathlib import Path
import pickle
import napari
import collections.abc
from collections.abc import Iterable 

from tomobase.core.data_classes import ImageAbstract
from tomobase.core.log import logger
from tomobase.core.environment import GPUContext, proxy
from tomobase.core import registers
from tomobase.domain.phantoms.nanocage import get_nanocage

from qtpy.QtWidgets import QWidget, QVBoxLayout, QMenu, QAction, QDockWidget, QLabel, QFrame, QFileDialog, QApplication, QAbstractItemView, QToolButton, QTableWidgetItem, QTreeWidget, QTreeWidgetItem
from qtpy.QtCore import Qt

from tdtomo.backends.qt.views.ui.image_list import refresh_table


from .....core.registers import model_controllers, layer_render_types
from tomobase.core.data_classes import *

class  InfoWideget(QTreeWidget):
    def __init__(self):
        super().__init__()
        self.setColumnCount(2)
        self.setWindowTitle(f"Image Info")

        self.add_info({'Active Images': len(model_controllers)})

    def add_info(self, _dict, parent=None):
        for key, value in _dict.items():
            if isinstance(value, dict):
                item = QTreeWidgetItem([str(key), ''])
                self.add_info(value, parent=item)
            else:
                item = QTreeWidgetItem([str(key), str(value)])
            if parent is None:
                self.addTopLevelItem(item)
            else:
                parent.addChild(item)


info_widget = InfoWideget()

def refresh_info_widget():
    info_widget.clear()
    info_widget.add_info({'Active Images': len(model_controllers)})
    for key, value in model_controllers.items():
        info_widget.add_info(model_controllers[key].get_info_for_widget())


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
    
    docked_gui = viewer.window.add_dock_widget(info_widget, name='Image Info', area='left')

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