# Executive Memo: Game A Q4 Growth & UA Spend Strategy

**To:** Chief Executive Officer & Chief Financial Officer  
**From:** Head of Growth / Growth Lead  
**Date:** September 30, 2025  
**Subject:** Game A Q4 Budget Allocation, Econometric Payback & Player Valuation  

---

### Executive Five-Line Summary (Mandatory CFO Briefing)

1. **Spend Recommendation:** We recommend deploying **$140,391.59** across 12 weeks as the primary CFO-compliant plan, strictly achieving **1.0000x D120 ROAS payback** (or **$158,000.00** when factoring in the verified **+4.85% organic halo**). We provide the CEO with the unconstrained **$250,000.00** scale option (delivering 107,957 installs at 0.7666x D120 ROAS / 0.8657x 1Y ROAS) and the **$182,325.00** 1-Year cash breakeven allocation (1.0000x 1Y ROAS).
2. **Expected Result:** The recommended CFO plan acquires **75,555 paid installs** (**79,219 total installs** with organic halo), generating **$140,391.61 in Day-120 gross revenue** (**1.0000x D120 ROAS**, 1.0532x blended) and **$158,072.89 in 1-Year gross revenue** (**1.1259x 1Y ROAS**).
3. **Payback Profile:** 
   - *Payback $\le$ 120 Days:* **Net-D Android US** (1.035x base, scaled to 0.50x), **10 international Net-A markets** (`ro`, `hk`, `se`, `mx`, `pl`, `ar`, `pt`, `il`, `gb`, `vn`), and **Regional Tiers 1, 3, 4**.
   - *Payback within 1 Year:* **Net-A Android US** (0.993x), **Net-B Android US** (1.012x), **Net-C Android US** (1.065x), and 7 scaled international markets (`gr`, `br`, `ca`, `jp`, `cl`, `tw`, `de`).
   - *Non-viable within 1 Year:* **Net-B iOS US** (0.895x 1Y) and structural drag markets (`at`, `sa`, `sk`, `Tier 2`), which are pruned or held to mandatory contractual minimums (40% baseline).
4. **Primary Data Distortions:** We proved and repaired 8 foundational data anomalies across raw MMP, telemetry, and cohort tables: (i) 1.99x ad mediation double-counting (+$283k spurious ad rev); (ii) right-censored immature cohorts repeating frozen cutoff values; (iii) July 14–16 eCPM glitch (+$60.6k telemetry spike); (iv) 100x local currency/cents logging bugs (-$31.0k IAP); (v) non-monotonic cumulative revenue (3,380 rows); (vi) 4,197 unmatched UA spend rows ($1,347 ad spend preserved to 100.00% audit match); (vii) non-mobile platforms & invalid signatures; and (viii) telemetry coverage gaps.
5. **Key Strategic Risks:** Rapid creative fatigue on high-spend networks (+300% CPI inflation per 1M imps on Net-B/C) and the **Thanksgiving/Holiday CPI surge (+25% inflation across Weeks 8–11)**. We mitigate this through a deterministic production schedule requiring **13 new creative units** (5 Net-A, 4 Net-B, 3 Net-C, 1 Net-D) deployed on strict 1-to-2 week production lead times.

---

### 1. Strategic Capital Allocation Dilemma: CFO Payback vs. CEO Growth

Our constrained portfolio optimization resolves the fundamental tension between capital preservation and scale. In casual mobile gaming, diminishing marginal returns ($x^{-k}$) and macro holiday seasonality create an inescapable tradeoff between spend volume and payback speed:

| Planning Strategy | Quarter Spend | Share of $250k Budget | Paid Installs | Total Installs (w/ Org) | Expected D120 Revenue | Expected D120 ROAS | Expected 1Y Revenue | Expected 1Y ROAS | Net D120 Cashflow | Strategic Recommendation |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **A. Primary CFO Breakeven Plan** | **$140,391.59** | **56.16%** | **75,555** | **79,219** | **$140,391.61** | **1.0000x** | **$158,072.89** | **1.1259x** | **+$0.02** | **Recommended Baseline Execution** |
| **B. Blended Organic Breakeven** | $158,000.00 | 63.20% | 82,140 | 86,124 | $148,800.00 | 0.9418x (1.00x bl.) | $167,700.00 | 1.0614x | -$9,200.00 (direct) | Validated if CFO credits organic halo |
| **C. 1-Year Cash Breakeven Plan** | $182,325.00 | 72.93% | 90,615 | 95,010 | $161,600.22 | 0.8863x | $182,325.14 | **1.0000x** | -$20,724.78 | 100% of baseline spend pace |
| **D. CEO Full Budget Growth Plan** | $250,000.00 | 100.00% | 107,957 | 113,193 | $191,656.96 | 0.7666x | $216,427.40 | 0.8657x | -$58,343.04 | Maximum scale; requires $58k CFO reserve |

