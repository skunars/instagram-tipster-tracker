from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class ParsedTip:
    event: str
    market: str
    selection: str
    odds: Optional[float]


ODDS_RE = re.compile(r"(?<!\d)(\d{1,3}(?:[.,]\d{1,2})?)(?!\d)")


def parse_odds(text: str) -> Optional[float]:
    values = []
    for match in ODDS_RE.finditer(text):
        value = match.group(1).replace(",", ".")
        try:
            number = float(value)
        except ValueError:
            continue
        if 1.01 <= number <= 1000:
            values.append(number)
    return values[-1] if values else None


def parse_prediction_line(line: str) -> Optional[ParsedTip]:
    clean = " ".join(line.split())
    if not clean:
        return None

    # We deliberately avoid guessing teams/markets from arbitrary prose.
    # A later source-specific parser can add structured rules once real samples exist.
    separators = (" - ", " – ", " — ", ": ", "|", " → ")
    for separator in separators:
        if separator in clean:
            left, right = clean.split(separator, 1)
            odds = parse_odds(right)
            return ParsedTip(event=left.strip(), market="UNCLASSIFIED", selection=right.strip(), odds=odds)
    return None
