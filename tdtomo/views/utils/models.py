import magicgui
from magicgui.widgets import Container, Label, FileEdit, PushButton

from pathlib import Path
import napari
import collections.abc
from collections.abc import Iterable 

from tomobase.data import BaseImageModel
from tomobase.globals import logger, proxy, GPUContext, image_datatypes_register
from tomobase.phantoms.nanocage import get_nanocage

from qtpy.QtWidgets import QWidget, QVBoxLayout, QMenu, QAction, QDockWidget, QLabel, QFrame
from qtpy.QtCore import Qt


from ...registration import _controllers
from tomobase.data import *


@magicgui.magicgui(labels=False, layout="horizontal", call_button="Import",data_type={"choices": list(image_datatypes_register.keys())}, file={"widget_type": "FileEdit", "mode": "r"},)
def import_widget(file: Path = Path("path/to/file"), data_type: str = image_datatypes_register.key(0)):

    key = data_type
    print('importing ', file, ' as ', key)
    if not file:
        return
    
    print(image_datatypes_register[key].value.readers.keys())
    print(file.suffix)
    #remove leading dot
    suffix = file.suffix.lstrip(".")
    if suffix in image_datatypes_register[key].value.readers.keys():
        reader = image_datatypes_register[key].value.readers[suffix]
        print(file.suffix.strip(), image_datatypes_register[key].value.readers.keys())
        obj = reader(file)
        _controllers[obj.sample_name] = obj 
        print(_controllers) # store the new object
        refresh_models_table() 
        return obj
    else:
        logger.warning("Selected file %s does not match allowed suffixes for %s",file, key)
        return
    

models_table = Container(layout="vertical") 

def _left_label(text: str, tooltip: str | None = None) -> Label:
    """Helper to create a left-aligned label with optional tooltip."""
    lbl = Label(value=text)
    lbl.native.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
    if tooltip:
        lbl.native.setToolTip(tooltip)
    return lbl


def _divider_label() -> Label:
    sep = Label(value="")                    
    sep.native.setFixedHeight(1)
    sep.native.setStyleSheet("background: palette(mid);")
    return sep


def refresh_models_table():
    models_table.clear()

    # ---- header row ----
    header = Container(layout="horizontal")
    header.append(_left_label("Name"))
    header.append(_left_label("Sample Name"))
    header.append(_left_label("Type"))
    models_table.append(header)
    models_table.append(_divider_label())

    # ---- data rows ----
    for name, obj in _controllers.items():
        row = Container(layout="horizontal")

        row.append(
            _left_label(
                text=str(name),
                tooltip=f"Controller key: {name}"
            )
        )
        row.append(
            _left_label(
                text=str(getattr(obj, "sample_name", "")),
                tooltip="Sample name"
            )
        )
        row.append(
            _left_label(
                text=obj.__class__.__name__,
                tooltip=f"Class: {obj.__class__.__module__}.{obj.__class__.__name__}"
            )
        )

        models_table.append(row)

    # force repaint
    models_table.native.update()

def _build_models_widget(viewer: 'napari.viewer.Viewer'):
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
                if child.objectName() == "layer list":
                    layer_list = child
                    break
            except Exception:
                continue
            
    
    gui = Container(labels=False,layout="vertical")
    gui.append(import_widget)
    gui.append(models_table)
    
    refresh_models_table()
    docked_gui = viewer.window.add_dock_widget(gui, name='models list', area='left')

    if layer_list is not None:
        try:
            viewer.window._qt_window.tabifyDockWidget(layer_list, docked_gui)
        except Exception:
            pass
    return docked_gui