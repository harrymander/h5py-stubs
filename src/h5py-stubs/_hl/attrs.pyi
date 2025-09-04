from collections.abc import MutableMapping, Sequence

from h5py import h5a
from numpy.typing import ArrayLike, DTypeLike

from . import base

type _AttributeValType = float | str | bytes | ArrayLike | base.Empty

class AttributeManager(MutableMapping[str, _AttributeValType], base.CommonStateObject):
    def get_id(self, name: str) -> h5a.AttrID: ...
    def create(
        self,
        name: str,
        data: _AttributeValType,
        shape: Sequence[int] = ...,
        dtype: DTypeLike = ...,
    ) -> None: ...
    def modify(self, name: str, value: _AttributeValType) -> None: ...
