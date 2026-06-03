import argparse
import sys
from datetime import date

from cafelibro.storage import load_data


def _parse_date(value: str) -> date:
    """Parse a YYYY-MM-DD string into a date, raising ValueError otherwise."""
    return date.fromisoformat(value)


def overdue_command(today: date) -> None:
    """Print every loan whose due_date is strictly before ``today`` (read-only)."""
    data = load_data()
    loans = data.get("loans", [])
    overdue = [loan for loan in loans if _parse_date(loan["due_date"]) < today]

    if not overdue:
        print("No overdue loans.")
        return

    for loan in overdue:
        print(
            f"[OVERDUE] {loan['book_code']} loaned to "
            f"{loan['member_id']} — due {loan['due_date']}"
        )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="main.py")
    subparsers = parser.add_subparsers(dest="command", required=True)

    overdue_parser = subparsers.add_parser(
        "overdue", help="Report loans whose due date has passed."
    )
    # --date is validated manually so that both a missing and an invalid
    # value produce a clear message and exit code 1 (not argparse's code 2).
    overdue_parser.add_argument("--date", dest="date", default=None)

    return parser


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "overdue":
        if not args.date:
            print("Error: --date is required (format YYYY-MM-DD).", file=sys.stderr)
            return 1
        try:
            today = _parse_date(args.date)
        except ValueError:
            print(
                f"Error: invalid --date '{args.date}', expected YYYY-MM-DD.",
                file=sys.stderr,
            )
            return 1
        overdue_command(today)
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
