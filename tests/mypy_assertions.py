import re
import textwrap

import mypy.api


def _add_line_numbers(s: str) -> str:
    lines = s.splitlines()
    width = len(str(len(lines)))
    return "\n".join(f"{i + 1:>{width}}| {line}" for i, line in enumerate(lines))


def _format_mypy_output(source: str, stdout: str, stderr: str) -> str:
    indent = "  "
    msg = ["=== source ==="]
    msg.append(_add_line_numbers(source))
    if stdout:
        msg.append("=== mypy stdout ===")
        msg.append(textwrap.indent(stdout, indent))
    if stderr:
        msg.append("=== mypy stderr ===")
        msg.append(textwrap.indent(stderr, indent))
    return "\n".join(msg)


def _assert_mypy_passes(dedented_source: str) -> None:
    __tracebackhide__ = True
    stdout, stderr, ret = mypy.api.run(["-c", dedented_source])
    if ret == 0:
        return

    error_msg = _format_mypy_output(dedented_source, stdout, stderr)
    header = (
        "mypy type checking failed"
        if ret == 1
        else f"mypy internal error (exit code = {ret})"
    )
    raise AssertionError(f"{header}\n{error_msg}")


def assert_mypy_passes(source: str) -> None:
    """
    Assert that mypy passes on the given source code.

    `source` is dedented before passing to mypy.
    """
    __tracebackhide__ = True
    _assert_mypy_passes(textwrap.dedent(source))


def assert_mypy_fails(source: str, line: int, regex: str) -> None:
    """
    Assert that mypy fails at a specific line with specific message.

    Args:
        source: Source code to check. It is dedented before passing to mypy.
        line: 1-based line number to match.
        regex: Regex to search for in error message. The regex is matched anywhere in
            the line after the line number designator: prepend with ^ to match the start
            of the error message.
    """
    __tracebackhide__ = True
    if line < 1:
        raise ValueError("line number must be >= 1")

    source = textwrap.dedent(source)
    stdout, stderr, ret = mypy.api.run(["-c", source])
    if ret == 0:
        raise AssertionError("mypy exited without error")
    if ret != 1:
        err_msg = _format_mypy_output(source, stdout, stderr)
        msg = f"mypy exited with internal error (code = {ret})\n{err_msg}"
        raise AssertionError(msg)

    line_match = re.match(rf"^<string>:{line}: (.*)$", stdout, re.MULTILINE)
    if not line_match:
        err_msg = _format_mypy_output(source, stdout, stderr)
        msg = f"mypy did not report an error on line {line}\n{err_msg}"
        raise AssertionError(msg)

    err_match = re.search(regex, line_match.group(1))
    if not err_match:
        err_msg = _format_mypy_output(source, stdout, stderr)
        msg = f'mypy error message on line {line} did not match "{regex}"\n{err_msg}'
        raise AssertionError(msg)


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
