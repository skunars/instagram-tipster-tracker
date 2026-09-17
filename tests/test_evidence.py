from src.evidence import sha256_text
from collector import extract_post_urls


def test_hash_is_stable():
    assert sha256_text("abc") == sha256_text("abc")


def test_extracts_post_and_reel_urls():
    html = 'x https://www.instagram.com/p/ABC123/ y https://www.instagram.com/reel/XYZ_9/'
    urls = extract_post_urls(html)
    assert urls == [
        "https://www.instagram.com/p/ABC123/",
        "https://www.instagram.com/reel/XYZ_9/",
    ]
