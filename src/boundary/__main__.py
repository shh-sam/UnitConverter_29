import sys

from boundary.input_parser import parse_input


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    raw = args[0] if args else ""

    result = parse_input(raw)
    if isinstance(result, str):
        print(result, file=sys.stderr)
        return 1
    if result is None:
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
