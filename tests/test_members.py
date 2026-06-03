import pytest
from unittest.mock import patch
from cafelibro.members import register_member


def test_register_member_returns_correct_dict(tmp_path):
    with patch("cafelibro.storage.DATA_FILE", tmp_path / "data.json"):
        result = register_member("M001", "Ana Torres")

    assert result == {"id": "M001", "name": "Ana Torres"}


def test_register_member_duplicate_id_raises_value_error(tmp_path):
    data_file = tmp_path / "data.json"
    with patch("cafelibro.storage.DATA_FILE", data_file):
        register_member("M001", "Ana Torres")
        with pytest.raises(ValueError):
            register_member("M001", "Otra Persona")