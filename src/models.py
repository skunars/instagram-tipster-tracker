from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Optional


@dataclass
class Tip:
    tip_id: str
    source: str
    first_seen_at: str
    published_at: Optional[str]
    post_url: Optional[str]
    post_id: Optional[str]
    coupon_id: Optional[str]
    event: str
    market: str
    selection: str
    odds: Optional[float]
    status: str = "OPEN"
    outcome: Optional[str] = None
    settled_at: Optional[str] = None
    evidence_url: Optional[str] = None
    evidence_note: Optional[str] = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
