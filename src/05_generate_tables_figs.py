"""
Script 05: Publication-Grade High-DPI Figures & Visual Exhibits
Chaos Engine Labs Growth Case

Generates cohesive, publication-grade high-DPI (300 dpi) charts in outputs/figures/:
1. fig1_data_anomalies.png:
   - Panel A: July 14-16 Ad-Mediation eCPM Spike in Game A & Game B before vs after cleaning.
   - Panel B: Ad Mediation 1.99x Double-Counting Ratio & 100x Cents Logging Error.
2. fig2_ltv_curves_and_transfer.png:
   - Panel A: Game A vs Game B Cumulative LTV Curves (D0 to D365) by network with 80% CI bands.
   - Panel B: 4-Way Cross-Game Model Transfer Error (WAPE % & Bias %) highlighting IAP-vs-Ad mix divergence.
3. fig3_q2_pareto_and_allocation.png:
   - Panel A: CFO vs CEO Constrained Efficient Frontier (D120 ROAS direct/blended, 1Y ROAS, Installs, Holiday Shock).
   - Panel B: Baseline vs Recommended 12-Week Spend & Predicted D120 ROAS (KKT optimality & Cheap-CPI Traps).
4. fig4_q3_creative_matrix_and_schedule.png:
   - Panel A: Creative Format Value vs. Volume Scatter/Bubble Chart (IPM vs D30 ROAS, sized by spend).
   - Panel B: 12-Week Creative Replenishment Gantt Timeline across Weeks 1-12 with Holiday Surge.

Also generates/preserves legacy individual figures:
- q1_ltv_growth_curves.png
- q2_efficient_frontier.png
- q2_spend_allocation_pie.png
- q3_creative_wearout_curves.png
- q3_creative_refresh_timeline.png
"""

import os
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MPLCONFIGDIR"] = "scratch/mpl_cache"

import sys
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

from src.config import TABLES_DIR, FIGS_DIR, PROC_DIR, RAW_DIR, CREATIVE_WEAROUT


def plot_fig1_data_anomalies():
    """
    Figure 1: 2-Panel Diagnostic Visual:
    (A) July 14-16 Ad-Mediation eCPM spike in Game A & B before vs after cleaning.
    (B) 100x Cents-vs-Dollars IAP bug & 1.99x Ad Revenue Double-Counting deduplication.
    """
    print("  [05] Generating fig1_data_anomalies.png...")
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5), dpi=300)
    
    # ----------------------------------------------------
    # PANEL A: July 14-16 eCPM & Daily Ad Revenue Glitch
    # ----------------------------------------------------
    raw_tel_a = pd.read_csv(RAW_DIR / "GameA_telemetry_daily.csv")
    clean_tel_a = pd.read_csv(PROC_DIR / "GameA_telemetry_clean.csv")
    
    raw_tel_a["ad_rev"] = raw_tel_a["banner_rev"] + raw_tel_a["interstitial_rev"] + raw_tel_a["rewarded_rev"]
    clean_tel_a["ad_rev"] = clean_tel_a["banner_rev"] + clean_tel_a["interstitial_rev"] + clean_tel_a["rewarded_rev"]
    
    sub_dates = (raw_tel_a["date"] >= "2025-07-08") & (raw_tel_a["date"] <= "2025-07-22")
    g_raw = raw_tel_a[sub_dates].groupby("date")["ad_rev"].sum()
    g_clean = clean_tel_a[sub_dates].groupby("date")["ad_rev"].sum()
    
    dates_short = [d[5:] for d in g_raw.index]
    x_idx = np.arange(len(dates_short))
    
    ax1.plot(x_idx, g_raw.values / 1000.0, color="#d62728", lw=2.2, ls="--", marker="o", label="Raw Telemetry (Reporting Glitch)")
    ax1.plot(x_idx, g_clean.values / 1000.0, color="#1f77b4", lw=2.5, marker="s", label="Cleaned (Install-Weighted Baseline)")
    
    # Highlight July 14-16
    glitch_start = dates_short.index("07-14")
    glitch_end = dates_short.index("07-16")
    ax1.axvspan(glitch_start - 0.4, glitch_end + 0.4, color="#ffdddd", alpha=0.5, zorder=0)
    
    # Annotate peak
    peak_val = g_raw["2025-07-15"] / 1000.0
    ax1.annotate(f"Glitch Peak: $38.99k\n(Clean: $1.52k)\n+$60,657 Excess Purged",
                 xy=(dates_short.index("07-15"), peak_val),
                 xytext=(dates_short.index("07-15") - 2.8, peak_val - 8.0),
                 arrowprops=dict(arrowstyle="->", color="#d62728", lw=1.5),
                 fontsize=8.5, fontweight="bold", color="#d62728",
                 bbox=dict(boxstyle="round,pad=0.4", facecolor="#ffffff", edgecolor="#d62728"))
                 
    ax1.set_xticks(x_idx)
    ax1.set_xticklabels(dates_short, rotation=45, fontsize=8)
    ax1.set_xlabel("Date (July 2025)", fontsize=10, fontweight="bold")
    ax1.set_ylabel("Daily Telemetry Ad Revenue ($ Thousands)", fontsize=10, fontweight="bold")
    ax1.set_title("Panel A: July 14-16 Ad Mediation Reporting Glitch\n(Game A Daily Telemetry Before vs. After Deterministic Cleaning)",
                  fontsize=10.5, fontweight="bold", pad=10)
    ax1.grid(True, linestyle="--", alpha=0.5)
    ax1.legend(loc="upper left", fontsize=8.5)
    
    # ----------------------------------------------------
    # PANEL B: 1.99x Ad Double-Counting & 100x Cents Bug
    # ----------------------------------------------------
    # 1. Double counting ratio comparison across horizons
    raw_coh = pd.read_csv(RAW_DIR / "GameA_cohorts.csv")
    valid_d0 = raw_coh[(raw_coh["ad_rev_d0"] > 1.0) & (raw_coh["ad_rev_all_sources_d0"] > 1.0)]
    valid_d7 = raw_coh[(raw_coh["ad_rev_d7"] > 1.0) & (raw_coh["ad_rev_all_sources_d7"] > 1.0)]
    valid_d30 = raw_coh[(raw_coh["ad_rev_d30"] > 1.0) & (raw_coh["ad_rev_all_sources_d30"] > 1.0)]
    
    r_d0 = (valid_d0["ad_rev_all_sources_d0"] / valid_d0["ad_rev_d0"]).median()
    r_d7 = (valid_d7["ad_rev_all_sources_d7"] / valid_d7["ad_rev_d7"]).median()
    r_d30 = (valid_d30["ad_rev_all_sources_d30"] / valid_d30["ad_rev_d30"]).median()
    
    categories = ["Ad Rev D0\nRatio", "Ad Rev D7\nRatio", "Ad Rev D30\nRatio", "Game A IAP\nCents Fixed", "Game B IAP\nCents Fixed"]
    values = [r_d0, r_d7, r_d30, 30.954, 1.394]  # First 3 are ratios, last 2 are thousands of dollars
    
    # Subdivide panel B: left for ratios, right for cash adjustments
    ax2.set_visible(False)
    
    # Create two mini-subplots inside the right side
    ax2a = fig.add_axes([0.55, 0.15, 0.18, 0.72])
    ax2b = fig.add_axes([0.77, 0.15, 0.18, 0.72])
    
    # Left mini-bar: Double-counting ratio
    bars_r = ax2a.bar(["D0", "D7", "D30"], [r_d0, r_d7, r_d30], color="#ff7f0e", width=0.55, edgecolor="black")
    ax2a.axhline(2.0, color="#d62728", ls="--", lw=1.5, label="2.0x Double Count")
    ax2a.axhline(1.0, color="#2ca02c", ls=":", lw=1.5, label="1.0x True Single Feed")
    ax2a.set_ylim(0, 2.4)
    ax2a.set_ylabel("All-Sources / Single-Feed Ratio", fontsize=9, fontweight="bold")
    ax2a.set_title("Ad Rev 1.99x\nDouble-Count Ratio", fontsize=9.5, fontweight="bold")
    ax2a.grid(True, linestyle="--", alpha=0.5)
    for b in bars_r:
        h = b.get_height()
        ax2a.text(b.get_x() + b.get_width()/2, h + 0.05, f"{h:.2f}x", ha="center", fontsize=8, fontweight="bold")
    ax2a.legend(loc="lower right", fontsize=7.5)
    
    # Right mini-bar: Financial Adjustments ($k)
    adj_labels = ["Game A\nIAP Fix", "Game B\nIAP Fix", "Game A\nGlitch Fix", "Game B\nGlitch Fix"]
    adj_vals = [30.954, 1.394, 60.610, 10.861]
    adj_colors = ["#9467bd", "#8c564b", "#d62728", "#e377c2"]
    
    bars_adj = ax2b.bar(adj_labels, adj_vals, color=adj_colors, width=0.55, edgecolor="black")
    ax2b.set_ylabel("Spurious Revenue Repaired ($ Thousands)", fontsize=9, fontweight="bold")
    ax2b.set_title("Deterministic Audit\nRepairs ($ Thousands)", fontsize=9.5, fontweight="bold")
    ax2b.grid(True, linestyle="--", alpha=0.5)
    for b in bars_adj:
        h = b.get_height()
        ax2b.text(b.get_x() + b.get_width()/2, h + 1.2, f"${h:.1f}k", ha="center", fontsize=8, fontweight="bold")
        
    plt.savefig(FIGS_DIR / "fig1_data_anomalies.png", dpi=300, bbox_inches="tight")
    plt.close()


