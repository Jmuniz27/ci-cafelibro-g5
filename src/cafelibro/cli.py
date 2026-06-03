import argparse
from cafelibro.books import register_book
from cafelibro.members import register_member
from cafelibro.queries import list_member_loans
from cafelibro.returns import return_book


def main():
    parser = argparse.ArgumentParser(prog="cafelibro")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_book = subparsers.add_parser("add-book", help="Register a book in the catalogue")
    add_book.add_argument("--code", required=True, help="Unique book code")
    add_book.add_argument("--title", required=True, help="Book title")

    add_member = subparsers.add_parser("add-member", help="Register a member")
    add_member.add_argument("--id", required=True, help="Unique member id")
    add_member.add_argument("--name", required=True, help="Member name")

    list_loans = subparsers.add_parser("list-loans", help="List active loans for a member")
    list_loans.add_argument("--member", required=True, help="Member id")

    return_book_parser = subparsers.add_parser("return", help="Return a borrowed book")
    return_book_parser.add_argument("--book", required=True, help="Book code to return")

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
    elif args.command == "return":
        try:
            loan = return_book(args.book)
            print(loan)
        except ValueError as e:
            print(f"Error: {e}")
            raise SystemExit(1)
    elif args.command == "list-loans":
        try:
            loans = list_member_loans(args.member)
        except ValueError as e:
            print(f"Error: {e}")
            raise SystemExit(1)
        if not loans:
            print(f"El miembro {args.member} no tiene libros prestados")
        for loan in loans:
            print(f"- {loan['book_code']} {loan['title']} (vence {loan['due_date']})")
    elif args.command == "add-member":
        try:
            member = register_member(args.id, args.name)
            print(member)
        except ValueError as e:
            print(f"Error: {e}")
            raise SystemExit(1)
