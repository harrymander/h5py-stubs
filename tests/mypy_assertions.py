import textwrap

import mypy.api


def _add_line_numbers(s: str) -> str:
    lines = s.splitlines()
    width = len(str(len(lines)))
    return "\n".join(f"{i + 1:>{width}}| {line}" for i, line in enumerate(lines))


def _assert_mypy_passes(dedented_source: str) -> None:
    __tracebackhide__ = True
    stdout, stderr, ret = mypy.api.run(["-c", dedented_source])
    if ret == 0:
        return

    msg = [f"mypy error ({ret = })"]
    indent = "  "
    msg.append("=== source ===")
    msg.append(_add_line_numbers(dedented_source))
    if stdout:
        msg.append("=== mypy stdout ===")
        msg.append(textwrap.indent(stdout, indent))
    if stderr:
        msg.append("=== mypy stderr ===")
        msg.append(textwrap.indent(stderr, indent))
    raise AssertionError("\n".join(msg))


def assert_mypy_passes(source: str) -> None:
    """
    Assert that mypy passes on the given source code.

    `source` is dedented before passing to mypy.
    """
    __tracebackhide__ = True
    _assert_mypy_passes(textwrap.dedent(source))


def assert_type_expressions(
    exp_type: str,
    *expressions: str,
    setup: str | None = None,
) -> None:
    """
    Calls `typing.assert_type({expr}, {exp_type})` for each expression in `expressions`.

    `setup` is dedented if provided.
    """
    __tracebackhide__ = True

    if not expressions:
        raise TypeError("got 1 positional argument, 2 or more required")

    lines: list[str] = ["from typing import assert_type"]
    if setup:
        lines.append(textwrap.dedent(setup))
    lines.extend(f"assert_type({expr}, {exp_type})" for expr in expressions)
    _assert_mypy_passes("\n".join(lines))
