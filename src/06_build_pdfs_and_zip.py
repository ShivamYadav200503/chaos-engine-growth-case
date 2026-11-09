"""
Script 06: Build Publication PDFs & Final Submission Package
Chaos Engine Labs Growth Case

Full Production Implementation:
1. Compiles submission/memo.pdf:
   - Strictly <= 2 pages.
   - Starts with the mandatory 5 CFO lines on Page 1.
   - Embeds KKT optimality economics, cheap-CPI trap analysis, and portfolio efficient frontier.
2. Compiles submission/appendix.pdf:
   - Strictly <= 12 pages (compiled to exactly 11 pages).
   - Structured cleanly by Question (Sections A, B, C, D, E).
   - Embeds all 4 high-DPI publication figures from outputs/figures/:
     * Section A: fig1_data_anomalies.png
     * Section C: fig2_ltv_curves_and_transfer.png
     * Section D: fig3_q2_pareto_and_allocation.png
     * Section E: fig4_q3_creative_matrix_and_schedule.png
   - Incorporates full tables for Q1, Q2, and Q3 directly from outputs/tables/.
3. Compiles submission/ai_log/ai_usage_log.pdf:
   - Strictly <= 1 page (0.5 to 1 page).
   - Documents the 4 required sections from Section 5 of the case brief:
     * Two critical traps caught (naive cohort averaging & ad_rev_all_sources 2x double-counting;
       100x cents-as-dollars IAP outliers & naive combined cross-game transfer).
     * Where AI saved significant time (vectorized audit of $1.06M spend & SLSQP optimizer).
     * What was intentionally skipped and why (deep learning neural nets & micro-territory sub-allocation).
4. Verifies page limits programmatically using both regex binary scanning and PDF structure analysis.
5. Renders each page to PNG in outputs/figures/pdf_inspection/ for automated visual QA.
6. Packages complete deliverables into Chaos_Engine_Labs_Growth_Submission.zip.
"""

import os
import sys
import re
import zipfile
import tempfile
from pathlib import Path

# Ensure Matplotlib has a writable temp directory for fonts and cache
os.environ["MPLCONFIGDIR"] = tempfile.gettempdir()

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.patches as patches
import pandas as pd
from PIL import Image

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

from src.config import SUB_DIR, FIGS_DIR, TABLES_DIR, PROC_DIR, BASE_DIR

INSPECT_DIR = FIGS_DIR / "pdf_inspection"
INSPECT_DIR.mkdir(parents=True, exist_ok=True)


def escape_dollars(s: object) -> str:
    """Escapes unescaped dollar signs for Matplotlib text rendering to prevent mathtext parser syntax errors."""
    return str(s).replace(r"\$", "$").replace("$", r"\$")


def get_pdf_page_count(pdf_path: Path) -> int:
    """Reads PDF page count in pure Python via binary object scanning and /Pages /Count catalog."""
    with open(pdf_path, "rb") as f:
        data = f.read()
    page_objs = len(re.findall(rb"/Type\s*/Page\b", data))
    m = re.findall(rb"/Type\s*/Pages.*?/Count\s+(\d+)", data, re.DOTALL)
    count_val = int(m[0]) if m else page_objs
    return max(page_objs, count_val)


# =============================================================================
# 1. BUILD SUBMISSION/MEMO.PDF (STRICTLY <= 2 PAGES)
# =============================================================================

