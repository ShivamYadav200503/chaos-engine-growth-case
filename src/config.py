"""
Central Configuration for Chaos Engine Growth Case.
Defines paths, exact dates, economic parameters, network constraints,
diminishing returns, and creative wear-out constants from the case brief and Appendix A.
"""

from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
PROC_DIR = BASE_DIR / "data" / "processed"
OUTPUTS_DIR = BASE_DIR / "outputs"
TABLES_DIR = OUTPUTS_DIR / "tables"
FIGS_DIR = OUTPUTS_DIR / "figures"
SUB_DIR = BASE_DIR / "submission"

# Backwards compatibility aliases
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = RAW_DIR
PROCESSED_DATA_DIR = PROC_DIR
FIGURES_DIR = FIGS_DIR
SUBMISSION_DIR = SUB_DIR

# Ensure key output directories exist
PROC_DIR.mkdir(parents=True, exist_ok=True)
TABLES_DIR.mkdir(parents=True, exist_ok=True)
FIGS_DIR.mkdir(parents=True, exist_ok=True)
SUB_DIR.mkdir(parents=True, exist_ok=True)

# Key Timeline Dates
AS_OF_DATE = "2025-09-30"  # All cohort data frozen as of this date; installs cover 2025-01-06 to 2025-09-28 (266 days)
HISTORICAL_START_DATE = "2025-01-06"
HISTORICAL_END_DATE = "2025-09-28"
TOTAL_HISTORICAL_DAYS = 266

# Baseline calculation window (4 full weeks = 28 days: Sep 1 to Sep 28, 2025; weekly baseline = Sep 1-28 sum / 4.0)
BASELINE_START = "2025-09-01"
BASELINE_END = "2025-09-28"
BASELINE_START_DATE = BASELINE_START
BASELINE_END_DATE = BASELINE_END
BASELINE_DAYS = 28
BASELINE_WEEKS = 4.0

# Quarter planning period (12 weeks: Mon 6 Oct - Sun 28 Dec 2025)
PLAN_START_DATE = "2025-10-06"
PLAN_END_DATE = "2025-12-28"
PLAN_WEEKS = 12
MAX_QUARTER_BUDGET = 250000.0
CFO_TARGET_D120_ROAS = 1.00

# Active Lines Game A (Mandatory networks that must keep running: >= 40% baseline spend over the quarter)
ACTIVE_LINES_GAME_A = [
    ("Net-A", "android"),
    ("Net-B", "android"),
    ("Net-B", "ios"),
    ("Net-C", "android"),
    ("Net-D", "android"),
]
MANDATORY_LINES = ACTIVE_LINES_GAME_A

# Spend limits and multipliers
MIN_LINE_MULTIPLIER = 0.40   # Each of the 5 lines must spend >= 40% of 12 * its baseline weekly spend
MAX_CELL_MULTIPLIER = 2.00   # Spending above double baseline weekly spend is not allowed
MIN_GAIN_MULTIPLIER = 0.50   # Below 0.5x weekly spend multiple, ROAS gain caps at 0.5^(-k)

MIN_SPEND_FACTOR = MIN_LINE_MULTIPLIER
MAX_SPEND_FACTOR = MAX_CELL_MULTIPLIER
BELOW_HALF_PLATEAU = MIN_GAIN_MULTIPLIER

# Diminishing returns exponents: ROAS(x) = baseline_ROAS * clip(x, 0.5, 2.0)**(-k)
# Assume 70% of the ROAS shift comes from CPI scaling (x**(0.7*k)) and 30% from LTV dilution (x**(-0.3*k))
K_EXPONENTS = {
    "Net-A": 0.35,
    "Net-B": 0.40,
    "Net-C": 0.45,
    "Net-D": 0.65,
}
DIMINISHING_RETURNS_K = K_EXPONENTS
CPI_SHARE_OF_ROAS_CHANGE = 0.70
LTV_SHARE_OF_ROAS_CHANGE = 0.30

# Holiday Season Window (4 weeks: Mon 24 Nov - Sun 21 Dec 2025)
# In these 4 weeks, installs cost +25% everywhere (CPI * 1.25, installs * 1/1.25 = 0.80), player LTV unchanged.
# With uniform weekly spend over 12 weeks:
# HOLIDAY_FACTOR = (8.0 / 12.0) * 1.0 + (4.0 / 12.0) * (1.0 / 1.25) = 11.2 / 12.0 = 0.9333333333333333
HOLIDAY_START_DATE = "2025-11-24"
HOLIDAY_END_DATE = "2025-12-21"
HOLIDAY_WEEKS = 4
HOLIDAY_CPI_INFLATION = 0.25
HOLIDAY_FACTOR = (8.0 / 12.0) * 1.0 + (4.0 / 12.0) * (1.0 / (1.0 + HOLIDAY_CPI_INFLATION))  # 11.2 / 12.0

# Creative fatigue rules (Appendix A)
# Existing creatives carry Weeks 1-2 (2025-10-06 to 2025-10-19).
# New creatives must carry Weeks 3-12 (10/12 of quarter impressions).
# CPI rises linearly per 1M impressions, retiring at +30% CPI.
EXISTING_CREATIVE_CARRY_WEEKS = 2
NEW_CREATIVE_WEEKS = 10
NEW_CREATIVE_FRACTION = NEW_CREATIVE_WEEKS / PLAN_WEEKS  # 10 / 12

CREATIVE_WEAROUT = {
    "Net-A": {
        "unit": "video_or_playable",
        "cpi_rise_per_million": 0.20,     # +20% per 1M impressions
        "max_impressions": 1_500_000,     # 0.30 / 0.20 * 1,000,000 = 1,500,000
        "shared_across_platforms": False,
    },
    "Net-B": {
        "unit": "ad_set",
        "cpi_rise_per_million": 3.00,     # +300% per 1M impressions
        "max_impressions": 100_000,       # 0.30 / 3.00 * 1,000,000 = 100,000
        "shared_across_platforms": True,  # One set serves both Android and iPhone
    },
    "Net-C": {
        "unit": "ad_pack",
        "cpi_rise_per_million": 3.00,     # +300% per 1M impressions
        "max_impressions": 100_000,       # 0.30 / 3.00 * 1,000,000 = 100,000
        "shared_across_platforms": False,
    },
    "Net-D": {
        "unit": "listing_image",
        "cpi_rise_per_million": 1.50,     # +150% per 1M impressions
        "max_impressions": 200_000,       # 0.30 / 1.50 * 1,000,000 = 200,000
        "shared_across_platforms": False,
    },
}

# Standard evaluation horizons
COHORT_HORIZONS = [0, 1, 3, 7, 14, 30, 60, 90, 120, 180]
RETENTION_HORIZONS = [1, 3, 7, 14, 30, 60, 90, 120]
