"""XmR chart limits."""
from dataclasses import dataclass


@dataclass(frozen=True)
class XmRLimits:
    mean: float
    lower: float
    upper: float
    mean_moving_range: float


def xmr_limits(values: list[float]) -> XmRLimits:
    """Process limits are mean ± 2.66 × the mean moving range."""
    if len(values) < 2:
        raise ValueError("Need at least two points")
    mean = sum(values) / len(values)
    moving_ranges = [abs(b - a) for a, b in zip(values, values[1:])]
    mr_bar = sum(moving_ranges) / len(moving_ranges)
    return XmRLimits(mean, mean - 2.66 * mr_bar, mean + 2.66 * mr_bar, mr_bar)
