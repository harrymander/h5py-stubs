from . import (
    h5a,
    h5d,
    h5ds,
    h5f,
    h5fd,
    h5g,
    h5p,
    h5pl,
    h5r,
    h5s,
    h5t,
    h5z,
    version,
)
from ._hl import filters
from ._hl.attrs import AttributeManager
from ._hl.base import Empty, HLObject, is_hdf5
from ._hl.dataset import Dataset
from ._hl.datatype import Datatype
from ._hl.files import File, register_driver, registered_drivers, unregister_driver
from ._hl.group import ExternalLink, Group, HardLink, SoftLink
from ._hl.vds import VirtualLayout, VirtualSource
from ._selector import MultiBlockSlice
from .h5 import get_config
from .h5r import Reference, RegionReference
from .h5s import UNLIMITED
from .h5t import (
    check_dtype,
    check_enum_dtype,
    check_opaque_dtype,
    check_ref_dtype,
    check_string_dtype,
    check_vlen_dtype,
    enum_dtype,
    opaque_dtype,
    ref_dtype,
    regionref_dtype,
    special_dtype,
    string_dtype,
    vlen_dtype,
)
from .version import version as __version__

__all__ = [
    "UNLIMITED",
    "AttributeManager",
    "Dataset",
    "Datatype",
    "Empty",
    "ExternalLink",
    "File",
    "Group",
    "HLObject",
    "HardLink",
    "MultiBlockSlice",
    "Reference",
    "RegionReference",
    "SoftLink",
    "VirtualLayout",
    "VirtualSource",
    "__version__",
    "check_dtype",
    "check_enum_dtype",
    "check_opaque_dtype",
    "check_ref_dtype",
    "check_string_dtype",
    "check_vlen_dtype",
    "enum_dtype",
    "filters",
    "get_config",
    "h5a",
    "h5d",
    "h5ds",
    "h5f",
    "h5fd",
    "h5g",
    "h5p",
    "h5pl",
    "h5r",
    "h5s",
    "h5t",
    "h5z",
    "is_hdf5",
    "opaque_dtype",
    "ref_dtype",
    "regionref_dtype",
    "register_driver",
    "registered_drivers",
    "special_dtype",
    "string_dtype",
    "unregister_driver",
    "version",
    "vlen_dtype",
]

def enable_ipython_completer() -> None: ...
