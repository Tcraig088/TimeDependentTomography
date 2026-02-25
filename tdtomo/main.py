import napari
import magicgui

from qtpy.QtWidgets import QMenu, QLabel
from qtpy.QtCore import Qt

from .views.menus import build_utilities_menu, build_tomography_menu, build_tilting_menu


#from tomobase.globals import logger


@magicgui.magicgui(call_button='Setup Menu')
def build_menu():
    viewer = napari.current_viewer()
    menu = QMenu('Continuous Tomography', viewer.window.main_menu)  # explicit parent
    viewer.window.main_menu.addMenu(menu)
    

    submenu = menu.addMenu('Utilities')
    build_utilities_menu(viewer, submenu)
    
    submenu = menu.addMenu('Tilting')
    build_tilting_menu(viewer, submenu)
    
    submenu = menu.addMenu('Tomography')
    build_tomography_menu(viewer, submenu)
    

    viewer.window.remove_dock_widget(build_menu.native)
    return 

def build_gui():
    note = QLabel("Welcome to the Continuous Tomography Module")
    build_menu.native.layout().insertWidget(0, note)
    return build_menu  # return the FunctionGui object itself