```
                       CFO-VS-CEO PARETO EFFICIENT FRONTIER
     ROAS
     1.30 |  * ($75k, 1.23x D120)
     1.20 |       * ($100k, 1.17x)
     1.10 |            * ($120k, 1.08x)
     1.00 |-----------------★ ($140.4k, 1.0000x) <--- CFO HARD CEILING
     0.90 |                      * ($182.3k, 0.89x D120, 1.00x 1Y)
     0.80 |                                * ($220k, 0.81x)
     0.70 |                                     ▲ ($250k, 0.7666x) <--- CEO MAX BUDGET
          +-------------------------------------------------------------
          $50k     $100k    $140k    $180k    $220k    $250k   Spend ($)
```

**Strategic Takeaway:** Deploying the full $250,000 budget is mathematically incompatible with a 100% Day-120 payback requirement on direct paid spend. Because the 14 cells with baseline D120 ROAS $\ge 1.00$ only have a combined 12-week baseline capacity of $65,120, scaling spend to $250k forces capital into sub-1.0x cells while diminishing returns and holiday CPI (+25%) drive marginal ROAS down. 

Therefore, **we recommend committing $140,391.59 immediately to guarantee 100% capital payback by Day 120**, while presenting the $250k plan as an explicit growth investment requiring board approval for a $58.3k working capital cycle.

---

### 2. Network & Line Portfolio Allocation (The 5 Mandatory Lines & KKT Economics)

All 5 mandatory active lines are maintained at or above their 40% spend floor over the 12-week quarter, governed by Karush-Kuhn-Tucker (KKT) first-order optimality conditions:

1. **Net-A Android ($68,051.05 total spend; 101.2% of baseline; 48.47% budget share):**
   - **United States:** Core domestic baseline paced at 0.50x spend ($17,522.76) to protect payback (D120 ROAS: 0.963x, 1Y ROAS: 1.121x).
   - **High-Payback Direct Outperformers (Scaled to 2.0x ceiling):** Romania (2.41x D120 ROAS), Hong Kong (2.14x), Mexico (1.47x), Sweden (1.46x), Argentina (1.19x), Poland (1.12x), Portugal (1.07x), Israel (1.01x), Vietnam (1.00x), and United Kingdom (1.02x).
   - **Regional Tiers:** Tiers 1, 3, and 4 scaled to 2.0x (D120 ROAS 1.01x–1.13x), aggregating affluent European and emerging mobile markets with favorable CPM/CPI ratios. Tier 2 (GCC & East Asia) pruned due to poor baseline return (0.584x).
   - **Counter-Intuitive CPI vs. ROAS Allocation (The "Cheap-CPI Trap"):** Budget multiples are dictated strictly by marginal net margin, not raw CPI. Higher-CPI markets like `GB` ($1.84 CPI) and `SE` ($0.79 CPI) receive maximum **2.0x budget multiples** because their strong LTV delivers >1.00x D120 payback. Conversely, nominal "cheap-CPI" traps like `IT` ($0.20 CPI), `PH` ($0.30 CPI), and `SA` ($0.58 CPI) are pruned or zeroed because poor player monetization yields sub-0.75x ROAS (e.g., SA D120 ROAS is only 0.531x).
2. **Net-D Android US ($28,695.54 spend; 50.0% of baseline; 20.44% budget share):**
   - Top-performing offerwall channel. Paced at exactly 0.50x baseline ($2,391.30/week) to capture its maximum **+56.9% efficiency boost** ($0.50^{-0.65} = 1.5692\times$, delivering **1.516x D120 ROAS** after holiday shock and generating **+$14,801 in net D120 cash surplus**).
   - *Why Net-D is held at 50.0% while Net-B Android is at 90.8% ($21,915 spend):* Due to Net-D's aggressive diminishing returns exponent ($k=0.65$ vs $k=0.40$ on Net-B), spending beyond 0.50x causes Net-D's marginal D120 revenue to drop immediately to **$0.531 per dollar**—just below the **$0.536 marginal revenue** where Net-B Android (90.8%), Net-B iOS (67.4%), and Net-C Android (60.7%) equilibrate under KKT shadow-price conditions. Reallocating that marginal capital to Net-B and Net-C maximizes total portfolio revenue.
