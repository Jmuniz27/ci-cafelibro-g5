import pytest
from unittest.mock import patch
from cafelibro.books import register_book


EMPTY_DATA = {"books": [], "members": [], "loans": []}


def _data_with_book():
    return {"books": [{"code": "B001", "title": "Clean Code", "available": True}], "members": [], "loans": []}


def test_register_book_returns_correct_dict(tmp_path):
    with patch("cafelibro.storage.DATA_FILE", tmp_path / "data.json"):
        result = register_book("B001", "Clean Code")

    assert result == {"code": "B001", "title": "Clean Code", "available": True}


def test_register_book_duplicate_code_raises_value_error(tmp_path):
    data_file = tmp_path / "data.json"
    with patch("cafelibro.storage.DATA_FILE", data_file):
        register_book("B001", "Clean Code")
        with pytest.raises(ValueError):
            register_book("B001", "Clean Code 2nd Edition")
