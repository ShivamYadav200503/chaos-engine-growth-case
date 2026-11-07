"""
Central Configuration for Chaos Engine Growth Case.
Defines paths, dates, economic parameters, network constraints, and model constants.
"""

from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

OUTPUTS_DIR = BASE_DIR / "outputs"
TABLES_DIR = OUTPUTS_DIR / "tables"
FIGURES_DIR = OUTPUTS_DIR / "figures"
SUBMISSION_DIR = BASE_DIR / "submission"

# Key Timeline Dates
AS_OF_DATE = "2025-09-30"
HISTORICAL_START_DATE = "2025-01-06"
HISTORICAL_END_DATE = "2025-09-28"

# Baseline calculation window (4 full weeks 1-28 Sept 2025)
BASELINE_START_DATE = "2025-09-01"
BASELINE_END_DATE = "2025-09-28"

# Quarter planning period (12 weeks: Mon 6 Oct - Sun 28 Dec 2025)
PLAN_START_DATE = "2025-10-06"
PLAN_END_DATE = "2025-12-28"
PLAN_WEEKS = 12
MAX_QUARTER_BUDGET = 250000.0

# Holiday Season Window (4 weeks: 24 Nov - 21 Dec 2025)
HOLIDAY_START_DATE = "2025-11-24"
HOLIDAY_END_DATE = "2025-12-21"
HOLIDAY_WEEKS = 4
HOLIDAY_CPI_INFLATION = 0.25  # Installs cost 25% more

# Diminishing Returns Exponents (ROAS multiplier = x^(-k))
# ROAS change: x=2 -> x^(-k), x=0.5 -> x^(-k)
DIMINISHING_RETURNS_K = {
    "Net-A": 0.35,
    "Net-B": 0.40,
    "Net-C": 0.45,
    "Net-D": 0.65,
}

# Spend limits
MIN_SPEND_FACTOR = 0.40  # >= 40% of baseline
MAX_SPEND_FACTOR = 2.00  # <= 200% of baseline (above double not allowed)
BELOW_HALF_PLATEAU = 0.50  # Below 0.5x, no further ROAS gain
CPI_SHARE_OF_ROAS_CHANGE = 0.70  # ~70% of ROAS change comes from CPI increase

# Creative Wear-out Rules (Appendix A)
CREATIVE_WEAROUT = {
    "Net-A": {
        "unit": "video_or_playable",
        "cpi_rise_per_million": 0.20,
        "max_impressions": 1_500_000,
    },
    "Net-B": {
        "unit": "ad_set",
        "cpi_rise_per_million": 3.00,
        "max_impressions": 100_000,
    },
    "Net-C": {
        "unit": "ad_pack",
        "cpi_rise_per_million": 3.00,
        "max_impressions": 100_000,
    },
    "Net-D": {
        "unit": "listing_image",
        "cpi_rise_per_million": 1.50,
        "max_impressions": 200_000,
    },
}

EXISTING_CREATIVE_CARRY_WEEKS = 2  # Current creatives carry first 2 weeks

# Mandatory networks that must keep running (>= 40% baseline spend)
MANDATORY_LINES = [
    ("Net-A", "android"),
    ("Net-B", "android"),
    ("Net-B", "ios"),
    ("Net-C", "android"),
    ("Net-D", "android"),
]

