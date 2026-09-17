from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path

from src.storage import JsonlStore

SETTLEMENTS = Path("data/settlements.jsonl")
ALLOWED = {"WON", "LOST", "VOID"}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def settle(tip_id: str, outcome: str, evidence_url: str | None = None, note: str | None = None) -> None:
    outcome = outcome.upper()
    if outcome not in ALLOWED:
        raise SystemExit(f"outcome must be one of: {', '.join(sorted(ALLOWED))}")
    JsonlStore(SETTLEMENTS).append({
        "tip_id": tip_id,
        "outcome": outcome,
        "settled_at": utc_now(),
        "evidence_url": evidence_url,
        "note": note,
    })


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Record an observed tip outcome without modifying the original tip record.")
    parser.add_argument("tip_id")
    parser.add_argument("outcome", choices=sorted(ALLOWED))
    parser.add_argument("--evidence-url")
    parser.add_argument("--note")
    args = parser.parse_args()
    settle(args.tip_id, args.outcome, args.evidence_url, args.note)
    print(f"settled {args.tip_id} -> {args.outcome}")
