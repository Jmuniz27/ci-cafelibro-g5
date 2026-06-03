from cafelibro.storage import load_data, save_data
from datetime import date

def loan_book(book_code: str, member_id: str, loan_date: str, due_date: str) -> None:
    data = load_data()

    start = date.fromisoformat(loan_date)
    end = date.fromisoformat(due_date)

    if end <= start:
        raise ValueError("due_date must be after loan_date")

    if not any(book["code"] == book_code for book in data["books"]):
        raise LookupError(f"Book {book_code} not found")

    if not any(member["id"] == member_id for member in data["members"]):
        raise LookupError(f"Member {member_id} not found")

    loan = {
        "book_code": book_code,
        "member_id": member_id,
        "loan_date": loan_date,
        "due_date": due_date
    }

    data["loans"].append(loan)
    save_data(data)



