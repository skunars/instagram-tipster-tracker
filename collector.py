from __future__ import annotations

import argparse
import re
from pathlib import Path

import requests

from src.evidence import save_snapshot

PROFILE = "https://www.instagram.com/kahinmahrezz/"
USER_AGENT = "Mozilla/5.0 (compatible; InstagramTipsterTracker/0.1; +https://github.com/skunars/instagram-tipster-tracker)"


def fetch_profile(url: str = PROFILE, timeout: int = 30) -> str:
    response = requests.get(
        url,
        headers={"User-Agent": USER_AGENT, "Accept-Language": "tr-TR,tr;q=0.9,en;q=0.8"},
        timeout=timeout,
        allow_redirects=True,
    )
    response.raise_for_status()
    return response.text


def extract_post_urls(html: str) -> list[str]:
    urls = re.findall(r"https://www\\.instagram\\.com/(?:p|reel)/[A-Za-z0-9_-]+/?", html)
    return sorted(set(urls))


def collect(url: str = PROFILE) -> dict:
    html = fetch_profile(url)
    manifest = save_snapshot("instagram", url, html)
    posts = extract_post_urls(html)
    return {"snapshot": manifest, "post_urls": posts, "post_count": len(posts)}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default=PROFILE)
    args = parser.parse_args()
    result = collect(args.url)
    print(f"snapshot={result['snapshot']['sha256']} posts_visible={result['post_count']}")
