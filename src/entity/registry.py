from entity.length_unit import LengthUnit


class UnitRegistry:
    def __init__(self) -> None:
        self._units: dict[str, LengthUnit] = {}

    def register(self, unit: LengthUnit) -> None:
        self._units[unit.name] = unit

    def get(self, name: str) -> LengthUnit:
        return self._units[name]
