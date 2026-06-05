"""D-CNV-01 — 1 feet → meter (FR-02 / SC-01)."""

import pytest

from tests._approval import assert_matches_golden


@pytest.mark.d_cnv_01
def test_d_cnv_01_feet_to_meter(meter_feet_registry):
    """D-CNV-01: 1 feet → 0.3048 m (±ε)."""
    # Given: Registry with feet and meter; input value 1 feet
    converter = meter_feet_registry

    # When: Converter.convert("feet", "meter", 1)
    result = converter.convert("feet", "meter", 1)

    # Then: 0.3048 m (±ε)
    assert result == pytest.approx(0.3048)
    assert_matches_golden(f"{result:.5f}", "d_cnv_01_feet_to_meter.approved.txt")
