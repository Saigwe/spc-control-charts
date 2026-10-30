"""XmR chart limits."""
from dataclasses import dataclass


@dataclass(frozen=True)
class XmRLimits:
    mean: float
    lower: float
    upper: float
    mean_moving_range: float

    @property
    def sigma(self) -> float:
        """Estimated process sigma: one third of the distance from mean to a limit."""
        return (self.upper - self.mean) / 3


def xmr_limits(values: list[float]) -> XmRLimits:
    """Process limits are mean ± 2.66 × the mean moving range."""
    if len(values) < 2:
        raise ValueError("Need at least two points")
    mean = sum(values) / len(values)
    moving_ranges = [abs(b - a) for a, b in zip(values, values[1:])]
    mr_bar = sum(moving_ranges) / len(moving_ranges)
    return XmRLimits(mean, mean - 2.66 * mr_bar, mean + 2.66 * mr_bar, mr_bar)


def baseline_limits(values: list[float], baseline_points: int | None = None) -> XmRLimits:
    """Limits from the first `baseline_points` values (Making Data Count recommends at least 15-20)."""
    return xmr_limits(values[:baseline_points] if baseline_points else values)
