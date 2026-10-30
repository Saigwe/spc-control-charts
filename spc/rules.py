"""Making Data Count special-cause rules.

Each rule returns the set of point indices it flags, with the side ("high" or "low") the signal sits on.
"""
from __future__ import annotations

from .xmr import XmRLimits

SHIFT_RUN = 7   # consecutive points on one side of the mean
TREND_RUN = 6   # consecutive points all increasing or all decreasing


def outside_limits(values: list[float], limits: XmRLimits) -> dict[int, str]:
    return {i: ("high" if v > limits.upper else "low")
            for i, v in enumerate(values) if v > limits.upper or v < limits.lower}


def shift(values: list[float], limits: XmRLimits, run: int = SHIFT_RUN) -> dict[int, str]:
    flags: dict[int, str] = {}
    start = 0
    for i in range(1, len(values) + 1):
        same_side = i < len(values) and _side(values[i], limits) == _side(values[start], limits) != "on"
        if not same_side:
            if i - start >= run and _side(values[start], limits) != "on":
                flags.update({j: _side(values[start], limits) for j in range(start, i)})
            start = i
    return flags


def trend(values: list[float], run: int = TREND_RUN) -> dict[int, str]:
    flags: dict[int, str] = {}
    for direction, side in ((1, "high"), (-1, "low")):
        start = 0
        for i in range(1, len(values) + 1):
            continues = i < len(values) and (values[i] - values[i - 1]) * direction > 0
            if not continues:
                if i - start >= run:
                    flags.update({j: side for j in range(start, i)})
                start = i
    return flags


def two_of_three_near_limit(values: list[float], limits: XmRLimits) -> dict[int, str]:
    """Two of three consecutive points beyond 2 sigma on the same side."""
    hi, lo = limits.mean + 2 * limits.sigma, limits.mean - 2 * limits.sigma
    flags: dict[int, str] = {}
    for i in range(len(values) - 2):
        window = range(i, i + 3)
        for side, test in (("high", lambda v: v > hi), ("low", lambda v: v < lo)):
            hits = [j for j in window if test(values[j])]
            if len(hits) >= 2:
                flags.update({j: side for j in hits})
    return flags


def special_causes(values: list[float], limits: XmRLimits) -> dict[int, set[str]]:
    """Map point index -> names of rules that flag it. Directions are available from the individual rules."""
    result: dict[int, set[str]] = {}
    for name, flags in (
        ("outside_limits", outside_limits(values, limits)),
        ("shift", shift(values, limits)),
        ("trend", trend(values)),
        ("two_of_three", two_of_three_near_limit(values, limits)),
    ):
        for i in flags:
            result.setdefault(i, set()).add(name)
    return result


def latest_signal_side(values: list[float], limits: XmRLimits, lookback: int = 6) -> str | None:
    """Side ("high"/"low") of any special cause in the last `lookback` points, preferring the latest."""
    sides: dict[int, str] = {}
    for flags in (outside_limits(values, limits), shift(values, limits), trend(values),
                  two_of_three_near_limit(values, limits)):
        sides.update(flags)
    recent = [i for i in sides if i >= len(values) - lookback]
    return sides[max(recent)] if recent else None


def _side(value: float, limits: XmRLimits) -> str:
    if value > limits.mean:
        return "high"
    if value < limits.mean:
        return "low"
    return "on"
