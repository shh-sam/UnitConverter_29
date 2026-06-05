"""Entity-layer pytest fixtures."""

import pytest

from entity.constants import METER_TO_FEET
from entity.converter import Converter
from entity.length_unit import LengthUnit
from entity.registry import UnitRegistry


@pytest.fixture
def meter_feet_registry():
    """Registry with meter and feet; returns Converter wired to that registry."""
    registry = UnitRegistry()
    registry.register(LengthUnit("meter", 1.0))
    registry.register(LengthUnit("feet", 1.0 / METER_TO_FEET))
    return Converter(registry)
