import textwrap

import pytest

from .mypy_assertions import assert_mypy_passes


def assert_mypy_passes_with_group(source: str) -> None:
    setup = """\
    from typing import assert_type
    from numpy.typing import NDArray
    import h5py
    import numpy as np
    group: h5py.Group
    """
    assert_mypy_passes(f"{textwrap.dedent(setup)}\n{textwrap.dedent(source)}")


def test_create_dataset_with_numpy_generic_type() -> None:
    assert_mypy_passes_with_group("""\
    dataset = group.create_dataset("name", shape=(100,), dtype=np.uint8)
    assert_type(dataset, h5py.Dataset[np.uint8])
    """)


def test_create_dataset_with_parameterized_ndarray() -> None:
    assert_mypy_passes_with_group("""\
    array: NDArray[np.float32]
    dataset = group.create_dataset("name", data=array)
    assert_type(dataset, h5py.Dataset[np.float32])
    """)


def test_create_dataset_with_dtype_overrides_type_of_ndarray() -> None:
    assert_mypy_passes_with_group("""\
    array: NDArray[np.float32]
    dataset = group.create_dataset("name", data=array, dtype=np.int32)
    assert_type(dataset, h5py.Dataset[np.int32])
    """)


def test_create_dataset_with_unknown_dtype_overrides_type_of_ndarray() -> None:
    assert_mypy_passes_with_group("""\
    from typing import Any
    array: NDArray[np.float32]
    dataset = group.create_dataset("name", data=array, dtype=int)
    assert_type(dataset, h5py.Dataset[Any])
    """)


@pytest.mark.parametrize(
    "args_expr",
    [
        "shape=(100, 2)",
        "data=[1, 2, 3]",
        "shape=(100, 2), dtype=float",
    ],
)
def test_create_dataset_with_unknown_type(args_expr: str) -> None:
    assert_mypy_passes_with_group(f"""\
    from typing import Any
    dataset = group.create_dataset("name", {args_expr})
    assert_type(dataset, h5py.Dataset[Any])
    """)
