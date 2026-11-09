"""
Script 06: Compile Publication-Ready PDFs & Final Submission Package
Chaos Engine Labs Growth Case

Full Production Implementation:
1. Compiles submission/memo.pdf:
   - Strictly <= 2 pages.
   - Starts with the mandatory 5 CFO lines on Page 1.
   - Embeds KKT optimality economics, cheap-CPI trap analysis, and portfolio efficient frontier.
2. Compiles submission/appendix.pdf:
   - Strictly <= 12 pages (compiled to exactly 10 pages).
   - Embeds all 5 high-DPI charts from outputs/figures/ and supporting tables for Q1, Q2, and Q3.
3. Compiles submission/ai_log/ai_usage_log.pdf:
   - Strictly <= 1 page.
   - Documents real debugging audit (censored-median contamination, single-day payer window,
     unconditioned P7/P8 partial age, Simpson's paradox on Net-A Non-US).
4. Verifies page limits programmatically.
5. Packages complete deliverables into Chaos_Engine_Labs_Growth_Submission.zip.
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

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

from src.config import SUB_DIR, FIGS_DIR, TABLES_DIR, PROC_DIR, BASE_DIR


def escape_dollars(s: object) -> str:
    """Escapes unescaped dollar signs for Matplotlib text rendering to prevent mathtext parser syntax errors."""
    return str(s).replace(r"\$", "$").replace("$", r"\$")


def get_pdf_page_count(pdf_path: Path) -> int:
    """Reads PDF page count in pure Python via binary object scanning."""
    with open(pdf_path, "rb") as f:
        data = f.read()
    # Match /Type /Page (excluding /Pages)
    pages = len(re.findall(rb"/Type\s*/Page\b", data))
    return pages


def compile_memo_pdf():
    """Generates submission/memo.pdf (strictly 2 pages)."""
    print("\n" + "=" * 70)
    print("[06] Compiling submission/memo.pdf (Strictly 2 Pages)...")
    print("=" * 70)
    
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
        
        pdf.savefig(fig2)
        plt.close()
        
    pages = get_pdf_page_count(pdf_path)
    print(f"  [MEMO PDF] Built {pdf_path}: Exactly {pages} pages (Constraint: <= 2 pages | PASS: {pages <= 2})")
    assert pages == 2, f"Expected exactly 2 pages, got {pages}"


def compile_ai_log_pdf():
    """Generates submission/ai_log/ai_usage_log.pdf (strictly 1 page)."""
    print("\n" + "=" * 70)
    print("[06] Compiling submission/ai_log/ai_usage_log.pdf (Strictly 1 Page)...")
    print("=" * 70)
    
    pdf_path = SUB_DIR / "ai_log" / "ai_usage_log.pdf"
    
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
        
        pdf.savefig(fig)
        plt.close()
        
    pages = get_pdf_page_count(pdf_path)
    print(f"  [AI LOG PDF] Built {pdf_path}: Exactly {pages} page (Constraint: <= 1 page | PASS: {pages <= 1})")
    assert pages == 1, f"Expected exactly 1 page, got {pages}"


def compile_appendix_pdf():
    """Generates submission/appendix.pdf (strictly <= 12 pages; compiled to 10 pages)."""
    print("\n" + "=" * 70)
    print("[06] Compiling submission/appendix.pdf (Strictly <= 12 Pages)...")
    print("=" * 70)
    
    pdf_path = SUB_DIR / "appendix.pdf"
    
    with PdfPages(pdf_path) as pdf:
        # Helper for page headers and footers
        def add_page_furniture(ax, page_num, total_pages, title):
            ax.add_patch(patches.Rectangle((0.05, 0.945), 0.90, 0.030, facecolor="#1b263b", edgecolor="none"))
            ax.text(0.07, 0.953, f"TECHNICAL APPENDIX: {title.upper()}", color="white", fontsize=9.5, fontweight="bold")
            ax.text(0.05, 0.025, "Chaos Engine Labs Growth Case | Technical Appendix", fontsize=8, color="#94a3b8")
            ax.text(0.88, 0.025, f"Page {page_num} of {total_pages}", fontsize=8, fontweight="bold", color="#94a3b8")

        # ----------------------------------------------------
        # PAGE 1: Overview & Section 1 Data Audit Reconciliations
        # ----------------------------------------------------
        fig = plt.figure(figsize=(8.5, 11), dpi=300)
        ax = fig.add_axes([0, 0, 1, 1]); ax.axis("off")
        add_page_furniture(ax, 1, 10, "Overview & Data Audit Framework")
        
        ax.text(0.05, 0.900, "Technical Appendix: Quantitative Methodologies & Proofs", fontsize=13, fontweight="bold", color="#0f172a")
        ax.text(0.05, 0.880, "Case: Chaos Engine Labs Games A & B   |   Lead Analyst: Head of Growth   |   As of: September 30, 2025", fontsize=8, color="#64748b")
        
        # Table of contents box
        ax.add_patch(patches.Rectangle((0.05, 0.730), 0.90, 0.135, facecolor="#f8fafc", edgecolor="#cbd5e1", lw=0.8))
        ax.text(0.07, 0.840, "TABLE OF CONTENTS", fontsize=9, fontweight="bold", color="#0f172a")
        toc = [
            "1. Data Audit & Deterministic Anomaly Resolution (Exhibit 1 Log)",
            "2. Market Cell Taxonomy & Baseline Economics (Exhibits 2 & 3)",
            "3. Dual-Stream Parametric LTV & ROAS Modeling (Question 1, P1-P8 Predictions)",
            "4. Cross-Game Model Transferability & Structural Divergence Matrix",
            "5. Constrained Media Plan Optimization & Organic Halo (Question 2, KKT Economics)",
            "6. Creative Fatigue Dynamics & Replenishment Schedule (Question 3, 12-Week Production)"
        ]
        ty = 0.820
        for item in toc:
            ax.text(0.07, ty, f"• {item}", fontsize=7.5, color="#334155")
            ty -= 0.016
            
        ax.text(0.05, 0.690, "1. Forensic Data Audit & Deterministic Reconciliation Summary", fontsize=11, fontweight="bold", color="#0f172a")
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
        pdf.savefig(fig); plt.close()

        # ----------------------------------------------------
        # PAGE 2: Section 1 (Cont.) Exhibit 1 Audit Table
        # ----------------------------------------------------
        fig = plt.figure(figsize=(8.5, 11), dpi=300)
        ax = fig.add_axes([0, 0, 1, 1]); ax.axis("off")
        add_page_furniture(ax, 2, 10, "Exhibit 1: Forensic Data Problems Audit Log")
        
        ax.text(0.05, 0.915, "Exhibit 1: Quantitative Audit Log of All 8 Data Problems & Deterministic Repairs", fontsize=10.5, fontweight="bold", color="#0f172a")
        
        audit_df = pd.read_csv(TABLES_DIR / "q1_data_problems_audit.csv")
        # Render table
        headers = ["ID", "Game", "Problem Name", "Where Found", "What It Distorts", "Dollar / ROAS Impact"]
        col_w = [0.03, 0.06, 0.22, 0.22, 0.22, 0.15]
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
                
        pdf.savefig(fig); plt.close()

        # ----------------------------------------------------
        # PAGE 3: Section 2 Market Cell Taxonomy & Baseline Economics
        # ----------------------------------------------------
        fig = plt.figure(figsize=(8.5, 11), dpi=300)
        ax = fig.add_axes([0, 0, 1, 1]); ax.axis("off")
        add_page_furniture(ax, 3, 10, "Market Cell Taxonomy & Baseline Economics")
        
        ax.text(0.05, 0.915, "2. Market Cell Taxonomy & Baseline Period Calibration", fontsize=10.5, fontweight="bold", color="#0f172a")
        sec2_desc = (
            "Baseline economics are established over September 1 to September 28, 2025 (4 full weeks = 28 days; weekly baseline = Sep sum / 4.0).\n"
            "• Game A (40 Active Cells): Net-A Android is structured into 32 major individual countries and 4 regional tiers (Tier 1 Affluent West, "
            "Tier 2 East Asia & GCC, Tier 3 LatAm & East Europe, Tier 4 Emerging RoW). Net-B Android US, Net-B iOS US, Net-C Android US, and Net-D Android US "
            "form the remaining active lines. Total baseline weekly spend = $15,193.72 ($182,324.64 12-week baseline).\n"
            "• Game B (28 Cells & Paused Networks): Explicit tracking of paused network test dates: Net-C paused on 2025-02-12; Net-F paused on 2025-03-31; "
            "Net-E paused on 2025-05-28; Net-D paused on 2025-08-25. Active channels in September: Net-A Android, Net-B Android, Net-B iOS."
        )
        ax.text(0.05, 0.810, escape_dollars(sec2_desc), fontsize=7.8, color="#334155", wrap=True)
        
        # Table snippet of Game A Baseline Cell Values
        ax.text(0.05, 0.770, "Exhibit 2: Core Game A Active UA Lines Baseline Summary (Sep 1-28, 2025)", fontsize=9, fontweight="bold", color="#0f172a")
        ga_cells = pd.read_csv(TABLES_DIR / "q1_gameA_cell_values.csv")
        sample_rows = ga_cells[ga_cells["country_cell"].isin(["us", "TOTAL", "all countries except United States"]) | 
                               ga_cells["country_cell"].str.startswith("Tier")].copy()
        
        headers = ["Network", "Platform", "Cell / Region", "Weekly Spend", "Base CPI", "Pred D120 ROAS", "Pred 1Y ROAS", "Payback Classification"]
        col_x = [0.05, 0.15, 0.24, 0.44, 0.54, 0.63, 0.72, 0.81]
        
        y = 0.740
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
            
        pdf.savefig(fig); plt.close()

        # ----------------------------------------------------
        # PAGE 4: Section 3 Dual-Stream LTV & ROAS Modeling (Question 1)
        # ----------------------------------------------------
        fig = plt.figure(figsize=(8.5, 11), dpi=300)
        ax = fig.add_axes([0, 0, 1, 1]); ax.axis("off")
        add_page_furniture(ax, 4, 10, "Dual-Stream LTV & Survival Curves")
        
        ax.text(0.05, 0.915, "3. Decoupled Dual-Stream LTV Architecture (Question 1)", fontsize=10.5, fontweight="bold", color="#0f172a")
        sec3_desc = (
            "Player lifetime value is modeled as the decoupled sum of independent Ad and IAP survival processes: LTV(t) = LTV_ad(t) + LTV_iap(t).\n"
            "• Retention Modeling: Retention decay follows a modified power-law survival curve S(t) = (1 + beta*t)^(-gamma). Game A fits beta=11.48, "
            "gamma=0.524, tail multiplier=2.28. Game B exhibits flatter retention decay (gamma=0.465), yielding +64% higher retention at Day 120.\n"
            "• Ad Stream: Ad monetization scales with active sessions: LTV_ad(t) = cumulative_sessions(t) * eCPM * ad_units_per_session.\n"
            "• IAP Stream: IAP monetization is modeled via an Empirical Bayes shifted lognormal/exponential process with shrinkage across small cells.\n"
            "• Monetization Contrast: Game A is a balanced hybrid (52% Ad / 48% IAP in US), whereas Game B is a pure ad engine (99.6% Ad / 0.4% IAP)."
        )
        ax.text(0.05, 0.770, sec3_desc, fontsize=7.8, color="#334155", wrap=True)
        
        # Embed LTV Growth Curves Chart
        img_ltv = mpimg.imread(str(FIGS_DIR / "q1_ltv_growth_curves.png"))
        ax_ltv = fig.add_axes([0.05, 0.18, 0.90, 0.55])
        ax_ltv.imshow(img_ltv)
        ax_ltv.axis("off")
        
        ax.text(0.05, 0.120, "Figure 1: Dual-Stream Parametric LTV Extrapolation Curves for Game A (Hybrid) vs Game B (Pure Ad).", fontsize=8, color="#64748b", fontstyle="italic")
        pdf.savefig(fig); plt.close()

        # ----------------------------------------------------
        # PAGE 5: Section 3 (Cont.) Official Predictions P1-P8
        # ----------------------------------------------------
        fig = plt.figure(figsize=(8.5, 11), dpi=300)
        ax = fig.add_axes([0, 0, 1, 1]); ax.axis("off")
        add_page_furniture(ax, 5, 10, "Official Predictions P1-P8 & Credible Intervals")
        
        ax.text(0.05, 0.915, "Official Submission Predictions (P1–P8 in submission/predictions.csv)", fontsize=10.5, fontweight="bold", color="#0f172a")
        p_desc = (
            "All predictions are strictly conditioned upon realized cumulative revenue banked as of September 30, 2025. Cohorts for P1-P6 are 16 to 29 days "
            "old (D14 fully observed + partial age banked). Cohorts for P7-P8 are 44 to 57 days old (D30 fully observed + partial age banked). "
            "Monotonicity is mathematically guaranteed: Obs_Prev < Banked_Sep30 < low_80 < prediction < high_80. 80% credible intervals are calibrated via "
            "conformal rolling residual quantiles, achieving honest 79.2% empirical coverage across historical holdout cohorts."
        )
        ax.text(0.05, 0.835, p_desc, fontsize=7.8, color="#334155", wrap=True)
        
        preds_df = pd.read_csv(SUB_DIR / "predictions.csv")
        headers = ["ID", "Cell / Line", "Target", "Obs Prev", "Banked Sep30", "Prediction", "Low 80", "High 80", "Methodology Note"]
        col_x = [0.05, 0.10, 0.34, 0.42, 0.50, 0.59, 0.67, 0.74, 0.81]
        
        y = 0.800
        ax.add_patch(patches.Rectangle((0.05, y), 0.90, 0.024, facecolor="#0f172a", edgecolor="none"))
        for h, x in zip(headers, col_x):
            ax.text(x + 0.003, y + 0.007, h, color="white", fontsize=7.2, fontweight="bold")
            
        y -= 0.052
        for idx, row in preds_df.iterrows():
            bg_col = "#f8fafc" if idx % 2 == 1 else "#ffffff"
            ax.add_patch(patches.Rectangle((0.05, y), 0.90, 0.048, facecolor=bg_col, edgecolor="#e2e8f0", lw=0.5))
            
            p_id = str(row["id"])
            p_cell = str(row["cell"])[:30]
            p_metric = str(row["metric"])
            # Format numbers using robust regex
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
                ax.text(x + 0.003, y + 0.018, escape_dollars(v), color="#0369a1" if is_pred else "#1e293b", fontsize=6.8, fontweight="bold" if is_pred else "normal")
            y -= 0.052
            
        pdf.savefig(fig); plt.close()

        # ----------------------------------------------------
        # PAGE 6: Section 4 Cross-Game Model Transferability
        # ----------------------------------------------------
        fig = plt.figure(figsize=(8.5, 11), dpi=300)
        ax = fig.add_axes([0, 0, 1, 1]); ax.axis("off")
        add_page_furniture(ax, 6, 10, "Cross-Game Model Transferability")
        
        ax.text(0.05, 0.915, "4. Cross-Game Transfer Matrix & Structural Divergence Drivers", fontsize=10.5, fontweight="bold", color="#0f172a")
        
        x_df = pd.read_csv(TABLES_DIR / "q1_cross_game_transfer.csv")
        headers = ["Combination", "Trained", "Evaluated", "WAPE", "MPE Bias", "RMSE ($)", "80% CI Cov", "Transfer Viability"]
        col_x = [0.05, 0.23, 0.33, 0.43, 0.52, 0.61, 0.71, 0.82]
        
        y = 0.865
        ax.add_patch(patches.Rectangle((0.05, y), 0.90, 0.024, facecolor="#0f172a", edgecolor="none"))
        for h, x in zip(headers, col_x):
            ax.text(x + 0.003, y + 0.007, h, color="white", fontsize=7.2, fontweight="bold")
            
        y -= 0.035
        for idx, row in x_df.iterrows():
            bg_col = "#f8fafc" if idx % 2 == 1 else "#ffffff"
            ax.add_patch(patches.Rectangle((0.05, y), 0.90, 0.032, facecolor=bg_col, edgecolor="#e2e8f0", lw=0.5))
            
            combo = str(row["transfer_combination"])
            trained = str(row["trained_on"])
            evaluated = str(row["evaluated_on"])
            wape = f"{float(row['wape_pct']):.2f}%"
            bias = f"{float(row['bias_mpe_pct']):.2f}%"
            rmse = f"${float(row['rmse_usd']):.2f}"
            cov = f"{float(row['ci_80_coverage_pct']):.1f}%"
            viab = "Native In-Domain" if trained == evaluated else ("Overprojects Ad / Misses IAP" if trained == "Game B" else "Cross-Domain Viable")
            
            vals = [combo, trained, evaluated, wape, bias, rmse, cov, viab]
            for v, x in zip(vals, col_x):
                ax.text(x + 0.003, y + 0.010, escape_dollars(v), color="#1e293b", fontsize=7.0)
            y -= 0.035
            
        sec4_narrative = (
            "Four Root Drivers of Cross-Game Divergence:\n"
            "1. Monetization Mix Asymmetry: Game A is a balanced hybrid (~78% Ad / ~22% IAP overall, 52% Ad / 48% IAP in US), while Game B is a casual tile-matching engine (99.6% Ad / 0.4% IAP; $303.6k Ad vs $1.1k IAP). "
            "Applying Game B's model to Game A yields a +4.34% positive bias because Game B's steeper D14->D120 Ad curve over-projects Game A's Ad stream while missing Game A's repeat-payer IAP dynamics. Conversely, Model A on Game B underprojects Game B's long-tail ad potential (-3.32% bias) due to assuming Game A's steeper retention decay.\n"
            "2. Retention Decay Dynamics: Game B exhibits flatter retention decay (gamma approx 0.72 vs Game A's gamma approx 0.82), delivering +64% higher active user "
            "retention at Day 120 (2.02% vs 1.23%). Game A users churn faster, requiring higher early monetization to pay back.\n"
            "3. Offerwall Line Dynamics: Net-D in Game A features highly front-loaded IAP monetization (85% of total IAP revenue occurs within 14 days), "
            "whereas Game B contains zero offerwall networks.\n"
            "4. Component vs Multiplier Transferability: Parametric retention decay curves transfer across casual games with high fidelity (Pearson r > 0.90), "
            "whereas raw revenue multipliers fail to transfer due to currency glitches and ad mediation reporting artifacts."
        )
        ax.text(0.05, 0.450, escape_dollars(sec4_narrative), fontsize=7.8, color="#334155", wrap=True)
        pdf.savefig(fig); plt.close()

        # ----------------------------------------------------
        # PAGE 7: Section 5 Constrained Spend Optimization (Question 2)
        # ----------------------------------------------------
        fig = plt.figure(figsize=(8.5, 11), dpi=300)
        ax = fig.add_axes([0, 0, 1, 1]); ax.axis("off")
        add_page_furniture(ax, 7, 10, "Spend Optimization & KKT Economics")
        
        ax.text(0.05, 0.915, "5. Constrained Media Plan Optimization & KKT Economics (Question 2)", fontsize=10.5, fontweight="bold", color="#0f172a")
        sec5_desc = (
            "The Media Plan is formulated as a non-linear constrained optimization across 40 decision cells in Game A:\n"
            "max sum(Expected_D120_Revenue_i(x)) subject to: Total Spend <= $250,000; Portfolio D120 ROAS >= 1.0000; Active Lines >= 40% baseline; x_i <= 2.0x.\n\n"
            "KKT Shadow Price Equilibrations (lambda approx 0.536):\n"
            "• Why Net-D is held at 50% ($28,696) while Net-B Android is at 90.8% ($21,912): Below 0.50x, Net-D captures its maximum +56.9% efficiency boost "
            "(0.50^-0.65 = 1.569x, yielding 1.516x D120 ROAS and +$14,801 net profit). Above 0.50x, Net-D's high diminishing returns exponent (k=0.65 vs k=0.40 "
            "on Net-B) drops its marginal D120 revenue to $0.531 per dollar—falling below the $0.536 marginal revenue where Net-B Android, Net-B iOS, and Net-C "
            "equilibrate. Reallocating marginal capital to Net-B and Net-C maximizes total revenue.\n"
            "• Counter-Intuitive Budget Allocation (The 'Cheap-CPI Trap'): Capital is allocated to maximize net margin (LTV - CPI), not gross CPI. "
            "Higher-CPI markets like Net-A GB ($1.84 CPI) and SE ($0.79 CPI) receive maximum 2.0x budget multiples because strong monetization delivers >1.00x "
            "D120 payback. Conversely, cheap-CPI traps like IT ($0.20 CPI), PH ($0.30 CPI), and SA ($0.58 CPI) are pruned because poor monetization yields sub-0.75x ROAS."
        )
        ax.text(0.05, 0.640, escape_dollars(sec5_desc), fontsize=7.6, color="#334155", wrap=True)
        
        # Embed Frontier Chart
        img_front = mpimg.imread(str(FIGS_DIR / "q2_efficient_frontier.png"))
        ax_front = fig.add_axes([0.05, 0.15, 0.90, 0.45])
        ax_front.imshow(img_front); ax_front.axis("off")
        
        ax.text(0.05, 0.100, "Figure 2: CFO-vs-CEO Pareto Efficient Frontier Mapping Budget Scale vs. Payback Speed and Installs.", fontsize=8, color="#64748b", fontstyle="italic")
        pdf.savefig(fig); plt.close()

        # ----------------------------------------------------
        # PAGE 8: Section 5 (Cont.) Sensitivity Frontier & Spend Donut
        # ----------------------------------------------------
        fig = plt.figure(figsize=(8.5, 11), dpi=300)
        ax = fig.add_axes([0, 0, 1, 1]); ax.axis("off")
        add_page_furniture(ax, 8, 10, "Budget Sensitivity Frontier & Allocations")
        
        ax.text(0.05, 0.915, "Exhibit 11: Budget Sensitivity & CFO-vs-CEO Efficient Frontier Table", fontsize=10.5, fontweight="bold", color="#0f172a")
        
        front_df = pd.read_csv(TABLES_DIR / "q2_budget_sensitivity_frontier.csv")
        headers = ["Budget", "Quarter Spend", "Total Installs", "D120 Rev", "D120 ROAS", "1Y Rev", "1Y ROAS", "CFO Payback"]
        col_x = [0.05, 0.16, 0.30, 0.44, 0.58, 0.69, 0.81, 0.90]
        
        y = 0.875
        ax.add_patch(patches.Rectangle((0.05, y), 0.90, 0.022, facecolor="#0f172a", edgecolor="none"))
        for h, x in zip(headers, col_x):
            ax.text(x + 0.003, y + 0.006, h, color="white", fontsize=7.2, fontweight="bold")
            
        y -= 0.025
        for idx, row in front_df.iterrows():
            is_cfo = (row["Budget"] == 140392)
            bg_col = "#e0f2fe" if is_cfo else ("#f8fafc" if idx % 2 == 1 else "#ffffff")
            ax.add_patch(patches.Rectangle((0.05, y), 0.90, 0.022, facecolor=bg_col, edgecolor="#e2e8f0", lw=0.5))
            
            vals = [
                f"${row['Budget']:,.0f}", f"${row['Quarter_Spend']:,.2f}", f"{int(row['Total_Installs']):,}",
                f"${row['D120_Revenue_Direct']:,.2f}", f"{row['D120_ROAS_Direct']:.4f}",
                f"${row['1Y_Revenue_Direct']:,.2f}", f"{row['1Y_ROAS_Direct']:.4f}",
                "PASS (1.0x)" if row["CFO_Compliant_Direct"] else "FAIL (<1.0x)"
            ]
            for v, x in zip(vals, col_x):
                ax.text(x + 0.003, y + 0.006, escape_dollars(v), color="#0369a1" if is_cfo else "#1e293b", fontsize=6.8, fontweight="bold" if is_cfo else "normal")
            y -= 0.025
            
        # Embed Pie Chart
        img_pie = mpimg.imread(str(FIGS_DIR / "q2_spend_allocation_pie.png"))
        ax_pie = fig.add_axes([0.05, 0.18, 0.90, 0.38])
        ax_pie.imshow(img_pie); ax_pie.axis("off")
        
        ax.text(0.05, 0.120, "Figure 3: Game A Q4 Media Plan Capital Allocation by Network and Net-A Geography.", fontsize=8, color="#64748b", fontstyle="italic")
        pdf.savefig(fig); plt.close()

        # ----------------------------------------------------
        # PAGE 9: Section 6 Creative Fatigue Mechanics (Question 3)
        # ----------------------------------------------------
        fig = plt.figure(figsize=(8.5, 11), dpi=300)
        ax = fig.add_axes([0, 0, 1, 1]); ax.axis("off")
        add_page_furniture(ax, 9, 10, "Creative Performance & Wear-Out Dynamics")
        
        ax.text(0.05, 0.915, "6. Creative Performance Decomposition & Wear-Out Mechanics (Question 3)", fontsize=10.5, fontweight="bold", color="#0f172a")
        sec6_desc = (
            "Historical creative analysis decomposes performance across formats:\n"
            "• Net-A Search Text Ads (Star Format): Highest conversion efficiency (IPM: 19.92, D30 ROAS: 1.5398, CPI: $0.70).\n"
            "• Net-A Auto-Assemble Display/Video (Core Engine): Highest volume (110k installs, IPM: 8.88, D30 ROAS: 1.0032, CPI: $1.10).\n"
            "• Net-B Playables vs Net-C Video+Playable: Net-B playables generate substantial LTV ($2.97 D30 LTV) at higher CPM ($69.51) and CPI ($4.95). "
            "Net-C video+playable delivers balanced $2.57 CPI and $1.33 D30 LTV.\n"
            "• Net-D Store Listing Images: Record Day-30 LTV ($6.14/user) driven by deep IAP engagement and rewarded actions."
        )
        ax.text(0.05, 0.770, escape_dollars(sec6_desc), fontsize=7.8, color="#334155", wrap=True)
        
        # Embed Creative Wear-out Curves Chart
        img_wear = mpimg.imread(str(FIGS_DIR / "q3_creative_wearout_curves.png"))
        ax_wear = fig.add_axes([0.05, 0.20, 0.90, 0.52])
        ax_wear.imshow(img_wear); ax_wear.axis("off")
        
        ax.text(0.05, 0.140, "Figure 4: Creative CPI Inflation Trajectories and Mandatory +30% Retirement Limits.", fontsize=8, color="#64748b", fontstyle="italic")
        pdf.savefig(fig); plt.close()

        # ----------------------------------------------------
        # PAGE 10: Section 6 (Cont.) Week-by-Week Operational Cadence
        # ----------------------------------------------------
        fig = plt.figure(figsize=(8.5, 11), dpi=300)
        ax = fig.add_axes([0, 0, 1, 1]); ax.axis("off")
        add_page_furniture(ax, 10, 10, "Creative Replenishment Schedule & Timeline")
        
        ax.text(0.05, 0.915, "Exhibit 14: Week-by-Week Creative Replenishment Schedule & Production Cadence", fontsize=10.5, fontweight="bold", color="#0f172a")
        sec6_sched = (
            "Existing creative library carries Weeks 1-2. Weeks 3-12 deploy 13 new creative units:\n"
            "• Net-A (5 Videos/Playables): 1.5M imps/unit (+20% CPI / 1M imps; 2-wk lead time; launches W3, W5, W7, W10, W12).\n"
            "• Net-B (3 Minimum vs 4 Recommended Ad Sets): Theoretical minimum = 3 ad sets (ceil(293,271 / 100,000) = 3). We recommend 4 ad sets "
            "(launches W3, W6, W9, W12) to provide a 1-set staggered operational buffer preventing either platform crossing +30% CPI during the peak Holiday Surge.\n"
            "• Net-C (3 Ad Packs): 100k imps/unit (+300% CPI / 1M imps; 1-wk lead time; launches W3, W7, W11).\n"
            "• Net-D (1 Listing Image): Burns only 50.9k imps (25.5% capacity), lasting all 10 weeks at only +7.6% wear."
        )
        ax.text(0.05, 0.770, escape_dollars(sec6_sched), fontsize=7.8, color="#334155", wrap=True)
        
        # Embed Creative Refresh Timeline Chart
        img_time = mpimg.imread(str(FIGS_DIR / "q3_creative_refresh_timeline.png"))
        ax_time = fig.add_axes([0.05, 0.20, 0.90, 0.52])
        ax_time.imshow(img_time); ax_time.axis("off")
        
        ax.text(0.05, 0.140, "Figure 5: 12-Week Operational Replenishment Gantt Chart with Production Lead Times & Holiday Surge Alignment.", fontsize=8, color="#64748b", fontstyle="italic")
        ex15_text = (
            "Exhibit 15 Production Risk Simulation: Baseline: 75,545 paid installs ($1.86 CPI, $140,392 D120 rev, 100.00% ROAS, PASS). "
            "Scenario 1 (2-Wk Delay): 72,940 installs ($1.92 CPI, $135,551 rev, -$4,841 loss, 96.55% ROAS, FAIL). "
            "Scenario 2 (50% Under-Production): 68,281 installs ($2.06 CPI, $126,892 rev, -$13,499 loss, 90.38% ROAS, FAIL). Production triggers are hard financial constraints."
        )
        ax.text(0.05, 0.080, escape_dollars(ex15_text), fontsize=7.2, color="#0f172a", wrap=True)
        pdf.savefig(fig); plt.close()
        
    pages = get_pdf_page_count(pdf_path)
    print(f"  [APPENDIX PDF] Built {pdf_path}: Exactly {pages} pages (Constraint: <= 12 pages | PASS: {pages <= 12})")
    assert pages <= 12, f"Expected <= 12 pages, got {pages}"


def package_submission_zip():
    """Packages complete deliverables into Chaos_Engine_Labs_Growth_Submission.zip."""
    print("\n" + "=" * 70)
    print("[06] Creating Final Submission ZIP Package...")
    print("=" * 70)
    
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
                    if p.is_file() and not p.name.endswith(".pyc") and "__pycache__" not in str(p):
                        arcname = p.relative_to(BASE_DIR)
                        zipf.write(p, arcname)
                        print(f"  Added directory asset: {arcname}")
                        
    size_mb = os.path.getsize(zip_path) / (1024.0 * 1024.0)
    print(f"\n  [PACKAGE SUCCESS] Created {zip_path} ({size_mb:.2f} MB)")


def main():
    print("=" * 70)
    print("CHAOS ENGINE GROWTH CASE - SCRIPT 06: PDF COMPILATION & PACKAGING")
    print("=" * 70)
    
    # 1. Compile memo.pdf
    compile_memo_pdf()
    
    # 2. Compile ai_usage_log.pdf
    compile_ai_log_pdf()
    
    # 3. Compile appendix.pdf
    compile_appendix_pdf()
    
    # 4. Programmatic Verification of Page Counts
    memo_pages = get_pdf_page_count(SUB_DIR / "memo.pdf")
    ai_pages = get_pdf_page_count(SUB_DIR / "ai_log" / "ai_usage_log.pdf")
    app_pages = get_pdf_page_count(SUB_DIR / "appendix.pdf")
    
    print("\n" + "=" * 70)
    print("PROGRAMMATIC PAGE LIMIT VERIFICATION:")
    print("=" * 70)
    print(f"  submission/memo.pdf:             {memo_pages} pages (Strict Limit: <= 2 | PASS: {memo_pages <= 2})")
    print(f"  submission/ai_log/ai_usage_log.pdf: {ai_pages} page  (Strict Limit: <= 1 | PASS: {ai_pages <= 1})")
    print(f"  submission/appendix.pdf:         {app_pages} pages (Strict Limit: <= 12 | PASS: {app_pages <= 12})")
    print("=" * 70)
    
    # 5. Create Final ZIP
    package_submission_zip()
    
    print("\n" + "=" * 70)
    print("[ALL COMPLETE] Final PDFs compiled, page counts verified, and submission package ready.")
    print("=" * 70)


if __name__ == "__main__":
    main()
