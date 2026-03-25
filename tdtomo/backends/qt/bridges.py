from tomobase.backends.qt.bridges import QtRegistryBridge
from ...core import registers

qt_model_controllers = QtRegistryBridge(registers.model_controllers)
qt_data_controllers = QtRegistryBridge(registers.data_controllers)
qt_tilt_bridges = QtRegistryBridge(registers.tilt_controllers)
qt_struct_data_controllers = QtRegistryBridge(registers.struct_data_controllers)
qt_plot_render_types = QtRegistryBridge(registers.plot_render_types)  
qt_layer_render_types = QtRegistryBridge(registers.layer_render_types)
qt_magic_widgets = QtRegistryBridge(registers.magic_widgets)  
