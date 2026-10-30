# SPC Control Charts (scaffold)

> **Status: scaffold.** Structure and interfaces are in place; the steps in the checklist below are still to do.

**Gap it closes:** Statistical Process Control (SPC) for improvement measurement, in the style of NHS
England's *Making Data Count*. Asked for by the Bristol NHS Quality Insight role and useful for any
operations or quality analytics job.

## Goal

Build XmR (individuals and moving range) charts for weekly quality metrics, apply the Making Data Count
rules to separate special-cause from common-cause variation, and produce a one-page summary that says
which metrics need action.

```mermaid
flowchart LR
    D[weekly metric series] --> L[XmR limits: mean ± 2.66 × mean moving range]
    L --> R[rules: outside limits, 7-point shift, 6-point trend, 2 of 3 near limit]
    R --> V[variation icon: improving / concerning / common cause]
    V --> C[charts + summary table]
```

## Checklist

- [ ] `spc/xmr.py`: centre line and process limits (implemented, see tests)
- [ ] `spc/rules.py`: the four Making Data Count special-cause rules
- [ ] Re-baselining: recalculate limits after a confirmed process change
- [ ] `spc/charts.py`: matplotlib XmR charts with special-cause points highlighted
- [ ] `spc/summary.py`: variation and assurance icons per metric (does the process reliably meet target?)
- [ ] Sample data: synthetic weekly patient-safety incidents, falls and complaint response times with a planted shift
- [ ] README: worked example interpreting one chart for a non-technical audience
