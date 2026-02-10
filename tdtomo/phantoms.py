from __future__ import annotations
from typing import Callable, Dict, List, Optional, Any, Sequence
import numpy as np

from napari.types import LayerData
from tomobase.globals import phantoms_register


_PHANTOMS: Dict[str, Callable[[], Any]] = {}

# registry values look like enums/objects where .value is the actual factory/callable
for key, value in phantoms_register.items():
    factory = value.value
    if callable(factory):
        _PHANTOMS[key] = factory


def _to_layerdata(obj: Any, *, name: str) -> LayerData:
    """Convert your phantom object (expects .data) to napari LayerData."""
    data = getattr(obj, "data", None)
    if data is None:
        raise TypeError(f"Phantom {name!r} returned {type(obj)!r} which has no .data attribute")

    data = np.asarray(data)
    meta = {"name": name}
    return (data, meta, "image")


def build_phantom_menu(which: Optional[str] = None) -> List[LayerData]:
    """
    Sample-data callable (used by Open Sample).
    - If which is None: load a default phantom.
    - If which is provided: load that phantom key.
    """
    if not _PHANTOMS:
        data = np.zeros((64, 64), dtype=np.float32)
        return [(data, {"name": "Empty phantom"}, "image")]

    key = which or next(iter(_PHANTOMS))
    result = _PHANTOMS[key]()  # your factory returns object (or list of objects)

    if isinstance(result, (list, tuple)):
        return [_to_layerdata(obj, name=f"{key} [{i}]") for i, obj in enumerate(result)]

    return [_to_layerdata(result, name=key)]
