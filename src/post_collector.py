from __future__ import annotations

import hashlib
import html
import json
import re
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

from src.storage import JsonlStore

POSTS = Path("data/posts.jsonl")
META_RE = re.compile(r'<meta[^>]+(?:property|name)=["\']([^"\']+)["\'][^>]+content=["\']([^"\']*)["\'][^>]*>', re.I)


@dataclass(frozen=True)
class PostObservation:
    post_url: str
    first_seen_at: str
    content_sha256: str
    title: str | None
    description: str | None
    image_url: str | None

    def to_dict(self) -> dict:
        return asdict(self)


def fetch_post(url: str, timeout: int = 20) -> bytes:
    request = Request(url, headers={
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/128 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    })
    with urlopen(request, timeout=timeout) as response:
        return response.read()


def _meta(html_text: str, names: set[str]) -> str | None:
    for key, value in META_RE.findall(html_text):
        if key.lower() in names:
            return html.unescape(value)
    return None


def parse_post(html_bytes: bytes, url: str) -> PostObservation:
    digest = hashlib.sha256(html_bytes).hexdigest()
    text = html_bytes.decode("utf-8", errors="ignore")
    return PostObservation(
        post_url=url,
        first_seen_at=datetime.now(timezone.utc).isoformat(),
        content_sha256=digest,
        title=_meta(text, {"og:title", "twitter:title"}),
        description=_meta(text, {"og:description", "twitter:description", "description"}),
        image_url=_meta(text, {"og:image", "twitter:image"}),
    )


def record_post(observation: PostObservation) -> bool:
    store = JsonlStore(POSTS)
    existing = {row.get("content_sha256") for row in store.read_all()}
    if observation.content_sha256 in existing:
        return False
    store.append(observation.to_dict())
    return True
