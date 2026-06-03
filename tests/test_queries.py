"""Pruebas de la Feature 4: listar prestamos de un miembro."""
import pytest
from cafelibro import queries


def fake_data():
    return {
        "books": [
            {"code": "B001", "title": "Clean Code", "available": False},
            {"code": "B002", "title": "Refactoring", "available": False},
        ],
        "members": [
            {"id": "M001", "name": "Ana Torres"},
            {"id": "M002", "name": "Beto Ruiz"},
        ],
        "loans": [
            {"book_code": "B001", "member_id": "M001",
             "loan_date": "2026-06-01", "due_date": "2026-06-15"},
            {"book_code": "B002", "member_id": "M001",
             "loan_date": "2026-06-02", "due_date": "2026-06-16"},
        ],
    }


def test_member_with_active_loans_includes_title(monkeypatch):
    monkeypatch.setattr(queries, "load_data", fake_data)
    result = queries.list_member_loans("M001")
    codes = {r["book_code"] for r in result}
    assert codes == {"B001", "B002"}
    assert all("title" in r and "due_date" in r for r in result)
    assert any(r["title"] == "Clean Code" for r in result)


def test_member_with_no_loans_returns_empty(monkeypatch):
    monkeypatch.setattr(queries, "load_data", fake_data)
    assert queries.list_member_loans("M002") == []


def test_unknown_member_raises_value_error(monkeypatch):
    monkeypatch.setattr(queries, "load_data", fake_data)
    with pytest.raises(ValueError):
        queries.list_member_loans("M999")