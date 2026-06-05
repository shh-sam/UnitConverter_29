"""Parse CLI input `unit:value` into unit and value, or return an error code."""


def parse_input(raw: str) -> tuple[str, float] | str | None:
    if raw == "":
        return "E001"
    return None
