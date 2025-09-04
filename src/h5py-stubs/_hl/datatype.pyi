from typing import Any

import numpy as np
from h5py import h5t

from .base import HLObject

class Datatype(HLObject):
    @property
    def dtype(self) -> np.dtype[Any]: ...
    def __init__(self, bind: h5t.TypeID) -> None: ...
