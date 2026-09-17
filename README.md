# Instagram Tipster Tracker

A standalone research and paper-tracking system for monitoring the public predictions of the Instagram account `kahinmahrezz`.

## What it does

- polls the public profile on a 15-minute schedule
- preserves first-seen observations with SHA-256 fingerprints
- extracts observed post/reel/TV URLs without assuming missing data
- fetches observed post pages and preserves public title/description/image metadata
- keeps original observations immutable; later outcomes are written as separate settlement records
- supports deterministic tip IDs and duplicate protection
- supports virtual 1,000 TL bankroll tracking with 100 TL per-selection paper stake
- reports selection hit rate, full-coupon hit rate, coupon counts, market distribution and virtual P/L
- runs isolated tests on every push/PR

## Outcome tracking

A tip is never rewritten after publication. When a result becomes observable, `settle.py` appends a separate settlement event:

```text
python settle.py TIP_ID WON --evidence-url "https://..." --note "verified final score"
```

Allowed outcomes are `WON`, `LOST`, and `VOID`. The report uses the latest settlement event for each tip ID.

## Data files

- `data/observations.jsonl` — immutable profile observations
- `data/posts.jsonl` — immutable public post-page observations
- `data/tips.jsonl` — structured tips when they can be extracted without guessing
- `data/settlements.jsonl` — separate outcome/evidence events
- `data/latest_report.json` — latest calculated paper statistics
- `data/snapshots/` — optional local raw HTML snapshots when the collector is run directly

## Important limitation

Instagram does not provide a simple public historical API for arbitrary accounts, and some content may be rendered dynamically or exist only inside an image/video. The collector therefore records only what is publicly observable. It must never invent a match, market, odds, publication time, or result. Image/video-only tips remain unclassified until reliable evidence is available.

## Repository isolation

This repository is intentionally separate from the other sports, crypto, and trading systems. No strategy, state file, Telegram namespace, or workflow from another repository is reused here.

## Status

**Foundation complete and ready for data collection.** The remaining work is data accumulation: observe enough real posts and verified outcomes to measure whether the account's claimed performance is supported by evidence. This is a research/paper-tracking system, not a real-money betting system.
