from collections.abc import Iterator, MutableMapping, Sequence
from typing import override

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

    # MutableMapping methods
    @override
    def __getitem__(self, name: str) -> _AttributeValType: ...
    @override
    def __setitem__(self, name: str, val: _AttributeValType) -> None: ...
    @override
    def __delitem__(self, name: str) -> None: ...
    @override
    def __len__(self) -> int: ...
    @override
    def __iter__(self) -> Iterator[str]: ...
