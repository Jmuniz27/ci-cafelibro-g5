"""Consultas sobre los prestamos. Feature 4: listar prestamos de un miembro."""
from cafelibro.storage import load_data


def list_member_loans(member_id: str) -> list[dict]:
    data = load_data()
    if not any(m["id"] == member_id for m in data["members"]):
        raise ValueError(f"No existe un miembro con id {member_id!r}")

    result = []
    for loan in data["loans"]:
        if loan["member_id"] == member_id:
            book = next(
                (b for b in data["books"] if b["code"] == loan["book_code"]), None
            )
            title = book["title"] if book else None
            result.append({
                "book_code": loan["book_code"],
                "title": title,
                "due_date": loan["due_date"],
            })
    return result
