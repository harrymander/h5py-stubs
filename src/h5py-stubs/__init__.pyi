# Since no __all__ is provided in h5py.__init__, don't include here.
# See https://typing.python.org/en/latest/guides/writing_stubs.html#all

from . import (
    h5a,  # pyright: ignore[reportUnusedImport]
    h5d,  # pyright: ignore[reportUnusedImport]
    h5ds,  # pyright: ignore[reportUnusedImport]
    h5f,  # pyright: ignore[reportUnusedImport]
    h5fd,  # pyright: ignore[reportUnusedImport]
    h5g,  # pyright: ignore[reportUnusedImport]
    h5p,  # pyright: ignore[reportUnusedImport]
    h5pl,  # pyright: ignore[reportUnusedImport]
    h5r,  # pyright: ignore[reportUnusedImport]
    h5s,  # pyright: ignore[reportUnusedImport]
    h5t,  # pyright: ignore[reportUnusedImport]
    h5z,  # pyright: ignore[reportUnusedImport]
    version,  # pyright: ignore[reportUnusedImport]
)
from ._hl import filters  # pyright: ignore[reportUnusedImport]
from ._hl.attrs import AttributeManager  # pyright: ignore[reportUnusedImport]
from ._hl.base import Empty, HLObject, is_hdf5  # pyright: ignore[reportUnusedImport]
from ._hl.dataset import Dataset  # pyright: ignore[reportUnusedImport]
from ._hl.datatype import Datatype  # pyright: ignore[reportUnusedImport]
from ._hl.files import (
    File,  # pyright: ignore[reportUnusedImport]
    register_driver,  # pyright: ignore[reportUnusedImport]
    registered_drivers,  # pyright: ignore[reportUnusedImport]
    unregister_driver,  # pyright: ignore[reportUnusedImport]
)
from ._hl.group import (
    ExternalLink,  # pyright: ignore[reportUnusedImport]
    Group,  # pyright: ignore[reportUnusedImport]
    HardLink,  # pyright: ignore[reportUnusedImport]
    SoftLink,  # pyright: ignore[reportUnusedImport]
)
from ._hl.vds import VirtualLayout, VirtualSource  # pyright: ignore[reportUnusedImport]
from ._selector import MultiBlockSlice  # pyright: ignore[reportUnusedImport]
from .h5 import get_config  # pyright: ignore[reportUnusedImport]
from .h5r import Reference, RegionReference  # pyright: ignore[reportUnusedImport]
from .h5s import UNLIMITED  # pyright: ignore[reportUnusedImport]
from .h5t import (
    check_dtype,  # pyright: ignore[reportUnusedImport]
    check_enum_dtype,  # pyright: ignore[reportUnusedImport]
    check_opaque_dtype,  # pyright: ignore[reportUnusedImport]
    check_ref_dtype,  # pyright: ignore[reportUnusedImport]
    check_string_dtype,  # pyright: ignore[reportUnusedImport]
    check_vlen_dtype,  # pyright: ignore[reportUnusedImport]
    enum_dtype,  # pyright: ignore[reportUnusedImport]
    opaque_dtype,  # pyright: ignore[reportUnusedImport]
    ref_dtype,  # pyright: ignore[reportUnusedImport]
    regionref_dtype,  # pyright: ignore[reportUnusedImport]
    special_dtype,  # pyright: ignore[reportUnusedImport]
    string_dtype,  # pyright: ignore[reportUnusedImport]
    vlen_dtype,  # pyright: ignore[reportUnusedImport]
)
from .version import version as __version__

def enable_ipython_completer() -> None: ...
def run_tests(args: str = ...) -> int: ...
