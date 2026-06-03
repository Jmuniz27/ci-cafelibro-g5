import argparse
import sys

from cafelibro.returns import return_book


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="cafelibro", description="CaféLibro CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    return_parser = subparsers.add_parser("return", help="Return a borrowed book")
    return_parser.add_argument("--book", required=True, help="Book code to return")

    return parser


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "return":
        try:
            loan = return_book(args.book)
        except ValueError as exc:
            print(f"Error: {exc}", file=sys.stderr)
            raise SystemExit(1)
        print(loan)


if __name__ == "__main__":
    main()
