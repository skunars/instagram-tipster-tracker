from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

TIPS = Path("data/tips.jsonl")
SETTLEMENTS = Path("data/settlements.jsonl")
INITIAL_BANKROLL = 1000.0
STAKE = 100.0


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def latest_settlements() -> dict[str, dict[str, Any]]:
    latest: dict[str, dict[str, Any]] = {}
    for row in read_jsonl(SETTLEMENTS):
        if row.get("tip_id"):
            latest[row["tip_id"]] = row
    return latest


def calculate() -> dict[str, Any]:
    tips = read_jsonl(TIPS)
    settlements = latest_settlements()
    outcomes = {"WON", "LOST", "VOID"}
    settled = [settlements[t["tip_id"]] for t in tips if t.get("tip_id") in settlements and settlements[t["tip_id"]].get("outcome") in outcomes]
    won = sum(1 for row in settled if row["outcome"] == "WON")
    lost = sum(1 for row in settled if row["outcome"] == "LOST")
    void = sum(1 for row in settled if row["outcome"] == "VOID")
    bankroll = INITIAL_BANKROLL
    for tip in tips:
        settlement = settlements.get(tip.get("tip_id"))
        if not settlement or settlement.get("outcome") not in outcomes:
            continue
        outcome = settlement["outcome"]
        odds = float(tip.get("odds") or 0)
        if outcome == "WON" and odds > 0:
            bankroll += STAKE * (odds - 1.0)
        elif outcome == "LOST":
            bankroll -= STAKE
    coupons: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for tip in tips:
        if tip.get("coupon_id"):
            coupons[tip["coupon_id"]].append(tip)
    full_coupons = 0
    full_won = 0
    for rows in coupons.values():
        results = [settlements.get(r["tip_id"], {}).get("outcome") for r in rows]
        if results and all(x in outcomes for x in results):
            full_coupons += 1
            if all(x == "WON" for x in results):
                full_won += 1
    market_counts = Counter(t.get("market", "UNCLASSIFIED") for t in tips)
    return {
        "tips": len(tips),
        "settled": len(settled),
        "open": len(tips) - len(settled),
        "won": won,
        "lost": lost,
        "void": void,
        "hit_rate_percent": round((won / (won + lost) * 100), 2) if won + lost else None,
        "virtual_bankroll_tl": round(bankroll, 2),
        "virtual_profit_tl": round(bankroll - INITIAL_BANKROLL, 2),
        "coupons": len(coupons),
        "fully_settled_coupons": full_coupons,
        "full_coupon_hit_rate_percent": round(full_won / full_coupons * 100, 2) if full_coupons else None,
        "markets": dict(market_counts),
    }


if __name__ == "__main__":
    print(json.dumps(calculate(), ensure_ascii=False, indent=2, sort_keys=True))
