import argparse
from cafelibro.books import register_book
from cafelibro.queries import list_member_loans          # <-- NUEVO


def main():
    parser = argparse.ArgumentParser(prog="cafelibro")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_book = subparsers.add_parser("add-book", help="Register a book in the catalogue")
    add_book.add_argument("--code", required=True, help="Unique book code")
    add_book.add_argument("--title", required=True, help="Book title")

    args = parser.parse_args()

    if args.command == "add-book":
        try:
            book = register_book(args.code, args.title)
            print(book)
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
