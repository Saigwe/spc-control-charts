"""Variation and assurance summary per metric, following Making Data Count's icon logic."""
from __future__ import annotations

from dataclasses import dataclass

from .rules import latest_signal_side
from .xmr import XmRLimits


@dataclass(frozen=True)
class MetricSummary:
    name: str
    latest: float
    mean: float
    lower: float
    upper: float
    variation: str   # common cause | special cause - improving | special cause - concerning
    assurance: str   # consistently passing | consistently failing | hit and miss | no target


def variation(values: list[float], limits: XmRLimits, higher_is_better: bool) -> str:
    side = latest_signal_side(values, limits)
    if side is None:
        return "common cause"
    good = (side == "high") == higher_is_better
    return "special cause - improving" if good else "special cause - concerning"


def assurance(limits: XmRLimits, target: float | None, higher_is_better: bool) -> str:
    """Can the process reliably meet the target? Compare the target with the process limits."""
    if target is None:
        return "no target"
    if higher_is_better:
        if limits.lower >= target:
            return "consistently passing"
        if limits.upper < target:
            return "consistently failing"
    else:
        if limits.upper <= target:
            return "consistently passing"
        if limits.lower > target:
            return "consistently failing"
    return "hit and miss"


def summarise(name, values, limits, higher_is_better, target=None) -> MetricSummary:
    return MetricSummary(name, values[-1], round(limits.mean, 2), round(limits.lower, 2), round(limits.upper, 2),
                         variation(values, limits, higher_is_better), assurance(limits, target, higher_is_better))
