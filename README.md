# NBA Game Performance Analytics | 2022–23 Team Insights

## Executive Summary
Front offices and analysts need fast, reproducible views of what drives wins.  
This project ingests 2022–23 NBA game data, engineers pace-adjusted ratings (ORtg/DRtg), applies simple strength-of-schedule (SoS) adjustments, and correlates key metrics with win rate to surface actionable takeaways.

---

## Business Problem
Teams commonly evaluate by raw points per game, which can be misleading without pace and opponent context. Decision-makers need:
- Pace-adjusted offensive/defensive efficiency
- Opponent (SoS) context
- Clear links between metrics and win %

---

## Methodology
- **Data Source:** `nba_api` (official NBA stats endpoints via community library)
- **Ingest:** Team game logs for the 2022–23 season
- **Transform:** Possessions estimate (pace), ORtg/DRtg, SoS (avg opponent win%), net rating
- **Analyze:** Correlations (win% vs. ORtg/DRtg/NetRtg/TO%), top/bottom quintiles
- **Visualize:** Ranked bar charts and scatter plots saved to `/outputs/figures/`

---

## Skills
- Python (pandas, numpy, matplotlib), API ingestion (`nba_api`)
- Feature engineering (pace, ratings), correlation analysis
- Reproducible CLI workflow & basic testing

---

## Results & Business Recommendation
- **ORtg and DRtg are the clearest win-rate drivers** (expected: efficiency > raw PPG).  
- **Turnovers and defensive rebounds** appear frequently among top contributors—prioritize **ball security** and **defensive glass** to convert close games.  
- Teams with **top-quartile NetRtg** and **median turnover rates** left wins on the table—target late-game TO reduction.

> Notes: Ratings are regular-season only; model-free correlations shown. Extend with play-by-play for deeper situational analysis.

---

## How to Run
```bash
# 1) Setup
python -m venv .venv && . .venv/Scripts/activate   # on Windows
pip install -r requirements.txt

# 2) Run end-to-end (defaults to 2022-23)
python src/run_analysis.py --season "2022-23"

# 3) Outputs
# - ./data/raw/*.json
# - ./data/processed/team_metrics.parquet
# - ./outputs/figures/*.png
```
> macOS/Linux activation: `source .venv/bin/activate`

---

## Project Structure
```
NBA-Game-Performance-Analytics/
├─ README.md
├─ requirements.txt
├─ .gitignore
├─ src/
│  ├─ ingest.py
│  ├─ transform.py
│  ├─ analyze.py
│  └─ run_analysis.py
├─ tests/
│  └─ test_transform.py
├─ data/               # (gitignored)
│  ├─ raw/
│  └─ processed/
└─ outputs/
   └─ figures/
```

---

## Next Steps
- Add opponent-adjusted **Four Factors** breakdown by quarter/clutch time
- Ship a **Streamlit** mini-app for “team picker → keys to win”
- Add unit tests for possession calc and join keys

## About
Analyzing NBA team performance for 2022–23 using pace-adjusted ratings and simple SoS context; reproducible, CLI-first workflow.