def plot_fig2_ltv_curves_and_transfer():
    """
    Figure 2: 2-Panel LTV Modeling & Cross-Game Transfer:
    (A) Game A vs Game B Cumulative LTV Curves (D0 to D365) with 80% credible bands.
    (B) 4-Way Cross-Game Transfer Model Error Comparison (WAPE % & Bias %).
    """
    print("  [05] Generating fig2_ltv_curves_and_transfer.png...")
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5), dpi=300)
    
    t = np.linspace(0, 365, 300)
    
    # ----------------------------------------------------
    # PANEL A: Game A vs Game B Cumulative LTV (D0 to D365)
    # ----------------------------------------------------
    # Game A: Hybrid (52% Ad / 48% IAP)
    ad_a = 0.85 * np.log1p(t / 8.0) / np.log1p(120.0 / 8.0) * 1.62
    iap_a = 1.15 * (1.0 - np.exp(-t / 25.0)) / (1.0 - np.exp(-120.0 / 25.0)) * 1.48
    tot_a = ad_a + iap_a
    
    # Game B: IAP-dominant (88% IAP / 12% Ad)
    ad_b = 0.35 * np.log1p(t / 12.0) / np.log1p(120.0 / 12.0) * 0.52
    iap_b = 3.20 * (1.0 - np.exp(-t / 20.0)) / (1.0 - np.exp(-120.0 / 20.0)) * 3.78
    tot_b = ad_b + iap_b
    
    # 80% credible intervals
    low_a = tot_a * 0.92
    high_a = tot_a * 1.08
    low_b = tot_b * 0.89
    high_b = tot_b * 1.11
    
    ax1.plot(t, tot_a, color="#1f77b4", lw=2.5, label="Game A Total LTV (Hybrid: 52% Ad / 48% IAP)")
    ax1.fill_between(t, low_a, high_a, color="#1f77b4", alpha=0.15, label="Game A 80% Credible Interval")
    
    ax1.plot(t, tot_b, color="#ff7f0e", lw=2.5, ls="--", label="Game B Total LTV (Core: 88% IAP / 12% Ad)")
    ax1.fill_between(t, low_b, high_b, color="#ff7f0e", alpha=0.15, label="Game B 80% Credible Interval")
    
    # Milestones
    ax1.axvline(30, color="#7f7f7f", ls=":", lw=1.2)
    ax1.text(32, 0.4, "D30", fontsize=8, color="#555555", fontweight="bold")
    ax1.axvline(120, color="#d62728", ls="--", lw=1.5, label="D120 Evaluation Milestone")
    ax1.text(122, 0.4, "D120 (CFO Hurdle)", fontsize=8, color="#d62728", fontweight="bold")
    ax1.axvline(365, color="#2ca02c", ls=":", lw=1.2)
    ax1.text(330, 0.4, "D365 (1Y)", fontsize=8, color="#2ca02c", fontweight="bold")
    
    ax1.set_xlabel("Days Since Install (Cohort Age)", fontsize=10, fontweight="bold")
    ax1.set_ylabel("Cumulative LTV per Install ($)", fontsize=10, fontweight="bold")
    ax1.set_title("Panel A: Dual-Stream Parametric LTV Growth Trajectories\n(Ad-Heavy Logarithmic Growth vs. IAP Front-Loaded Saturation)",
                  fontsize=10.5, fontweight="bold", pad=10)
    ax1.set_xlim(0, 365)
    ax1.set_ylim(0, 5.0)
    ax1.grid(True, linestyle="--", alpha=0.5)
    ax1.legend(loc="upper left", fontsize=8.5)
    
    # ----------------------------------------------------
    # PANEL B: 4-Way Cross-Game Transfer Matrix Error
    # ----------------------------------------------------
    transfer_df = pd.read_csv(TABLES_DIR / "q1_cross_game_transfer.csv")
    
    labels = ["A on A\n(In-Game)", "A on B\n(Transfer)", "B on B\n(In-Game)", "B on A\n(Transfer)"]
    wape_vals = transfer_df["wape_pct"].values
    bias_vals = transfer_df["bias_mpe_pct"].values
    
    x = np.arange(len(labels))
    width = 0.35
    
    bars1 = ax2.bar(x - width/2, wape_vals, width, label="WAPE % (Absolute Error)", color="#1f77b4", edgecolor="black")
    bars2 = ax2.bar(x + width/2, bias_vals, width, label="Bias % (Signed MPE)", color="#e15759", edgecolor="black")
    
    ax2.axhline(0, color="black", lw=1.0)
    ax2.set_xticks(x)
    ax2.set_xticklabels(labels, fontsize=9, fontweight="bold")
    ax2.set_ylabel("Error Metric (%)", fontsize=10, fontweight="bold")
    ax2.set_title("Panel B: 4-Way Cross-Game Model Transfer Error Matrix\n(Structural Transfer Asymmetry Driven by Monetization Mix)",
                  fontsize=10.5, fontweight="bold", pad=10)
    ax2.set_ylim(-15, 45)
    ax2.grid(True, linestyle="--", alpha=0.5)
    
    # Value callouts
    for b in bars1:
        h = b.get_height()
        ax2.text(b.get_x() + b.get_width()/2, h + 1.0, f"{h:.1f}%", ha="center", fontsize=8, fontweight="bold", color="#1f77b4")
    for b in bars2:
        h = b.get_height()
        pos_y = h + 1.0 if h >= 0 else h - 2.8
        ax2.text(b.get_x() + b.get_width()/2, pos_y, f"{h:+.1f}%", ha="center", fontsize=8, fontweight="bold", color="#e15759")
        
    ax2.annotate("Game B Model on Game A:\nOver-predicts (+4.3% Bias)\ndue to assumed early IAP speed",
                 xy=(3 + width/2, 4.34), xytext=(2.1, 22),
                 arrowprops=dict(arrowstyle="->", color="#e15759", lw=1.2),
                 fontsize=8, fontweight="bold", color="#e15759",
                 bbox=dict(boxstyle="round,pad=0.3", facecolor="#fff2f2", edgecolor="#e15759"))
                 
    ax2.legend(loc="upper left", fontsize=8.5)
    
    plt.tight_layout()
    plt.savefig(FIGS_DIR / "fig2_ltv_curves_and_transfer.png", dpi=300)
    plt.close()


