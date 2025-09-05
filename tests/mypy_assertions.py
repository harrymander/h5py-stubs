import textwrap

import mypy.api


def _add_line_numbers(s: str) -> str:
    lines = s.splitlines()
    width = len(str(len(lines)))
    return "\n".join(f"{i + 1:>{width}}| {line}" for i, line in enumerate(lines))


def assert_mypy_passes(source: str) -> None:
    __tracebackhide__ = True
    stdout, stderr, ret = mypy.api.run(["-c", source])
    if ret == 0:
        return

    msg = [f"mypy error ({ret = })"]
    indent = "  "
    msg.append("=== source ===")
    msg.append(textwrap.indent(_add_line_numbers(source), indent))
    if stdout:
        msg.append("=== mypy stdout ===")
        msg.append(textwrap.indent(stdout, indent))
    if stderr:
        msg.append("=== mypy stderr ===")
        msg.append(textwrap.indent(stderr, indent))
    raise AssertionError("\n".join(msg))


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
    assert_mypy_passes("\n".join(lines))
