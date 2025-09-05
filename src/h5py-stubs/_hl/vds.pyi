from os import PathLike
from typing import Any, NamedTuple, Self

from _typeshed import Incomplete
from h5py._hl.dataset import Dataset
from h5py._hl.group import Group
from numpy.typing import DTypeLike

# TODO: type these fields
class VDSmap(NamedTuple):
    vspace: Incomplete
    file_name: Incomplete
    dset_name: Incomplete
    src_space: Incomplete

vds_support: bool

class VirtualSource:
    def __init__(
        self,
        path_or_dataset: str | bytes | PathLike[str] | Dataset[Any],
        name: str = ...,
        shape: tuple[int, ...] | None = ...,
        dtype: DTypeLike | None = ...,
        maxshape: tuple[int | None, ...] | None = ...,
    ) -> None: ...
    @property
    def shape(self) -> tuple[int, ...]: ...
    def __getitem__(self, key: Any) -> Self: ...

class VirtualLayout:
    def __init__(
        self,
        shape: tuple[int, ...],
        dtype: DTypeLike,
        maxshape: tuple[int | None, ...] | None = ...,
        filename: str | None = ...,
    ) -> None: ...

    # TODO: source type
    def __setitem__(self, key: str, source: VirtualSource) -> None: ...

    # TODO: return type is a "low-level dataset" - what type is this?
    def make_dataset(
        self,
        parent: Group,
        name: str,
        fillvalue: Any = ...,
    ) -> Incomplete: ...