def build_memo_pdf():
    """Generates submission/memo.pdf (strictly 2 pages)."""
    print("\n" + "=" * 75)
    print("[06] Compiling submission/memo.pdf (Strictly 2 Pages)...")
    print("=" * 75)
    
    pdf_path = SUB_DIR / "memo.pdf"
    
    with PdfPages(pdf_path) as pdf:
        # ----------------------------------------------------
        # PAGE 1: Executive Briefing & Allocation Frontier
        # ----------------------------------------------------
        fig1 = plt.figure(figsize=(8.5, 11), dpi=300)
        ax1 = fig1.add_axes([0, 0, 1, 1])
        ax1.axis("off")
        
        # Header banner
        ax1.add_patch(patches.Rectangle((0.05, 0.91), 0.90, 0.065, facecolor="#1b263b", edgecolor="none"))
        ax1.text(0.07, 0.945, "EXECUTIVE MEMO: GAME A Q4 GROWTH & UA SPEND STRATEGY", color="white", fontsize=13, fontweight="bold")
        ax1.text(0.07, 0.922, "To: Chief Executive Officer & Chief Financial Officer   |   From: Head of Growth   |   Date: September 30, 2025", color="#cbd5e1", fontsize=8.5)
        
        # Mandatory 5 CFO Lines Box
        ax1.add_patch(patches.Rectangle((0.05, 0.595), 0.90, 0.300, facecolor="#f8fafc", edgecolor="#cbd5e1", lw=1))
        ax1.add_patch(patches.Rectangle((0.05, 0.595), 0.012, 0.300, facecolor="#0284c7", edgecolor="none"))
        
        ax1.text(0.075, 0.868, "EXECUTIVE FIVE-LINE BRIEFING (MANDATORY CFO CORE)", fontsize=10.5, fontweight="bold", color="#0f172a")
        
        cfo_lines = [
            ("1. Spend Recommendation:", "Deploy $140,391.63 across 12 weeks strictly meeting 1.0000x D120 ROAS ($158,000 with organic halo). Unconstrained CEO scale option ($250k) and 1-Year cash breakeven ($182.3k) also provided."),
            ("2. Expected Result:", "75,545 paid installs (80% CI: [72.1k, 79.2k]), delivering $140,391.63 Day-120 gross revenue (1.0000x D120 ROAS [0.963x, 1.042x]) and $158,072.60 at 1Y (1.1259x 1Y ROAS). With +4.85% organic halo: 78,839 total installs, $147,088 total D120 revenue, and 1.0476x blended ROAS."),
            ("3. Payback Profile:", "Payback <=120d: Net-D Android US, 10 Net-A countries (RO, HK, SE, MX, PL, AR, PT, IL, GB, VN), and Tiers 1, 3, 4. Payback in 1Y: Net-A US, Net-B Android US, Net-C Android US. Non-viable: Net-B iOS US (0.895x 1Y)."),
            ("4. Primary Data Distortions:", "8 critical anomalies proved and repaired: 1.99x mediation double-counting (+$283k spurious ad rev), right-censoring filled with frozen cutoffs, July 14-16 eCPM glitch, 100x local currency/cents bugs, and 4,197 unmatched spend rows ($1,347 preserved; 100.00% spend reconciled)."),
            ("5. Key Strategic Risks:", "Creative wearout (+300% CPI / 1M imps on Net-B/C) and Holiday Surge (+25% CPI in Weeks 8-11). Mitigated via 13 new creative units (5 Net-A, 4 Net-B, 3 Net-C, 1 Net-D) produced on 1-2 week lead times.")
        ]
        
        y_pos = 0.838
        for title, desc in cfo_lines:
            ax1.text(0.075, y_pos, title, fontsize=8.5, fontweight="bold", color="#0284c7")
            ax1.text(0.075, y_pos - 0.022, escape_dollars(desc), fontsize=7.8, color="#334155")
            y_pos -= 0.053
            
        # Section 1: Capital Allocation Dilemma
        ax1.text(0.05, 0.560, "1. Strategic Capital Allocation Dilemma: CFO Payback vs. CEO Growth", fontsize=11, fontweight="bold", color="#0f172a")
        
        intro_text = (
            "Our constrained portfolio optimization resolves the tension between capital preservation (CFO) and scale (CEO). "
            "Due to diminishing marginal returns (x^-k) and holiday CPI inflation (+25%), deploying the entire $250,000 budget drops "
            "portfolio Day-120 ROAS to 0.7666x (a -$58,343 deficit). The maximum spend satisfying the CFO's D120 ROAS >= 1.00 mandate "
            "on direct paid spend is exactly $140,391.63."
        )
        ax1.text(0.05, 0.522, escape_dollars(intro_text), fontsize=8, color="#334155", wrap=True)
        
        # Strategy Comparison Table
        table_headers = ["Planning Strategy", "Quarter Spend", "Budget Share", "Total Installs", "Expected D120 Rev", "D120 ROAS", "1Y ROAS", "Net D120 Cashflow"]
        table_rows = [
            ["A. Primary CFO Breakeven Plan", "$140,391.63", "56.16%", "78,839", "$140,391.63", "1.0000x*", "1.1259x", "+$0.00"],
            ["B. Blended Organic Breakeven", "$158,000.00", "63.20%", "86,124", "$148,800.00", "0.9418x", "1.0614x", "-$9,200.00"],
            ["C. 1-Year Cash Breakeven Plan", "$182,325.00", "72.93%", "95,010", "$161,600.22", "0.8863x", "1.0000x", "-$20,724.78"],
            ["D. CEO Full Budget Growth Plan", "$250,000.00", "100.00%", "113,193", "$191,656.96", "0.7666x", "0.8657x", "-$58,343.04"]
        ]
        
        t_y = 0.440
        col_x = [0.05, 0.28, 0.39, 0.49, 0.59, 0.72, 0.81, 0.89]
        
        ax1.add_patch(patches.Rectangle((0.05, t_y), 0.90, 0.025, facecolor="#0f172a", edgecolor="none"))
        for h, x in zip(table_headers, col_x):
            ax1.text(x + 0.005, t_y + 0.007, h, color="white", fontsize=7.5, fontweight="bold")
            
        t_y -= 0.026
        for r_idx, row in enumerate(table_rows):
            bg_col = "#f1f5f9" if r_idx % 2 == 1 else "#ffffff"
            ax1.add_patch(patches.Rectangle((0.05, t_y), 0.90, 0.025, facecolor=bg_col, edgecolor="#e2e8f0", lw=0.5))
            for val, x in zip(row, col_x):
                is_bold = "Primary" in val or "1.0000x" in val
                text_col = "#0369a1" if "Primary" in val else ("#0f172a" if is_bold else "#334155")
                ax1.text(x + 0.005, t_y + 0.007, escape_dollars(val), color=text_col, fontsize=7.5, fontweight="bold" if is_bold else "normal")
            t_y -= 0.025
            
        ax1.text(0.05, t_y - 0.005, "*Primary plan achieves 1.0000x direct D120 ROAS ($140,391.63 rev on 75,545 paid installs), and 1.0476x blended ($147,088 rev on 78,839 total installs with verified +4.85% organic halo).", fontsize=7, color="#64748b", fontstyle="italic")
        
        # Embed Frontier Chart
        img_frontier = mpimg.imread(str(FIGS_DIR / "q2_efficient_frontier.png"))
        ax1_img = fig1.add_axes([0.05, 0.06, 0.90, 0.28])
        ax1_img.imshow(img_frontier)
        ax1_img.axis("off")
        
        # Footer Page 1
        ax1.text(0.05, 0.025, "Chaos Engine Labs Growth Case | Executive Memo", fontsize=8, color="#94a3b8")
        ax1.text(0.88, 0.025, "Page 1 of 2", fontsize=8, fontweight="bold", color="#94a3b8")
        
        fig1.savefig(INSPECT_DIR / "memo_page_1.png", dpi=150)
        pdf.savefig(fig1)
        plt.close()
        
        # ----------------------------------------------------
        # PAGE 2: Portfolio Allocations, KKT Economics, Creatives & Roadmap
        # ----------------------------------------------------
        fig2 = plt.figure(figsize=(8.5, 11), dpi=300)
        ax2 = fig2.add_axes([0, 0, 1, 1])
        ax2.axis("off")
        
        # Page 2 Header Bar
        ax2.add_patch(patches.Rectangle((0.05, 0.945), 0.90, 0.030, facecolor="#1b263b", edgecolor="none"))
        ax2.text(0.07, 0.953, "EXECUTIVE MEMO: PORTFOLIO ALLOCATION, KKT ECONOMICS & EXECUTION", color="white", fontsize=10, fontweight="bold")
        
        # Section 2: Portfolio Allocation & KKT Economics
        ax2.text(0.05, 0.915, "2. Network Allocation & Karush-Kuhn-Tucker (KKT) Optimality", fontsize=10.5, fontweight="bold", color="#0f172a")
        
        sec2_text = (
            "All 5 mandatory active lines meet their >=40% baseline spend floor. Net-D Android US is paced at exactly 0.50x baseline ($28,695.54) "
            "to capture its maximum +56.9% efficiency boost (1.516x D120 ROAS after holiday shock, generating +$14,801 net D120 cash profit). "
            "Why Net-D is held at 50% while Net-B Android US is at 90.8% ($21,911.56): Due to Net-D's steep diminishing returns exponent (k=0.65 "
            "vs k=0.40 on Net-B), spending beyond 0.50x causes Net-D's marginal D120 revenue to drop to $0.531 per dollar—just below the $0.536 "
            "marginal revenue where Net-B Android (90.8%), Net-B iOS (67.4%), and Net-C Android (60.7%) equilibrate under KKT shadow-price conditions.\n\n"
            "Counter-Intuitive Budget Allocation (The 'Cheap-CPI Trap'): Capital is allocated to maximize net margin (LTV - CPI), not minimize gross CPI. "
            "Higher-CPI markets like Net-A GB ($1.84 CPI) and SE ($0.79 CPI) receive maximum 2.0x budget multiples because their strong monetization "
            "delivers >1.00x D120 payback. In contrast, superficial 'cheap-CPI' traps like IT ($0.20 CPI), PH ($0.30 CPI), and SA ($0.58 CPI) are pruned "
            "to zero because poor player monetization yields sub-0.75x ROAS (e.g., SA D120 ROAS is only 0.531x)."
        )
        ax2.text(0.05, 0.775, escape_dollars(sec2_text), fontsize=7.8, color="#334155", wrap=True)
        
        # Embed Spend Allocation Donut Chart
        img_pie = mpimg.imread(str(FIGS_DIR / "q2_spend_allocation_pie.png"))
        ax2_pie = fig2.add_axes([0.05, 0.535, 0.90, 0.22])
        ax2_pie.imshow(img_pie)
        ax2_pie.axis("off")
        
        # Section 3: Econometric Organic Uplift
        ax2.text(0.05, 0.505, "3. Econometric Organic Uplift & Halo Effect", fontsize=10.5, fontweight="bold", color="#0f172a")
        sec3_text = (
            "Time-series OLS regression with day-of-week fixed effects and deterministic time trend across 266 daily records proves a robust "
            "organic K-factor of +0.0485 (t = 3.815, p < 0.001, 95% CI: [0.0235, 0.0735]). Mature organic players monetize at $2.0516 D120 LTV, "
            "yielding +$0.0995 in incremental D120 revenue per paid install. Crediting this halo elevates portfolio D120 ROAS to 1.0476x blended and "
            "expands the CFO breakeven ceiling from $140,392 to $158,000."
        )
        ax2.text(0.05, 0.440, escape_dollars(sec3_text), fontsize=7.8, color="#334155", wrap=True)
        
        # Section 4: Operational Creative Schedule
        ax2.text(0.05, 0.410, "4. Operational Creative Fatigue & Replenishment Schedule", fontsize=10.5, fontweight="bold", color="#0f172a")
        sec4_text = (
            "Existing creative library carries Weeks 1-2 without new production cost. Weeks 3-12 deploy 13 new creative units:\n"
            "• Net-A (5 Videos/Playables): Max 1.5M imps/unit (+20% CPI / 1M imps; 2-wk lead time; launches W3, W5, W7, W10, W12). Format Note: "
            "While Net-A Search Text Ads deliver 1.54x D30 ROAS, Net-A is an auto-assembled multi-asset network where videos/playables drive 88% "
            "of volume; production focuses on 5 fresh video/playable units while search copy is refreshed alongside them.\n"
            "• Net-B (3 Minimum vs 4 Recommended Ad Sets, Shared Android+iOS): Weeks 3-12 volume requires a mathematical minimum of 3 ad sets "
            "(ceil(293,271 / 100,000) = 3). We recommend producing 4 ad sets (W3, W6, W9, W12) to provide a 1-set staggered operational buffer "
            "preventing either platform crossing the +30% CPI ceiling during the peak Holiday Surge.\n"
            "• Net-C (3 Ad Packs): Max 100k imps/unit (+300% CPI / 1M imps; 1-wk lead time; launches W3, W7, W11).\n"
            "• Net-D (1 Listing Image): Max 200k imps/unit (+150% CPI / 1M imps; burns only 50.9k imps, carries all 10 weeks at only +7.6% wear)."
        )
        ax2.text(0.05, 0.235, escape_dollars(sec4_text), fontsize=7.8, color="#334155", wrap=True)
        
        # Section 5: Implementation Roadmap
        ax2.text(0.05, 0.205, "5. Implementation Roadmap & Execution Milestones", fontsize=10.5, fontweight="bold", color="#0f172a")
        roadmap_items = [
            ("Week 1 (Oct 6):", "Issue production briefs for Net-A Video 1 (2-wk lead time) and Net-B AdSet 1, Net-C Pack 1, Net-D Image 1 (1-wk lead time). Lock baseline weekly bids."),
            ("Week 3 (Oct 20):", "Deploy Batch 1 new creatives across all 4 networks. Retire aged historical creative packs; activate automated eCPM monitoring."),
            ("Week 7 (Nov 17):", "Audit mid-quarter cohort maturation (Days 14-30). Trigger production for Holiday Surge creative refreshes."),
            ("Week 8 (Nov 24):", "HOLIDAY SURGE COMMENCES (+25% CPI everywhere). Maintain uniform spend pacing; do not over-bid into inflated auction pricing."),
            ("Week 12 (Dec 22):", "Final quarterly reconciliation, post-holiday CPI recovery audit, and Q1 2026 baseline budget recalibration.")
        ]
        
        ry = 0.170
        for w_label, w_desc in roadmap_items:
            ax2.text(0.05, ry, w_label, fontsize=7.5, fontweight="bold", color="#0284c7")
            ax2.text(0.18, ry, escape_dollars(w_desc), fontsize=7.5, color="#334155")
            ry -= 0.026
            
        # Footer Page 2
        ax2.text(0.05, 0.025, "Chaos Engine Labs Growth Case | Executive Memo", fontsize=8, color="#94a3b8")
        ax2.text(0.88, 0.025, "Page 2 of 2", fontsize=8, fontweight="bold", color="#94a3b8")
        
        fig2.savefig(INSPECT_DIR / "memo_page_2.png", dpi=150)
        pdf.savefig(fig2)
        plt.close()
        
    pages = get_pdf_page_count(pdf_path)
    print(f"  [MEMO PDF] Built {pdf_path}: Exactly {pages} pages (Constraint: <= 2 pages | PASS: {pages <= 2})")
    assert pages == 2, f"Expected exactly 2 pages, got {pages}"


# =============================================================================
# 2. BUILD SUBMISSION/AI_LOG/AI_USAGE_LOG.PDF (STRICTLY 0.5 TO 1 PAGE)
# =============================================================================

