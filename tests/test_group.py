import pytest

from .mypy_assertions import assert_mypy_fails, assert_mypy_passes


@pytest.mark.parametrize("key", ['"str"', 'b"bytes"'])
def test_index_group(key: str) -> None:
    assert_mypy_passes(f"""\
    from typing import assert_type
    import h5py

    group: h5py.Group
    assert_type(group[{key}], h5py.HLObject)
    """)


@pytest.mark.parametrize("key", ['"str"', 'b"bytes"'])
def test_group_del_item(key: str) -> None:
    assert_mypy_passes(f"""\
    import h5py
    group: h5py.Group
    del group[{key}]
    """)


@pytest.mark.parametrize("key", ['"str"', 'b"bytes"'])
def test_group_set_item(key: str) -> None:
    assert_mypy_passes(f"""\
    import h5py
    group: h5py.Group
    group[{key}] = 100
    """)


@pytest.mark.parametrize("key", ['"str"', 'b"bytes"'])
def test_group_contains(key: str) -> None:
    assert_mypy_passes(f"""\
    import h5py
    group: h5py.Group
    {key} in group
    """)


def test_group_contains_invalid_type_fails() -> None:
    assert_mypy_fails(
        """\
        import h5py
        group: h5py.Group
        12 in group
        """,
        3,
        "Unsupported operand types for in",
    )


@pytest.mark.parametrize("abc_type", ["Mapping", "MutableMapping"])
def test_group_compatible_with_mapping_str(abc_type: str) -> None:
    """
    Only compatible with (Mutable)Mapping[str, HLObject] because __iter__, keys(), etc.
    always returns str.
    """
    assert_mypy_passes(f"""\
    from collections.abc import {abc_type}
    import h5py

    def func(mapping: {abc_type}[str, h5py.HLObject]) -> None:
        ...

    group: h5py.Group
    func(group)
    """)


def test_group_iter_returns_str() -> None:
    assert_mypy_passes("""\
    from typing import assert_type
    import h5py

    group: h5py.Group
    for key in group:
        assert_type(key, str)
    """)


def test_group_keys_returns_str() -> None:
    assert_mypy_passes("""\
    from typing import assert_type
    import h5py

    group: h5py.Group
    for key in group.keys():
        assert_type(key, str)
    """)


def test_group_values_returns_hlobject() -> None:
    assert_mypy_passes("""\
    from typing import assert_type
    import h5py

    group: h5py.Group
    for value in group.values():
        assert_type(value, h5py.HLObject)
    """)


def test_group_items_returns_str_hlobject() -> None:
    assert_mypy_passes("""\
    from typing import assert_type
    import h5py

    group: h5py.Group
    for key, value in group.items():
        assert_type(key, str)
        assert_type(value, h5py.HLObject)
    """)
