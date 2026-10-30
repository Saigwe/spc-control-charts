"""Build XmR charts and a one-page summary: python -m spc.report"""
from __future__ import annotations

from pathlib import Path

from .charts import xmr_chart
from .sample_data import generate
from .summary import summarise
from .xmr import baseline_limits

ROOT = Path(__file__).resolve().parent.parent


def slug(name: str) -> str:
    return "".join(c if c.isalnum() else "_" for c in name.lower()).strip("_")


def run(out_dir: Path = ROOT / "output") -> list:
    rows, sections = [], []
    for name, m in generate().items():
        limits = baseline_limits(m["values"], m["baseline"])
        s = summarise(name, m["values"], limits, m["higher_is_better"], m["target"])
        chart = xmr_chart(name, m["values"], limits, out_dir / f"{slug(name)}.png", m["target"], m["baseline"])
        rows.append(s)
        sections.append(f"### {name}\n\n![{name}]({chart.name})\n")
    table = ["| Metric | Latest | Mean | Lower limit | Upper limit | Variation | Assurance |",
             "|---|---|---|---|---|---|---|"]
    table += [f"| {r.name} | {r.latest} | {r.mean} | {r.lower} | {r.upper} | {r.variation} | {r.assurance} |"
              for r in rows]
    report = ("# Quality metrics: SPC summary\n\nLimits are calculated from the first 26 weeks (baseline) and "
              "projected forward, so later changes show up as special cause.\n\n" + "\n".join(table) + "\n\n"
              + "\n".join(sections))
    (out_dir / "report.md").write_text(report, encoding="utf-8")
    return rows


if __name__ == "__main__":
    for r in run():
        print(f"{r.name}: {r.variation}; {r.assurance}")
