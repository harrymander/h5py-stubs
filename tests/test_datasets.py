import textwrap

import pytest

from .mypy_assertions import assert_mypy_fails, assert_mypy_passes


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


def parametrize_bytes_prefix() -> pytest.MarkDecorator:
    return pytest.mark.parametrize("b", ["b", ""])


@pytest.mark.parametrize(
    "args_expr",
    [
        "data=[1, 2, 3]",
        "shape=(10,)",
        "dtype=int",
    ],
)
@parametrize_bytes_prefix()
def test_create_dataset_with_unknown_type_returns_any_dataset(b: str, args_expr: str):
    assert_mypy_passes(f"""\
    from typing import assert_type, Any
    import h5py
    import numpy as np
    group: h5py.Group
    dataset = group.create_dataset({b}"name", {args_expr})
    assert_type(dataset, h5py.Dataset[Any])
    """)


@parametrize_bytes_prefix()
def test_create_dataset_with_data_of_known_type_returns_typed_dataset(b: str) -> None:
    assert_mypy_passes(f"""\
    from typing import assert_type
    import h5py
    import numpy as np
    group: h5py.Group
    data = np.array([1, 2, 3], dtype=np.float32)
    dataset = group.create_dataset({b}"name", data=data)
    assert_type(dataset, h5py.Dataset[np.float32])
    """)


@parametrize_bytes_prefix()
def test_create_dataset_with_untyped_data_and_typed_dtype_returns_typed_dataset(b: str):
    assert_mypy_passes(f"""\
    from typing import assert_type
    import h5py
    import numpy as np
    group: h5py.Group
    dataset = group.create_dataset({b}"name", data=[1, 2, 3], dtype=np.float32)
    assert_type(dataset, h5py.Dataset[np.float32])
    """)


@parametrize_bytes_prefix()
@pytest.mark.parametrize(
    "dtype,exp_type",
    [("np.uint16", "np.uint16"), ("int", "Any")],
)
def test_create_dataset_dtype_overrides_type_of_data(b: str, dtype: str, exp_type: str):
    assert_mypy_passes(f"""\
    from typing import assert_type, Any
    import h5py
    import numpy as np
    data = np.array([1, 2, 3], dtype=np.float32)
    group: h5py.Group
    dataset = group.create_dataset({b}"name", data=data, dtype={dtype})
    assert_type(dataset, h5py.Dataset[{exp_type}])
    """)


@parametrize_bytes_prefix()
def test_create_dataset_with_dtype_numpy_generic_class_returns_typed_dataset(b: str):
    assert_mypy_passes(f"""\
    from typing import assert_type
    import h5py
    import numpy as np
    group: h5py.Group
    dataset = group.create_dataset({b}"name", dtype=np.uint8)
    assert_type(dataset, h5py.Dataset[np.uint8])
    """)


@parametrize_bytes_prefix()
def test_create_dataset_with_dtype_object_returns_typed_dataset(b: str):
    assert_mypy_passes(f"""\
    from typing import assert_type
    import h5py
    import numpy as np
    dtype: np.dtype[np.float64]
    group: h5py.Group
    dataset = group.create_dataset({b}"name", dtype=dtype)
    assert_type(dataset, h5py.Dataset[np.float64])
    """)


@parametrize_bytes_prefix()
@pytest.mark.parametrize(
    "extra_args",
    [
        "",
        "dtype=int",
        "data=[1, 2, 3]",
        "data=np.array([1, 2, 3], dtype=np.float32)",
    ],
)
def test_create_dataset_like_untyped_dataset_returns_untyped_dataset(
    b: str,
    extra_args: str,
):
    assert_mypy_passes(f"""\
    from typing import assert_type, Any
    import h5py
    import numpy as np
    dataset: h5py.Dataset
    group: h5py.Group
    new = group.create_dataset_like({b}"name", dataset, {extra_args})
    assert_type(new, h5py.Dataset[Any])
    """)


@parametrize_bytes_prefix()
@pytest.mark.parametrize(
    "extra_args",
    [
        "",
        "data=[1, 2, 3]",
        "shape=(100,)",
        # dtype of original dataset is kept unless dtype explicitly passed:
        "data=[1.2, 2.2, 3.2]",
        "data=np.array([1, 2, 3], dtype=np.float32)",
    ],
)
def test_create_dataset_like_typed_dataset_returns_dataset_of_same_type(
    b: str,
    extra_args: str,
):
    assert_mypy_passes(f"""\
    from typing import assert_type
    import h5py
    import numpy as np
    dataset: h5py.Dataset[np.uint32]
    group: h5py.Group
    new = group.create_dataset_like({b}"name", dataset, {extra_args})
    assert_type(new, h5py.Dataset[np.uint32])
    """)


@parametrize_bytes_prefix()
@pytest.mark.parametrize("dataset_type", ["np.uint32", "Any"])
@pytest.mark.parametrize(
    "dtype,exp_type",
    [
        ("np.float32", "np.float32"),
        ("float", "Any"),
    ],
)
def test_create_dataset_like_with_dtype_overrides_type_of_original_dataset(
    dataset_type: str,
    dtype: str,
    exp_type: str,
    b: str,
):
    assert_mypy_passes(f"""\
    from typing import assert_type, Any
    import h5py
    import numpy as np
    dataset: h5py.Dataset[{dataset_type}]
    group: h5py.Group
    new = group.create_dataset_like({b}"name", dataset, dtype={dtype})
    assert_type(new, h5py.Dataset[{exp_type}])
    """)


@pytest.mark.parametrize(
    "args",
    [
        '"name"',  # name only
        '"name", "name2"',  # two strings
        '"name", dataset, 100',  # three positional args
    ],
)
def test_create_dataset_like_invalid_arguments_fails(args: str) -> None:
    assert_mypy_fails(
        f"""\
        import h5py
        dataset: h5py.Dataset
        group: h5py.Group
        group.create_dataset_like({args})
        """,
        4,
        'No overload variant of "create_dataset_like"',
    )


def test_create_dataset_like_without_arguments_fails() -> None:
    assert_mypy_fails(
        """\
        import h5py
        dataset: h5py.Dataset
        group: h5py.Group
        group.create_dataset_like()
        """,
        4,
        (
            'All overload variants of "create_dataset_like" of "Group" '
            "require at least one argument"
        ),
    )


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
