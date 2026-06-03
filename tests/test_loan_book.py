import pytest
from unittest.mock import patch
from cafelibro.loan_book import loan_book

@pytest.fixture
def mock_storage():
    with patch("cafelibro.loan_book.load_data") as load_mock, \
         patch("cafelibro.loan_book.save_data") as save_mock:
        yield load_mock, save_mock

def test_invalid_dates(mock_storage):
    _, save_mock = mock_storage

    with pytest.raises(ValueError, match="due_date must be after loan_date"):
        loan_book("B001", "M001", "2026-06-15", "2026-06-01")

    save_mock.assert_not_called()

def test_book_not_found(mock_storage):
    load_mock, save_mock = mock_storage

    load_mock.return_value = {
        "books": [],
        "members": [{"id": "M001"}],
        "loans": [],
    }

    with pytest.raises(LookupError, match="Book B001 not found"):
        loan_book("B001", "M001", "2026-06-01", "2026-06-15")

    save_mock.assert_not_called()

def test_member_not_found(mock_storage):
    load_mock, save_mock = mock_storage

    load_mock.return_value = {
        "books": [{"code": "B001"}],
        "members": [],
        "loans": [],
    }

    with pytest.raises(LookupError, match="Member M001 not found"):
        loan_book("B001", "M001", "2026-06-01", "2026-06-15")

    save_mock.assert_not_called()

def test_successful_loan(mock_storage):
    load_mock, save_mock = mock_storage

    data = {
        "books": [{"code": "B001"}],
        "members": [{"id": "M001"}],
        "loans": [],
    }

    load_mock.return_value = data

    result = loan_book(
        "B001",
        "M001",
        "2026-06-01",
        "2026-06-15"
    )

    assert result is None

    assert data["loans"] == [{
        "book_code": "B001",
        "member_id": "M001",
        "loan_date": "2026-06-01",
        "due_date": "2026-06-15",
    }]

    save_mock.assert_called_once_with(data)
