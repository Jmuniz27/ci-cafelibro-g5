from cafelibro.storage import load_data, save_data


def register_book(code: str, title: str) -> dict:
    data = load_data()
    if any(b["code"] == code for b in data["books"]):
        raise ValueError(f"A book with code '{code}' already exists.")
    book = {"code": code, "title": title, "available": True}
    data["books"].append(book)
    save_data(data)
    return book
