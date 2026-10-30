"""XmR chart rendering with special-cause points highlighted."""
from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from .rules import special_causes  # noqa: E402
from .xmr import XmRLimits  # noqa: E402


def xmr_chart(name: str, values: list[float], limits: XmRLimits, out: Path, target: float | None = None,
              baseline_points: int | None = None) -> Path:
    x = list(range(1, len(values) + 1))
    flagged = special_causes(values, limits)
    fig, ax = plt.subplots(figsize=(9, 3.6))
    ax.plot(x, values, color="#5B6770", marker="o", ms=3.5, lw=1.2, zorder=2)
    ax.scatter([i + 1 for i in flagged], [values[i] for i in flagged], color="#E46C0A", s=28, zorder=3,
               label="Special cause")
    ax.axhline(limits.mean, color="#1F3A5F", lw=1.2, label=f"Mean {limits.mean:.1f}")
    for y in (limits.lower, limits.upper):
        ax.axhline(y, color="#1F3A5F", lw=1, ls="--")
    if target is not None:
        ax.axhline(target, color="#C00000", lw=1, ls=":", label=f"Target {target:g}")
    if baseline_points:
        ax.axvspan(0.5, baseline_points + 0.5, color="#1F3A5F", alpha=0.05, label="Baseline")
    ax.set_title(name)
    ax.set_xlabel("Week")
    ax.legend(loc="upper left", fontsize=8, ncol=4, frameon=False)
    fig.tight_layout()
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=120)
    plt.close(fig)
    return out
