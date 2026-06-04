import argparse
from datetime import date

from cafelibro.books import register_book
from cafelibro.loan_book import loan_book
from cafelibro.members import register_member
from cafelibro.queries import list_member_loans
from cafelibro.returns import return_book
from main import overdue_command


def main():
    parser = argparse.ArgumentParser(prog="cafelibro")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_book = subparsers.add_parser("add-book", help="Register a book in the catalogue")
    add_book.add_argument("--code", required=True, help="Unique book code")
    add_book.add_argument("--title", required=True, help="Book title")

    add_member = subparsers.add_parser("add-member", help="Register a member")
    add_member.add_argument("--id", required=True, help="Unique member id")
    add_member.add_argument("--name", required=True, help="Member name")

    loan_parser = subparsers.add_parser("loan", help="Loan a book to a member")
    loan_parser.add_argument("--book", required=True, help="Book code")
    loan_parser.add_argument("--member", required=True, help="Member id")
    loan_parser.add_argument("--due-date", required=True, help="Due date (YYYY-MM-DD)")

    list_loans = subparsers.add_parser("list-loans", help="List active loans for a member")
    list_loans.add_argument("--member", required=True, help="Member id")

    return_parser = subparsers.add_parser("return", help="Return a borrowed book")
    return_parser.add_argument("--book", required=True, help="Book code to return")

    overdue_parser = subparsers.add_parser("overdue", help="Report overdue loans")
    overdue_parser.add_argument("--today", required=True, help="Today's date (YYYY-MM-DD)")

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

    elif args.command == "loan":
        try:
            loan_book(args.book, args.member, date.today().isoformat(), args.due_date)
            print(f"Book {args.book} loaned to {args.member}, due {args.due_date}.")
        except (ValueError, LookupError) as e:
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

    elif args.command == "return":
        try:
            loan = return_book(args.book)
            print(loan)
        except ValueError as e:
            print(f"Error: {e}")
            raise SystemExit(1)

    elif args.command == "overdue":
        try:
            today = date.fromisoformat(args.today)
        except ValueError:
            print(f"Error: invalid date '{args.today}', expected YYYY-MM-DD.")
            raise SystemExit(1)
        overdue_command(today)


if __name__ == "__main__":
    main()
