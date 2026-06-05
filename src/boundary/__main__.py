import sys

from boundary.input_parser import parse_input
from control.convert_use_case import ConvertUseCase


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    raw = args[0] if args else ""

    outcome = ConvertUseCase(parse_input).execute(raw)
    if outcome.kind == "error":
        print(outcome.error_code, file=sys.stderr)
        return 1
    if outcome.kind == "not_ready":
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
