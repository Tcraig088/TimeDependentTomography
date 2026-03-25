import napari
import magicgui

from qtpy.QtWidgets import QMenu, QLabel
from qtpy.QtCore import Qt

from .backends.qt.views.menus import build_utilities_menu, build_tomography_menu
from tomobase.core import bootstrap

#from tomobase.globals import logger


@magicgui.magicgui(call_button='Setup Menu')
def build_menu():
    viewer = napari.current_viewer()
    menu = QMenu('Continuous Tomography', viewer.window.main_menu)
    viewer.window.main_menu.addMenu(menu)
    
    submenu = menu.addMenu('Utilities')
    build_utilities_menu(viewer, submenu)
    build_tomography_menu(viewer, menu)
    
    viewer.window.remove_dock_widget(build_menu.native)
    return 

def build_gui():
    bootstrap(qt_enabled=True)
    note = QLabel("Welcome to the Continuous Tomography Module")
    build_menu.native.layout().insertWidget(0, note)
    return build_menu  # return the FunctionGui object itself

