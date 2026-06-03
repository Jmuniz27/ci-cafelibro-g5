import pytest
from unittest.mock import patch
from cafelibro.storage import load_data


def test_load_data_returns_empty_structure_when_no_file(tmp_path):
    with patch("cafelibro.storage.DATA_FILE", tmp_path / "data.json"):
        result = load_data()

    assert result == {"books": [], "members": [], "loans": []}
