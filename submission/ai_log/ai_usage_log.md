# AI Usage Reflection & Log

## 1. Two Moments When AI Tools Gave Misleading or Erroneous Output
1. **Right-Censored Cohort Day-120/180 Values**: AI initially treated unobserved revenue cells in recent cohorts as 0 rather than right-censored nulls, which would have artificially depressed recent ROAS and distorted baseline projections. Replaced with strict right-censor date masking (`install_date + day_n <= 2025-09-30`).
2. **CPI Diminishing Returns Formula Application**: AI initially inverted the diminishing returns exponent when scaling spend, applying cost reduction to increased spend instead of cost inflation. Caught via unit sanity checks on marginal ROAS vs. average ROAS.

## 2. One Moment When AI Really Saved Time
- **Vectorized Dual-Stream LTV Parameter Fitting**: Rapidly implementing and tuning non-linear curve fits across hundreds of network-platform-country slices, generating robust empirical confidence intervals.

## 3. Short List of What Was Skipped and Why
- Granular sub-campaign level modeling where data volume was below statistical significance (<50 installs), aggregating to network × platform × country tiers instead to preserve statistical power.

