import argparse
from cafelibro.books import register_book
from cafelibro.members import register_member


def main():
    parser = argparse.ArgumentParser(prog="cafelibro")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_book = subparsers.add_parser("add-book", help="Register a book in the catalogue")
    add_book.add_argument("--code", required=True, help="Unique book code")
    add_book.add_argument("--title", required=True, help="Book title")

    add_member = subparsers.add_parser("add-member", help="Register a member")
    add_member.add_argument("--id", required=True, help="Unique member id")
    add_member.add_argument("--name", required=True, help="Member name")

    args = parser.parse_args()

    if args.command == "add-book":
        try:
            book = register_book(args.code, args.title)
            print(book)
        except ValueError as e:
            print(f"Error: {e}")
            raise SystemExit(1)
    elif args.command == "add-member":
        try:
            member = register_member(args.id, args.name)
            print(member)
        except ValueError as e:
            print(f"Error: {e}")
            raise SystemExit(1)
