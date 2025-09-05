from .mypy_assertions import assert_type_expressions


def assert_group_get_return_type(exp_type: str, *calls_args: str) -> None:
    __tracebackhide__ = True

    assert_type_expressions(
        exp_type,
        *(f"group.get({args})" for args in calls_args),
        setup="""\
        import h5py
        group: h5py.Group
        """,
    )


def test_group_get_no_default() -> None:
    assert_group_get_return_type("h5py.HLObject | None", '"hello, world"')


def test_group_get_with_default() -> None:
    assert_group_get_return_type(
        "int | h5py.HLObject",
        '"hello, world", 42',
        '"hello, world", default=42',
    )


def test_group_get_getclass_no_default() -> None:
    assert_group_get_return_type(
        "type[h5py.HLObject] | None",
        '"hello, world", getclass=True',
        '"hello, world", None, getclass=True',
        '"hello, world", None, True',
        '"hello, world", default=None, getclass=True',
        '"hello, world", getclass=True, default=None',
        '"hello, world", None, True, False',
        '"hello, world", getclass=True, getlink=False',
        '"hello, world", getlink=False, getclass=True',
    )


def test_group_get_getclass_with_default() -> None:
    assert_group_get_return_type(
        "type[h5py.HLObject] | int",
        '"hello, world", 42, True',
        '"hello, world", 42, getclass=True',
        '"hello, world", default=42, getclass=True',
        '"hello, world", getclass=True, default=42',
        '"hello, world", 42, True, False',
        '"hello, world", 42, getclass=True, getlink=False',
        '"hello, world", 42, getlink=False, getclass=True',
        '"hello, world", default=42, getlink=False, getclass=True',
        '"hello, world", default=42, getclass=True, getlink=False',
    )


def test_group_get_getlink_no_default() -> None:
    assert_group_get_return_type(
        "h5py.HardLink | h5py.ExternalLink | h5py.SoftLink | None",
        '"hello, world", getlink=True',
        '"hello, world", None, getlink=True',
        '"hello, world", None, False, True',
        '"hello, world", default=None, getlink=True',
        '"hello, world", getlink=True, default=None',
        '"hello, world", getlink=True, getclass=False',
        '"hello, world", getclass=False, getlink=True',
        '"hello, world", default=None, getclass=False, getlink=True',
        '"hello, world", default=None, getlink=True, getclass=False',
    )


def test_group_get_getlink_with_default() -> None:
    assert_group_get_return_type(
        "h5py.HardLink | h5py.ExternalLink | h5py.SoftLink | int",
        '"hello, world", 42, getclass=False, getlink=True',
        '"hello, world", 42, getlink=True, getclass=False',
        '"hello, world", 42, False, True',
        '"hello, world", default=42, getlink=True',
        '"hello, world", getlink=True, default=42',
        '"hello, world", 42, getclass=False, getlink=True',
        '"hello, world", 42, getlink=True, getclass=False',
        '"hello, world", default=42, getlink=True, getclass=False',
        '"hello, world", default=42, getclass=False, getlink=True',
    )


def test_group_get_getclass_and_getlink_no_default() -> None:
    assert_group_get_return_type(
        "type[h5py.HardLink] | type[h5py.ExternalLink] | type[h5py.SoftLink] | None",
        '"hello, world", getclass=True, getlink=True',
        '"hello, world", getlink=True, getclass=True',
        '"hello, world", None, getlink=True, getclass=True',
        '"hello, world", default=None, getlink=True, getclass=True',
        '"hello, world", None, True, True',
    )


def test_group_get_getclass_and_getlink_with_default() -> None:
    assert_group_get_return_type(
        "type[h5py.HardLink] | type[h5py.ExternalLink] | type[h5py.SoftLink] | int",
        '"hello, world", 42, getclass=True, getlink=True',
        '"hello, world", 42, getlink=True, getclass=True',
        '"hello, world", getlink=True, getclass=True, default=42',
        '"hello, world", 42, True, True',
    )
