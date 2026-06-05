"""Convert CLI input — orchestration in control layer (NFR-02)."""

from collections.abc import Callable
from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True)
class ConvertOutcome:
    kind: Literal["error", "not_ready", "ready"]
    error_code: str | None = None
    unit_and_value: tuple[str, float] | None = None


class ConvertUseCase:
    def __init__(
        self,
        parse_input: Callable[[str], tuple[str, float] | str | None],
    ) -> None:
        self._parse_input = parse_input

    def execute(self, raw: str) -> ConvertOutcome:
        result = self._parse_input(raw)
        if isinstance(result, str):
            return ConvertOutcome(kind="error", error_code=result)
        if result is None:
            return ConvertOutcome(kind="not_ready")
        return ConvertOutcome(kind="ready", unit_and_value=result)
