import pathlib

from tomobase.data import ImageAbstract
from tomobase.core.registers.categories import categories

from ...hooks import visualize_hook

subcategory = categories.add_category('Animate', value=76, inheritor='Visualization')

@visualize_hook(name='Visualize OrthoSlices', categories=subcategory)
def ortho_slice_pass(viewer:'napari.viewer.Viewer', image: ImageAbstract, axis: str ='x', folder: pathlib.Path = None, **kwargs):
    return