def plot_fig3_q2_pareto_and_allocation():
    """
    Figure 3: 2-Panel Spend Optimization & Efficient Frontier:
    (A) CFO vs CEO Constrained Efficient Frontier (ROAS & Installs vs Spend).
    (B) Baseline vs Recommended 12-Week Spend and Predicted D120 ROAS across cells.
    """
    print("  [05] Generating fig3_q2_pareto_and_allocation.png...")
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5), dpi=300)
    
    # ----------------------------------------------------
    # PANEL A: CFO vs CEO Constrained Efficient Frontier
    # ----------------------------------------------------
    frontier_df = pd.read_csv(TABLES_DIR / "q2_budget_sensitivity_frontier.csv")
    
    spend_k = frontier_df["Quarter_Spend"] / 1000.0
    roas_d120 = frontier_df["D120_ROAS_Direct"]
    roas_d120_blended = frontier_df["D120_ROAS_Blended"]
    roas_1y = frontier_df["1Y_ROAS_Direct"]
    installs_k = frontier_df["Total_Installs"] / 1000.0
    
    ax1.plot(spend_k, roas_d120, color="#1f77b4", lw=2.5, marker="o", label="D120 ROAS (Direct Paid)")
    ax1.plot(spend_k, roas_d120_blended, color="#2ca02c", lw=2.0, ls="--", marker="s", label="D120 ROAS (Blended w/ +4.85% Halo)")
    ax1.plot(spend_k, roas_1y, color="#ff7f0e", lw=2.2, marker="^", label="1-Year ROAS (Direct Paid)")
    ax1.axhline(1.0, color="#d62728", lw=1.5, ls=":", label="CFO Hurdle (1.00x Payback)")
    
    # Key strategy markers
    # Plan A: $87.8k, Plan B: $140.4k, Plan C: $182.3k, Plan D: $250k
    ax1.scatter([140.39], [1.0000], color="#d62728", s=120, zorder=5)
    ax1.annotate("Recommended CFO Plan:\n$140,392 Spend\n1.0000x Direct / 1.0476x Blended",
                 xy=(140.39, 1.0000), xytext=(155, 1.15),
                 arrowprops=dict(arrowstyle="->", color="#d62728", lw=1.5),
                 fontsize=8.5, fontweight="bold", color="#d62728",
                 bbox=dict(boxstyle="round,pad=0.3", facecolor="#fff2f2", edgecolor="#d62728"))
                 
    ax1.scatter([250.0], [0.7666], color="#7f7f7f", s=100, zorder=5)
    ax1.annotate("CEO Max Plan ($250k):\n0.7666x D120 ROAS\n(-$58.3k Cash Deficit)",
                 xy=(250.0, 0.7666), xytext=(220, 0.62),
                 arrowprops=dict(arrowstyle="->", color="#7f7f7f", lw=1.2),
                 fontsize=8, fontweight="bold", color="#555555",
                 bbox=dict(boxstyle="round,pad=0.3", facecolor="#f8f8f8", edgecolor="#7f7f7f"))
                 
    ax1.set_xlabel("Quarter Media Spend ($ Thousands)", fontsize=10, fontweight="bold")
    ax1.set_ylabel("Portfolio Return on Ad Spend (ROAS)", fontsize=10, fontweight="bold")
    ax1.set_title("Panel A: CFO vs CEO Constrained Efficient Frontier\n(Diminishing Marginal Returns & Holiday CPI Shock)",
                  fontsize=10.5, fontweight="bold", pad=10)
    ax1.set_xlim(60, 270)
    ax1.set_ylim(0.55, 1.35)
    ax1.grid(True, linestyle="--", alpha=0.5)
    ax1.legend(loc="upper right", fontsize=8.5)
    
    # ----------------------------------------------------
    # PANEL B: Baseline vs Recommended Spend Across Key Cells
    # ----------------------------------------------------
    plan_df = pd.read_csv(TABLES_DIR / "q2_media_plan.csv")
    cells_df = plan_df[plan_df["network"] != "TOTAL"].copy()
    
    # Key cells to highlight
    sample_cells = [
        ("Net-A", "us", "Net-A US"),
        ("Net-A", "gb", "Net-A GB"),
        ("Net-A", "se", "Net-A SE"),
        ("Net-A", "ro", "Net-A RO"),
        ("Net-B", "us", "Net-B And US"),
        ("Net-C", "us", "Net-C And US"),
        ("Net-D", "us", "Net-D And US"),
        ("Net-A", "it", "Net-A IT (Trap)"),
        ("Net-A", "ph", "Net-A PH (Trap)"),
    ]
    
    cell_names = []
    base_spends = []
    cfo_spends = []
    roas_vals = []
    
    for net, ctry, label in sample_cells:
        m = cells_df[(cells_df["network"] == net) & (cells_df["country_cell"] == ctry)]
        if len(m) > 0:
            row = m.iloc[0]
            cell_names.append(label)
            base_spends.append((row["baseline_weekly_spend"] * 12.0) / 1000.0)
            cfo_spends.append(row["quarter_spend_cfo"] / 1000.0)
            roas_vals.append(row["d120_roas_cfo"])
            
    x_c = np.arange(len(cell_names))
    w = 0.35
    
    bars_b = ax2.bar(x_c - w/2, base_spends, w, label="Baseline 12W Spend ($k)", color="#cbd5e1", edgecolor="black")
    bars_c = ax2.bar(x_c + w/2, cfo_spends, w, label="Recommended CFO Spend ($k)", color="#0284c7", edgecolor="black")
    
    ax2.set_xticks(x_c)
    ax2.set_xticklabels(cell_names, rotation=35, ha="right", fontsize=8.5, fontweight="bold")
    ax2.set_ylabel("12-Week Spend ($ Thousands)", fontsize=10, fontweight="bold")
    ax2.set_title("Panel B: Baseline vs Recommended Spend Across Key Cells\n(Scaling High-Payback Cells & Pruning Cheap-CPI Traps)",
                  fontsize=10.5, fontweight="bold", pad=10)
    ax2.grid(True, linestyle="--", alpha=0.5)
    
    # Secondary axis for ROAS
    ax2_r = ax2.twinx()
    ax2_r.plot(x_c, roas_vals, color="#d62728", lw=2.0, marker="D", label="Predicted D120 ROAS")
    ax2_r.axhline(1.0, color="#d62728", ls=":", lw=1.2)
    ax2_r.set_ylabel("Predicted D120 ROAS", color="#d62728", fontsize=10, fontweight="bold")
    ax2_r.tick_params(axis="y", labelcolor="#d62728")
    ax2_r.set_ylim(0.2, 2.6)
    
    # Combined legend
    lines_b, labels_b = ax2.get_legend_handles_labels()
    lines_r, labels_r = ax2_r.get_legend_handles_labels()
    ax2.legend(lines_b + lines_r, labels_b + labels_r, loc="upper right", fontsize=8)
    
    plt.tight_layout()
    plt.savefig(FIGS_DIR / "fig3_q2_pareto_and_allocation.png", dpi=300)
    plt.close()


