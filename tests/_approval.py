"""Golden Master (Approval Test) helpers."""

import difflib
import os
from pathlib import Path

_GOLDEN_ROOT = Path(__file__).resolve().parent / "golden"


def assert_matches_golden(actual: str, relative: str) -> None:
    """Compare actual output against a golden file under tests/golden/."""
    golden_path = _GOLDEN_ROOT / relative

    if os.environ.get("UPDATE_GOLDEN") == "1":
        golden_path.parent.mkdir(parents=True, exist_ok=True)
        golden_path.write_text(actual, encoding="utf-8")
        return

    if not golden_path.is_file():
        raise AssertionError(f"Golden file not found: {golden_path}")

    expected = golden_path.read_text(encoding="utf-8")
    if actual == expected:
        return

    diff = "".join(
        difflib.unified_diff(
            expected.splitlines(keepends=True),
            actual.splitlines(keepends=True),
            fromfile=f"expected ({relative})",
            tofile="actual",
        )
    )
    raise AssertionError(
        f"Golden mismatch for {relative}\n\n"
        f"--- expected ---\n{expected!r}\n\n"
        f"--- actual ---\n{actual!r}\n\n"
        f"--- diff ---\n{diff}"
    )
