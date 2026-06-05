from entity.registry import UnitRegistry


class Converter:
    def __init__(self, registry: UnitRegistry) -> None:
        self._registry = registry

    def convert(self, from_unit: str, to_unit: str, value: float) -> float:
        from_u = self._registry.get(from_unit)
        to_u = self._registry.get(to_unit)
        in_meters = value * from_u.meters_per_unit
        return in_meters / to_u.meters_per_unit
