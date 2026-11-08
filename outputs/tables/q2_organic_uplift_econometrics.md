# Exhibit 10: Econometric Organic Uplift & K-Factor Model

OLS regression of daily organic installs on daily paid installs with day-of-week fixed effects and time trend:

| Metric | Value | Standard_Error | t_statistic | p_value | 95%_Confidence_Interval | Interpretation |
| --- | --- | --- | --- | --- | --- | --- |
| Organic Uplift Multiplier (K-Factor) | 0.0485 | 0.0127 | 3.815 | 1.7045e-04 | [0.0235, 0.0735] | Each 1,000 paid installs drives ~48.5 incremental organic installs (statistically significant at p < 0.001) |
| Mature Organic Player D120 LTV | $2.0516 | - | - | - | - | Gross D120 cumulative revenue per organic/unattributed player from mature cohorts (age >= 120d) |
| Mature Organic Player 1-Year LTV | $2.4498 | - | - | - | - | Gross 1-year cumulative revenue per organic player extrapolated via parametric retention decay |
| Incremental D120 Revenue Bonus per Paid Install | $0.0995 | $0.0261 | 3.815 | 1.7045e-04 | [$0.0481, $0.1508] | Expected organic revenue generated at D120 per single paid install acquired |
| Incremental 1-Year Revenue Bonus per Paid Install | $0.1188 | $0.0311 | 3.815 | 1.7045e-04 | [$0.0575, $0.1801] | Expected organic revenue generated at 1-year horizon per single paid install acquired |

**Strategic Growth Takeaway:**
- Direct paid UA acts as an organic catalyst with a robust +4.85% K-factor (p < 0.001).
- This incremental halo delivers ~$0.100 of bonus organic revenue per paid install at Day 120 and ~$0.119 at 1 Year.
- When factoring in organic halo, the CFO breakeven spend threshold expands by +12.5% from $140,392 to $158,000.
