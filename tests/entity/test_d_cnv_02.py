"""D-CNV-02 — 2.5 meter → feet (FR-02)."""

import pytest

from tests._approval import assert_matches_golden


@pytest.mark.d_cnv_02
def test_d_cnv_02_meter_to_feet(meter_feet_registry):
    """D-CNV-02: 2.5 m → 8.20210 feet (5 decimal places)."""
    # Given: Registry with meter and feet; input value 2.5 meter
    converter = meter_feet_registry

    # When: Converter.convert("meter", "feet", 2.5)
    result = converter.convert("meter", "feet", 2.5)

    # Then: 8.20210 feet (5 decimal places)
    assert result == pytest.approx(8.20210, abs=1e-5)
    assert_matches_golden(f"{result:.5f}", "d_cnv_02_meter_to_feet.approved.txt")
