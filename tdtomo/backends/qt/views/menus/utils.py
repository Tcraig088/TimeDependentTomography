from qtpy.QtWidgets import QWidget, QVBoxLayout, QMenu, QAction, QDockWidget, QLabel
from qtpy.QtCore import Qt

from .io import build_io_menu
from ..operators import build_context_widget
from ..ui import build_image_table_widget, build_info_widget, build_structured_data_widget, _build_variables_widget, build_graph_widget

def build_utilities_menu(viewer, parent_menu):   
    submenu2 = parent_menu.addMenu('File')
    build_io_menu(viewer, submenu2)
    
    action = QAction('Context', parent_menu)
    parent_menu.addAction(action)
    action.triggered.connect(lambda x: build_context_widget(viewer))

    action = QAction('Models', parent_menu)
    parent_menu.addAction(action)
    action.triggered.connect(lambda x: build_image_table_widget(viewer))
    build_image_table_widget(viewer)
    
    action = QAction('Structured Data', parent_menu)
    parent_menu.addAction(action)
    action.triggered.connect(lambda x: _build_variables_widget(viewer))
    build_structured_data_widget(viewer, parent_menu)

    
    action = QAction('Model Info', parent_menu)
    parent_menu.addAction(action)
    action.triggered.connect(lambda x: build_info_widget(viewer))
    build_info_widget(viewer)
    
    action = QAction('Graph', parent_menu)
    parent_menu.addAction(action)
    action.triggered.connect(lambda x: build_graph_widget(viewer))
    build_graph_widget(viewer)