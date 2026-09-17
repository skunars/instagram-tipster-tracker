from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def save_snapshot(source: str, url: str, body: str, directory: str | Path = "data/evidence") -> dict[str, Any]:
    digest = sha256_text(body)
    root = Path(directory)
    root.mkdir(parents=True, exist_ok=True)
    path = root / f"{digest}.html"
    if not path.exists():
        path.write_text(body, encoding="utf-8")
    manifest = {
        "source": source,
        "url": url,
        "first_seen_at": utc_now(),
        "sha256": digest,
        "path": str(path),
        "bytes": len(body.encode("utf-8")),
    }
    with (root / "manifest.jsonl").open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(manifest, ensure_ascii=False, sort_keys=True) + "\n")
    return manifest
