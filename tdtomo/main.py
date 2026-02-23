import napari
import magicgui

from qtpy.QtWidgets import QWidget, QVBoxLayout, QMenu, QAction, QDockWidget, QLabel
from qtpy.QtCore import Qt

from .views.utils import _build_models_widget, _build_variables_widget, _build_context_widget, _build_info_widget, _build_graph_widget


from .tomo import _buildtomomenu
from .io import _buildiomenu
from .registers import _modules

#from tomobase.globals import logger


@magicgui.magicgui(call_button='Setup Menu')
def buildmenu_gui():
    viewer = napari.current_viewer()
    menu = QMenu('Continuous Tomography', viewer.window.main_menu)  # explicit parent
    viewer.window.main_menu.addMenu(menu)
    
    submenu = menu.addMenu('Utilities')    
    submenu2 = submenu.addMenu('File')
    _buildiomenu(viewer, submenu2)
    
    action = QAction('Context', submenu)
    submenu.addAction(action)
    action.triggered.connect(lambda x: _build_context_widget(viewer))
    _build_context_widget(viewer)
    
    action = QAction('Models', submenu)
    submenu.addAction(action)
    action.triggered.connect(lambda x: _build_models_widget(viewer))
    _build_models_widget(viewer)
    
    action = QAction('Variables', submenu)
    submenu.addAction(action)
    action.triggered.connect(lambda x: _build_variables_widget(viewer))
    _build_variables_widget(viewer)
    
    action = QAction('Model Info', submenu)
    submenu.addAction(action)
    action.triggered.connect(lambda x: _build_info_widget(viewer))
    _build_info_widget(viewer)
    
    action = QAction('Graph', submenu)
    submenu.addAction(action)
    action.triggered.connect(lambda x: _build_graph_widget(viewer))
    _build_graph_widget(viewer)

    #if _modules.tomoacquire:
        # add the import here 
    submenu.addMenu('Acquisition')
    
    submenu = menu.addMenu('Tomography')
    _buildtomomenu(viewer, submenu)
    
    print(_modules.tomoacquire)
    #print(_modules.tomondt)
    #if _modules.tomondt:
    from .ndt import _buildndtmenu
    submenu = menu.addMenu('Time Dependent Tomography')
    _buildndtmenu(viewer, submenu)
        #pass
    

    viewer.window.remove_dock_widget(buildmenu_gui.native)
    return 

def _buildmenu():
    note = QLabel("Welcome to the Continuous Tomography Module")
    buildmenu_gui.native.layout().insertWidget(0, note)
    return buildmenu_gui  # return the FunctionGui object itself

