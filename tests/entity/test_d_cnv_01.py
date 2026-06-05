"""D-CNV-01 — 1 feet → meter (FR-02 / SC-01)."""

import pytest

from entity.constants import METER_TO_FEET
from entity.converter import Converter
from entity.length_unit import LengthUnit
from entity.registry import UnitRegistry


@pytest.mark.d_cnv_01
def test_d_cnv_01_feet_to_meter():
    """D-CNV-01: 1 feet → 0.3048 m (±ε)."""
    # Given: Registry with feet and meter; input value 1 feet
    registry = UnitRegistry()
    registry.register(LengthUnit("meter", 1.0))
    registry.register(LengthUnit("feet", 1.0 / METER_TO_FEET))
    converter = Converter(registry)

    # When: Converter.convert("feet", "meter", 1)
    result = converter.convert("feet", "meter", 1)

    # Then: 0.3048 m (±ε)
    assert result == pytest.approx(0.3048)