3. **Net-B Android US ($21,911.59 spend; 90.8% of baseline; 15.61% budget share):**
   - Mainstream video/social engine. Maintained at 0.91x spend ($1,825.97/week) delivering 0.954x D120 ROAS and 1.048x 1-Year cash payback.
4. **Net-B iOS US ($13,725.20 spend; 67.4% of baseline; 9.78% budget share):**
   - Held to controlled levels ($1,143.77/week). Under ATT tracking loss, iOS D120 ROAS is 0.918x and 1Y ROAS is 1.005x. Preserves high-value iOS telemetry while mitigating cash drag.
5. **Net-C Android US ($8,011.09 spend; 60.7% of baseline; 5.71% budget share):**
   - Ad-heavy network paced at $667.59/week, delivering 0.966x D120 ROAS and 1.233x 1-Year ROAS (strong long-tail ad revenue growth).

---

### 3. Econometric Organic Uplift & Halo Effect

Using daily time-series regression with day-of-week fixed effects and time trends across the 266-day historical record, we proved a statistically significant organic halo:
- **Estimated K-Factor:** **+0.0485** ($t = 3.815$, $p < 0.001$, 95% CI: $[0.0235, 0.0735]$).
- **Organic Player Valuation:** Mature organic cohorts (age $\ge 120$d) monetize at **$2.0516 per install** ($1.24 ad rev + $0.81 IAP rev).
- **Revenue Halo:** Each paid install generates **+$0.0995 in incremental D120 revenue** and **+$0.1188 at 1 Year**.
- **Portfolio Impact:** Across the 75,555 paid installs in the CFO plan, the organic halo generates **3,664 incremental organic installs** and **+$7,517 in uncredited revenue**, elevating portfolio D120 ROAS from 1.0000x to **1.0532x**.

---

### 4. Operational Creative Fatigue & Replenishment Schedule

To counter aggressive creative wearout and survive the November 24 – December 21 holiday shock (+25% CPI), creative production must adhere to a deterministic 12-week schedule:
- **Existing Asset Carryover:** Existing creative packs carry **Weeks 1–2 (Oct 6 – Oct 19)** without new production spend.
- **Weeks 3–12 Replenishment Volume (13 New Units Total Recommended):**
  - **Net-A (5 Videos/Playables):** Max 1.5M imps/unit (+20% CPI / 1M imps). 2-week production lead time. Launches: W3, W5, W7, W10, W12. *Format Mechanics Note:* While Net-A Search Text Ads achieve the highest standalone D30 ROAS (1.54x), Net-A operates as an auto-assembled multi-asset ecosystem where video and playable components drive 88% of volume and lower network-wide blended CPI; thus, production focuses on 5 fresh video/playable units while search text copy is refreshed in-house alongside them.
  - **Net-B (3 Minimum vs. 4 Recommended Ad Sets, Shared Android+iOS):** Delivering 293.3k impressions across Weeks 3–12 requires a strict mathematical minimum of $\lceil 293,271 / 100,000 \rceil = 3$ shared ad sets. However, **we recommend producing 4 ad sets** (launches: W3, W6, W9, W12) to provide a 1-set staggered operational buffer ensuring neither Android nor iOS crosses the +30% CPI fatigue ceiling during the peak November 24 – December 21 holiday surge (+300% CPI / 1M imps; 1-week lead time).
  - **Net-C (3 Ad Packs):** Max 100k imps/unit (+300% CPI / 1M imps). 1-week lead time. Launches: W3, W7, W11.
  - **Net-D (1 Store Listing Image):** Max 200k imps/unit (+150% CPI / 1M imps). 1-week lead time. Burns only 50.9k imps (25.5% capacity), lasting the entire quarter at only +7.6% wear.
- **Production Triggers:** Creative briefs must be issued on **October 6 (Week 1)** for Net-A Video 1 and on **October 13 (Week 2)** for Net-B/C/D batches.

---

### 5. Implementation Roadmap & Milestones

1. **Week 1 (Oct 6):** Initiate production on Net-A Video 1 and issue briefs for Net-B AdSet 1, Net-C Pack 1, Net-D Image 1. Lock baseline pacing.
2. **Week 3 (Oct 20):** Deploy Batch 1 new creatives across all 4 networks. Retire aged historical creatives.
3. **Week 7 (Nov 17):** Audit mid-quarter cohort maturation (Days 14–30). Trigger production for Holiday Surge creative refreshes.
4. **Week 8 (Nov 24):** **Holiday Season Shock begins (+25% CPI everywhere).** Maintain strict uniform spend pacing; do not panic-inflate bids.
5. **Week 12 (Dec 22):** Final quarterly reconciliation, post-holiday CPI recovery audit, and Q1 2026 baseline budget recalibration.
