from datetime import date
from unittest.mock import patch

import main


def _data(loans):
    return {"books": [], "members": [], "loans": loans}


def test_single_overdue_loan_reported(capsys):
    loans = [
        {
            "book_code": "B001",
            "member_id": "M001",
            "loan_date": "2026-05-01",
            "due_date": "2026-05-15",
        }
    ]
    with patch("main.load_data", return_value=_data(loans)):
        rc = main.main(["overdue", "--date", "2026-06-03"])

    assert rc == 0
    out = capsys.readouterr().out
    assert "[OVERDUE] B001 loaned to M001 — due 2026-05-15" in out


def test_loan_due_exactly_on_date_not_reported(capsys):
    loans = [
        {
            "book_code": "B001",
            "member_id": "M001",
            "loan_date": "2026-05-20",
            "due_date": "2026-06-03",
        }
    ]
    with patch("main.load_data", return_value=_data(loans)):
        rc = main.main(["overdue", "--date", "2026-06-03"])

    assert rc == 0
    out = capsys.readouterr().out
    assert "No overdue loans." in out
    assert "[OVERDUE]" not in out


def test_future_loan_not_reported(capsys):
    loans = [
        {
            "book_code": "B002",
            "member_id": "M002",
            "loan_date": "2026-06-01",
            "due_date": "2026-07-01",
        }
    ]
    with patch("main.load_data", return_value=_data(loans)):
        rc = main.main(["overdue", "--date", "2026-06-03"])

    assert rc == 0
    out = capsys.readouterr().out
    assert "No overdue loans." in out
    assert "[OVERDUE]" not in out


def test_multiple_overdue_loans_all_appear(capsys):
    loans = [
        {
            "book_code": "B001",
            "member_id": "M001",
            "loan_date": "2026-05-01",
            "due_date": "2026-05-10",
        },
        {
            "book_code": "B002",
            "member_id": "M002",
            "loan_date": "2026-05-05",
            "due_date": "2026-06-02",
        },
        {
            "book_code": "B003",
            "member_id": "M003",
            "loan_date": "2026-06-01",
            "due_date": "2026-07-01",  # future, must NOT appear
        },
    ]
    with patch("main.load_data", return_value=_data(loans)):
        rc = main.main(["overdue", "--date", "2026-06-03"])

    assert rc == 0
    out = capsys.readouterr().out
    assert "[OVERDUE] B001 loaned to M001 — due 2026-05-10" in out
    assert "[OVERDUE] B002 loaned to M002 — due 2026-06-02" in out
    assert "B003" not in out


def test_no_overdue_loans_message(capsys):
    with patch("main.load_data", return_value=_data([])):
        rc = main.main(["overdue", "--date", "2026-06-03"])

    assert rc == 0
    out = capsys.readouterr().out
    assert out.strip() == "No overdue loans."


def test_invalid_date_exits_code_1(capsys):
    # load_data must never be called on a validation failure.
    with patch("main.load_data") as mocked:
        rc = main.main(["overdue", "--date", "not-a-date"])

    assert rc == 1
    mocked.assert_not_called()
    err = capsys.readouterr().err
    assert "invalid --date" in err
