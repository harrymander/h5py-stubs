import pytest

from .mypy_assertions import assert_mypy_passes


def test_indexing_group_with_reference_returns_hlobject() -> None:
    assert_mypy_passes("""\
    from typing import assert_type
    import h5py

    group: h5py.Group
    node: h5py.HLObject
    assert_type(group[node.ref], h5py.HLObject)
    """)


@pytest.mark.parametrize("obj_type", ["HLObject", "Group", "Dataset"])
def test_ref_is_parameterized(obj_type: str):
    assert_mypy_passes(f"""\
    from typing import assert_type
    import h5py

    node: h5py.{obj_type}
    assert_type(node.ref, h5py.Reference[h5py.{obj_type}])
    """)


@pytest.mark.parametrize(
    "obj_type", ["HLObject", "Group", "Dataset[Any]", "Dataset[np.float64]"]
)
def test_indexing_group_with_parameterized_ref_returns_narrowed_object(obj_type: str):
    assert_mypy_passes(f"""\
    from typing import assert_type, Any
    import h5py
    import numpy as np

    group: h5py.Group
    ref: h5py.Reference[h5py.{obj_type}]
    assert_type(group[ref], h5py.{obj_type})
    """)


@pytest.mark.parametrize("dataset_dtype", ["Any", "np.float64"])
def test_indexing_group_with_dataset_regionref_returns_dataset(dataset_dtype: str):
    assert_mypy_passes(f"""\
    from typing import assert_type, Any
    import h5py
    import numpy as np

    group: h5py.Group
    dataset: h5py.Dataset[{dataset_dtype}]
    region = dataset.regionref[:10]
    assert_type(group[region], h5py.Dataset[{dataset_dtype}])
    """)


def test_indexing_group_with_hlobject_regionref_returns_hlobject() -> None:
    assert_mypy_passes("""\
    from typing import assert_type
    import h5py

    group: h5py.Group
    object: h5py.HLObject
    region = object.regionref[:10]
    assert_type(group[region], h5py.HLObject)
    """)


def test_code_unreachable_after_indexing_group_regionref() -> None:
    """
    All HLObjects return a _RegionProxy from regionref property, but all proxy objects
    except those returned from Dataset.regionref will fail with TypeError if indexed.
    """
    assert_mypy_passes("""
    from typing import assert_never, assert_type
    import h5py

    group: h5py.Group
    regionref = group.regionref
    assert_type(regionref, "h5py._hl.base._RegionProxy[h5py.Group]")
    assert_never(regionref[:10])
    """)
