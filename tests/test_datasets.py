import textwrap

import pytest

from .mypy_assertions import assert_mypy_passes


def assert_mypy_passes_with_group(source: str) -> None:
    """Convenience function that imports various names and declares a h5py.Group object
    named `group`."""
    setup = """\
    from typing import assert_type
    from numpy.typing import NDArray, ArrayLike
    import h5py
    import numpy as np
    group: h5py.Group
    """
    assert_mypy_passes(f"{textwrap.dedent(setup)}\n{textwrap.dedent(source)}")


@pytest.mark.parametrize(
    "args_expr",
    [
        "data=[1, 2, 3]",
        "shape=(10,)",
        "dtype=int",
    ],
)
def test_create_dataset_with_unknown_type_returns_any_dataset(args_expr: str):
    assert_mypy_passes(f"""\
    from typing import assert_type, Any
    import h5py
    import numpy as np
    group: h5py.Group
    dataset = group.create_dataset("name", {args_expr})
    assert_type(dataset, h5py.Dataset[Any])
    """)


def test_create_dataset_with_data_of_known_type_returns_typed_dataset() -> None:
    assert_mypy_passes("""\
    from typing import assert_type
    import h5py
    import numpy as np
    group: h5py.Group
    data = np.array([1, 2, 3], dtype=np.float32)
    dataset = group.create_dataset("name", data=data)
    assert_type(dataset, h5py.Dataset[np.float32])
    """)


def test_create_dataset_with_untyped_data_and_typed_dtype_returns_typed_dataset() -> (
    None
):
    assert_mypy_passes("""\
    from typing import assert_type
    import h5py
    import numpy as np
    group: h5py.Group
    dataset = group.create_dataset("name", data=[1, 2, 3], dtype=np.float32)
    assert_type(dataset, h5py.Dataset[np.float32])
    """)


@pytest.mark.parametrize(
    "dtype,exp_type",
    [("np.uint16", "np.uint16"), ("int", "Any")],
)
def test_create_dataset_dtype_overrides_type_of_data(dtype: str, exp_type: str):
    assert_mypy_passes(f"""\
    from typing import assert_type, Any
    import h5py
    import numpy as np
    data = np.array([1, 2, 3], dtype=np.float32)
    group: h5py.Group
    dataset = group.create_dataset("name", data=data, dtype={dtype})
    assert_type(dataset, h5py.Dataset[{exp_type}])
    """)


def test_create_dataset_with_dtype_numpy_generic_class_returns_typed_dataset() -> None:
    assert_mypy_passes("""\
    from typing import assert_type
    import h5py
    import numpy as np
    group: h5py.Group
    dataset = group.create_dataset("name", dtype=np.uint8)
    assert_type(dataset, h5py.Dataset[np.uint8])
    """)


def test_create_dataset_with_dtype_object_returns_typed_dataset() -> None:
    assert_mypy_passes("""\
    from typing import assert_type
    import h5py
    import numpy as np
    dtype: np.dtype[np.float64]
    group: h5py.Group
    dataset = group.create_dataset("name", dtype=dtype)
    assert_type(dataset, h5py.Dataset[np.float64])
    """)


def test_index_typed_dataset_returns_typed_ndarray() -> None:
    assert_mypy_passes("""\
    from typing import assert_type
    import h5py
    import numpy as np
    from numpy.typing import NDArray

    dataset: h5py.Dataset[np.float32]
    assert_type(dataset[1:5], NDArray[np.float32])
    """)


def test_index_untyped_dataset_returns_untyped_ndarray() -> None:
    assert_mypy_passes("""\
    from typing import assert_type, Any
    import h5py
    import numpy as np
    from numpy.typing import NDArray

    dataset: h5py.Dataset
    assert_type(dataset[1:5], NDArray[Any])
    """)


def test_iterating_typed_dataset_returns_typed_ndarray() -> None:
    assert_mypy_passes("""\
    from typing import assert_type
    import h5py
    import numpy as np
    from numpy.typing import NDArray

    dataset: h5py.Dataset[np.float32]
    for i in dataset:
        assert_type(i, NDArray[np.float32])
    """)


def test_iterating_untyped_dataset_returns_untyped_ndarray() -> None:
    assert_mypy_passes("""\
    from typing import assert_type, Any
    import h5py
    import numpy as np
    from numpy.typing import NDArray

    dataset: h5py.Dataset
    for i in dataset:
        assert_type(i, NDArray[Any])
    """)