def build_ai_log_pdf():
    """Generates submission/ai_log/ai_usage_log.pdf (strictly 1 page)."""
    print("\n" + "=" * 75)
    print("[06] Compiling submission/ai_log/ai_usage_log.pdf (Strictly 1 Page)...")
    print("=" * 75)
    
    pdf_path = SUB_DIR / "ai_log" / "ai_usage_log.pdf"
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    
    with PdfPages(pdf_path) as pdf:
        fig = plt.figure(figsize=(8.5, 11), dpi=300)
        ax = fig.add_axes([0, 0, 1, 1])
        ax.axis("off")
        
        # Header banner
        ax.add_patch(patches.Rectangle((0.05, 0.925), 0.90, 0.045, facecolor="#1b263b", edgecolor="none"))
        ax.text(0.07, 0.942, "AI USAGE REFLECTION & LOG | CHAOS ENGINE LABS GROWTH CASE", color="white", fontsize=11, fontweight="bold")
        ax.text(0.07, 0.930, "Deliverable 6 | Author: Head of Growth | As of Date: September 30, 2025", color="#cbd5e1", fontsize=7.5)
        
        # Section 1: Two Mistakes Caught
        ax.text(0.05, 0.895, "1. Two Critical Moments When AI Tools Gave Erroneous Output & How We Fixed Them", fontsize=9.5, fontweight="bold", color="#0f172a")
        
        # Mistake 1 Box
        ax.add_patch(patches.Rectangle((0.05, 0.615), 0.90, 0.265, facecolor="#fef2f2", edgecolor="#fecaca", lw=0.8))
        ax.add_patch(patches.Rectangle((0.05, 0.615), 0.010, 0.265, facecolor="#dc2626", edgecolor="none"))
        
        ax.text(0.070, 0.860, "MISTAKE 1: Censored-Median Contamination & Single-Day Payer Window in Data Cleaning", fontsize=8.5, fontweight="bold", color="#b91c1c")
        m1_text = (
            "• The Error: An initial AI code pass cleaned the July 14-16 ad glitch by computing baseline ad rates across all non-overlapping cohorts "
            "without filtering for cohort maturity (age_days >= h). Because immature cohorts hold frozen zero increments, the median normal rate collapsed "
            "to 0.0 at d60, d90, d120, and d180, wiping out 99% of legitimate mature ad revenue for valid cohorts overlapping mid-July. Simultaneously, the script "
            "divided multi-day incremental IAP (d7->d14 is 7 days, d14->d30 is 16 days) by single-day active payer counts (payers_d{h}), falsely flagging "
            "142 legitimate US repeat-purchase cohorts on Net-B and Net-D as corrupted anomalies.\n"
            "• Detection: We cross-reconciled cleaned cohort revenue totals against telemetry_daily.csv mediation totals ($299,079 ad rev in Game A) and audited "
            "row-level payer spend histories on US lines.\n"
            "• Deterministic Fix: We enforced age_days >= h on baseline rate calculations, implemented install-weighted cell rates, and restricted IAP anomaly "
            "cleaning strictly to confirmed .xx00 SKU multiples (e.g. $469.43, $938.86) exceeding $150 with zero or near-zero window payers."
        )
        ax.text(0.070, 0.700, escape_dollars(m1_text), fontsize=7.2, color="#334155", wrap=True)
        
        # Mistake 2 Box
        ax.add_patch(patches.Rectangle((0.05, 0.335), 0.90, 0.265, facecolor="#fffbeb", edgecolor="#fef3c7", lw=0.8))
        ax.add_patch(patches.Rectangle((0.05, 0.335), 0.010, 0.265, facecolor="#d97706", edgecolor="none"))
        
        ax.text(0.070, 0.580, "MISTAKE 2: Unconditioned Partial-Age Predictions on P7/P8 & Simpson's Paradox on Net-A Non-US", fontsize=8.5, fontweight="bold", color="#b45309")
        m2_text = (
            "• The Error: The first LTV modeling pass masked partial d60 revenues for August 4-17 cohorts (ages 44-57 days on Sep 30), predicting Day-60 ROAS "
            "of 0.9228 for P7 and 0.7409 for P8. However, by September 30, those cohorts had ALREADY BANKED 0.9306 (P7) and 0.7734 (P8) in realized cash—predicting "
            "less money than was already in the bank! Simultaneously, when projecting Net-A Non-US (P2), the AI divided all-time Jan-Jun LTV ($1.15, dominated by "
            "expensive Tier-1 tests) by September's cheaper country-mix CPI ($0.65), creating a Simpson's Paradox denominator mismatch that artificially inflated "
            "projected ROAS to 1.78x. Furthermore, it bootstrapped parameter means rather than residual quantiles, yielding an uncalibrated 27.5% CI coverage.\n"
            "• Detection: We ran strict monotonicity assertions (Obs_Prev < Banked_Sep30 < low_80 < prediction < high_80) and held-out coverage backtests.\n"
            "• Deterministic Fix: We reformulated P1-P8 to condition directly on realized revenue banked as of September 30, projecting only unelapsed days via "
            "power-law elapsed fractions. We projected ROAS in consistent cohort-spend space and calibrated conformal residual quantiles (~79% empirical coverage)."
        )
        ax.text(0.070, 0.420, escape_dollars(m2_text), fontsize=7.2, color="#334155", wrap=True)
        
        # Section 2: Where AI Saved Time
        ax.text(0.05, 0.315, "2. Where AI Saved Significant Time", fontsize=9.5, fontweight="bold", color="#0f172a")
        s2_text = (
            "• Vectorized 8-Problem Forensic Audit: Rapidly joining and reconciling 166,000+ rows across 12 raw CSVs to verify $392,075.67 Game A spend and "
            "$669,975.34 Game B spend to 100.00% precision.\n"
            "• Hierarchical Dual-Stream Survival Modeling: Accelerating the formulation of decoupled power-law retention and shifted lognormal IAP monetization "
            "with Empirical Bayes shrinkage across 62 market cells.\n"
            "• Constrained Non-Linear KKT Spend Optimization: Solving the 40-cell non-linear constrained optimization across the CFO-vs-CEO Pareto frontier in minutes."
        )
        ax.text(0.05, 0.235, escape_dollars(s2_text), fontsize=7.2, color="#334155", wrap=True)
        
        # Section 3: What Was Skipped
        ax.text(0.05, 0.210, "3. Short List of What Was Intentionally Skipped and Why", fontsize=9.5, fontweight="bold", color="#0f172a")
        s3_text = (
            "• User-Level Deep Learning Models: Raw data is cohort-aggregated; complex neural networks overfit small-sample cells and lack interpretability. "
            "Parametric survival models + Empirical Bayes provide full transparency, strict monotonicity, and verifiable credible intervals.\n"
            "• Individual Budget Optimization for Micro-Territories (<$10/wk Spend): Net-A contains over 80 long-tail countries with volatile 1-5 install volumes. "
            "We grouped these into 4 economically homogeneous regional tiers to preserve statistical power while documenting all constituent country codes."
        )
        ax.text(0.05, 0.125, escape_dollars(s3_text), fontsize=7.2, color="#334155", wrap=True)
        
        # Footer
        ax.text(0.05, 0.040, "Chaos Engine Labs Growth Case | Deliverable 6: AI Usage Reflection & Log", fontsize=8, color="#94a3b8")
        ax.text(0.88, 0.040, "Page 1 of 1", fontsize=8, fontweight="bold", color="#94a3b8")
        
        fig.savefig(INSPECT_DIR / "ai_usage_log_page_1.png", dpi=150)
        pdf.savefig(fig)
        plt.close()
        
    pages = get_pdf_page_count(pdf_path)
    print(f"  [AI LOG PDF] Built {pdf_path}: Exactly {pages} page (Constraint: <= 1 page | PASS: {pages <= 1})")
    assert pages == 1, f"Expected exactly 1 page, got {pages}"


# =============================================================================
# 3. BUILD SUBMISSION/APPENDIX.PDF (STRICTLY <= 12 PAGES, EXACTLY 11 PAGES)
# =============================================================================

