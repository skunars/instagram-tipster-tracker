from pathlib import Path

from src.storage import JsonlStore
from tracker import make_tip_id


def test_tip_id_is_deterministic():
    assert make_tip_id("123", "Team A - Team B", "1X2", "Team A") == make_tip_id(
        "123", "Team A - Team B", "1X2", "Team A"
    )


def test_jsonl_store_roundtrip(tmp_path: Path):
    store = JsonlStore(tmp_path / "tips.jsonl")
    store.append({"tip_id": "abc", "status": "OPEN"})
    assert store.read_all() == [{"tip_id": "abc", "status": "OPEN"}]
