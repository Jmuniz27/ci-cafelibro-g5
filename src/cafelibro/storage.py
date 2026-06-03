import json
from pathlib import Path

DATA_FILE = Path("data.json")
EMPTY_DATA = {"books": {}, "members": {}, "loans": {}}


def load_data() -> dict:
    if not DATA_FILE.exists():
        return {"books": {}, "members": {}, "loans": {}}
    with DATA_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_data(data: dict) -> None:
    with DATA_FILE.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
