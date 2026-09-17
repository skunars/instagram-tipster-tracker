import json
from pathlib import Path


def test_report_calculation(tmp_path: Path, monkeypatch):
    import src.report as report

    tips = [
        {"tip_id": "a", "market": "1X2", "odds": 2.0, "coupon_id": "c1"},
        {"tip_id": "b", "market": "BTTS", "odds": 1.5, "coupon_id": "c1"},
        {"tip_id": "c", "market": "1X2", "odds": 3.0, "coupon_id": "c2"},
    ]
    settlements = [
        {"tip_id": "a", "outcome": "WON"},
        {"tip_id": "b", "outcome": "WON"},
        {"tip_id": "c", "outcome": "LOST"},
    ]
    tips_path = tmp_path / "tips.jsonl"
    settlements_path = tmp_path / "settlements.jsonl"
    tips_path.write_text("\n".join(json.dumps(x) for x in tips) + "\n", encoding="utf-8")
    settlements_path.write_text("\n".join(json.dumps(x) for x in settlements) + "\n", encoding="utf-8")
    monkeypatch.setattr(report, "TIPS", tips_path)
    monkeypatch.setattr(report, "SETTLEMENTS", settlements_path)

    result = report.calculate()
    assert result["settled"] == 3
    assert result["won"] == 2
    assert result["lost"] == 1
    assert result["hit_rate_percent"] == 66.67
    assert result["full_coupon_hit_rate_percent"] == 50.0
    assert result["virtual_profit_tl"] == 50.0
