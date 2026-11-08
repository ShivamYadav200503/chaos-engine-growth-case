# AI Usage Reflection & Log

**Case:** Chaos Engine Labs Growth Case — Games A & B  
**Author:** Head of Growth / Growth Lead  
**As of Date:** September 30, 2025  

---

## 1. Two Moments When AI Tools Gave Misleading or Erroneous Output

### Mistake 1 Caught: Censored-Median Contamination & Single-Day `payers_dN` Window in Data Cleaning
- **The AI Error:** An initial AI code generation pass attempted to clean the July 14–16 ad mediation glitch by computing baseline ad-revenue increment rates across non-overlapping cohorts without filtering for cohort maturity (`age_days >= h`). Because immature cohorts hold frozen cumulative revenue (`incremental_rev == 0.0`), the median normal rate collapsed to exactly `0.0` at horizons $d60$, $d90$, $d120$, and $d180$. This wiped out 99% of legitimate late-tail ad revenue for valid mature cohorts (e.g., Game B Q1 cohorts whose $d120\to d180$ window overlapped mid-July). Simultaneously, the AI script divided multi-day IAP increments ($d7\to d14$ spans 7 days, $d14\to d30$ spans 16 days) by the single-day active payer count `payers_d{h}` (which records only transactions on that exact 24-hour day), falsely flagging 142 legitimate US repeat-purchase cohorts on `Net-B` and `Net-D` as corrupted anomalies.
- **How We Caught It:** We cross-reconciled cleaned cohort revenue totals against `telemetry_daily.csv` mediation totals ($299,079 ad rev in Game A) and audited row-level player spending on high-value US lines.
- **The Deterministic Fix:** We enforced `age_days >= h` on baseline cohort rate calculations, switched to an install-weighted normal rate, and restricted IAP anomaly cleaning strictly to confirmed `.xx00` SKU multiples (e.g., $469.43, $938.86) exceeding $150 with zero or near-zero window payers.

### Mistake 2 Caught: Unconditioned Partial-Age Predictions on P7/P8 & Simpson's Paradox on Net-A Non-US
- **The AI Error:** The first LTV modeling pass masked partial $d60$ revenue for August 4–17 cohorts (ages 44–57 days on September 30), predicting Day-60 ROAS of `0.9228` for `P7` and `0.7409` for `P8`. However, by September 30, those cohorts had *already banked* `0.9306` (`P7`) and `0.7734` (`P8`) in realized cash—making the AI predictions lower than money already in the bank. Simultaneously, when projecting `Net-A Non-US` (P2), the AI divided all-time historical Jan–Jun LTV ($1.15, dominated by expensive Tier-1 test countries) by September's lower blended CPI ($0.65, dominated by emerging markets), creating a Simpson's Paradox denominator mismatch that artificially inflated projected ROAS to `1.78x`. Furthermore, it bootstrapped parameter means rather than residual quantiles, yielding an uncalibrated 27.5% CI coverage.
- **How We Caught It:** We ran monotonicity assertions ($\text{Observed Prev} < \text{Banked Sep 30} < \text{low\_80} < \text{prediction} < \text{high\_80}$) and held-out historical cohort coverage backtests.
- **The Deterministic Fix:** We reformulated `P1–P8` to condition directly on realized revenue banked as of September 30, projecting only unelapsed tail days via power-law elapsed fractions ($f_{\text{elapsed}}(a_i) = \frac{\sqrt{a_i} - \sqrt{\text{prev}}}{\sqrt{\text{target}} - \sqrt{\text{prev}}}$). We projected ROAS directly in consistent cohort-spend space, recovering consistent baseline LTV ($\text{Baseline CPI} \times \text{Pred ROAS}$), and calibrated conformal residual intervals achieving honest ~79% empirical coverage.

---

## 2. Where AI Saved Significant Time
- **Vectorized Forensic Audit Across 166,000+ Records:** Rapidly querying, joining, and reconciling 8 distinct anomaly classes across 12 raw CSV tables, verifying that $392,075.67 in Game A spend and $669,975.34 in Game B spend reconciled to 100.00% precision.
- **Hierarchical Dual-Stream Survival Modeling Across 62 Cells:** Accelerating the formulation and numerical optimization of decoupled power-law retention ($S(t) = (1 + \beta t)^{-\gamma}$) and shifted lognormal IAP monetization curves with empirical Bayes pooling across 32 individual countries and 4 regional tiers.
- **Constrained Non-Linear KKT Spend Optimization:** Formulating and solving the 40-cell non-linear constrained optimization across the entire CFO-vs-CEO Pareto frontier ($75k to $350k spend) in seconds.

---

## 3. Short List of What Was Intentionally Skipped and Why
- **User-Level Deep Learning / Neural Network LTV Models:** Raw data is cohort-aggregated rather than user-event-level. Deep learning architectures on small-sample cohort tables overfit and introduce black-box opacity; parametric survival curves combined with Empirical Bayes shrinkage provide full statistical transparency, exact monotonicity guarantees, and verifiable credible intervals.
- **Individual Country Budget Optimization for Micro-Territories (<$10/wk Spend):** Net-A contains over 80 long-tail countries spending <$10/week with volatile 1–5 install sample sizes. Rather than attempting noisy individual parameter optimization, we aggregated these countries into 4 economically homogeneous regional tiers (`Tier 1 Affluent West`, `Tier 2 East Asia & GCC`, `Tier 3 LatAm & East Europe`, `Tier 4 Emerging RoW`), preserving statistical power while fulfilling the case requirement to document constituent country codes.
