"""D-CNV-01 — 1 feet → meter (FR-02 / SC-01)."""

import pytest


@pytest.mark.d_cnv_01
def test_d_cnv_01_feet_to_meter():
    """D-CNV-01: 1 feet → 0.3048 m (±ε)."""
    # Given: Registry with feet and meter; input value 1 feet
    # When: Converter.convert("feet", "meter", 1)
    # Then: 0.3048 m (±ε)
    pytest.fail("RED: D-CNV-01 — 구현 없음, 의도적 실패")
