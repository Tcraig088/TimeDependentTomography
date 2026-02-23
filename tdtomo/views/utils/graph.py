import pyqtgraph as pg



from qtpy.QtWidgets import QWidget, QTabWidget, QVBoxLayout, QMenu, QAction, QDockWidget, QLabel, QFrame, QFileDialog, QApplication, QAbstractItemView, QToolButton, QTableWidgetItem
from qtpy.QtCore import Qt


def test_graph():
    win = pg.GraphicsLayoutWidget()
    plot = win.addPlot(title="Plot 1")
    plot.plot([1, 2, 3], [4, 5, 6])
    plot.plot([1, 2, 3], [6, 5, 4])
    return win



def _build_graph_widget(viewer: 'napari.viewer.Viewer'):
    graph_tab_widget = QTabWidget(parent=viewer.window._qt_window)
    viewer.window.add_dock_widget(graph_tab_widget, name="Graph", area="right")
    
    test_graph_widget = test_graph()
    graph_tab_widget.addTab(test_graph_widget, "Test Graph")