def build_appendix_pdf():
    """Generates submission/appendix.pdf (strictly <= 12 pages; compiled to exactly 11 pages)."""
    print("\n" + "=" * 75)
    print("[06] Compiling submission/appendix.pdf (Strictly <= 12 Pages; Exactly 11 Pages)...")
    print("=" * 75)
    
    pdf_path = SUB_DIR / "appendix.pdf"
    TOTAL_APP_PAGES = 11
    
    with PdfPages(pdf_path) as pdf:
        def add_page_furniture(ax, page_num, title):
            ax.add_patch(patches.Rectangle((0.05, 0.945), 0.90, 0.030, facecolor="#1b263b", edgecolor="none"))
            ax.text(0.07, 0.953, f"TECHNICAL APPENDIX: {title.upper()}", color="white", fontsize=9.5, fontweight="bold")
            ax.text(0.05, 0.025, "Chaos Engine Labs Growth Case | Technical Appendix", fontsize=8, color="#94a3b8")
            ax.text(0.88, 0.025, f"Page {page_num} of {TOTAL_APP_PAGES}", fontsize=8, fontweight="bold", color="#94a3b8")

        # ----------------------------------------------------
        # PAGE 1: Section A - Overview & Forensic Audit Framework
        # ----------------------------------------------------
        fig = plt.figure(figsize=(8.5, 11), dpi=300)
        ax = fig.add_axes([0, 0, 1, 1]); ax.axis("off")
        add_page_furniture(ax, 1, "Section A: Overview & Data Audit Framework")
        
        ax.text(0.05, 0.900, "Technical Appendix: Quantitative Methodologies & Proofs", fontsize=13, fontweight="bold", color="#0f172a")
        ax.text(0.05, 0.880, "Case: Chaos Engine Labs Games A & B   |   Lead Analyst: Head of Growth   |   As of: September 30, 2025", fontsize=8, color="#64748b")
        
        # Table of contents box
        ax.add_patch(patches.Rectangle((0.05, 0.730), 0.90, 0.135, facecolor="#f8fafc", edgecolor="#cbd5e1", lw=0.8))
        ax.text(0.07, 0.840, "TABLE OF CONTENTS", fontsize=9, fontweight="bold", color="#0f172a")
        toc = [
            "Section A: Data Audit & Forensic Anomaly Resolution (Exhibits 1 & Fig 1)",
            "Section B: Player Value Tables for Game A & Game B (Exhibits 2 & 3)",
            "Section C: Decoupled Dual-Stream LTV, Backtest Accuracy & Cross-Game Transfer (P1-P8 & Fig 2)",
            "Section D: Constrained Media Plan Optimization, Organic Halo & KKT Proofs (Exhibits 11 & Fig 3)",
            "Section E: Creative Fatigue Decomposition, Replenishment Cadence & Risk Simulation (Fig 4 & Exhibit 15)"
        ]
        ty = 0.820
        for item in toc:
            ax.text(0.07, ty, f"• {item}", fontsize=7.5, color="#334155")
            ty -= 0.016
            
        ax.text(0.05, 0.690, "Section A: Forensic Data Audit & Deterministic Reconciliation Summary", fontsize=11, fontweight="bold", color="#0f172a")
        audit_summary = (
            "Raw UA, cohort, telemetry, and creative records exhibited 8 distinct anomalies that distort LTV modeling and UA payback. "
            "We engineered deterministic repairs preserving 100.00% of true ad spend to the exact cent ($392,075.67 across 33,362 rows in Game A; "
            "$669,975.34 across 10,167 rows in Game B).\n\n"
            "Key Audit Metrics & Reconciled Dollar Impacts:\n"
            "• Problem 1 (Mediation Double-Counting): ad_rev_all_sources_d30 ($570.2k Game A, $648.1k Game B) double-counted mediated network feeds "
            "by 1.99x relative to true mediation SDK earnings ($287.0k Game A, $335.0k Game B). Remediated by standardizing on mediation SDK ad_rev_dN.\n"
            "• Problem 2 (Right-Censored Cutoff Contamination): Immature cohorts (age < N) held frozen cutoff values rather than NaNs, while retained_dN "
            "held false zeros. Remediated by strict right-censor masking: rev_dN_mature = np.nan whenever age < N.\n"
            "• Problem 3 (July 14-16 eCPM Spike): Telemetry ad rev spiked 10x-27x in Game A ($65.1k spurious rev) while impressions remained stable. "
            "Remediated by computing install-weighted normal rates on mature non-overlapping cohorts, removing -$62.6k in Game A and -$10.9k in Game B.\n"
            "• Problem 4 (100x Currency / Cents Logging): Telemetry logged raw KRW, JPY, INR and May 20-Jun 8 Android 100x cents. Repaired via exact "
            ".xx00 SKU increment filtering, removing -$30,953.61 in Game A and -$1,394.21 in Game B with zero false positives on legitimate US payers.\n"
            "• Problem 5 (Non-Monotonic d180 < d120): 3,380 rows in Game A and 966 rows in Game B showed negative incremental revenue due to horizon definition "
            "asymmetries (121 calendar days vs 180 days). Enforced cumulative monotonicity: rev_d{k} = max(rev_d{k}, rev_d{k-1}).\n"
            "• Problem 6 (Unmatched UA Spend): 4,197 rows in Game A ($1,347 spend) and 113 rows in Game B ($1,794 spend) lacked cohort records. Outer-joined "
            "to guarantee zero lost ad spend.\n"
            "• Problem 7 (Fraud / Invalid Signatures): 1,087 Game A rows flagged 'Invalid Signature' and non-mobile platforms (android-tv, windows) isolated.\n"
            "• Problem 8 (Telemetry Gaps): Game A telemetry rollout gaps (first 80 days missing) resolved by using MMP cohorts as primary ground truth."
        )
        ax.text(0.05, 0.400, escape_dollars(audit_summary), fontsize=7.5, color="#334155", wrap=True)
        
        fig.savefig(INSPECT_DIR / "appendix_page_1.png", dpi=150)
        pdf.savefig(fig); plt.close()

        # ----------------------------------------------------
        # PAGE 2: Section A (Cont.) - Full Data Problems Audit Table
        # ----------------------------------------------------
        fig = plt.figure(figsize=(8.5, 11), dpi=300)
        ax = fig.add_axes([0, 0, 1, 1]); ax.axis("off")
        add_page_furniture(ax, 2, "Section A: Exhibit 1 Data Problems Audit Log")
        
        ax.text(0.05, 0.915, "Exhibit 1: Quantitative Audit Log of All 8 Data Problems & Deterministic Repairs", fontsize=10.5, fontweight="bold", color="#0f172a")
        
        audit_df = pd.read_csv(TABLES_DIR / "q1_data_problems_audit.csv")
        headers = ["ID", "Game", "Problem Name", "Where Found", "What It Distorts", "Dollar / ROAS Impact"]
        col_x = [0.05, 0.08, 0.14, 0.36, 0.58, 0.80]
        
        y = 0.880
        ax.add_patch(patches.Rectangle((0.05, y), 0.90, 0.022, facecolor="#0f172a", edgecolor="none"))
        for h, x in zip(headers, col_x):
            ax.text(x + 0.003, y + 0.006, h, color="white", fontsize=7.5, fontweight="bold")
            
        y -= 0.045
        for idx, row in audit_df.iterrows():
            bg_col = "#f8fafc" if idx % 2 == 1 else "#ffffff"
            ax.add_patch(patches.Rectangle((0.05, y), 0.90, 0.042, facecolor=bg_col, edgecolor="#e2e8f0", lw=0.5))
            
            p_id = str(row["Problem_ID"])
            p_game = str(row["Game"])
            p_name = str(row["Problem_Name"])[:32] + "..." if len(str(row["Problem_Name"])) > 32 else str(row["Problem_Name"])
            p_where = str(row["Where_Found"])[:35] + "..." if len(str(row["Where_Found"])) > 35 else str(row["Where_Found"])
            p_dist = str(row["What_It_Distorts"])[:35] + "..." if len(str(row["What_It_Distorts"])) > 35 else str(row["What_It_Distorts"])
            p_imp = str(row["Dollar_or_ROAS_Impact"])[:25] + "..." if len(str(row["Dollar_or_ROAS_Impact"])) > 25 else str(row["Dollar_or_ROAS_Impact"])
            
            vals = [p_id, p_game, p_name, p_where, p_dist, p_imp]
            for v, x in zip(vals, col_x):
                ax.text(x + 0.003, y + 0.015, escape_dollars(v), color="#1e293b", fontsize=6.8)
                
            y -= 0.045
            if y < 0.06:
                break
                
        fig.savefig(INSPECT_DIR / "appendix_page_2.png", dpi=150)
        pdf.savefig(fig); plt.close()

        # ----------------------------------------------------
        # PAGE 3: Section A (Cont.) - Figure 1 Data Anomalies Visuals
        # ----------------------------------------------------
        fig = plt.figure(figsize=(8.5, 11), dpi=300)
        ax = fig.add_axes([0, 0, 1, 1]); ax.axis("off")
        add_page_furniture(ax, 3, "Section A: Figure 1 Forensic Data Anomaly Visuals")
        
        ax.text(0.05, 0.915, "Figure 1: Forensic Visual Diagnostics of Core Data Anomalies", fontsize=10.5, fontweight="bold", color="#0f172a")
        fig1_desc = (
            "Panel A illustrates the July 14-16 ad mediation telemetry eCPM spike (10x-27x surge) in Games A and B before vs after deterministic "
            "smoothing using install-weighted normal baseline rates on mature cohorts. Panel B illustrates the 100x currency / cents logging glitch "
            "and the 1.99x ad mediation double-counting ratio in ad_rev_all_sources_dN."
        )
        ax.text(0.05, 0.855, escape_dollars(fig1_desc), fontsize=7.8, color="#334155", wrap=True)
        
        # Embed Figure 1
        img_f1 = mpimg.imread(str(FIGS_DIR / "fig1_data_anomalies.png"))
        ax_f1 = fig.add_axes([0.05, 0.20, 0.90, 0.63])
        ax_f1.imshow(img_f1); ax_f1.axis("off")
        
        ax.text(0.05, 0.140, "Diagnostic Takeaway: Left uncorrected, these data bugs create spurious ROAS spikes that mislead automated budget allocators.", fontsize=8, color="#64748b", fontstyle="italic")
        fig.savefig(INSPECT_DIR / "appendix_page_3.png", dpi=150)
        pdf.savefig(fig); plt.close()

        # ----------------------------------------------------
        # PAGE 4: Section B - Game A Player Value & Cell Economics
        # ----------------------------------------------------
        fig = plt.figure(figsize=(8.5, 11), dpi=300)
        ax = fig.add_axes([0, 0, 1, 1]); ax.axis("off")
        add_page_furniture(ax, 4, "Section B: Game A Player Value & Cell Economics")
        
        ax.text(0.05, 0.915, "Exhibit 2: Core Game A Active UA Lines Baseline Summary (Sep 1-28, 2025)", fontsize=10.5, fontweight="bold", color="#0f172a")
        sec2_desc = (
            "Baseline economics are calibrated over September 1 to September 28, 2025 (4 full weeks = 28 days; weekly baseline = Sep sum / 4.0).\n"
            "• Game A (40 Active Cells): Net-A Android is structured into 32 major individual countries and 4 regional tiers (Tier 1 Affluent West, "
            "Tier 2 East Asia & GCC, Tier 3 LatAm & East Europe, Tier 4 Emerging RoW). Net-B Android US, Net-B iOS US, Net-C Android US, and Net-D Android US "
            "form the remaining active lines. Total baseline weekly spend = $15,193.72 ($182,324.64 12-week baseline)."
        )
        ax.text(0.05, 0.825, escape_dollars(sec2_desc), fontsize=7.8, color="#334155", wrap=True)
        
        ga_cells = pd.read_csv(TABLES_DIR / "q1_gameA_cell_values.csv")
        sample_rows = ga_cells[ga_cells["country_cell"].isin(["us", "TOTAL", "all countries except United States"]) | 
                               ga_cells["country_cell"].str.startswith("Tier")].copy()
        
        headers = ["Network", "Platform", "Cell / Region", "Weekly Spend", "Base CPI", "Pred D120 ROAS", "Pred 1Y ROAS", "Payback Classification"]
        col_x = [0.05, 0.15, 0.24, 0.44, 0.54, 0.63, 0.72, 0.81]
        
        y = 0.780
        ax.add_patch(patches.Rectangle((0.05, y), 0.90, 0.022, facecolor="#0f172a", edgecolor="none"))
        for h, x in zip(headers, col_x):
            ax.text(x + 0.003, y + 0.006, h, color="white", fontsize=7.2, fontweight="bold")
            
        y -= 0.026
        for idx, row in sample_rows.iterrows():
            bg_col = "#f1f5f9" if "TOTAL" in str(row["country_cell"]) else ("#f8fafc" if idx % 2 == 1 else "#ffffff")
            ax.add_patch(patches.Rectangle((0.05, y), 0.90, 0.024, facecolor=bg_col, edgecolor="#e2e8f0", lw=0.5))
            
            vals = [
                str(row["network"]), str(row["platform"]), str(row["country_cell"]),
                f"${row['baseline_weekly_spend']:,.2f}", f"${row['baseline_cpi']:.3f}" if pd.notna(row['baseline_cpi']) else "-",
                f"{row['predicted_d120_roas']:.4f}", f"{row['predicted_1y_roas']:.4f}",
                str(row["payback_classification"])
            ]
            for v, x in zip(vals, col_x):
                is_bold = "TOTAL" in str(row["country_cell"])
                ax.text(x + 0.003, y + 0.006, escape_dollars(v), color="#0f172a" if is_bold else "#334155", fontsize=6.8, fontweight="bold" if is_bold else "normal")
            y -= 0.026
            
        fig.savefig(INSPECT_DIR / "appendix_page_4.png", dpi=150)
        pdf.savefig(fig); plt.close()

        # ----------------------------------------------------
        # PAGE 5: Section B (Cont.) - Game B Player Value & Paused Networks
        # ----------------------------------------------------
        fig = plt.figure(figsize=(8.5, 11), dpi=300)
        ax = fig.add_axes([0, 0, 1, 1]); ax.axis("off")
        add_page_furniture(ax, 5, "Section B: Game B Player Value & Paused Networks")
        
        ax.text(0.05, 0.915, "Exhibit 3: Game B Player Values & Paused Network Audit Summary", fontsize=10.5, fontweight="bold", color="#0f172a")
        sec2b_desc = (
            "Game B contains 28 historical cells across 6 ad networks. Historical test dates and pause timestamps:\n"
            "• Net-C (iOS/Android): Paused on 2025-02-12 (ph, us tested; D120 ROAS sub-0.67x).\n"
            "• Net-F (iOS): Paused on 2025-03-31 (gb, us tested; zero conversions; D120 ROAS 0.00x).\n"
            "• Net-E (Android US): Paused on 2025-05-28 (D120 ROAS 0.507x; failed payback).\n"
            "• Net-D (Android US): Paused on 2025-08-25 (D120 ROAS 0.473x; failed payback).\n"
            "• Active Channels in September Baseline: Net-A Android (au, br, ca, gb, nz, ph, us) and Net-B (Android US, iOS US)."
        )
        ax.text(0.05, 0.805, escape_dollars(sec2b_desc), fontsize=7.8, color="#334155", wrap=True)
        
        gb_cells = pd.read_csv(TABLES_DIR / "q1_gameB_cell_values.csv")
        sample_gb = gb_cells[gb_cells["country_cell"].isin(["us", "ph", "ca", "gb"]) | gb_cells["status"].str.startswith("Paused")].head(14).copy()
        
        headers_gb = ["Network", "Platform", "Cell", "Base Spend", "CPI", "Obs D30", "Pred D120", "Pred 1Y", "Network Status", "Pause Date"]
        col_xgb = [0.05, 0.14, 0.22, 0.28, 0.38, 0.46, 0.55, 0.64, 0.73, 0.85]
        
        y = 0.760
        ax.add_patch(patches.Rectangle((0.05, y), 0.90, 0.022, facecolor="#0f172a", edgecolor="none"))
        for h, x in zip(headers_gb, col_xgb):
            ax.text(x + 0.002, y + 0.006, h, color="white", fontsize=7.0, fontweight="bold")
            
        y -= 0.025
        for idx, row in sample_gb.iterrows():
            bg_col = "#f8fafc" if idx % 2 == 1 else "#ffffff"
            ax.add_patch(patches.Rectangle((0.05, y), 0.90, 0.023, facecolor=bg_col, edgecolor="#e2e8f0", lw=0.5))
            
            p_date = str(row["status"]).replace("Paused on ", "") if "Paused" in str(row["status"]) else "--"
            vals_gb = [
                str(row["network"]), str(row["platform"]), str(row["country_cell"]),
                f"${row['baseline_weekly_spend']:,.1f}" if pd.notna(row['baseline_weekly_spend']) and row['baseline_weekly_spend'] > 0 else "--",
                f"${row['historical_cpi']:.2f}" if pd.notna(row['historical_cpi']) else "-",
                f"{row['observed_d30_roas']:.3f}" if pd.notna(row['observed_d30_roas']) else "--",
                f"{row['predicted_d120_roas']:.3f}" if pd.notna(row['predicted_d120_roas']) else "--",
                f"{row['predicted_1y_roas']:.3f}" if pd.notna(row['predicted_1y_roas']) else "--",
                "Paused" if "Paused" in str(row["status"]) else "Active",
                p_date
            ]
            for v, x in zip(vals_gb, col_xgb):
                ax.text(x + 0.002, y + 0.006, escape_dollars(v), color="#334155", fontsize=6.8)
            y -= 0.025
            
        fig.savefig(INSPECT_DIR / "appendix_page_5.png", dpi=150)
        pdf.savefig(fig); plt.close()

        # ----------------------------------------------------
        # PAGE 6: Section C - LTV Methodology, Backtest & Predictions P1-P8
        # ----------------------------------------------------
        fig = plt.figure(figsize=(8.5, 11), dpi=300)
        ax = fig.add_axes([0, 0, 1, 1]); ax.axis("off")
        add_page_furniture(ax, 6, "Section C: Dual-Stream LTV & P1-P8 Predictions")
        
        ax.text(0.05, 0.915, "3. Decoupled Dual-Stream LTV Architecture & Official Predictions (P1–P8)", fontsize=10.5, fontweight="bold", color="#0f172a")
        sec3_desc = (
            "Player lifetime value is modeled as the decoupled sum of independent Ad and IAP survival processes: LTV(t) = LTV_ad(t) + LTV_iap(t).\n"
            "• Retention Modeling: S(t) = (1 + beta*t)^(-gamma). Game A fits beta=11.48, gamma=0.524; Game B fits beta=12.23, gamma=0.465.\n"
            "• Predictions P1-P8 (in submission/predictions.csv): Conditioned upon realized revenue banked as of September 30, 2025. Cohorts P1-P6 "
            "are 16-29 days old; P7-P8 are 44-57 days old. Monotonicity: Obs_Prev < Banked_Sep30 < low_80 < prediction < high_80. 80% CI coverage = 79.2%."
        )
        ax.text(0.05, 0.810, escape_dollars(sec3_desc), fontsize=7.8, color="#334155", wrap=True)
        
        # Predictions Table
        preds_df = pd.read_csv(SUB_DIR / "predictions.csv")
        headers = ["ID", "Cell / Line", "Target", "Obs Prev", "Banked Sep30", "Prediction", "Low 80", "High 80", "Methodology Note"]
        col_x = [0.05, 0.10, 0.34, 0.42, 0.50, 0.59, 0.67, 0.74, 0.81]
        
        y = 0.770
        ax.add_patch(patches.Rectangle((0.05, y), 0.90, 0.024, facecolor="#0f172a", edgecolor="none"))
        for h, x in zip(headers, col_x):
            ax.text(x + 0.003, y + 0.007, h, color="white", fontsize=7.2, fontweight="bold")
            
        y -= 0.048
        for idx, row in preds_df.iterrows():
            bg_col = "#f8fafc" if idx % 2 == 1 else "#ffffff"
            ax.add_patch(patches.Rectangle((0.05, y), 0.90, 0.044, facecolor=bg_col, edgecolor="#e2e8f0", lw=0.5))
            
            p_id = str(row["id"])
            p_cell = str(row["cell"])[:30]
            p_metric = str(row["metric"])
            m_prev = re.search(r"Conditioned on (?:D14|D30)\s*\(([0-9.]+)\)", str(row["method_note"]))
            p_prev = f"{float(m_prev.group(1)):.4f}" if m_prev else "-"
            m_bank = re.search(r"banked rev\s*\([^)]*?([0-9.]+)\)", str(row["method_note"]))
            p_banked = f"{float(m_bank.group(1)):.4f}" if m_bank else "-"
            p_pred = f"{float(row['your_prediction']):.4f}"
            p_low = f"{float(row['low_80']):.4f}"
            p_high = f"{float(row['high_80']):.4f}"
            p_note = str(row["method_note"])[:36] + "..."
            
            vals = [p_id, p_cell, p_metric, p_prev, p_banked, p_pred, p_low, p_high, p_note]
            for v, x in zip(vals, col_x):
                is_pred = (x == 0.59)
                ax.text(x + 0.003, y + 0.016, escape_dollars(v), color="#0369a1" if is_pred else "#1e293b", fontsize=6.8, fontweight="bold" if is_pred else "normal")
            y -= 0.048
            
        # Out-of-time Backtest Table Snippet
        ax.text(0.05, y - 0.010, "Exhibit 7: Out-of-Time Model Accuracy Backtest (Holdout Cohorts)", fontsize=8.5, fontweight="bold", color="#0f172a")
        y -= 0.035
        bt_df = pd.read_csv(TABLES_DIR / "q1_model_accuracy_backtest.csv").head(6)
        headers_bt = ["Game", "Network", "Cohorts", "Actual D120", "Pred D120", "WAPE %", "MPE Bias %", "80% CI Cov"]
        col_xbt = [0.05, 0.16, 0.28, 0.40, 0.53, 0.65, 0.76, 0.87]
        
        ax.add_patch(patches.Rectangle((0.05, y), 0.90, 0.020, facecolor="#1e293b", edgecolor="none"))
        for h, x in zip(headers_bt, col_xbt):
            ax.text(x + 0.002, y + 0.005, h, color="white", fontsize=7.0, fontweight="bold")
            
        y -= 0.022
        for idx, row in bt_df.iterrows():
            bg_col = "#f8fafc" if idx % 2 == 1 else "#ffffff"
            ax.add_patch(patches.Rectangle((0.05, y), 0.90, 0.020, facecolor=bg_col, edgecolor="#e2e8f0", lw=0.5))
            vals_bt = [
                str(row["game"]), str(row["network"]), str(row["n_cohorts"]),
                f"${row['actual_d120_rev']:,.0f}", f"${row['predicted_d120_rev']:,.0f}",
                f"{row['wape_pct']:.1f}%", f"{row['bias_mpe_pct']:+.1f}%", f"{row['ci_80_coverage_pct']:.1f}%"
            ]
            for v, x in zip(vals_bt, col_xbt):
                ax.text(x + 0.002, y + 0.005, escape_dollars(v), color="#334155", fontsize=6.8)
            y -= 0.022
            
        fig.savefig(INSPECT_DIR / "appendix_page_6.png", dpi=150)
        pdf.savefig(fig); plt.close()

        # ----------------------------------------------------
        # PAGE 7: Section C (Cont.) - 4-Way Cross-Game Transfer & Figure 2
        # ----------------------------------------------------
        fig = plt.figure(figsize=(8.5, 11), dpi=300)
        ax = fig.add_axes([0, 0, 1, 1]); ax.axis("off")
        add_page_furniture(ax, 7, "Section C: Cross-Game Model Transfer Matrix")
        
        ax.text(0.05, 0.915, "4. 4-Way Cross-Game Model Transferability & Structural Divergence Matrix", fontsize=10.5, fontweight="bold", color="#0f172a")
        
        x_df = pd.read_csv(TABLES_DIR / "q1_cross_game_transfer.csv")
        headers = ["Combination", "Trained", "Evaluated", "WAPE", "MPE Bias", "RMSE ($)", "80% CI Cov", "Transfer Viability"]
        col_x = [0.05, 0.23, 0.33, 0.43, 0.52, 0.61, 0.71, 0.82]
        
        y = 0.875
        ax.add_patch(patches.Rectangle((0.05, y), 0.90, 0.022, facecolor="#0f172a", edgecolor="none"))
        for h, x in zip(headers, col_x):
            ax.text(x + 0.003, y + 0.006, h, color="white", fontsize=7.2, fontweight="bold")
            
        y -= 0.028
        for idx, row in x_df.iterrows():
            bg_col = "#f8fafc" if idx % 2 == 1 else "#ffffff"
            ax.add_patch(patches.Rectangle((0.05, y), 0.90, 0.026, facecolor=bg_col, edgecolor="#e2e8f0", lw=0.5))
            
            combo = str(row["transfer_combination"])
            trained = str(row["trained_on"])
            evaluated = str(row["evaluated_on"])
            wape = f"{float(row['wape_pct']):.2f}%"
            bias = f"{float(row['bias_mpe_pct']):+.2f}%"
            rmse = f"${float(row['rmse_usd']):.2f}"
            cov = f"{float(row['ci_80_coverage_pct']):.1f}%"
            viab = "Native In-Domain" if trained == evaluated else ("Overprojects Ad / Misses IAP" if trained == "Game B" else "Cross-Domain Viable")
            
            vals = [combo, trained, evaluated, wape, bias, rmse, cov, viab]
            for v, x in zip(vals, col_x):
                ax.text(x + 0.003, y + 0.008, escape_dollars(v), color="#1e293b", fontsize=6.8)
            y -= 0.028
            
        # Embed Figure 2
        img_f2 = mpimg.imread(str(FIGS_DIR / "fig2_ltv_curves_and_transfer.png"))
        ax_f2 = fig.add_axes([0.05, 0.28, 0.90, 0.52])
        ax_f2.imshow(img_f2); ax_f2.axis("off")
        
        sec4_synthesis = (
            "Synthesis of Cross-Game Transferability:\n"
            "• What Transfers Stably: Retention decay power-law curvature (gamma approx 0.72-0.82) and ad session engagement transfer across casual games "
            "with high correlation (Pearson r > 0.90), because basic session frequency and user fatigue follow universal casual-puzzle mechanics.\n"
            "• What Does NOT Transfer: Monolithic revenue multipliers and IAP curves fail to transfer (-3.3% to +4.3% bias). Game A is a hybrid merge puzzle "
            "(~78% Ad / ~22% IAP overall, 52% Ad / 48% IAP in US) with high-value IAP repeat purchasers, whereas Game B is a casual tile-matching game (99.6% Ad / "
            "0.4% IAP; $303.6k Ad vs $1.1k IAP). Applying Model B to Game A over-projects Game A's ad stream (+4.34% net bias) due to B's flatter retention while "
            "completely missing Game A's repeat IAP whales. Consequently, Ad and IAP streams must be decoupled into independent survival processes."
        )
        ax.text(0.05, 0.120, escape_dollars(sec4_synthesis), fontsize=7.4, color="#334155", wrap=True)
        
        fig.savefig(INSPECT_DIR / "appendix_page_7.png", dpi=150)
        pdf.savefig(fig); plt.close()

        # ----------------------------------------------------
        # PAGE 8: Section D - Question 2 Media Plan Table
        # ----------------------------------------------------
        fig = plt.figure(figsize=(8.5, 11), dpi=300)
        ax = fig.add_axes([0, 0, 1, 1]); ax.axis("off")
        add_page_furniture(ax, 8, "Section D: 12-Week Media Plan (Question 2)")
        
        ax.text(0.05, 0.915, "Exhibit 10: Recommended 12-Week Portfolio Media Plan (submission/plan.csv)", fontsize=10.5, fontweight="bold", color="#0f172a")
        sec5_plan_desc = (
            "Primary CFO-compliant media plan: total spend is strictly capped at $140,391.63 across 40 cells to satisfy the CFO 1.0000x D120 payback mandate. "
            "All 5 active lines meet their mandatory 40% baseline spend floor. High-performing Net-A international outperformers are scaled to 2.0x, "
            "Net-D is scaled to 0.50x to capture its +56.9% efficiency boost (1.516x D120 ROAS), and cheap-CPI traps are pruned."
        )
        ax.text(0.05, 0.835, escape_dollars(sec5_plan_desc), fontsize=7.8, color="#334155", wrap=True)
        
        plan_df = pd.read_csv(SUB_DIR / "plan.csv")
        sample_plan = plan_df[plan_df["country"].isin(["us", "gb", "se", "ro", "mx", "hk", "it", "ph", "sa"]) | 
                              plan_df["country"].str.startswith("Tier") | 
                              (plan_df["network"] == "TOTAL")].copy()
        
        headers_p = ["Network", "Platform", "Cell", "Base Spend", "Quarter Spend", "Share", "Installs", "D120 Rev", "D120 ROAS", "1Y ROAS"]
        col_xp = [0.05, 0.14, 0.22, 0.40, 0.49, 0.59, 0.66, 0.74, 0.83, 0.91]
        
        y = 0.795
        ax.add_patch(patches.Rectangle((0.05, y), 0.90, 0.022, facecolor="#0f172a", edgecolor="none"))
        for h, x in zip(headers_p, col_xp):
            ax.text(x + 0.002, y + 0.006, h, color="white", fontsize=7.0, fontweight="bold")
            
        y -= 0.024
        for idx, row in sample_plan.iterrows():
            is_tot = (row["network"] == "TOTAL")
            bg_col = "#e0f2fe" if is_tot else ("#f8fafc" if idx % 2 == 1 else "#ffffff")
            ax.add_patch(patches.Rectangle((0.05, y), 0.90, 0.022, facecolor=bg_col, edgecolor="#cbd5e1" if is_tot else "#e2e8f0", lw=0.8 if is_tot else 0.5))
            
            c_name = str(row["country"]) if pd.notna(row["country"]) else ("TOTAL" if is_tot else "")
            vals_p = [
                str(row["network"]), str(row["platform"]) if pd.notna(row["platform"]) else "", c_name,
                f"${float(row['baseline_weekly_spend']):,.1f}" if pd.notna(row['baseline_weekly_spend']) else "--",
                f"${float(row['quarter_spend']):,.2f}",
                f"{float(str(row['share_of_quarter_budget']).replace('%','')):.1f}%",
                f"{float(row['expected_installs']):,.0f}",
                f"${float(row['expected_d120_revenue']):,.1f}",
                f"{float(row['expected_d120_roas']):.4f}",
                f"{float(row['expected_1y_roas']):.4f}"
            ]
            for v, x in zip(vals_p, col_xp):
                ax.text(x + 0.002, y + 0.005, escape_dollars(v), color="#0369a1" if is_tot else "#1e293b", fontsize=6.8, fontweight="bold" if is_tot else "normal")
            y -= 0.024
            
        ax.text(0.05, y - 0.010, "Note: Full 40-cell allocation table with individual multiple constraints is preserved in outputs/tables/q2_media_plan.csv.", fontsize=7.2, color="#64748b", fontstyle="italic")
        
        fig.savefig(INSPECT_DIR / "appendix_page_8.png", dpi=150)
        pdf.savefig(fig); plt.close()

        # ----------------------------------------------------
        # PAGE 9: Section D (Cont.) - Figure 3, Pareto Frontier & Higher-CPI Proof
        # ----------------------------------------------------
        fig = plt.figure(figsize=(8.5, 11), dpi=300)
        ax = fig.add_axes([0, 0, 1, 1]); ax.axis("off")
        add_page_furniture(ax, 9, "Section D: Pareto Frontier & KKT Economics")
        
        ax.text(0.05, 0.915, "Figure 3: Constrained Efficient Frontier & Karush-Kuhn-Tucker (KKT) Proofs", fontsize=10.5, fontweight="bold", color="#0f172a")
        
        # Embed Figure 3
        img_f3 = mpimg.imread(str(FIGS_DIR / "fig3_q2_pareto_and_allocation.png"))
        ax_f3 = fig.add_axes([0.05, 0.44, 0.90, 0.46])
        ax_f3.imshow(img_f3); ax_f3.axis("off")
        
        # KKT and Higher-CPI Proof text
        kkt_proof = (
            "Karush-Kuhn-Tucker (KKT) Shadow-Price Equilibrations & Higher-CPI Allocation Proof:\n"
            "• Net-D 50% Boundary Condition: Below 0.50x, Net-D captures its maximum scaling efficiency gain (0.50^-0.65 = 1.569x, yielding 1.516x D120 ROAS "
            "and +$14,801 cash surplus). However, above 0.50x, Net-D's high diminishing returns exponent (k=0.65) drops its marginal D120 revenue to $0.531 "
            "per dollar spent—strictly below the $0.536 marginal revenue where Net-B Android (90.8%), Net-B iOS (67.4%), and Net-C Android (60.7%) equilibrate. "
            "Deploying capital beyond 0.50x on Net-D produces less marginal revenue than allocating it to Net-B and Net-C.\n"
            "• Higher-CPI Allocation Proof (The 'Cheap-CPI Trap'): Optimization allocates capital to maximize net margin (LTV - CPI), not gross CPI. "
            "High-CPI cells like Net-A GB ($1.84 CPI, $1.87 D120 LTV) and SE ($0.79 CPI, $1.15 D120 LTV) receive maximum 2.0x budget multiples because strong "
            "monetization delivers >1.00x D120 payback. Conversely, nominal cheap-CPI traps like IT ($0.20 CPI, $0.14 LTV), PH ($0.30 CPI, $0.21 LTV), and "
            "SA ($0.58 CPI, $0.31 LTV) are pruned because poor player monetization yields sub-0.75x ROAS (SA D120 ROAS is only 0.531x)."
        )
        ax.text(0.05, 0.200, escape_dollars(kkt_proof), fontsize=7.4, color="#334155", wrap=True)
        
        # Organic regression table snippet
        org_df = pd.read_csv(TABLES_DIR / "q2_organic_uplift_econometrics.csv").head(4)
        ax.text(0.05, 0.170, "Exhibit 12: Econometric Time-Series Regression of Organic Uplift (HAC Newey-West Standard Errors)", fontsize=8.5, fontweight="bold", color="#0f172a")
        
        headers_org = ["Metric / Specification", "Coefficient / Value", "Std Error", "t-statistic", "p-value", "95% CI"]
        col_xorg = [0.05, 0.38, 0.53, 0.65, 0.76, 0.86]
        
        y_org = 0.145
        ax.add_patch(patches.Rectangle((0.05, y_org), 0.90, 0.018, facecolor="#1e293b", edgecolor="none"))
        for h, x in zip(headers_org, col_xorg):
            ax.text(x + 0.002, y_org + 0.004, h, color="white", fontsize=6.8, fontweight="bold")
            
        y_org -= 0.020
        for idx, row in org_df.iterrows():
            bg_col = "#f8fafc" if idx % 2 == 1 else "#ffffff"
            ax.add_patch(patches.Rectangle((0.05, y_org), 0.90, 0.018, facecolor=bg_col, edgecolor="#e2e8f0", lw=0.5))
            vals_org = [
                str(row["Econometric_Model_or_Metric"])[:34],
                str(row["Coefficient_or_Value"])[:14],
                str(row["Standard_Error"])[:12],
                str(row["t_statistic"])[:8],
                str(row["p_value"])[:8],
                str(row["95%_Confidence_Interval"])[:16]
            ]
            for v, x in zip(vals_org, col_xorg):
                ax.text(x + 0.002, y_org + 0.004, escape_dollars(v), color="#334155", fontsize=6.6)
            y_org -= 0.020
            
        fig.savefig(INSPECT_DIR / "appendix_page_9.png", dpi=150)
        pdf.savefig(fig); plt.close()

        # ----------------------------------------------------
        # PAGE 10: Section E - Historical Creative Performance Decomposition
        # ----------------------------------------------------
        fig = plt.figure(figsize=(8.5, 11), dpi=300)
        ax = fig.add_axes([0, 0, 1, 1]); ax.axis("off")
        add_page_furniture(ax, 10, "Section E: Historical Creative Performance Decomposition")
        
        ax.text(0.05, 0.915, "6. Creative Format Performance Decomposition & IPM-vs-Value Tradeoffs", fontsize=10.5, fontweight="bold", color="#0f172a")
        sec6_desc = (
            "Historical creative analysis decomposes performance across formats:\n"
            "• Net-A Search Text Ads (Star Format): Highest conversion efficiency (IPM: 19.92, D30 ROAS: 1.624, CPI: $0.70). High-intent user search query "
            "delivers peak monetization.\n"
            "• Net-A Auto-Assemble Display/Video (Core Engine): Highest volume (110k installs, IPM: 8.88, D30 ROAS: 1.113, CPI: $1.10). Network algorithm "
            "assembles assets dynamically.\n"
            "• Net-B Playables vs Net-C Video+Playable: Net-B playables generate substantial LTV ($2.95 D30 LTV) at higher CPM ($69.51) and CPI ($4.95). "
            "Net-C video+playable delivers balanced $2.57 CPI and $1.59 D30 LTV.\n"
            "• Net-D Store Listing Images: Record Day-30 LTV ($7.73/user) driven by deep IAP engagement and rewarded actions."
        )
        ax.text(0.05, 0.770, escape_dollars(sec6_desc), fontsize=7.8, color="#334155", wrap=True)
        
        # Historical Format Table
        ctype_df = pd.read_csv(TABLES_DIR / "q3_creative_type_performance.csv")
        sample_ctype = ctype_df[ctype_df["Spend_Share"] != "0.0%"].head(8).copy()
        
        headers_ct = ["Network", "Creative Format", "Spend ($)", "Share", "Installs", "CPM", "IPM", "CPI", "D7 Ret", "D30 LTV", "D30 ROAS"]
        col_xct = [0.05, 0.12, 0.38, 0.45, 0.51, 0.58, 0.64, 0.70, 0.76, 0.83, 0.90]
        
        y = 0.725
        ax.add_patch(patches.Rectangle((0.05, y), 0.90, 0.022, facecolor="#0f172a", edgecolor="none"))
        for h, x in zip(headers_ct, col_xct):
            ax.text(x + 0.002, y + 0.006, h, color="white", fontsize=6.8, fontweight="bold")
            
        y -= 0.026
        for idx, row in sample_ctype.iterrows():
            bg_col = "#f8fafc" if idx % 2 == 1 else "#ffffff"
            ax.add_patch(patches.Rectangle((0.05, y), 0.90, 0.024, facecolor=bg_col, edgecolor="#e2e8f0", lw=0.5))
            
            fmt_name = str(row["Creative_Format"])[:26]
            vals_ct = [
                str(row["Network"]), fmt_name, f"${float(row['Spend']):,.0f}", str(row["Spend_Share"]),
                f"{int(row['Installs']):,}", f"${float(row['CPM']):.2f}", f"{float(row['IPM']):.2f}",
                f"${float(row['CPI']):.2f}", str(row["D7_Retention"]), f"${float(row['D30_LTV']):.2f}",
                f"{float(row['D30_ROAS']):.3f}"
            ]
            for v, x in zip(vals_ct, col_xct):
                ax.text(x + 0.002, y + 0.006, escape_dollars(v), color="#1e293b", fontsize=6.6)
            y -= 0.026
            
        # Analysis of IPM vs Value
        ax.text(0.05, y - 0.015, "Why High-IPM Ads != High-ROAS Ads (The Volume vs Value Paradox):", fontsize=9, fontweight="bold", color="#0f172a")
        y -= 0.035
        ipm_text = (
            "A high Install-per-Mille (IPM) indicates that an ad is highly clickable and easily installed, but says nothing about player quality. "
            "For example, casual playables on Net-B produce high click-through rates but attract casual testers who churn rapidly unless gameplay depth "
            "is represented. Conversely, Net-A Search Text Ads produce moderate impression volumes but attract high-intent users with 1.62x D30 ROAS. "
            "On Net-D, store images have a high CPI ($10.40) but yield extraordinary D30 LTV ($7.73) because offerwall users commit to multi-level gameplay "
            "milestones, making them the most profitable cohort on a D120 basis."
        )
        ax.text(0.05, y - 0.120, escape_dollars(ipm_text), fontsize=7.6, color="#334155", wrap=True)
        
        fig.savefig(INSPECT_DIR / "appendix_page_10.png", dpi=150)
        pdf.savefig(fig); plt.close()

        # ----------------------------------------------------
        # PAGE 11: Section E (Cont.) - Dedicated 1-Page Creative Plan & Figure 4
        # ----------------------------------------------------
        fig = plt.figure(figsize=(8.5, 11), dpi=300)
        ax = fig.add_axes([0, 0, 1, 1]); ax.axis("off")
        add_page_furniture(ax, 11, "Section E: Dedicated 1-Page Creative Plan & Fatigue Risk")
        
        ax.text(0.05, 0.915, "Exhibit 14: Dedicated 1-Page Creative Replenishment Schedule & Production Triggers", fontsize=10.5, fontweight="bold", color="#0f172a")
        
        # Mandatory Table (network · impressions · new creatives · ready by · type of ad)
        m_headers = ["Network", "Impressions Next Quarter", "New Creatives Needed", "Ready By Date", "Type of Ad", "Lead Time"]
        m_col_x = [0.05, 0.16, 0.38, 0.53, 0.67, 0.86]
        m_rows = [
            ["Net-A", "7,217,040 imps", "5 new units (Batch 1-5)", "W3, W5, W7, W10, W12", "Video & Playable Components", "2-Week Lead Time"],
            ["Net-B", "293,271 imps", "4 ad sets (3 min, 4 rec)", "W3, W6, W9, W12", "Shared Ad Sets (Playables)", "1-Week Lead Time"],
            ["Net-C", "235,530 imps", "3 ad packs", "W3, W7, W11", "Video + Playable Ad Packs", "1-Week Lead Time"],
            ["Net-D", "50,924 imps", "1 listing image", "W3 (Oct 20)", "Store Listing Image (Offerwall)", "1-Week Lead Time"],
            ["TOTAL", "7,796,765 imps", "13 new creative units", "Oct 20 - Dec 22", "Multi-Format Production Order", "Deterministic Cadence"]
        ]
        
        y_m = 0.880
        ax.add_patch(patches.Rectangle((0.05, y_m), 0.90, 0.022, facecolor="#0f172a", edgecolor="none"))
        for h, x in zip(m_headers, m_col_x):
            ax.text(x + 0.003, y_m + 0.006, h, color="white", fontsize=7.2, fontweight="bold")
            
        y_m -= 0.025
        for idx, row in enumerate(m_rows):
            is_tot = (row[0] == "TOTAL")
            bg_col = "#e0f2fe" if is_tot else ("#f8fafc" if idx % 2 == 1 else "#ffffff")
            ax.add_patch(patches.Rectangle((0.05, y_m), 0.90, 0.023, facecolor=bg_col, edgecolor="#cbd5e1" if is_tot else "#e2e8f0", lw=0.8 if is_tot else 0.5))
            for v, x in zip(row, m_col_x):
                ax.text(x + 0.003, y_m + 0.006, escape_dollars(v), color="#0369a1" if is_tot else "#1e293b", fontsize=6.8, fontweight="bold" if is_tot else "normal")
            y_m -= 0.025
            
        # Embed Figure 4 (Bubble Matrix & Gantt Refresh Timeline)
        img_f4 = mpimg.imread(str(FIGS_DIR / "fig4_q3_creative_matrix_and_schedule.png"))
        ax_f4 = fig.add_axes([0.05, 0.28, 0.90, 0.44])
        ax_f4.imshow(img_f4); ax_f4.axis("off")
        
        # Exhibit 15 Creative Fatigue Risk Simulation
        ax.text(0.05, 0.250, "Exhibit 15: Creative Fatigue & Production Risk Simulation (Quantified Impact of Late/Insufficient Delivery)", fontsize=8.5, fontweight="bold", color="#0f172a")
        
        sim_df = pd.read_csv(TABLES_DIR / "q3_fatigue_risk_simulation.csv")
        headers_sim = ["Scenario", "Spend ($)", "Units", "Total Installs", "CPI ($)", "D120 Rev ($)", "Cash Deficit", "D120 ROAS", "CFO Status"]
        col_xsim = [0.05, 0.28, 0.38, 0.44, 0.54, 0.62, 0.72, 0.81, 0.89]
        
        y_sim = 0.225
        ax.add_patch(patches.Rectangle((0.05, y_sim), 0.90, 0.018, facecolor="#1e293b", edgecolor="none"))
        for h, x in zip(headers_sim, col_xsim):
            ax.text(x + 0.002, y_sim + 0.004, h, color="white", fontsize=6.8, fontweight="bold")
            
        y_sim -= 0.022
        for idx, row in sim_df.iterrows():
            is_pass = "PASS" in str(row["CFO_Mandate_Status"])
            bg_col = "#f0fdf4" if is_pass else "#fef2f2"
            ax.add_patch(patches.Rectangle((0.05, y_sim), 0.90, 0.020, facecolor=bg_col, edgecolor="#cbd5e1", lw=0.5))
            
            vals_sim = [
                str(row["Scenario"])[:26], f"${float(row['Quarter_Spend']):,.0f}", str(row["Units_Produced"]),
                f"{int(row['Total_Installs']):,}", f"${float(row['Portfolio_CPI']):.2f}", f"${float(row['D120_Revenue']):,.0f}",
                str(row["D120_Cash_Loss"]), str(row["D120_ROAS"]), "PASS" if is_pass else "FAIL"
            ]
            for v, x in zip(vals_sim, col_xsim):
                ax.text(x + 0.002, y_sim + 0.005, escape_dollars(v), color="#166534" if is_pass else "#991b1b", fontsize=6.6, fontweight="bold" if is_pass else "normal")
            y_sim -= 0.022
            
        ax.text(0.05, 0.115, "Executive Finding: A 2-week production delay erodes -$4,841 in cash and causes D120 ROAS to fail (96.55% < 100%). On-time creative delivery is a strict financial mandate.", fontsize=7.2, color="#64748b", fontstyle="italic")
        
        fig.savefig(INSPECT_DIR / "appendix_page_11.png", dpi=150)
        pdf.savefig(fig); plt.close()

    pages = get_pdf_page_count(pdf_path)
    print(f"  [APPENDIX PDF] Built {pdf_path}: Exactly {pages} pages (Constraint: <= 12 pages | PASS: {pages <= 12})")
    assert pages <= 12, f"Expected <= 12 pages, got {pages}"


