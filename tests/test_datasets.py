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


@pytest.mark.parametrize("name", ['"name"', 'b"name"'])
def test_create_dataset_with_numpy_generic_type(name: str):
    assert_mypy_passes_with_group(f"""\
    dataset = group.create_dataset({name}, shape=(100,), dtype=np.uint8)
    assert_type(dataset, h5py.Dataset[np.uint8])
    """)


@pytest.mark.parametrize("name", ['"name"', 'b"name"'])
def test_create_dataset_with_parameterized_ndarray(name: str):
    assert_mypy_passes_with_group(f"""\
    array: NDArray[np.float32]
    dataset = group.create_dataset({name}, data=array)
    assert_type(dataset, h5py.Dataset[np.float32])
    """)


@pytest.mark.parametrize("name", ['"name"', 'b"name"'])
def test_create_dataset_with_dtype_overrides_type_of_ndarray(name: str):
    assert_mypy_passes_with_group(f"""\
    array: NDArray[np.float32]
    dataset = group.create_dataset({name}, data=array, dtype=np.int32)
    assert_type(dataset, h5py.Dataset[np.int32])
    """)


@pytest.mark.parametrize("name", ['"name"', 'b"name"'])
def test_create_dataset_with_unknown_dtype_overrides_type_of_ndarray(name: str):
    assert_mypy_passes_with_group(f"""\
    from typing import Any
    array: NDArray[np.float32]
    dataset = group.create_dataset({name}, data=array, dtype=int)
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
