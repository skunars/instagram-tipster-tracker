# Instagram Tipster Tracker

A standalone research and paper-tracking system for monitoring the public predictions of the Instagram account `kahinmahrezz`.

## Purpose

The system does **not** place real bets. It records publicly observable tips, preserves first-seen timestamps, tracks outcomes, and measures whether claims such as consistently hitting 10+ selections can be supported by data.

## What we track

- source account
- post/reel identifier when available
- first-seen timestamp
- match/event
- market
- selection
- odds when available
- coupon/accumulator grouping
- outcome
- deleted/edited observation when detectable
- virtual paper P/L
- per-selection hit rate
- full-coupon hit rate
- coupon length and odds distribution

## Important limitation

Instagram does not provide a simple public historical API for arbitrary accounts. The collector is therefore designed around **observable public data** and immutable local records. It must never invent missing tips or outcomes.

## Repository isolation

This repository is intentionally separate from the other sports, crypto, and trading systems. No strategy, state file, Telegram namespace, or workflow from another repository is reused here.

## Status

Phase 1: data model + paper-tracking foundation.

Phase 2: public-source collection and evidence preservation.

Phase 3: outcome reconciliation and statistical reporting.

Phase 4: optional external runner/automation once the dataset proves useful.
