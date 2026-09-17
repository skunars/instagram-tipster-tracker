from __future__ import annotations

import hashlib
import json
import re
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

SOURCE = "kahinmahrezz"
PROFILE_URL = f"https://www.instagram.com/{SOURCE}/"
SNAPSHOT_DIR = Path("data/snapshots")
OBSERVATION_FILE = Path("data/observations.jsonl")
POST_RE = re.compile(r"/(p|reel|tv)/([A-Za-z0-9_-]+)/")


@dataclass(frozen=True)
class Snapshot:
    source: str
    url: str
    first_seen_at: str
    sha256: str
    byte_length: int
    post_urls: tuple[str, ...]

    def to_dict(self) -> dict:
        return asdict(self)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def fetch_public_profile(url: str = PROFILE_URL, timeout: int = 20) -> bytes:
    request = Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/128 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
        },
    )
    with urlopen(request, timeout=timeout) as response:
        return response.read()


def extract_post_urls(html: bytes) -> tuple[str, ...]:
    text = html.decode("utf-8", errors="ignore")
    urls = {f"https://www.instagram.com/{kind}/{post_id}/" for kind, post_id in POST_RE.findall(text)}
    return tuple(sorted(urls))


def save_snapshot(html: bytes, url: str = PROFILE_URL, persist_raw: bool = True) -> Snapshot:
    digest = hashlib.sha256(html).hexdigest()
    snapshot = Snapshot(
        source=SOURCE,
        url=url,
        first_seen_at=utc_now(),
        sha256=digest,
        byte_length=len(html),
        post_urls=extract_post_urls(html),
    )
    if persist_raw:
        SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
        (SNAPSHOT_DIR / f"{digest}.html").write_bytes(html)
        (SNAPSHOT_DIR / f"{digest}.json").write_text(
            json.dumps(snapshot.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8"
        )
    return snapshot


def append_observation(snapshot: Snapshot) -> bool:
    OBSERVATION_FILE.parent.mkdir(parents=True, exist_ok=True)
    existing = set()
    if OBSERVATION_FILE.exists():
        for line in OBSERVATION_FILE.read_text(encoding="utf-8").splitlines():
            if line.strip():
                existing.add(json.loads(line).get("sha256"))
    if snapshot.sha256 in existing:
        return False
    with OBSERVATION_FILE.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(snapshot.to_dict(), ensure_ascii=False, sort_keys=True) + "\n")
    return True


if __name__ == "__main__":
    html = fetch_public_profile()
    snapshot = save_snapshot(html, persist_raw=True)
    print(json.dumps(snapshot.to_dict(), ensure_ascii=False, indent=2))
