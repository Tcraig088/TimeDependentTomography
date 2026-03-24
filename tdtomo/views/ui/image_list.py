import magicgui
from magicgui.widgets import Container, Label, FileEdit, PushButton, Table

from pathlib import Path
import pickle
import napari
import collections.abc
from collections.abc import Iterable 

from tomobase.data import ImageAbstract
from tomobase.core.log import logger
from tomobase.core.environment import GPUContext, proxy
from tomobase.core import registers
from tomobase.phantoms.nanocage import get_nanocage

from qtpy.QtWidgets import QWidget, QVBoxLayout, QMenu, QAction, QDockWidget, QLabel, QFrame, QFileDialog, QApplication, QAbstractItemView, QToolButton, QTableWidgetItem
from qtpy.QtCore import Qt


from ...registers import model_controllers, layer_render_types
from tomobase.data import *



models_table = Table({'Name': ['a'], 'Sample Name': ['b'], 'Type': ['c']})
_syncing_selections = False

def ensure_options_column(table):
    # add header if missing and return its index
    for c in range(table.columnCount()):
        h = table.horizontalHeaderItem(c)
        if h and h.text() == "Options":
            return c
    table.insertColumn(0)
    table.setHorizontalHeaderItem(0, QTableWidgetItem("Options"))
    return 0


def add_row_menu(table, row, model_name):
    col = ensure_options_column(table)
    btn = QToolButton()
    menu = QMenu(btn)
    
    submenu = menu.addMenu("Views")
    for key, renderer in model_controllers[model_name].renderers.items():
        submenu.addAction(key, lambda k=key: model_controllers[model_name].add_render(k))
    menu.addAction("Save", model_controllers[model_name].model.write)
    menu.addAction("Remove", lambda m=model_name: model_controllers.pop(m))
    btn.setMenu(menu)
    btn.setPopupMode(QToolButton.InstantPopup)
    table.setCellWidget(row, col, btn)

def refresh_table():
    models_table.clear()
    table = {'Name': [], 'Sample Name': [], 'Type': []}
    for key, value in model_controllers.items():
        table['Name'].append(key)
        table['Sample Name'].append(getattr(value.model, 'sample_name', ''))
        table['Type'].append(type(value.model).__name__)
    # update the magicgui table data
    for k in table:
        table[k] = list(reversed(table[k]))
    models_table['Name'] = table['Name']
    models_table['Sample Name'] = table['Sample Name']
    models_table['Type'] = table['Type']

    models_table.native.setEditTriggers(QAbstractItemView.NoEditTriggers)
    qt_table = models_table.native
    for i, name in enumerate(table['Name']):
        add_row_menu(qt_table, i, name)
 
def select_table_rows(viewer: 'napari.viewer.Viewer'):
    global _syncing_selections
    if _syncing_selections:
        return
    _syncing_selections = True
    selected = viewer.layers.selection
    models_table.native.clearSelection()
    for key, value in model_controllers.items():
        for layer in selected:
            if layer.name in value._layers:
                row = models_table['Name'].index(key)
                models_table.native.selectRow(row)               
    _syncing_selections = False
        
def select_layers(viewer: 'napari.viewer.Viewer'):
    global _syncing_selections
    if _syncing_selections:
        return
    _syncing_selections = True
    viewer.layers.selection.clear()
    selected_rows = models_table.native.selectionModel().selectedRows()
    for index in selected_rows:
        model_name = models_table['Name'][index.row()]
        for layer in model_controllers[model_name]._layers.values():
            viewer.layers.selection.add(layer)      
    _syncing_selections = False         
    
def build_image_table_widget(viewer: 'napari.viewer.Viewer'):
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
                ValueError("Could not find layer list in napari viewer window")
            
    
    gui = Container(labels=False,layout="vertical")
    gui.append(models_table)
    
    model_controllers.removed.connect(refresh_table)
    model_controllers.added.connect(refresh_table)
    model_controllers.updated.connect(refresh_table)
    
    viewer.layers.selection.events.changed.connect(lambda v=viewer:select_table_rows(viewer))
    models_table.native.itemSelectionChanged.connect(lambda v=viewer:select_layers(viewer))
    refresh_table()  
    docked_gui = viewer.window.add_dock_widget(gui, name='models list', area='left')

    if layer_list is not None:
        try:
            viewer.window._qt_window.tabifyDockWidget(layer_list, docked_gui)
        except Exception:
            pass
    return docked_gui