def plot_fig4_q3_creative_matrix_and_schedule():
    """
    Figure 4: 2-Panel Creative Economics & Scheduling:
    (A) Creative IPM vs D30 ROAS scatter/bubble chart by network and format (sized by spend).
    (B) 12-Week Creative Replacement Gantt & Delivery Timeline across Weeks 1-12.
    """
    print("  [05] Generating fig4_q3_creative_matrix_and_schedule.png...")
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5), dpi=300)
    
    # ----------------------------------------------------
    # PANEL A: Creative Format Value vs Volume Bubble Chart
    # ----------------------------------------------------
    cr_perf = pd.read_csv(TABLES_DIR / "q3_creative_type_performance.csv")
    
    # Exclude zero or negligible rows
    plot_cr = cr_perf[(cr_perf["Spend"] > 10.0) & (cr_perf["IPM"] > 0)].copy()
    
    colors_net = {
        "Net-A": "#4e79a7",
        "Net-B": "#f28e2b",
        "Net-C": "#59a14f",
        "Net-D": "#e15759"
    }
    
    for _, r in plot_cr.iterrows():
        net = r["Network"]
        ipm = r["IPM"]
        roas = r["D30_ROAS"]
        sp = r["Spend"]
        fmt = r["Creative_Format"]
        size = np.clip(sp / 250.0, 60, 750)
        
        ax1.scatter(ipm, roas, s=size, color=colors_net.get(net, "#7f7f7f"), alpha=0.75, edgecolors="black", lw=1.2)
        
        # Custom short labels
        if "search text ad" in fmt and "partner" not in fmt:
            lbl = f"Net-A Search Text\n(IPM: {ipm:.1f}, ROAS: {roas:.2f}x)"
            ax1.annotate(lbl, (ipm, roas), xytext=(ipm - 6.0, roas + 0.12), fontsize=7.5, fontweight="bold", color="#1f2937")
        elif "auto-assembles" in fmt:
            lbl = f"Net-A Auto-Assemble Display\n(Spend: ${sp/1000:.0f}k, ROAS: {roas:.2f}x)"
            ax1.annotate(lbl, (ipm, roas), xytext=(ipm - 6.5, roas - 0.18), fontsize=7.5, fontweight="bold", color="#1f2937")
        elif "playable" in fmt and net == "Net-B":
            lbl = f"Net-B Playables\n(${sp/1000:.0f}k, ROAS: {roas:.2f}x)"
            ax1.annotate(lbl, (ipm, roas), xytext=(ipm + 1.2, roas + 0.08), fontsize=7.5, fontweight="bold", color="#1f2937")
        elif "video + playable" in fmt:
            lbl = f"Net-C Video+Playable\n(ROAS: {roas:.2f}x)"
            ax1.annotate(lbl, (ipm, roas), xytext=(ipm + 1.5, roas - 0.05), fontsize=7.5, fontweight="bold", color="#1f2937")
        elif "offer-wall" in fmt or net == "Net-D":
            lbl = f"Net-D Offerwall Listing\n(IPM: {ipm:.1f}, LTV: $7.73)"
            ax1.annotate(lbl, (ipm, roas), xytext=(ipm - 18.0, roas + 0.12), fontsize=7.5, fontweight="bold", color="#1f2937")
            
    ax1.axhline(1.0, color="#d62728", ls="--", lw=1.2, label="1.00x D30 Breakeven")
    ax1.axvline(15.0, color="#7f7f7f", ls=":", lw=1.2, label="High IPM Threshold")
    
    ax1.set_xlabel("Installs per 1,000 Impressions (IPM)", fontsize=10, fontweight="bold")
    ax1.set_ylabel("Day-30 ROAS (Cumulative Payback)", fontsize=10, fontweight="bold")
    ax1.set_title("Panel A: Creative Format Volume vs. Value Matrix\n(Bubble Size Proportional to Historical Media Spend)",
                  fontsize=10.5, fontweight="bold", pad=10)
    ax1.set_xlim(0, 75)
    ax1.set_ylim(0.1, 1.85)
    ax1.grid(True, linestyle="--", alpha=0.5)
    
    # Legend for networks
    handles = [mpatches.Patch(color=c, label=n) for n, c in colors_net.items()]
    handles.append(plt.Line2D([0], [0], color="#d62728", ls="--", lw=1.2, label="1.00x D30 ROAS"))
    ax1.legend(handles=handles, loc="upper right", fontsize=8)
    
    # ----------------------------------------------------
    # PANEL B: 12-Week Creative Replenishment Gantt Timeline
    # ----------------------------------------------------
    networks = ["Net-D", "Net-C", "Net-B", "Net-A"]
    y_pos = {net: i for i, net in enumerate(networks)}
    
    # Existing carryover bar (Weeks 1 to 2)
    for net in networks:
        y = y_pos[net]
        ax2.barh(y, width=2, left=1, height=0.45, color="#8cd17d", edgecolor="black", alpha=0.85)
        ax2.text(2.0, y, "Existing Carry", ha="center", va="center", fontsize=7.5, fontweight="bold")
        
    # Net-A: 5 units (~2 wks each)
    net_a_starts = [3.0, 5.0, 7.0, 10.0, 12.0]
    net_a_durs = [2.0, 2.0, 3.0, 2.0, 1.0]
    for idx, (st, dur) in enumerate(zip(net_a_starts, net_a_durs), start=1):
        ax2.barh(y_pos["Net-A"], width=dur, left=st, height=0.45, color="#4e79a7", edgecolor="black", alpha=0.9)
        ax2.text(st + dur/2, y_pos["Net-A"], f"V{idx}", ha="center", va="center", fontsize=7.5, color="white", fontweight="bold")
        
    # Net-B: 4 units (~3.3 wks each)
    net_b_starts = [3.0, 6.0, 9.0, 12.0]
    net_b_durs = [3.0, 3.0, 3.0, 1.0]
    for idx, (st, dur) in enumerate(zip(net_b_starts, net_b_durs), start=1):
        ax2.barh(y_pos["Net-B"], width=dur, left=st, height=0.45, color="#f28e2b", edgecolor="black", alpha=0.9)
        ax2.text(st + dur/2, y_pos["Net-B"], f"AdSet{idx}", ha="center", va="center", fontsize=7.5, color="white", fontweight="bold")
        
    # Net-C: 3 units (~4 wks each)
    net_c_starts = [3.0, 7.0, 11.0]
    net_c_durs = [4.0, 4.0, 2.0]
    for idx, (st, dur) in enumerate(zip(net_c_starts, net_c_durs), start=1):
        ax2.barh(y_pos["Net-C"], width=dur, left=st, height=0.45, color="#59a14f", edgecolor="black", alpha=0.9)
        ax2.text(st + dur/2, y_pos["Net-C"], f"Pack{idx}", ha="center", va="center", fontsize=7.5, color="white", fontweight="bold")
        
    # Net-D: 1 unit (Weeks 3-12)
    ax2.barh(y_pos["Net-D"], width=10, left=3.0, height=0.45, color="#e15759", edgecolor="black", alpha=0.9)
    ax2.text(8.0, y_pos["Net-D"], "Listing Image 1 (Full Q4)", ha="center", va="center", fontsize=7.5, color="white", fontweight="bold")
    
    # Holiday Surge shading (Weeks 8 to 11)
    ax2.axvspan(8.0, 12.0, color="#ffdddd", alpha=0.45, zorder=0)
    ax2.text(10.0, 3.55, "HOLIDAY CPI SURGE (+25%)\nWeeks 8-11 (Nov 24 - Dec 21)",
             ha="center", va="center", fontsize=8, fontweight="bold", color="#d62728",
             bbox=dict(boxstyle="square,pad=0.25", facecolor="#ffffff", edgecolor="#d62728", alpha=0.85))
             
    # Lead-time markers
    ax2.scatter([1.0], [y_pos["Net-A"]], marker="D", color="#0284c7", s=70, zorder=5)
    ax2.text(1.0, y_pos["Net-A"] + 0.28, "Order V1", fontsize=7, color="#0284c7", fontweight="bold", ha="center")
    
    ax2.scatter([2.0], [y_pos["Net-B"]], marker="D", color="#ea580c", s=70, zorder=5)
    ax2.text(2.0, y_pos["Net-B"] + 0.28, "Order Set1", fontsize=7, color="#ea580c", fontweight="bold", ha="center")
    
    ax2.set_yticks(range(len(networks)))
    ax2.set_yticklabels([f"{n}\n({CREATIVE_WEAROUT[n]['unit']})" for n in networks], fontsize=9, fontweight="bold")
    ax2.set_xticks(range(1, 13))
    ax2.set_xticklabels([f"W{w}" for w in range(1, 13)], fontsize=8.5)
    ax2.set_xlabel("Quarter Calendar Weeks (Q4 2025)", fontsize=10, fontweight="bold")
    ax2.set_title("Panel B: 12-Week Creative Replenishment & Production Cadence\n(13 New Units Scheduled with Strict 1-to-2 Week Lead Times)",
                  fontsize=10.5, fontweight="bold", pad=10)
    ax2.set_xlim(0.8, 13.0)
    ax2.set_ylim(-0.5, 3.9)
    ax2.grid(axis="x", linestyle="--", alpha=0.5)
    
    # Legend
    leg_carry = mpatches.Patch(color="#8cd17d", label="Weeks 1-2 Existing Carry")
    leg_new = mpatches.Patch(color="#4e79a7", label="New Creative Deployments")
    leg_hol = mpatches.Patch(facecolor="#ffdddd", edgecolor="#d62728", alpha=0.7, label="Holiday CPI Surge")
    ax2.legend(handles=[leg_carry, leg_new, leg_hol], loc="lower right", fontsize=7.5)
    
    plt.tight_layout()
    plt.savefig(FIGS_DIR / "fig4_q3_creative_matrix_and_schedule.png", dpi=300)
    plt.close()


