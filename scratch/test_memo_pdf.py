import sys
from pathlib import Path
import re
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.patches as patches

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

from src.config import SUB_DIR, FIGS_DIR

def get_pdf_page_count(pdf_path):
    with open(pdf_path, "rb") as f:
        data = f.read()
    return len(re.findall(rb"/Type\s*/Page\b", data))

def build_test_memo():
    pdf_path = SUB_DIR / "memo.pdf"
    
    with PdfPages(pdf_path) as pdf:
        # ==========================================
        # PAGE 1: Executive Briefing & Allocation Frontier
        # ==========================================
        fig = plt.figure(figsize=(8.5, 11), dpi=300)
        ax = fig.add_axes([0, 0, 1, 1])
        ax.axis("off")
        
        # Header banner
        ax.add_patch(patches.Rectangle((0.05, 0.91), 0.90, 0.065, facecolor="#1b263b", edgecolor="none"))
        ax.text(0.07, 0.945, "EXECUTIVE MEMO: GAME A Q4 GROWTH & UA SPEND STRATEGY", color="white", fontsize=13, fontweight="bold")
        ax.text(0.07, 0.922, "To: Chief Executive Officer & Chief Financial Officer   |   From: Head of Growth   |   Date: September 30, 2025", color="#cbd5e1", fontsize=8.5)
        
        # Mandatory 5 CFO Lines Box
        ax.add_patch(patches.Rectangle((0.05, 0.60), 0.90, 0.295, facecolor="#f8fafc", edgecolor="#cbd5e1", lw=1))
        ax.add_patch(patches.Rectangle((0.05, 0.60), 0.012, 0.295, facecolor="#0284c7", edgecolor="none"))
        
        ax.text(0.075, 0.865, "EXECUTIVE FIVE-LINE BRIEFING (MANDATORY CFO CORE)", fontsize=10.5, fontweight="bold", color="#0f172a")
        
        cfo_lines = [
            ("1. Spend Recommendation:", "$140,391.59 across 12 weeks strictly meeting 1.0000x D120 ROAS ($158,000 with organic halo). Unconstrained CEO scale option ($250k) and 1-Year cash breakeven ($182.3k) also provided."),
            ("2. Expected Result:", "75,555 paid installs (79,219 total with organic halo), delivering $140,391.61 Day-120 gross revenue (1.0000x D120 ROAS; 1.0532x blended) and $158,072.89 at 1 Year (1.1259x 1Y ROAS)."),
            ("3. Payback Profile:", "Payback <=120d: Net-D Android US, 10 Net-A countries (RO, HK, SE, MX, PL, AR, PT, IL, GB, VN), and Tiers 1, 3, 4. Payback in 1Y: Net-A US, Net-B Android US, Net-C Android US. Non-viable: Net-B iOS US (0.895x 1Y)."),
            ("4. Primary Data Distortions:", "8 critical anomalies proved and repaired: 1.99x mediation double-counting (+$283k spurious ad rev), right-censoring filled with frozen cutoffs, July 14-16 eCPM glitch, 100x local currency/cents bugs, and 4,197 unmatched spend rows ($1,347 preserved; 100.00% spend reconciled)."),
            ("5. Key Strategic Risks:", "Creative wearout (+300% CPI / 1M imps on Net-B/C) and Holiday Surge (+25% CPI in Weeks 8-11). Mitigated via 13 new creative units (5 Net-A, 4 Net-B, 3 Net-C, 1 Net-D) produced on 1-2 week lead times.")
        ]
        
        y_pos = 0.835
        for title, desc in cfo_lines:
            ax.text(0.075, y_pos, title, fontsize=8.5, fontweight="bold", color="#0284c7")
            ax.text(0.075, y_pos - 0.022, desc, fontsize=8, color="#334155")
            y_pos -= 0.052
            
        # Section 1: Capital Allocation Dilemma
        ax.text(0.05, 0.565, "1. Strategic Capital Allocation Dilemma: CFO Payback vs. CEO Growth", fontsize=11, fontweight="bold", color="#0f172a")
        
        intro_text = (
            "Our constrained portfolio optimization resolves the tension between capital preservation (CFO) and scale (CEO). "
            "Due to diminishing marginal returns (x^-k) and holiday CPI inflation (+25%), deploying the entire $250,000 budget drops "
            "portfolio Day-120 ROAS to 0.7666x (a -$58,343 deficit). The maximum spend satisfying the CFO's D120 ROAS >= 1.00 mandate "
            "on direct paid spend is exactly $140,391.59."
        )
        ax.text(0.05, 0.525, intro_text, fontsize=8, color="#334155", wrap=True)
        
        # Strategy Comparison Table
        table_headers = ["Planning Strategy", "Quarter Spend", "Budget Share", "Total Installs", "Expected D120 Rev", "D120 ROAS", "1Y ROAS", "Net D120 Cashflow"]
        table_rows = [
            ["A. Primary CFO Breakeven Plan", "$140,391.59", "56.16%", "79,219", "$140,391.61", "1.0000x", "1.1259x", "+$0.02"],
            ["B. Blended Organic Breakeven", "$158,000.00", "63.20%", "86,124", "$148,800.00", "0.9418x*", "1.0614x", "-$9,200.00"],
            ["C. 1-Year Cash Breakeven Plan", "$182,325.00", "72.93%", "95,010", "$161,600.22", "0.8863x", "1.0000x", "-$20,724.78"],
            ["D. CEO Full Budget Growth Plan", "$250,000.00", "100.00%", "113,193", "$191,656.96", "0.7666x", "0.8657x", "-$58,343.04"]
        ]
        
        t_y = 0.440
        col_x = [0.05, 0.28, 0.39, 0.49, 0.59, 0.72, 0.81, 0.89]
        
        # Table Header Bar
        ax.add_patch(patches.Rectangle((0.05, t_y), 0.90, 0.025, facecolor="#0f172a", edgecolor="none"))
        for h, x in zip(table_headers, col_x):
            ax.text(x + 0.005, t_y + 0.007, h, color="white", fontsize=7.5, fontweight="bold")
            
        t_y -= 0.026
        for r_idx, row in enumerate(table_rows):
            bg_col = "#f1f5f9" if r_idx % 2 == 1 else "#ffffff"
            ax.add_patch(patches.Rectangle((0.05, t_y), 0.90, 0.025, facecolor=bg_col, edgecolor="#e2e8f0", lw=0.5))
            for val, x in zip(row, col_x):
                is_bold = "Primary" in val or "1.0000x" in val
                text_col = "#0369a1" if "Primary" in val else ("#0f172a" if is_bold else "#334155")
                ax.text(x + 0.005, t_y + 0.007, val, color=text_col, fontsize=7.5, fontweight="bold" if is_bold else "normal")
            t_y -= 0.025
            
        ax.text(0.05, t_y - 0.005, "*Strategy B achieves 1.0000x blended D120 ROAS when crediting incremental organic halo (+4.85% K-factor, $2.0516 organic LTV).", fontsize=7, color="#64748b", fontstyle="italic")
        
        # Embed Frontier Chart
        img_frontier = mpimg.imread(str(FIGS_DIR / "q2_efficient_frontier.png"))
        ax_img = fig.add_axes([0.05, 0.06, 0.90, 0.28])
        ax_img.imshow(img_frontier)
        ax_img.axis("off")
        
        # Footer Page 1
        ax.text(0.05, 0.025, "Chaos Engine Labs Growth Case | Executive Memo", fontsize=8, color="#94a3b8")
        ax.text(0.88, 0.025, "Page 1 of 2", fontsize=8, fontweight="bold", color="#94a3b8")
        
        pdf.savefig(fig)
        plt.close()
        
        # ==========================================
        # PAGE 2: Portfolio Allocations, KKT Economics, Creatives & Roadmap
        # ==========================================
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
            "Why Net-D is held at 50% while Net-B Android US is at 90.8% ($21,911.59): Due to Net-D's steep diminishing returns exponent (k=0.65 "
            "vs k=0.40 on Net-B), spending beyond 0.50x causes Net-D's marginal D120 revenue to drop to $0.531 per dollar—just below the $0.536 "
            "marginal revenue where Net-B Android (90.8%), Net-B iOS (67.4%), and Net-C Android (60.7%) equilibrate under KKT shadow-price conditions.\n\n"
            "Counter-Intuitive Budget Allocation (The 'Cheap-CPI Trap'): Capital is allocated to maximize net margin (LTV - CPI), not minimize gross CPI. "
            "Higher-CPI markets like Net-A GB ($1.84 CPI) and SE ($0.79 CPI) receive maximum 2.0x budget multiples because their strong monetization "
            "delivers >1.00x D120 payback. In contrast, superficial 'cheap-CPI' traps like IT ($0.20 CPI), PH ($0.30 CPI), and SA ($0.58 CPI) are pruned "
            "to zero because poor player monetization yields sub-0.75x ROAS (e.g., SA D120 ROAS is only 0.531x)."
        )
        ax2.text(0.05, 0.775, sec2_text, fontsize=7.8, color="#334155", wrap=True)
        
        # Embed Spend Allocation Donut Chart
        img_pie = mpimg.imread(str(FIGS_DIR / "q2_spend_allocation_pie.png"))
        ax_pie = fig2.add_axes([0.05, 0.535, 0.90, 0.22])
        ax_pie.imshow(img_pie)
        ax_pie.axis("off")
        
        # Section 3: Econometric Organic Uplift
        ax2.text(0.05, 0.505, "3. Econometric Organic Uplift & Halo Effect", fontsize=10.5, fontweight="bold", color="#0f172a")
        sec3_text = (
            "Time-series OLS regression with day-of-week fixed effects and deterministic time trend across 266 daily records proves a robust "
            "organic K-factor of +0.0485 (t = 3.815, p < 0.001, 95% CI: [0.0235, 0.0735]). Mature organic players monetize at $2.0516 D120 LTV, "
            "yielding +$0.0995 in incremental D120 revenue per paid install. Crediting this halo elevates portfolio D120 ROAS to 1.0532x and "
            "expands the CFO breakeven ceiling from $140,392 to $158,000."
        )
        ax2.text(0.05, 0.440, sec3_text, fontsize=7.8, color="#334155", wrap=True)
        
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
        ax2.text(0.05, 0.235, sec4_text, fontsize=7.8, color="#334155", wrap=True)
        
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
            ax2.text(0.18, ry, w_desc, fontsize=7.5, color="#334155")
            ry -= 0.026
            
        # Footer Page 2
        ax2.text(0.05, 0.025, "Chaos Engine Labs Growth Case | Executive Memo", fontsize=8, color="#94a3b8")
        ax2.text(0.88, 0.025, "Page 2 of 2", fontsize=8, fontweight="bold", color="#94a3b8")
        
        pdf.savefig(fig2)
        plt.close()
        
    pages = get_pdf_page_count(pdf_path)
    print(f"  [MEMO PDF] Built {pdf_path}: Page count = {pages} (strictly <= 2: {pages <= 2})")
    assert pages == 2, f"Expected exactly 2 pages, got {pages}"

build_test_memo()
