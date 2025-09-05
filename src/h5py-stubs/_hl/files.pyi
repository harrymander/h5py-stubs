from collections.abc import Buffer, Callable
from os import PathLike
from typing import IO, Literal, Self, TypedDict, Unpack, overload, override

from _typeshed import Incomplete
from h5py.h5f import FileID

from .group import Group

mpi: bool
ros3: bool
direct_vfd: bool
hdf5_version: tuple[int, ...]
swmr_support: bool
libver_dict: dict[str, int]
libver_dict_r: dict[int, str]

def register_driver(name: str, set_fapl: Callable[..., None]) -> None: ...
def unregister_driver(name: str) -> None: ...
def registered_drivers() -> frozenset[str]: ...
def make_fapl(
    driver: Incomplete,
    libver: Incomplete = ...,
    rdcc_nslots: Incomplete = ...,
    rdcc_nbytes: Incomplete = ...,
    rdcc_w0: Incomplete = ...,
    locking: Incomplete = ...,
    page_buf_size: Incomplete = ...,
    min_meta_keep: Incomplete = ...,
    min_raw_keep: Incomplete = ...,
    alignment_threshold: Incomplete = ...,
    alignment_interval: Incomplete = ...,
    meta_block_size: Incomplete = ...,
    **kwds: Incomplete,
) -> Incomplete: ...
def make_fcpl(
    track_order: Incomplete = ...,
    fs_strategy: Incomplete = ...,
    fs_persist: Incomplete = ...,
    fs_threshold: Incomplete = ...,
    fs_page_size: Incomplete = ...,
) -> Incomplete: ...
def make_fid(
    name: str,
    mode: str,
    userblock_size: Incomplete,
    fapl: Incomplete,
    fcpl: Incomplete = ...,
    swmr: Incomplete = ...,
) -> Incomplete: ...

type _LibverSpec = Literal[
    "earliest",
    "latest",
    "v108",
    "v110",
    "v112",
    "v114",
]

class _FileInMemoryKwargs(TypedDict, total=False):
    libver: _LibverSpec | tuple[_LibverSpec, _LibverSpec]
    userblock_size: int
    swmr: bool
    rdcc_nbytes: int
    rdcc_w0: float
    rdcc_nslots: int
    track_order: bool
    fs_strategy: Literal["fsm", "page", "aggregate", "none"]
    fs_persist: bool
    fs_page_size: int
    fs_threshold: int
    page_buf_size: int
    min_meta_keep: float
    min_raw_keep: float
    alignment_threshold: int
    alignment_interval: int
    meta_block_size: int

class _FileKwargs(_FileInMemoryKwargs, total=False):
    name: PathLike[str] | bytes | str
    locking: bool | Literal["true", "false", "best-effort"]

type _FileOpenMode = Literal["r", "r+", "w", "w-", "a", "x"] | str  # noqa: PYI051

class File(Group):
    @overload
    def __init__(
        self,
        path: str | PathLike[str] | IO[bytes],
        mode: _FileOpenMode = "r",
        **kwargs: Unpack[_FileKwargs],
    ) -> None: ...
    @overload
    def __init__(
        self,
        path: str | PathLike[str] | IO[bytes],
        mode: _FileOpenMode = "r",
        *,
        driver: Literal["mpio"],
        comm: Incomplete,
        **kwargs: Unpack[_FileKwargs],
    ) -> None: ...

    # Create file in memory
    @classmethod
    def in_memory(
        cls,
        file_image: bytes | Buffer | None = ...,
        *,
        block_size: int = ...,
        **kwargs: Unpack[_FileInMemoryKwargs],
    ) -> Self: ...

    #
    @property
    def filename(self) -> str: ...
    @property
    def mode(self) -> str: ...
    @property
    @override
    def id(self) -> FileID: ...  # type: ignore[override] # pyright: ignore[reportIncompatibleMethodOverride]

    #
    def __enter__(self) -> Self: ...
    def __exit__(self, *_) -> None: ...
    def close(self) -> None: ...
    @property
    def driver(self) -> str: ...
    @property
    def libver(self) -> tuple[str, ...]: ...
    @property
    def userblock_size(self) -> int: ...
    @property
    def meta_block_size(self) -> int: ...
    def flush(self) -> None: ...

    # TODO: atomic is bool?
    @property
    def atomic(self) -> Incomplete: ...
    @atomic.setter
    def atomic(self, value: Incomplete) -> None: ...

    #
    @property
    def swmr_mode(self) -> bool: ...
    @swmr_mode.setter
    def swmr_mode(self, value: bool) -> None: ...
