
import inspect
import magicgui
from magicgui.widgets import Container, Label

import napari
import collections.abc
from collections.abc import Iterable 

from qtpy.QtWidgets import QWidget, QVBoxLayout, QMenu, QAction, QDockWidget, QLabel
from qtpy.QtCore import Qt

#from tomondt.operators import deform_ndt

def _buildndtmenu(viewer, parent_menu):
    
    action = parent_menu.addAction('Deform')
    action.triggered.connect(lambda x: _builddeformwidget(viewer))
    
    parent_menu.addAction('Project')
    submenu = parent_menu.addMenu('Reconstruct')
    submenu.addAction('Dynamic')
    submenu.addAction('Moving Window')
    parent_menu.addAction('Post Process')
    
def _builddeformwidget(viewer):
    
    gui = Container()
    gui.native.layout().addWidget(Label(value="Deform VolumeNDt").native)
    gui.native.layout().addWidget(Label(value="Select VolumeNDt Layer").native)
    
    viewer.window.add_dock_widget(gui.native, area='right')
    