"""D-CNV-02 — 2.5 meter → feet (FR-02)."""

import pytest

from entity.constants import METER_TO_FEET
from entity.converter import Converter
from entity.length_unit import LengthUnit
from entity.registry import UnitRegistry


@pytest.mark.d_cnv_02
def test_d_cnv_02_meter_to_feet():
    """D-CNV-02: 2.5 m → 8.20210 feet (5 decimal places)."""
    # Given: Registry with meter and feet; input value 2.5 meter
    registry = UnitRegistry()
    registry.register(LengthUnit("meter", 1.0))
    registry.register(LengthUnit("feet", 1.0 / METER_TO_FEET))
    converter = Converter(registry)

    # When: Converter.convert("meter", "feet", 2.5)
    result = converter.convert("meter", "feet", 2.5)

    # Then: 8.20210 feet (5 decimal places)
    assert result == pytest.approx(8.20210, abs=1e-5)
