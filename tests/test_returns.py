import json
from unittest.mock import patch

import pytest

from cafelibro.returns import return_book


def _write_data(path, data):
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f)


def test_return_removes_loan_and_sets_available(tmp_path):
    data_file = tmp_path / "data.json"
    _write_data(
        data_file,
        {
            "books": [{"code": "B001", "title": "Clean Code", "available": False}],
            "members": [{"id": "M001", "name": "Ana Torres"}],
            "loans": [
                {
                    "book_code": "B001",
                    "member_id": "M001",
                    "loan_date": "2026-06-01",
                    "due_date": "2026-06-15",
                }
            ],
        },
    )

    with patch("cafelibro.storage.DATA_FILE", data_file):
        removed = return_book("B001")

    assert removed["book_code"] == "B001"
    assert removed["member_id"] == "M001"

    with data_file.open(encoding="utf-8") as f:
        saved = json.load(f)

    assert saved["loans"] == []
    assert saved["books"][0]["available"] is True


def test_return_book_not_in_loans_raises_value_error(tmp_path):
    data_file = tmp_path / "data.json"
    _write_data(
        data_file,
        {
            "books": [{"code": "B001", "title": "Clean Code", "available": True}],
            "members": [{"id": "M001", "name": "Ana Torres"}],
            "loans": [],
        },
    )

    with patch("cafelibro.storage.DATA_FILE", data_file):
        with pytest.raises(ValueError):
            return_book("B001")
