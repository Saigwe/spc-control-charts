"""Synthetic weekly quality metrics with planted signals."""
from __future__ import annotations

import random

WEEKS = 52


def generate(seed: int = 1) -> dict[str, dict]:
    rng = random.Random(seed)
    # Falls per 1,000 bed days: a falls-prevention programme starts in week 30 and lowers the level.
    falls = [round(rng.gauss(6.5 if w < 30 else 5.0, 0.6), 2) for w in range(WEEKS)]
    # Complaints answered within 25 working days (%): stable, common-cause variation around a target it misses.
    complaints = [round(min(100, rng.gauss(82, 4)), 1) for _ in range(WEEKS)]
    # Incidents awaiting review: a growing backlog from week 40.
    backlog = [round(rng.gauss(40, 4) + (max(0, w - 40) * 3), 1) for w in range(WEEKS)]
    return {
        "Falls per 1,000 bed days": {"values": falls, "higher_is_better": False, "target": 6.0, "baseline": 26},
        "Complaints answered within 25 days (%)": {"values": complaints, "higher_is_better": True,
                                                   "target": 85.0, "baseline": 26},
        "Incidents awaiting review": {"values": backlog, "higher_is_better": False, "target": None, "baseline": 26},
    }