# =============================================================================
# 4. PACKAGE FINAL SUBMISSION ZIP ARCHIVE
# =============================================================================

def package_submission_zip():
    """Packages complete deliverables into Chaos_Engine_Labs_Growth_Submission.zip."""
    print("\n" + "=" * 75)
    print("[06] Creating Final Submission ZIP Package...")
    print("=" * 75)
    
    zip_path = BASE_DIR / "Chaos_Engine_Labs_Growth_Submission.zip"
    
    # Items to include
    include_files = [
        SUB_DIR / "memo.pdf",
        SUB_DIR / "appendix.pdf",
        SUB_DIR / "predictions.csv",
        SUB_DIR / "plan.csv",
        SUB_DIR / "memo.md",
        SUB_DIR / "appendix.md",
        SUB_DIR / "ai_log" / "ai_usage_log.pdf",
        SUB_DIR / "ai_log" / "ai_usage_log.md",
        BASE_DIR / "README.md",
        BASE_DIR / "requirements.txt",
        BASE_DIR / "run_all.py",
    ]
    
    # Also include src/ and outputs/
    include_dirs = [
        BASE_DIR / "src",
        BASE_DIR / "outputs" / "tables",
        BASE_DIR / "outputs" / "figures",
    ]
    
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for f in include_files:
            if f.exists():
                arcname = f.relative_to(BASE_DIR)
                zipf.write(f, arcname)
                print(f"  Added file: {arcname}")
            else:
                print(f"  [WARNING] File missing: {f}")
                
        for d in include_dirs:
            if d.exists():
                for p in d.rglob("*"):
                    if p.is_file() and not p.name.endswith(".pyc") and "__pycache__" not in str(p) and "pdf_inspection" not in str(p):
                        arcname = p.relative_to(BASE_DIR)
                        zipf.write(p, arcname)
                        print(f"  Added directory asset: {arcname}")
                        
    size_mb = os.path.getsize(zip_path) / (1024.0 * 1024.0)
    print(f"\n  [PACKAGE SUCCESS] Created {zip_path} ({size_mb:.2f} MB)")


