from cafelibro.storage import load_data, save_data


def return_book(book_code: str) -> dict:
    """Return a borrowed book.

    Removes the loan entry for ``book_code`` and marks the matching book as
    available again. Raises ``ValueError`` if no loan exists for the book.
    """
    data = load_data()

    loan = next(
        (entry for entry in data["loans"] if entry["book_code"] == book_code),
        None,
    )
    if loan is None:
        raise ValueError(f"No active loan found for book {book_code}")

    data["loans"].remove(loan)

    for book in data["books"]:
        if book["code"] == book_code:
            book["available"] = True
            break

    save_data(data)
    return loan
