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


from qtpy.QtWidgets import QWidget, QVBoxLayout, QMenu, QAction, QDockWidget, QLabel, QFrame, QFileDialog, QApplication, QAbstractItemView, QToolButton, QTableWidgetItem
from qtpy.QtCore import Qt


from ...registers import data_controllers, tilt_controllers, plot_render_types
from tomobase.data import *


tilts_table = Table({'Name': ['a'], 'Scheme': ['b'], 'Current Angle': ['c'], 'Min Angle': ['d'], 'Max Angle': ['e']})
plots_table = Table({'Name': ['a'], 'Sample Name': ['b'], 'Type': ['c']})



def ensure_options_column(table):
    # add header if missing and return its index
    for c in range(table.columnCount()):
        h = table.horizontalHeaderItem(c)
        if h and h.text() == "Options":
            return c
    table.insertColumn(0)
    table.setHorizontalHeaderItem(0, QTableWidgetItem("Options"))
    return 0    


def add_tilt_row_menu(table, row, model_name):
    col = ensure_options_column(table)
    btn = QToolButton()
    menu = QMenu(btn)
    
    menu.addAction("Reset", tilt_controllers[model_name].model.reset)
    menu.addAction("Remove", lambda m=model_name: tilt_controllers.pop(m))
    btn.setMenu(menu)
    btn.setPopupMode(QToolButton.InstantPopup)
    table.setCellWidget(row, col, btn)

def refresh_tilts_table():
    tilts_table.clear()
    table = {'Name': [], 'Scheme': [], 'Current Angle': [], 'Min Angle': [], 'Max Angle': []}
    for key, value in tilt_controllers.items():
        table['Name'].append(key)
        table['Scheme'].append(type(value.model).__name__)
        table['Current Angle'].append(getattr(value.model, 'current_angle', ''))
        table['Min Angle'].append(getattr(value.model, 'angle_min', ''))
        table['Max Angle'].append(getattr(value.model, 'angle_max', ''))
    # update the magicgui table data
    for k in table:
        table[k] = list(reversed(table[k]))
    tilts_table['Name'] = table['Name']
    tilts_table['Scheme'] = table['Scheme']
    tilts_table['Current Angle'] = table['Current Angle']
    tilts_table['Min Angle'] = table['Min Angle']
    tilts_table['Max Angle'] = table['Max Angle']
    
    tilts_table.native.setEditTriggers(QAbstractItemView.NoEditTriggers)
    qt_table  = tilts_table.native
    for i, name in enumerate(table['Name']):
        add_tilt_row_menu(qt_table, i, name)

def refresh_plots_table():
    plots_table.clear()
    table = {'Name': [], 'Sample Name': [], 'Type': []}
    for key, value in data_controllers.items():
        table['Name'].append(key)
        table['Sample Name'].append(getattr(value.model, 'sample_name', ''))
        table['Type'].append(type(value.model).__name__)
    # update the magicgui table data
    for k in table:
        table[k] = list(reversed(table[k]))
    plots_table['Name'] = table['Name']
    plots_table['Sample Name'] = table['Sample Name']
    plots_table['Type'] = table['Type']

def build_structured_data_widget(viewer, parent_menu):
    main_window = viewer.window._qt_window
    layer_list = None
    for child in main_window.children():
        try:
            if child.objectName() == 'layer list':
                layer_list = child
                break
        except Exception:
            ValueError("Could not find layer list in napari viewer window")

    gui = Container(labels=False,layout="vertical")
    gui.append(tilts_table)
    gui.append(plots_table)
    
    tilt_controllers.removed.connect(refresh_tilts_table)
    tilt_controllers.added.connect(refresh_tilts_table)
    tilt_controllers.updated.connect(refresh_tilts_table)
    
    data_controllers.removed.connect(refresh_plots_table)
    data_controllers.added.connect(refresh_plots_table) 
    data_controllers.updated.connect(refresh_plots_table)
    
    refresh_plots_table()
    refresh_tilts_table()
    
    docked_gui = viewer.window.add_dock_widget(gui, name='Structured Data List', area='left')

    if layer_list is not None:
        try:
            viewer.window._qt_window.tabifyDockWidget(layer_list, docked_gui)
        except Exception:
            pass
    return docked_gui