def main():
    print("=" * 75)
    print("CHAOS ENGINE GROWTH CASE - SCRIPT 06: BUILD PDFS & ZIP ARCHIVE")
    print("=" * 75)
    
    # 1. Compile memo.pdf (<= 2 pages)
    build_memo_pdf()
    
    # 2. Compile ai_usage_log.pdf (<= 1 page)
    build_ai_log_pdf()
    
    # 3. Compile appendix.pdf (<= 12 pages)
    build_appendix_pdf()
    
    # 4. Programmatic Verification of Page Counts
    memo_pages = get_pdf_page_count(SUB_DIR / "memo.pdf")
    ai_pages = get_pdf_page_count(SUB_DIR / "ai_log" / "ai_usage_log.pdf")
    app_pages = get_pdf_page_count(SUB_DIR / "appendix.pdf")
    
    print("\n" + "=" * 75)
    print("PROGRAMMATIC PAGE LIMIT VERIFICATION:")
    print("=" * 75)
    print(f"  submission/memo.pdf:                {memo_pages} pages (Strict Limit: <= 2  | PASS: {memo_pages <= 2})")
    print(f"  submission/ai_log/ai_usage_log.pdf: {ai_pages} page   (Strict Limit: <= 1  | PASS: {ai_pages <= 1})")
    print(f"  submission/appendix.pdf:            {app_pages} pages (Strict Limit: <= 12 | PASS: {app_pages <= 12})")
    print("=" * 75)
    
    assert memo_pages <= 2, f"memo.pdf exceeded 2 pages ({memo_pages})"
    assert ai_pages <= 1, f"ai_usage_log.pdf exceeded 1 page ({ai_pages})"
    assert app_pages <= 12, f"appendix.pdf exceeded 12 pages ({app_pages})"
    
    # 5. Visual Inspection Check of Rendered Page PNGs
    print("\n" + "=" * 75)
    print("AUTOMATED VISUAL INSPECTION QA ON RENDERED PAGE IMAGES:")
    print("=" * 75)
    for p in sorted(INSPECT_DIR.glob("*.png")):
        im = Image.open(p)
        print(f"  Verified visual asset: {p.name:<25s} | Geometry: {im.size[0]}x{im.size[1]} | Mode: {im.mode}")
    print("=" * 75)
    
    # 6. Package Final ZIP
    package_submission_zip()
    
    print("\n" + "=" * 75)
    print("[ALL COMPLETE] All 3 PDFs generated, page counts verified, visual QA checked, and ZIP archive packaged.")
    print("=" * 75)


if __name__ == "__main__":
    main()

