from collections.abc import Callable, Iterable, Iterator, MutableMapping
from contextlib import contextmanager
from os import PathLike
from typing import Any, Literal, TypedDict, Unpack, overload, override

import numpy as np
from _typeshed import Incomplete
from h5py import h5g
from h5py._hl.dataset import Dataset
from h5py._hl.vds import VirtualLayout
from numpy.typing import ArrayLike, DTypeLike, NDArray

from .base import HLObject

class _CreateDatasetKwargs(TypedDict, total=False):
    chunks: bool | tuple[int, ...] | int
    maxshape: tuple[int | None, ...] | int
    compression: Literal["gzip", "szip", "lzf"] | int
    compression_opts: Incomplete
    scaleoffset: Incomplete
    shuffle: bool
    fletcher32: bool
    fillvalue: Incomplete
    track_times: bool
    track_order: bool
    external: Iterable[
        tuple[
            str | bytes | PathLike[str] | PathLike[bytes],
            int,
            int,
        ]
    ]
    efile_prefix: str
    virtual_prefix: str
    allow_unknown_filter: bool
    rdcc_nbytes: int
    rdcc_w0: float
    rdcc_nslots: int

class Group(HLObject, MutableMapping[str, HLObject]):
    def __init__(self, id: h5g.GroupID) -> None: ...
    @property
    @override
    def id(self) -> h5g.GroupID: ...

    # MutableMapping iterface
    @override
    def __len__(self) -> int: ...
    @override
    def __getitem__(self, key: str) -> HLObject: ...
    @override
    def __delitem__(self, key: str) -> None: ...
    @override
    def __setitem__(
        self,
        key: str,
        val: HLObject | np.dtype[Any] | ArrayLike,
    ) -> None: ...
    @override
    def __iter__(self) -> Iterator[str]: ...

    #
    def require_group(self, name: str) -> Group: ...
    def require_dataset(self, name: str) -> Dataset[Any]: ...
    def create_group(
        self,
        name: str,
        track_order: bool | None = ...,
    ) -> Group: ...

    #
    @overload
    def create_dataset[T: np.generic](
        self,
        name: str,
        shape: tuple[int, ...] | None,
        dtype: None,
        data: NDArray[T],
        **kwargs: Unpack[_CreateDatasetKwargs],
    ) -> Dataset[T]: ...
    @overload
    def create_dataset[T: np.generic](
        self,
        name: str,
        *,
        data: NDArray[T],
        shape: tuple[int, ...] | None = ...,
        dtype: None = ...,
        **kwargs: Unpack[_CreateDatasetKwargs],
    ) -> Dataset[T]: ...
    @overload
    def create_dataset[T: np.generic](
        self,
        name: str,
        shape: tuple[int, ...] | None,
        dtype: type[T],
        data: ArrayLike | None = ...,
        **kwargs: Unpack[_CreateDatasetKwargs],
    ) -> Dataset[T]: ...
    @overload
    def create_dataset[T: np.generic](
        self,
        name: str,
        *,
        dtype: type[T],
        shape: tuple[int, ...] | None = ...,
        data: ArrayLike | None = ...,
        **kwargs: Unpack[_CreateDatasetKwargs],
    ) -> Dataset[T]: ...
    @overload
    def create_dataset(
        self,
        name: str,
        shape: tuple[int, ...] | None = None,
        dtype: type | None = None,
        data: ArrayLike | None = None,
        **kwargs: Unpack[_CreateDatasetKwargs],
    ) -> Dataset[Any]: ...

    #
    @overload
    def create_dataset_like[T: np.generic](
        self,
        name: str,
        other: Dataset[Any],
        *,
        dtype: type[T],
        shape: tuple[int, ...] | None = ...,
        data: ArrayLike | None = ...,
        **kwargs: Unpack[_CreateDatasetKwargs],
    ) -> Dataset[T]: ...
    @overload
    def create_dataset_like[T: np.generic](
        self,
        name: str,
        other: Dataset[T],
        *,
        dtype: None = ...,
        shape: tuple[int, ...] | None = ...,
        data: ArrayLike | None = ...,
        **kwargs: Unpack[_CreateDatasetKwargs],
    ) -> Dataset[T]: ...
    @overload
    def create_dataset_like(
        self,
        name: str,
        other: Dataset[Any],
        *,
        dtype: type | None = ...,
        shape: tuple[int, ...] | None = ...,
        data: ArrayLike | None = ...,
        **kwargs: Unpack[_CreateDatasetKwargs],
    ) -> Dataset[Any]: ...

    #
    def create_virtual_dataset(
        self,
        name: str,
        layout: VirtualLayout,
        fillvalue: Any = ...,
    ) -> Dataset[Any]: ...
    @contextmanager
    def build_virtual_dataset(
        self,
        name: str,
        shape: tuple[int, ...],
        dtype: DTypeLike,
        maxshape: tuple[int | None, ...] | None = ...,
        fillvalue: Any = ...,
    ) -> Iterator[VirtualLayout]: ...

    #
    def move(self, source: str, dest: str) -> None: ...
    def copy(
        self,
        source: str | Group | Dataset[Any],
        dest: str | Group,
        name: str | None = ...,
        shallow: bool = ...,
        expand_soft: bool = ...,
        expand_external: bool = ...,
        expand_refs: bool = ...,
        without_attrs: bool = ...,
    ) -> None: ...
    def visit[T](self, visitor: Callable[[str], T | None]) -> T | None: ...
    def visititems[T](
        self,
        visitor: Callable[[str, HLObject], T | None],
    ) -> T | None: ...
    def visit_links[T](self, visitor: Callable[[str], T | None]) -> T | None: ...
    def visititems_links[T](
        self,
        visitor: Callable[[str, _LinkType], T | None],
    ) -> T | None: ...

    # h5py overrides get() to return different types depending on the getclass
    # and getlink kwargs
    # (https://docs.h5py.org/en/stable/high/group.html#h5py.Group.get).
    #
    # This violates the LSP but will try to capture it in these overloads
    # anyway. Note these overloads only narrow the return type when both
    # getclass/getlink are literals; i.e., if one is a non-literal bool and the
    # other is literal, the type checker will just assume return type is the
    # full range of types as specified in the first (bottom) overload.

    # getlink=True and getclass=True -> type[_LinkType] | T
    @overload  # type: ignore[override]
    def get(
        self,
        name: str,
        /,
        *,
        getclass: Literal[True],
        getlink: Literal[True],
    ) -> type[_LinkType] | None: ...
    @overload
    def get[T](
        self,
        name: str,
        /,
        default: T,
        getclass: Literal[True],
        getlink: Literal[True],
    ) -> type[_LinkType] | T: ...

    # getlink=True, with getclass=False or missing -> _LinkType | T
    @overload
    def get[T](
        self,
        name: str,
        /,
        default: T,
        getclass: Literal[False],
        getlink: Literal[True],
    ) -> _LinkType | T: ...
    @overload
    def get(
        self,
        name: str,
        /,
        *,
        getclass: Literal[False],
        getlink: Literal[True],
    ) -> _LinkType | None: ...
    @overload
    def get[T](
        self,
        name: str,
        /,
        default: T,
        *,
        getlink: Literal[True],
    ) -> _LinkType | T: ...
    @overload
    def get(self, name: str, /, *, getlink: Literal[True]) -> _LinkType | None: ...

    # getclass=True, getlink=False or not provided -> type[HLObject] | T
    @overload
    def get[T](
        self,
        name: str,
        /,
        default: T,
        getclass: Literal[True],
        getlink: Literal[False],
    ) -> type[HLObject] | T: ...
    @overload
    def get(
        self,
        name: str,
        /,
        *,
        getclass: Literal[True],
        getlink: Literal[False],
    ) -> type[HLObject] | None: ...
    @overload
    def get[T](
        self,
        name: str,
        /,
        default: T,
        getclass: Literal[True],
    ) -> type[HLObject] | T: ...
    @overload
    def get(
        self,
        name: str,
        /,
        *,
        getclass: Literal[True],
    ) -> type[HLObject] | None: ...

    # getclass=False/getlink=False or not provided -> HLObject | T
    @overload
    def get[T](
        self,
        name: str,
        /,
        default: T,
        getlink: Literal[False],
    ) -> HLObject | T: ...
    @overload
    def get(
        self,
        name: str,
        /,
        *,
        getlink: Literal[False],
    ) -> HLObject | None: ...
    @overload
    def get[T](
        self,
        name: str,
        /,
        default: T,
        getclass: Literal[False],
    ) -> HLObject | T: ...
    @overload
    def get(
        self,
        name: str,
        /,
        *,
        getclass: Literal[False],
    ) -> HLObject | None: ...
    @overload
    def get[T](
        self,
        name: str,
        /,
        default: T,
        getclass: Literal[False],
        getlink: Literal[False],
    ) -> HLObject | T: ...
    @overload
    def get[T](
        self,
        name: str,
        /,
        *,
        getclass: Literal[False],
        getlink: Literal[False],
    ) -> HLObject | None: ...

    # No getclass/getlink -> HLObject | T
    @overload
    def get(self, name: str, /) -> HLObject | None: ...
    @overload
    def get[T](self, name: str, /, default: T) -> HLObject | T: ...

    # unknown getclass/getlink with explicit default
    @overload
    def get[T](
        self,
        name: str,
        /,
        default: T,
        getclass: bool = ...,
        getlink: bool = ...,
    ) -> HLObject | _LinkType | type[HLObject | _LinkType] | T: ...

    # unknown getclass/getlink without explicit default
    @overload
    def get(
        self,
        name: str,
        /,
        *,
        getclass: bool = ...,
        getlink: bool = ...,
    ) -> HLObject | _LinkType | type[HLObject | _LinkType] | None: ...

    # Need to ignore error about incompatible method override since this is
    # actually what h5py does...
    @overload
    def get[T](  # pyright: ignore[reportIncompatibleMethodOverride]
        self,
        name: str,
        /,
        default: T | None = None,
        getclass: bool = False,
        getlink: bool = False,
    ) -> HLObject | _LinkType | type[HLObject | _LinkType] | T | None: ...

type _LinkType = HardLink | ExternalLink | SoftLink

class HardLink: ...

class SoftLink:
    @property
    def path(self) -> str: ...
    def __init__(self, path: str) -> None: ...

class ExternalLink:
    @property
    def path(self) -> str: ...
    @property
    def filename(self) -> str: ...
    def __init__(
        self,
        filename: str | bytes | PathLike[str],
        path: str,
    ) -> None: ...
