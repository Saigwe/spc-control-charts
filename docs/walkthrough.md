# 3-minute walkthrough: SPC Control Charts

A timed script for a Loom recording of about 3 minutes (screen plus camera bubble, 1080p). Say it in your own words; the lines are a guide, not a teleprompter.

**Open these tabs before you press record:** README, `output/falls_per_1_000_bed_days.png`, `spc/xmr.py`, `spc/rules.py`, `spc/summary.py`, `output/report.md`, `tests/test_rules.py`, GitHub Actions.

| Time | On screen | What to say |
|---|---|---|
| 0:00–0:20 | Portfolio card, then the README title | Hospitals react to every up and down in a metric, and most of it is noise. This applies NHS England's Making Data Count method to say what has really changed. |
| 0:20–0:40 | README intro and the falls chart | The weekly series are sample data with signals planted. It's a skills demonstration for quality-improvement roles; the closest work on my CV is the PDCA balanced scorecard I designed at Ikeja Electric. |
| 0:40–1:05 | `spc/xmr.py` | XmR charts: limits are the mean plus or minus 2.66 times the mean moving range, calculated on a 26-week baseline and projected forward, so later changes show as special cause instead of being absorbed. |
| 1:05–1:35 | `spc/rules.py` | Four special-cause rules: a point outside the limits, seven in a row on one side, six steadily rising or falling, and two of three beyond two sigma. |
| 1:35–2:05 | `spc/summary.py` and the results table | Each metric gets two verdicts. Variation: did something change, and is it good or bad? Assurance: can the process reliably hit its target? |
| 2:05–2:30 | `output/report.md` | Falls improved after the programme started but still miss target at random. Complaints show only common cause, so hitting 85% is luck and the process needs redesign. The review backlog has been growing since week 40. |
| 2:30–2:45 | `tests/test_rules.py` and GitHub Actions | 9 tests cover each rule's edge cases, six against seven points and five against six, metric direction, the assurance logic and the planted signals end to end. |
| 2:45–3:00 | Back to the README top | For a board, that's fewer reactions to noise and action where the data says it's needed. Links are under the video. |

## Recording checklist
- Close email, chat and notifications. Zoom the browser to 125% so code is readable.
- Run `python -m spc.report` once so the charts and report are fresh.
- Keep to one take per section; Loom lets you trim. Aim for 2:45 to 3:10.
- Show real numbers on screen as you say them; never estimate on camera.
- Say "synthetic" out loud when you introduce the data. This is a skills demonstration, not a rebuild of client work.

## After recording
1. Copy the Loom share link.
2. In `README.md`, replace the walkthrough line with `- [x] [3-minute Loom walkthrough](<your Loom link>)` and add the link under the title.
3. Add the link to this project's card on saigwe.github.io.
