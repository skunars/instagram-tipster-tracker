from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from src.models import Tip
from src.storage import JsonlStore

SOURCE = "kahinmahrezz"
DATA_FILE = Path("data/tips.jsonl")


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def make_tip_id(post_id: Optional[str], event: str, market: str, selection: str) -> str:
    raw = "|".join((SOURCE, post_id or "", event, market, selection))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:20]


def record_tip(
    event: str,
    market: str,
    selection: str,
    *,
    odds: Optional[float] = None,
    post_url: Optional[str] = None,
    post_id: Optional[str] = None,
    published_at: Optional[str] = None,
    coupon_id: Optional[str] = None,
    evidence_url: Optional[str] = None,
    evidence_note: Optional[str] = None,
) -> Tip:
    tip = Tip(
        tip_id=make_tip_id(post_id, event, market, selection),
        source=SOURCE,
        first_seen_at=utc_now(),
        published_at=published_at,
        post_url=post_url,
        post_id=post_id,
        coupon_id=coupon_id,
        event=event,
        market=market,
        selection=selection,
        odds=odds,
        evidence_url=evidence_url,
        evidence_note=evidence_note,
    )
    store = JsonlStore(DATA_FILE)
    existing = {row["tip_id"] for row in store.read_all() if "tip_id" in row}
    if tip.tip_id not in existing:
        store.append(tip.to_dict())
    return tip


if __name__ == "__main__":
    print(f"Tracker ready for @{SOURCE}. No live collection is enabled yet.")
