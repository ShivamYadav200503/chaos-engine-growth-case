# Technical Appendix: Growth Case Analysis & Modeling

**Case:** Chaos Engine Growth Case — Games A & B  
**Author:** Head of Growth / Growth Lead  
**As of Date:** September 30, 2025  
**Code Repository:** Fully automated and reproducible via `python run_all.py`  

---

## Table of Contents
1. [Data Audit & Deterministic Anomaly Resolution](#1-data-audit--deterministic-anomaly-resolution)
2. [Market Cell Taxonomy & Baseline Economics](#2-market-cell-taxonomy--baseline-economics)
3. [Dual-Stream LTV & ROAS Modeling (Question 1)](#3-dual-stream-ltv--roas-modeling-question-1)
4. [Cross-Game Model Transferability & Structural Divergence](#4-cross-game-model-transferability--structural-divergence)
5. [Constrained Spend Optimization & Organic Uplift (Question 2)](#5-constrained-spend-optimization--organic-uplift-question-2)
6. [Creative Fatigue Mechanics & Replenishment Scheduling (Question 3)](#6-creative-fatigue-mechanics--replenishment-scheduling-question-3)

---

## 1. Data Audit & Deterministic Anomaly Resolution

All empirical modeling is built upon cleaned master panels preserving **100.00% of historical UA ad spend to the exact cent** ($392,075.67 across 33,362 rows in Game A; $669,975.34 across 10,167 rows in Game B).

Refer to [q1_data_problems_audit.md](file:///c:/Users/sy422/OneDrive/Documents/GitHub/chaos-engine-growth-case/outputs/tables/q1_data_problems_audit.md) for the complete quantitative audit log:

1. **Ad Revenue Double-Counting (ad_rev_all_sources_dN vs ad_rev_dN):**
   - *Proof:* Mediation SDK ad revenue (`ad_rev_d30 = $286,979.44`) matches telemetry gross ad revenue ($299,079.46), whereas `ad_rev_all_sources_d30 = $570,204.05` represents a 1.987x inflation due to raw network feed double-counting.
   - *Remediation:* Exclusively utilize mediation SDK `ad_rev_dN` as authoritative gross ad earnings; drop `ad_rev_all_sources_dN`.
2. **Right-Censored / Immature Cohorts Filled with Frozen Cutoffs & Zeros:**
   - *Proof:* In raw cohorts, rows with `age_days < N` held frozen Sep 30 cutoff values rather than nulls, while `retained_dN` was filled with 0.
   - *Remediation:* Strict maturity masking: set `ad_rev_d{N}_mature`, `iap_rev_d{N}_mature`, and `retained_d{N}_mature` to `np.nan` whenever `age_days < N`.
3. **July 14–16, 2025 Ad-Mediation eCPM Reporting Glitch:**
   - *Proof:* Telemetry ad revenue spiked 10x–27x in Game A ($9,145 on Jul 14, $38,987 on Jul 15, $16,960 on Jul 16 vs ~$1,500/day baseline) with stable impressions.
   - *Remediation:* Telemetry imputed from 14-day baseline eCPM. Cohorts and creatives repaired by computing install-weighted normal daily rates on mature non-overlapping cohorts, replacing spikes where increment > 2.5x expected with baseline expectation (-$62.6k Game A; -$10.9k Game B).
4. **100x Cents-vs-Dollars & Local Currency Logging Bugs:**
   - *Proof:* Game A Android telemetry logged raw KRW ($726.7k), JPY ($58.4k), and INR ($19.8k), and 100x cents-as-dollars between May 20 – Jun 08. Cohorts logged 34 corrupted increments with exact .xx00 SKU multiples > $150 (e.g. $469.43, $938.86).
   - *Remediation:* Raw FX converted; corrupted cohort increments divided by 100.0 (-$30,953.61 Game A; -$1,394.21 Game B). Zero false positives on legitimate US payers.
5. **Non-Monotonic Cumulative Revenue (ad_rev_d180 < ad_rev_d120):**
   - *Proof:* 3,380 rows in Game A and 966 rows in Game B showed negative incremental revenue between d120 and d180 due to horizon definition mismatches (121 calendar days vs 180 days).
   - *Remediation:* Cumulative monotonicity strictly enforced: $\text{rev}_{d\{k\}} = \max(\text{rev}_{d\{k\}}, \text{rev}_{d\{k-1\}})$.
6. **Unmatched UA Spend Rows (ua_daily vs cohorts):**
   - *Proof:* 4,197 rows in Game A ($1,347.41 spend, 0 MMP installs) and 113 rows in Game B ($1,793.75 spend) lacked cohort records.
   - *Remediation:* Strict outer join between `ua_daily` and `cohorts`, preserving 100% of UA expenditure.
7. **Zero-Install Cohorts, Retained > Installs, & Invalid Signature Campaigns:**
   - *Proof:* 626 rows in Game A and 690 in Game B had `installs == 0`; 41 and 39 rows had `retained > installs`; 1,087 rows in Game A were flagged `Invalid Signature`.
   - *Remediation:* Retained capped at installs; non-mobile platforms (`android-tv`, `windows`) isolated; fraud/bot installs excluded from paid cell modeling.
8. **Telemetry Coverage Gaps & Attribution Funnel Anomalies:**
   - *Proof:* Game A telemetry starts 2025-03-27 on Android and 2025-04-09 on iOS (first ~80 days missing); 514 rows showed view-through attribution (`installs_network > clicks`).
   - *Remediation:* MMP cohorts established as authoritative ground truth for full-period cohort economics.

---

## 2. Market Cell Taxonomy & Baseline Economics

Baseline economics are established over the 4-week pre-quarter window (**September 1 to September 28, 2025**, 28 days; weekly baseline = Sep sum / 4.0).

- **Game A:** 40 active decision cells across 5 mandatory lines:
  - `Net-A Android`: 32 major countries + 4 economically homogeneous regional tiers:
    - *Tier 1 (Affluent West/Europe):* `ch`, `be`, `ie`, `no`, `dk`, `nz`, `fi`, `sg`, `lu`, `is`, `mt`, `cy`, `pr`, `je`, `gg`, `im`, `gi`
    - *Tier 2 (East Asia & GCC):* `kw`, `qa`, `om`, `bh`, `bn`, `mo`
    - *Tier 3 (LatAm & East Europe):* `co`, `pe`, `cz`, `bg`, `hr`, `si`, `ee`, `lv`, `lt`, `rs`, `ec`, `cr`, `uy`, `pa`, `do`, `gt`, `sv`, `bo`, `py`, `mk`, `ba`, `al`, `ge`, `am`, `md`, `by`
    - *Tier 4 (RoW Emerging):* `id`, `pk`, `bd`, `ng`, `eg`, `za`, `ke`, `gh`, `dz`, `ma`, `tn`, `iq`, `jo`, `lb`, `lk`, `np`, `kh`, `mm`, `la`, `uz`, `kz`, `az`, `zz`
  - `Net-B Android US`, `Net-B iOS US`, `Net-C Android US`, `Net-D Android US`.
- **Game B:** 28 cells with explicit tracking of paused lines (`Net-C` stopped 2025-02-12; `Net-F` stopped 2025-03-31; `Net-E` stopped 2025-05-28; `Net-D` stopped 2025-08-25).

Refer to:
- [q1_market_cell_taxonomy_game_a.md](file:///c:/Users/sy422/OneDrive/Documents/GitHub/chaos-engine-growth-case/outputs/tables/q1_market_cell_taxonomy_game_a.md)
- [q1_market_cell_taxonomy_game_b.md](file:///c:/Users/sy422/OneDrive/Documents/GitHub/chaos-engine-growth-case/outputs/tables/q1_market_cell_taxonomy_game_b.md)
- [q1_gameA_cell_values.md](file:///c:/Users/sy422/OneDrive/Documents/GitHub/chaos-engine-growth-case/outputs/tables/q1_gameA_cell_values.md)
- [q1_gameB_cell_values.md](file:///c:/Users/sy422/OneDrive/Documents/GitHub/chaos-engine-growth-case/outputs/tables/q1_gameB_cell_values.md)

---

## 3. Dual-Stream LTV & ROAS Modeling (Question 1)

Player lifetime value is modeled via a decoupled dual-stream survival process:
$$\text{LTV}(t) = \text{LTV}_{\text{ad}}(t) + \text{LTV}_{\text{iap}}(t)$$
where retention follows a modified power-law survival curve $S(t) = (1 + \beta t)^{-\gamma}$, ad revenue scales with cumulative active user sessions, and IAP follows an empirical-Bayes shifted lognormal/exponential process.

### Official Submission Predictions (P1–P8 in `submission/predictions.csv`):
All predictions are strictly conditioned upon realized cumulative revenue banked as of September 30, 2025 (cohort ages 16–29d for P1–P6; 44–57d for P7–P8) with calibrated 80% empirical credible intervals:

| ID | Cell | Metric | Window | Obs Prev | Banked Sep 30 | Prediction | Low 80 | High 80 | Method Note |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **P1** | `Net-A, Android, United States` | ROAS D30 | 2025-09-01..09-14 | 0.4652 (D14) | 0.5164 | **0.5626** | 0.5349 | 0.5903 | Conditioned on D14 (0.4652) + realized Sep 30 banked rev (age 16-29d, 0.5164); power-law elapsed tail completion & calibrated 80% CI |
| **P2** | `Net-A, Android, all countries except United States` | ROAS D30 | 2025-09-01..09-14 | 0.7058 (D14) | 0.7961 | **0.8573** | 0.8206 | 0.8941 | Aggregate non-US 116-country cell; conditioned on D14 (0.7058) + realized Sep 30 banked rev (0.7961); power-law tail completion |
| **P3** | `Net-B, Android, United States` | ROAS D30 | 2025-09-01..09-14 | 0.5983 (D14) | 0.6732 | **0.7618** | 0.7087 | 0.8149 | Core line conditioned on D14 (0.5983) + realized Sep 30 banked rev (age 16-29d, 0.6732); power-law elapsed tail completion |
| **P4** | `Net-B, iOS, United States` | ROAS D30 | 2025-09-01..09-14 | 0.3864 (D14) | 0.3988 | **0.4312** | 0.4117 | 0.4507 | iOS core line conditioned on D14 (0.3864) + realized Sep 30 banked rev (age 16-29d, 0.3988); power-law elapsed tail completion |
| **P5** | `Net-C, Android, United States` | ROAS D30 | 2025-09-01..09-14 | 0.4001 (D14) | 0.4819 | **0.5543** | 0.5109 | 0.5978 | Ad-heavy core line conditioned on D14 (0.4001) + realized Sep 30 banked rev (age 16-29d, 0.4819); power-law elapsed tail completion |
| **P6** | `Net-D, Android, United States` | ROAS D30 | 2025-09-01..09-14 | 0.5180 (D14) | 0.5524 | **0.5788** | 0.5629 | 0.5946 | Offerwall conditioned on D14 (0.5180) + realized Sep 30 banked rev (0.5524); front-loaded IAP pacing & power-law elapsed tail completion |
| **P7** | `Net-A, Android, United States` | ROAS D60 | 2025-08-04..08-17 | 0.7700 (D30) | 0.9306 | **0.9879** | 0.9535 | 1.0223 | Conditioned on D30 (0.7700) + realized Sep 30 banked rev (age 44-57d, 0.9306); power-law remaining tail to D60 & calibrated 80% CI |
| **P8** | `Net-D, Android, United States` | ROAS D60 | 2025-08-04..08-17 | 0.7205 (D30) | 0.7734 | **0.7887** | 0.7795 | 0.7980 | Offerwall conditioned on D30 (0.7205) + realized Sep 30 banked rev (age 44-57d, 0.7734); mature tail to D60 & calibrated 80% CI |

Refer to [predictions.csv](file:///c:/Users/sy422/OneDrive/Documents/GitHub/chaos-engine-growth-case/submission/predictions.csv) and [q1_cell_ltv_roas_predictions.md](file:///c:/Users/sy422/OneDrive/Documents/GitHub/chaos-engine-growth-case/outputs/tables/q1_cell_ltv_roas_predictions.md).

---

## 4. Cross-Game Model Transferability & Structural Divergence

We evaluated the 4-way cross-game transfer matrix on mature 14-day holdout cohorts:

| Training Game | Evaluation Game | Metric Target | WAPE (%) | Bias (%) | Pearson $r$ | 80% CI Coverage | Transfer Viability |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **Game A** | **Game A** | D120 ROAS | **30.76%** | -2.71% | 0.8841 | **79.2%** | **In-Sample Baseline (Calibrated)** |
| **Game A** | **Game B** | D120 ROAS | **21.71%** | +4.12% | 0.9124 | **79.0%** | **High Transferability (Ad Curve Robust)** |
| **Game B** | **Game B** | D120 ROAS | **18.41%** | -1.15% | 0.9412 | **79.8%** | **In-Sample Baseline (Pure Ad)** |
| **Game B** | **Game A** | D120 ROAS | **34.57%** | -8.45% | 0.8241 | **75.6%** | **Moderate Transferability (Underpredicts IAP)** |

### Four Structural Divergence Drivers:
1. **Monetization Architecture Asymmetry:** Game A is a balanced hybrid (52% Ad / 48% IAP in US), whereas Game B is a pure ad engine (99.6% Ad / 0.4% IAP). Transferring B's parameters to A systematically underprojects high-value IAP whales.
2. **Retention Decay & Longevity:** Game B exhibits flatter retention decay ($\gamma = 0.465$ vs Game A's $\gamma = 0.524$), yielding +64% higher active user retention at Day 120.
3. **Offerwall Channel Dynamics:** Net-D in Game A features highly front-loaded IAP monetization (85% of IAP occurs within 14 days), whereas Game B contains no active offerwall networks.
4. **Component vs Multiplier Robustness:** Retention decay curves transfer across casual games far more stably than raw revenue multipliers, which are heavily distorted by local currency and ad mediation bugs.

Refer to [q1_cross_game_transfer.md](file:///c:/Users/sy422/OneDrive/Documents/GitHub/chaos-engine-growth-case/outputs/tables/q1_cross_game_transfer.md).

---

## 5. Constrained Spend Optimization & Organic Uplift (Question 2)

### Optimization Formulation:
$$\max_{\mathbf{x}} \sum_{i=1}^{40} \text{Expected D120 Revenue}_i(\mathbf{x})$$
subject to:
1. $\sum_{i=1}^{40} S_i \le \$250,000.00$
2. $\frac{\sum_{i=1}^{40} \text{Expected D120 Revenue}_i}{\sum_{i=1}^{40} S_i} \ge 1.0000$ (CFO Hurdle)
3. $\sum_{i \in \text{Line } L} S_i \ge 0.40 \cdot S_{0, L}$ for all 5 mandatory active lines
4. $0.0 \le x_i \le 2.00$ for all cells ($x_i \ge 0.40$ for single-cell lines)
5. Diminishing returns: $\text{ROAS}(x) = R_{0, i} \cdot [\text{clip}(x, 0.50, 2.00)]^{-k_i} \cdot \text{HOLIDAY\_FACTOR}$
   where $k_{\text{Net-A}} = 0.35$, $k_{\text{Net-B}} = 0.40$, $k_{\text{Net-C}} = 0.45$, $k_{\text{Net-D}} = 0.65$.
6. Holiday Shock: $\text{HOLIDAY\_FACTOR} = \frac{8}{12} \cdot 1.0 + \frac{4}{12} \cdot \frac{1}{1.25} = \frac{11.2}{12.0} \approx 0.933333$.

### Key Findings:
- **CFO Breakeven Ceiling:** Direct paid spend is capped at **$140,391.59** to satisfy 1.0000x D120 payback.
- **Organic Uplift Catalyst:** Econometric OLS confirms an organic K-factor of **+0.0485** ($t=3.815, p < 0.001$), generating +$0.0995 D120 revenue per paid install. Crediting this halo expands the CFO breakeven ceiling to **$158,000.00**.
- **CEO Scale Option:** The full $250,000 budget deploys 107,957 installs at 0.7666x D120 ROAS ($191.7k rev) and 0.8657x 1Y ROAS ($216.4k rev).

Refer to:
- [plan.csv](file:///c:/Users/sy422/OneDrive/Documents/GitHub/chaos-engine-growth-case/submission/plan.csv)
- [q2_media_plan.md](file:///c:/Users/sy422/OneDrive/Documents/GitHub/chaos-engine-growth-case/outputs/tables/q2_media_plan.md)
- [q2_budget_sensitivity_frontier.md](file:///c:/Users/sy422/OneDrive/Documents/GitHub/chaos-engine-growth-case/outputs/tables/q2_budget_sensitivity_frontier.md)
- [q2_organic_uplift_econometrics.md](file:///c:/Users/sy422/OneDrive/Documents/GitHub/chaos-engine-growth-case/outputs/tables/q2_organic_uplift_econometrics.md)
- Figure: [q2_efficient_frontier.png](file:///c:/Users/sy422/OneDrive/Documents/GitHub/chaos-engine-growth-case/outputs/figures/q2_efficient_frontier.png)
- Figure: [q2_spend_allocation_pie.png](file:///c:/Users/sy422/OneDrive/Documents/GitHub/chaos-engine-growth-case/outputs/figures/q2_spend_allocation_pie.png)

---

## 6. Creative Fatigue Mechanics & Replenishment Scheduling (Question 3)

### Wear-Out Rules & Asset Capacities:
- **Net-A (Videos & Playables):** +20% CPI / 1M imps; max capacity = 1,500,000 impressions before +30% retirement ceiling. 2-week production lead time.
- **Net-B (Ad Sets, Shared Android + iOS):** +300% CPI / 1M imps; max capacity = 100,000 impressions. 1-week lead time.
- **Net-C (Ad Packs):** +300% CPI / 1M imps; max capacity = 100,000 impressions. 1-week lead time.
- **Net-D (Store Listing Images):** +150% CPI / 1M imps; max capacity = 200,000 impressions. 1-week lead time.

### Operational Production Schedule (13 New Units Total):
- **Weeks 1–2 (Oct 6 – Oct 19):** Carried entirely by existing creative library.
- **Weeks 3–12 (Oct 20 – Dec 28):**
  - **Net-A:** 5 new videos/playables launched at Weeks 3, 5, 7, 10, 12.
  - **Net-B:** 4 new ad sets launched at Weeks 3, 6, 9, 12.
  - **Net-C:** 3 new ad packs launched at Weeks 3, 7, 11.
  - **Net-D:** 1 new store listing image (endures all 10 weeks at only +7.6% wear).

Refer to:
- [q3_creative_performance_decomposition.md](file:///c:/Users/sy422/OneDrive/Documents/GitHub/chaos-engine-growth-case/outputs/tables/q3_creative_performance_decomposition.md)
- [q3_creative_replenishment_schedule.md](file:///c:/Users/sy422/OneDrive/Documents/GitHub/chaos-engine-growth-case/outputs/tables/q3_creative_replenishment_schedule.md)
- Figure: [q3_creative_wearout_curves.png](file:///c:/Users/sy422/OneDrive/Documents/GitHub/chaos-engine-growth-case/outputs/figures/q3_creative_wearout_curves.png)
- Figure: [q3_creative_refresh_timeline.png](file:///c:/Users/sy422/OneDrive/Documents/GitHub/chaos-engine-growth-case/outputs/figures/q3_creative_refresh_timeline.png)
- Figure: [q1_ltv_growth_curves.png](file:///c:/Users/sy422/OneDrive/Documents/GitHub/chaos-engine-growth-case/outputs/figures/q1_ltv_growth_curves.png)
