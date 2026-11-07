# Chaos Engine Growth Case: Games A & B

Growth and User Acquisition analytics, econometric LTV modeling, constrained portfolio spend optimization, and creative fatigue scheduling for mobile casual games.

---

## Repository Structure

```text
chaos-engine-growth-case/
├── README.md                        # Exact 1-command reproduction instructions & environment setup
├── requirements.txt                 # Locked Python dependencies (pandas, numpy, scipy, statsmodels, matplotlib)
├── .gitignore                       # Ignores __pycache__, .DS_Store, .venv, and temporary build artifacts
├── run_all.py                       # Master orchestrator script: runs scripts 01 -> 05 in sequence
│
├── data/
│   ├── raw/                         # Unmodified original files from Growth_Assignment_Pack.zip
│   │   ├── GameA_ua_daily.csv
│   │   ├── GameA_cohorts.csv
│   │   ├── GameA_telemetry_daily.csv
│   │   ├── GameA_telemetry_retention.csv
│   │   ├── GameA_creatives_daily.csv
│   │   ├── GameA_creatives_catalog.csv
│   │   ├── GameB_ua_daily.csv
│   │   ├── GameB_cohorts.csv
│   │   ├── GameB_telemetry_daily.csv
│   │   ├── GameB_telemetry_retention.csv
│   │   ├── GameB_creatives_daily.csv
│   │   ├── GameB_creatives_catalog.csv
│   │   ├── Template_predictions.csv
│   │   └── Template_plan.csv
│   └── processed/                   # Cleaned, right-censor-masked, and anomaly-adjusted intermediate parquets/CSVs
│
├── src/
│   ├── __init__.py
│   ├── config.py                    # Central constants: AS_OF_DATE='2025-09-30', k-exponents, holiday window, paths
│   ├── 01_data_audit_cleaning.py    # Q1 Part A: Detects & fixes data bugs; outputs audit logs & cleaned data
│   ├── 02_ltv_roas_modeling.py      # Q1 Part B: Dual-stream (Ad + IAP) survival/EB LTV model, 4-way transfer, P1-P8
│   ├── 03_spend_optimizer_q2.py     # Q2: Organic uplift econometrics + constrained non-linear spend optimizer
│   ├── 04_creative_wearout_q3.py    # Q3: Creative IPM vs. LTV decomposition + fatigue & replenishment schedule
│   └── 05_generate_tables_figs.py   # Exports all publication-ready tables and figures for Memo & Appendix
│
├── outputs/
│   ├── tables/                      # Generated CSV/Markdown tables for Appendix (data bugs, cell values, 4-way transfer)
│   └── figures/                     # High-DPI plots (LTV curves, CFO-vs-CEO Pareto frontier, creative fatigue)
│
└── submission/                      # Final hand-in folder (everything that gets zipped for the email reply)
    ├── memo.pdf                     # Deliverable 1: <= 2-page Executive Memo (starts with the 5 mandatory CFO lines)
    ├── appendix.pdf                 # Deliverable 2: <= 12-page Technical Appendix (Questions 1–3 supporting tables)
    ├── predictions.csv              # Deliverable 3: Filled-in Template_predictions.csv (P1–P8 with 80% intervals)
    ├── plan.csv                     # Deliverable 4: Filled-in Template_plan.csv (Game A 12-week budget plan)
    └── ai_log/                      # Deliverable 6: AI Usage Log + full exported chat transcripts
        ├── ai_usage_log.pdf         # Half-page reflection (2 AI mistakes caught, 1 time-saver, what was skipped)
        └── transcripts/             # Full exported AI chat transcripts / HTML / Markdown logs
```

---

## Reproduction Instructions

### 1. Environment Setup

Python 3.10+ is recommended. Install required packages:

```bash
pip install -r requirements.txt
```

### 2. Run Complete Pipeline

Run the master orchestrator to reproduce the entire end-to-end pipeline (data audit, LTV models, spend optimizer, creative schedule, and all output tables & charts):

```bash
python run_all.py
```

