"""U-IN-03 — negative value → E003 (FR-04 / SC-02)."""

import pytest


@pytest.mark.u_in_03
def test_u_in_03_negative_value():
    """U-IN-03: CLI \"meter:-1\" → stderr E003, exit≠0, no conversion stdout."""
    # Given: CLI argument "meter:-1" (negative value)
    # When: python -m boundary "meter:-1"
    # Then: stderr E003, exit≠0, stdout has no conversion lines
    pytest.fail("RED: U-IN-03 — 음수 거부 미구현, 의도적 실패")