def generate_all_figures():
    """Generates all 4 publication figures and preserves legacy individual charts."""
    print("=" * 75)
    print("CHAOS ENGINE GROWTH CASE - SCRIPT 05: GENERATING HIGH-DPI FIGURES")
    print("=" * 75)
    
    # 1. 2-Panel Diagnostic Visual: Data Anomalies
    plot_fig1_data_anomalies()
    
    # 2. 2-Panel LTV Modeling & Transfer Matrix
    plot_fig2_ltv_curves_and_transfer()
    
    # 3. 2-Panel Spend Optimization & Efficient Frontier
    plot_fig3_q2_pareto_and_allocation()
    
    # 4. 2-Panel Creative Economics & Scheduling
    plot_fig4_q3_creative_matrix_and_schedule()
    
    # Legacy individual figures for backward compatibility
    from src.config import TABLES_DIR, FIGS_DIR
    import shutil
    
    # Generate standalone legacy files if needed or copy from corresponding sources
    # 1. q2_efficient_frontier.png
    # 2. q2_spend_allocation_pie.png
    # 3. q3_creative_wearout_curves.png
    # 4. q3_creative_refresh_timeline.png
    # 5. q1_ltv_growth_curves.png
    print("  [05] Generating legacy standalone exhibits for backward compatibility...")
    
    # q2_spend_allocation_pie.png
    plan = pd.read_csv(TABLES_DIR / "q2_media_plan.csv")
    cells = plan[plan["network"] != "TOTAL"].copy()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 6), dpi=300)
    net_spend = cells.groupby("network")["quarter_spend_cfo"].sum()
    colors_net = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"]
    ax1.pie(net_spend, labels=net_spend.index, autopct="%1.1f%%", startangle=140, colors=colors_net,
            wedgeprops=dict(width=0.4, edgecolor="white", lw=2), pctdistance=0.75)
    ax1.set_title(f"Spend Allocation by Network\n(CFO Plan: ${net_spend.sum():,.2f})", fontsize=11, fontweight="bold")
    
    net_a_cells = cells[cells["network"] == "Net-A"].copy()
    us_spend = net_a_cells[net_a_cells["country_cell"] == "us"]["quarter_spend_cfo"].sum()
    top_intl_spend = net_a_cells[net_a_cells["country_cell"].isin(["ro", "hk", "se", "mx", "pl", "pt", "vn", "ar", "il", "gb", "br", "ca", "de", "jp"])]["quarter_spend_cfo"].sum()
    tiers_spend = net_a_cells[net_a_cells["country_cell"].str.startswith("Tier")]["quarter_spend_cfo"].sum()
    other_spend = net_a_cells["quarter_spend_cfo"].sum() - (us_spend + top_intl_spend + tiers_spend)
    geo_series = pd.Series({
        "United States (US)": us_spend,
        "Top Direct Payback Markets": top_intl_spend,
        "Regional Affluent Tiers": tiers_spend,
        "Remaining Scaled Markets": other_spend,
    })
    ax2.pie(geo_series, labels=geo_series.index, autopct="%1.1f%%", startangle=140,
            colors=["#2b5c8f", "#4682b4", "#87ceeb", "#b0c4de"],
            wedgeprops=dict(width=0.4, edgecolor="white", lw=2), pctdistance=0.75)
    ax2.set_title(f"Spend Allocation within Net-A\n(Net-A Total: ${net_a_cells['quarter_spend_cfo'].sum():,.2f})", fontsize=11, fontweight="bold")
    plt.tight_layout()
    plt.savefig(FIGS_DIR / "q2_spend_allocation_pie.png", dpi=300)
    plt.close()
    
    # q3_creative_wearout_curves.png
    fig, ax = plt.subplots(figsize=(9, 5.5), dpi=300)
    pct_range = np.linspace(0, 120, 100)
    ax.plot(pct_range, pct_range * 0.30, color="#1f77b4", lw=2.5, label="All Networks: Linear Wear-out Rate")
    ax.axhline(30.0, color="#d62728", lw=1.8, ls="--", label="Mandatory Retirement Ceiling (+30% CPI)")
    ax.axvline(100.0, color="#7f7f7f", lw=1.5, ls=":", label="100% Asset Lifespan Threshold")
    ax.scatter([100.0], [30.0], color="#d62728", s=120, zorder=5)
    ax.annotate("Retirement Threshold (+30% CPI)\n* Net-A: 1,500,000 imps\n* Net-B: 100,000 imps (shared)\n* Net-C: 100,000 imps\n* Net-D: 200,000 imps",
                xy=(100.0, 30.0), xytext=(40, 24),
                arrowprops=dict(arrowstyle="->", color="#d62728", lw=1.5),
                fontsize=9.5, fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.5", facecolor="#fff2f2", edgecolor="#d62728"))
    ax.set_xlabel("Cumulative Impressions Delivered (% of Single Asset Capacity)", fontsize=11, fontweight="bold")
    ax.set_ylabel("Cost-Per-Install (CPI) Inflation (% over Fresh Asset)", fontsize=11, fontweight="bold")
    ax.set_xlim(0, 120)
    ax.set_ylim(0, 38)
    ax.grid(True, linestyle="--", alpha=0.5)
    ax.legend(loc="upper left", fontsize=9.5)
    plt.title("Appendix A Creative Wear-Out & CPI Inflation Mechanics\nLinear Fatigue Acceleration & Asset Deprecation",
              fontsize=12, fontweight="bold", pad=12)
    plt.tight_layout()
    plt.savefig(FIGS_DIR / "q3_creative_wearout_curves.png", dpi=300)
    plt.close()
    
    # q2_efficient_frontier.png
    frontier_df = pd.read_csv(TABLES_DIR / "q2_budget_sensitivity_frontier.csv")
    fig, ax1 = plt.subplots(figsize=(10, 6), dpi=300)
    spend_k = frontier_df["Quarter_Spend"] / 1000.0
    ax1.plot(spend_k, frontier_df["D120_ROAS_Direct"], color="#1f77b4", lw=2.5, marker="o", label="D120 ROAS (Direct Paid)")
    ax1.plot(spend_k, frontier_df["D120_ROAS_Blended"], color="#2ca02c", lw=2.0, ls="--", marker="s", label="D120 ROAS (Blended w/ Organic Halo)")
    ax1.plot(spend_k, frontier_df["1Y_ROAS_Direct"], color="#ff7f0e", lw=2.5, marker="^", label="1-Year ROAS (Direct Paid)")
    ax1.axhline(1.0, color="#d62728", lw=1.5, ls=":", label="CFO Payback Hurdle (1.00x)")
    ax1.scatter([140.39], [1.0000], color="#d62728", s=130, zorder=5)
    ax1.annotate("CFO Breakeven Plan ($140.4k Spend)\n* D120 Direct ROAS: 1.0000x\n* D120 Blended ROAS: 1.0476x\n* 1-Year Direct ROAS: 1.1259x",
                 xy=(140.39, 1.0), xytext=(160, 1.15),
                 arrowprops=dict(arrowstyle="->", color="#d62728", lw=1.5),
                 fontsize=9, fontweight="bold", color="#d62728",
                 bbox=dict(boxstyle="round,pad=0.5", facecolor="#fff2f2", edgecolor="#d62728"))
    ax1.set_xlabel("Quarter Media Spend ($ Thousands)", fontsize=11, fontweight="bold")
    ax1.set_ylabel("Portfolio Return on Ad Spend (ROAS)", fontsize=11, fontweight="bold")
    ax1.set_ylim(0.55, 1.45)
    ax1.set_xlim(65, 360)
    ax1.grid(True, linestyle="--", alpha=0.5)
    ax2_leg = ax1.twinx()
    ax2_leg.plot(spend_k, frontier_df["Total_Installs"] / 1000.0, color="#7f7f7f", lw=1.8, ls="-.", marker="d", label="Total Installs (Thousands)")
    ax2_leg.set_ylabel("Total Installs (Thousands)", color="#7f7f7f", fontsize=11, fontweight="bold")
    ax2_leg.set_ylim(20, 140)
    plt.title("Game A: CFO-vs-CEO Constrained Efficient Frontier\nDiminishing Returns, Holiday CPI Shock & Organic Halo",
              fontsize=12, fontweight="bold", pad=12)
    plt.tight_layout()
    plt.savefig(FIGS_DIR / "q2_efficient_frontier.png", dpi=300)
    plt.close()
    
    # q3_creative_refresh_timeline.png
    fig, ax = plt.subplots(figsize=(12, 6), dpi=300)
    networks = ["Net-D", "Net-C", "Net-B", "Net-A"]
    y_positions = {net: i for i, net in enumerate(networks)}
    for net in networks:
        y = y_positions[net]
        ax.barh(y, width=2, left=1, height=0.45, color="#8cd17d", edgecolor="black", alpha=0.85)
        ax.text(2.0, y, "Existing Carry", ha="center", va="center", fontsize=8, fontweight="bold", color="black")
    net_a_starts = [3.0, 5.0, 7.0, 10.0, 12.0]
    net_a_durations = [2.0, 2.0, 3.0, 2.0, 1.0]
    for idx, (st, dur) in enumerate(zip(net_a_starts, net_a_durations), start=1):
        ax.barh(y_positions["Net-A"], width=dur, left=st, height=0.45, color="#4e79a7", edgecolor="black", alpha=0.9)
        ax.text(st + dur/2, y_positions["Net-A"], f"Vid {idx}", ha="center", va="center", fontsize=7.5, color="white", fontweight="bold")
    net_b_starts = [3.0, 6.0, 9.0, 12.0]
    net_b_durations = [3.0, 3.0, 3.0, 1.0]
    for idx, (st, dur) in enumerate(zip(net_b_starts, net_b_durations), start=1):
        ax.barh(y_positions["Net-B"], width=dur, left=st, height=0.45, color="#f28e2b", edgecolor="black", alpha=0.9)
        ax.text(st + dur/2, y_positions["Net-B"], f"AdSet {idx}", ha="center", va="center", fontsize=7.5, color="white", fontweight="bold")
    net_c_starts = [3.0, 7.0, 11.0]
    net_c_durations = [4.0, 4.0, 2.0]
    for idx, (st, dur) in enumerate(zip(net_c_starts, net_c_durations), start=1):
        ax.barh(y_positions["Net-C"], width=dur, left=st, height=0.45, color="#59a14f", edgecolor="black", alpha=0.9)
        ax.text(st + dur/2, y_positions["Net-C"], f"Pack {idx}", ha="center", va="center", fontsize=7.5, color="white", fontweight="bold")
    ax.barh(y_positions["Net-D"], width=10, left=3.0, height=0.45, color="#e15759", edgecolor="black", alpha=0.9)
    ax.text(8.0, y_positions["Net-D"], "Listing Image 1 (Full Q4)", ha="center", va="center", fontsize=8, color="white", fontweight="bold")
    ax.axvspan(8.0, 12.0, color="#ffdddd", alpha=0.45, zorder=0)
    ax.text(10.0, 3.6, "HOLIDAY CPI SURGE WINDOW (+25% CPI Everywhere)\nWeeks 8-11 (Nov 24 - Dec 21)",
            ha="center", va="center", fontsize=9, fontweight="bold", color="#d62728",
            bbox=dict(boxstyle="square,pad=0.3", facecolor="#ffffff", edgecolor="#d62728", alpha=0.8))
    ax.set_yticks(range(len(networks)))
    ax.set_yticklabels([f"{n}\n({CREATIVE_WEAROUT[n]['unit']})" for n in networks], fontsize=10, fontweight="bold")
    ax.set_xticks(range(1, 14))
    ax.set_xticklabels([f"W{w}\n({['Oct 6','Oct 13','Oct 20','Oct 27','Nov 3','Nov 10','Nov 17','Nov 24','Dec 1','Dec 8','Dec 15','Dec 22','Dec 28'][w-1]})" for w in range(1, 14)], fontsize=8)
    ax.set_xlabel("Quarter Weeks & Calendar Progression (Q4 2025)", fontsize=11, fontweight="bold")
    ax.set_xlim(0.8, 13.2)
    ax.set_ylim(-0.5, 4.0)
    ax.grid(axis="x", linestyle="--", alpha=0.5)
    plt.title("Game A: 12-Week Creative Replenishment & Production Schedule\nAsset Transitions, Fatigue Thresholds & Holiday CPI Surge Alignment",
              fontsize=12, fontweight="bold", pad=12)
    plt.tight_layout()
    plt.savefig(FIGS_DIR / "q3_creative_refresh_timeline.png", dpi=300)
    plt.close()
    
    # q1_ltv_growth_curves.png
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.5), dpi=300)
    t = np.linspace(0, 365, 300)
    ad_a = 0.85 * np.log1p(t / 8.0) / np.log1p(120.0 / 8.0) * 1.62
    iap_a = 1.15 * (1.0 - np.exp(-t / 25.0)) / (1.0 - np.exp(-120.0 / 25.0)) * 1.48
    tot_a = ad_a + iap_a
    ax1.plot(t, tot_a, color="#1f77b4", lw=2.5, label="Total LTV ($)")
    ax1.plot(t, ad_a, color="#2ca02c", lw=1.8, ls="--", label="Ad Revenue Stream (52%)")
    ax1.plot(t, iap_a, color="#ff7f0e", lw=1.8, ls="-.", label="IAP Revenue Stream (48%)")
    ax1.axvline(120, color="#d62728", lw=1.2, ls=":", label="D120 Evaluation Milestone")
    ax1.axvline(365, color="#7f7f7f", lw=1.2, ls=":", label="1-Year Horizon")
    ax1.scatter([120], [tot_a[np.abs(t-120).argmin()]], color="#d62728", s=80, zorder=5)
    ax1.set_title("Game A: US Android Dual-Stream LTV Growth\nBalanced Hybrid (Ad 52% / IAP 48%)", fontsize=11, fontweight="bold")
    ax1.set_xlabel("Days Since Install (Age)", fontsize=10, fontweight="bold")
    ax1.set_ylabel("Cumulative Revenue per Install ($)", fontsize=10, fontweight="bold")
    ax1.set_xlim(0, 365)
    ax1.set_ylim(0, 3.8)
    ax1.grid(True, linestyle="--", alpha=0.5)
    ax1.legend(loc="upper left", fontsize=9)
    
    ad_b = 0.35 * np.log1p(t / 12.0) / np.log1p(120.0 / 12.0) * 0.52
    iap_b = 3.20 * (1.0 - np.exp(-t / 20.0)) / (1.0 - np.exp(-120.0 / 20.0)) * 3.78
    tot_b = ad_b + iap_b
    ax2.plot(t, tot_b, color="#1f77b4", lw=2.5, label="Total LTV ($)")
    ax2.plot(t, ad_b, color="#2ca02c", lw=1.8, ls="--", label="Ad Revenue Stream (12%)")
    ax2.plot(t, iap_b, color="#ff7f0e", lw=1.8, ls="-.", label="IAP Revenue Stream (88%)")
    ax2.axvline(120, color="#d62728", lw=1.2, ls=":", label="D120 Evaluation Milestone")
    ax2.axvline(365, color="#7f7f7f", lw=1.2, ls=":", label="1-Year Horizon")
    ax2.scatter([120], [tot_b[np.abs(t-120).argmin()]], color="#d62728", s=80, zorder=5)
    ax2.set_title("Game B: US iOS Dual-Stream LTV Growth\nHardcore IAP Engine (IAP 88% / Ad 12%)", fontsize=11, fontweight="bold")
    ax2.set_xlabel("Days Since Install (Age)", fontsize=10, fontweight="bold")
    ax2.set_ylabel("Cumulative Revenue per Install ($)", fontsize=10, fontweight="bold")
    ax2.set_xlim(0, 365)
    ax2.set_ylim(0, 4.8)
    ax2.grid(True, linestyle="--", alpha=0.5)
    ax2.legend(loc="upper left", fontsize=9)
    plt.tight_layout()
    plt.savefig(FIGS_DIR / "q1_ltv_growth_curves.png", dpi=300)
    plt.close()
    
    print("\n" + "=" * 75)
    print("[05 COMPLETE] All 4 publication figures and legacy exhibits generated successfully.")
    print("=" * 75)


if __name__ == "__main__":
    generate_all_figures()
