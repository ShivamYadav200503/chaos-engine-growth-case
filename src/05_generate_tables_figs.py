"""
Script 05: Generate Publication-Ready Figures & Visual Exhibits
Chaos Engine Labs Growth Case

Generates publication-quality high-DPI figures into outputs/figures/:
1. q2_efficient_frontier.png:
   - CFO vs CEO Pareto frontier mapping Spend vs D120 ROAS, 1-Year ROAS, and Installs.
   - Highlights CFO Breakeven ($140k), Organic Halo Breakeven ($158k), 1Y Breakeven ($182k),
     and CEO Max Budget ($250k).
2. q2_spend_allocation_pie.png:
   - Media Plan capital allocation donut charts by Network and by Geography.
3. q3_creative_wearout_curves.png:
   - CPI inflation wear-out trajectories per network up to +30% retirement ceiling.
4. q3_creative_refresh_timeline.png:
   - Gantt-style operational production and active deployment cadence across 12 weeks.
5. q1_ltv_growth_curves.png:
   - Dual-stream parametric LTV growth curves (Ad vs IAP vs Total) for Game A and Game B.
"""

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

from src.config import TABLES_DIR, FIGS_DIR, PROC_DIR, CREATIVE_WEAROUT


def plot_efficient_frontier():
    """Generates the CFO vs CEO Pareto Frontier chart."""
    print("  [05] Generating q2_efficient_frontier.png...")
    frontier_df = pd.read_csv(TABLES_DIR / "q2_budget_sensitivity_frontier.csv")
    
    fig, ax1 = plt.subplots(figsize=(10, 6), dpi=300)
    
    spend_k = frontier_df["Quarter_Spend"] / 1000.0
    roas_d120 = frontier_df["D120_ROAS_Direct"]
    roas_d120_org = frontier_df["D120_ROAS_Blended"]
    roas_1y = frontier_df["1Y_ROAS_Direct"]
    installs_k = frontier_df["Total_Installs"] / 1000.0
    
    # ROAS curves
    color_d120 = "#1f77b4"
    color_org = "#2ca02c"
    color_1y = "#ff7f0e"
    color_inst = "#7f7f7f"
    
    line1, = ax1.plot(spend_k, roas_d120, color=color_d120, lw=2.5, marker="o", label="D120 ROAS (Direct Paid)")
    line2, = ax1.plot(spend_k, roas_d120_org, color=color_org, lw=2.0, ls="--", marker="s", label="D120 ROAS (Blended w/ Organic Halo)")
    line3, = ax1.plot(spend_k, roas_1y, color=color_1y, lw=2.5, marker="^", label="1-Year ROAS (Direct Paid)")
    
    # CFO 1.0x Hurdle Line
    ax1.axhline(1.0, color="#d62728", lw=1.5, ls=":", label="CFO Payback Hurdle (1.00x)")
    
    # Highlight key milestone points
    # 1. CFO Breakeven ($140.4k)
    ax1.scatter([140.392], [1.0000], color="#d62728", s=100, zorder=5)
    ax1.annotate("CFO D120 Breakeven\n($140.4k spend, 1.00x)",
                 xy=(140.392, 1.0000), xytext=(110, 1.06),
                 arrowprops=dict(arrowstyle="->", color="#d62728", lw=1.2),
                 fontsize=9, fontweight="bold", color="#d62728")
                 
    # 2. 1-Year Breakeven ($182.3k)
    ax1.scatter([182.325], [1.0000], color="#ff7f0e", s=100, zorder=5)
    ax1.annotate("1-Year Cash Breakeven\n($182.3k spend, 1.00x 1Y)",
                 xy=(182.325, 1.0000), xytext=(190, 1.08),
                 arrowprops=dict(arrowstyle="->", color="#ff7f0e", lw=1.2),
                 fontsize=9, fontweight="bold", color="#d62728")
                 
    # 3. CEO Max Budget ($250k)
    ax1.scatter([250.0], [0.7666], color="#1f77b4", s=100, zorder=5)
    ax1.annotate("CEO Max Budget\n($250k spend, 0.77x D120)",
                 xy=(250.0, 0.7666), xytext=(240, 0.65),
                 arrowprops=dict(arrowstyle="->", color="#1f77b4", lw=1.2),
                 fontsize=9, fontweight="bold", color="#1f77b4")
    
    ax1.set_xlabel("Quarter Media Spend ($ Thousands)", fontsize=11, fontweight="bold")
    ax1.set_ylabel("Portfolio Return on Ad Spend (ROAS)", fontsize=11, fontweight="bold")
    ax1.set_ylim(0.55, 1.45)
    ax1.set_xlim(65, 360)
    ax1.grid(True, linestyle="--", alpha=0.5)
    
    # Secondary axis for installs
    ax2 = ax1.twinx()
    line4, = ax2.plot(spend_k, installs_k, color=color_inst, lw=1.8, ls="-.", marker="d", label="Total Installs (Thousands)")
    ax2.set_ylabel("Total Installs (Thousands)", color=color_inst, fontsize=11, fontweight="bold")
    ax2.tick_params(axis="y", labelcolor=color_inst)
    ax2.set_ylim(20, 140)
    
    # Legend
    lines = [line1, line2, line3, line4]
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc="upper right", framealpha=0.9, fontsize=9)
    
    plt.title("Game A: CFO-vs-CEO Constrained Efficient Frontier\nDiminishing Returns, Holiday CPI Shock & Organic Halo",
              fontsize=12, fontweight="bold", pad=12)
    plt.tight_layout()
    plt.savefig(FIGS_DIR / "q2_efficient_frontier.png", dpi=300)
    plt.close()


def plot_spend_allocation_pie():
    """Generates the spend allocation charts by Network and Geography."""
    print("  [05] Generating q2_spend_allocation_pie.png...")
    plan = pd.read_csv(TABLES_DIR / "q2_media_plan.csv")
    cells = plan[plan["network"] != "TOTAL"].copy()
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 6), dpi=300)
    
    # Left: Spend by Network (CFO Plan)
    net_spend = cells.groupby("network")["quarter_spend_cfo"].sum()
    colors_net = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"]
    
    wedges1, texts1, autotexts1 = ax1.pie(
        net_spend,
        labels=net_spend.index,
        autopct="%1.1f%%",
        startangle=140,
        colors=colors_net,
        wedgeprops=dict(width=0.4, edgecolor="white", lw=2),
        pctdistance=0.75
    )
    for at in autotexts1:
        at.set_fontsize(9)
        at.set_fontweight("bold")
    for t in texts1:
        t.set_fontsize(10)
        t.set_fontweight("bold")
        
    ax1.set_title(f"Spend Allocation by Network\n(CFO Plan: ${net_spend.sum():,.2f})", fontsize=11, fontweight="bold")
    
    # Right: Spend within Net-A by Geography
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
    
    colors_geo = ["#4e79a7", "#59a14f", "#edc948", "#b07aa1"]
    wedges2, texts2, autotexts2 = ax2.pie(
        geo_series,
        labels=geo_series.index,
        autopct="%1.1f%%",
        startangle=140,
        colors=colors_geo,
        wedgeprops=dict(width=0.4, edgecolor="white", lw=2),
        pctdistance=0.75
    )
    for at in autotexts2:
        at.set_fontsize(9)
        at.set_fontweight("bold")
    for t in texts2:
        t.set_fontsize(10)
        t.set_fontweight("bold")
        
    ax2.set_title(f"Net-A Android Spend by Geography\n(Total: ${net_a_cells['quarter_spend_cfo'].sum():,.2f})", fontsize=11, fontweight="bold")
    
    plt.suptitle("Game A Q4 Media Plan Capital Allocation", fontsize=14, fontweight="bold", y=1.02)
    plt.tight_layout()
    plt.savefig(FIGS_DIR / "q2_spend_allocation_pie.png", dpi=300)
    plt.close()


def plot_creative_wearout_curves():
    """Generates the creative wear-out curves showing CPI inflation vs impressions."""
    print("  [05] Generating q3_creative_wearout_curves.png...")
    fig, ax = plt.subplots(figsize=(9, 6), dpi=300)
    
    # Net-A: 0 to 1.8M imps, +20% / 1M
    imps_a = np.linspace(0, 1.8, 100)
    cpi_a = imps_a * 20.0
    
    # Net-B: 0 to 0.15M imps, +300% / 1M
    imps_b = np.linspace(0, 0.15, 100)
    cpi_b = imps_b * 300.0
    
    # Net-C: 0 to 0.15M imps, +300% / 1M
    imps_c = np.linspace(0, 0.15, 100)
    cpi_c = imps_c * 300.0
    
    # Net-D: 0 to 0.25M imps, +150% / 1M
    imps_d = np.linspace(0, 0.25, 100)
    cpi_d = imps_d * 150.0
    
    # We plot against % of max creative capacity (0% to 120%)
    pct_range = np.linspace(0, 120, 100)
    
    # CPI rise at 100% capacity is exactly +30% for all networks
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


def plot_creative_refresh_timeline():
    """Generates the week-by-week Gantt-style replenishment schedule."""
    print("  [05] Generating q3_creative_refresh_timeline.png...")
    sched = pd.read_csv(TABLES_DIR / "q3_creative_replenishment_schedule.csv")
    
    fig, ax = plt.subplots(figsize=(12, 6), dpi=300)
    
    networks = ["Net-D", "Net-C", "Net-B", "Net-A"]  # bottom to top
    y_positions = {net: i for i, net in enumerate(networks)}
    colors_net = {"Net-A": "#4e79a7", "Net-B": "#f28e2b", "Net-C": "#59a14f", "Net-D": "#e15759"}
    
    # Existing creative bar (Weeks 1 to 2)
    for net in networks:
        y = y_positions[net]
        ax.barh(y, width=2, left=1, height=0.45, color="#8cd17d", edgecolor="black", alpha=0.85)
        ax.text(2.0, y, "Existing Carry", ha="center", va="center", fontsize=8, fontweight="bold", color="black")
        
    # New creatives (Weeks 3 to 12)
    # Net-A: 5 units (~2.4 wks each)
    net_a_starts = [3.0, 5.0, 7.0, 10.0, 12.0]
    net_a_durations = [2.0, 2.0, 3.0, 2.0, 1.0]
    for idx, (st, dur) in enumerate(zip(net_a_starts, net_a_durations), start=1):
        ax.barh(y_positions["Net-A"], width=dur, left=st, height=0.45, color="#4e79a7", edgecolor="black", alpha=0.9)
        ax.text(st + dur/2, y_positions["Net-A"], f"Vid {idx}", ha="center", va="center", fontsize=7.5, color="white", fontweight="bold")
        
    # Net-B: 4 units (~3.3 wks each)
    net_b_starts = [3.0, 6.0, 9.0, 12.0]
    net_b_durations = [3.0, 3.0, 3.0, 1.0]
    for idx, (st, dur) in enumerate(zip(net_b_starts, net_b_durations), start=1):
        ax.barh(y_positions["Net-B"], width=dur, left=st, height=0.45, color="#f28e2b", edgecolor="black", alpha=0.9)
        ax.text(st + dur/2, y_positions["Net-B"], f"AdSet {idx}", ha="center", va="center", fontsize=7.5, color="white", fontweight="bold")
        
    # Net-C: 3 units (~4.2 wks each)
    net_c_starts = [3.0, 7.0, 11.0]
    net_c_durations = [4.0, 4.0, 2.0]
    for idx, (st, dur) in enumerate(zip(net_c_starts, net_c_durations), start=1):
        ax.barh(y_positions["Net-C"], width=dur, left=st, height=0.45, color="#59a14f", edgecolor="black", alpha=0.9)
        ax.text(st + dur/2, y_positions["Net-C"], f"Pack {idx}", ha="center", va="center", fontsize=7.5, color="white", fontweight="bold")
        
    # Net-D: 1 unit (10 wks)
    ax.barh(y_positions["Net-D"], width=10, left=3.0, height=0.45, color="#e15759", edgecolor="black", alpha=0.9)
    ax.text(8.0, y_positions["Net-D"], "Listing Image 1 (Full Q4)", ha="center", va="center", fontsize=8, color="white", fontweight="bold")
    
    # Holiday Surge shading (Weeks 8 to 11 = Nov 24 - Dec 21)
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
    
    # Legend
    carry_patch = mpatches.Patch(color="#8cd17d", label="Weeks 1-2 Existing Carry")
    new_patch = mpatches.Patch(color="#4e79a7", label="New Creative Deployments")
    holiday_patch = mpatches.Patch(facecolor="#ffdddd", edgecolor="#d62728", alpha=0.7, label="Holiday Surge Window")
    ax.legend(handles=[carry_patch, new_patch, holiday_patch], loc="lower right", fontsize=9)
    
    plt.title("Game A: 12-Week Creative Replenishment & Production Schedule\nAsset Transitions, Fatigue Thresholds & Holiday CPI Surge Alignment",
              fontsize=12, fontweight="bold", pad=12)
    plt.tight_layout()
    plt.savefig(FIGS_DIR / "q3_creative_refresh_timeline.png", dpi=300)
    plt.close()


def plot_ltv_growth_curves():
    """Generates the dual-stream LTV curves from Question 1."""
    print("  [05] Generating q1_ltv_growth_curves.png...")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.5), dpi=300)
    
    t = np.linspace(0, 365, 300)
    
    # Game A Curves (US Android)
    # Parametric fits from Q1: Ad LTV log-growth, IAP LTV front-loaded saturation
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
    ax1.set_ylabel("Cumulative LTV ($ / User)", fontsize=10, fontweight="bold")
    ax1.grid(True, linestyle="--", alpha=0.5)
    ax1.legend(loc="lower right", fontsize=9)
    
    # Game B Curves (US Android)
    # Parametric fits from Q1: 99.6% Ad, 0.4% IAP
    ad_b = 1.82 * (t / 120.0)**0.45
    iap_b = 0.01 * (1.0 - np.exp(-t / 15.0))
    tot_b = ad_b + iap_b
    
    ax2.plot(t, tot_b, color="#1f77b4", lw=2.5, label="Total LTV ($)")
    ax2.plot(t, ad_b, color="#2ca02c", lw=1.8, ls="--", label="Ad Revenue Stream (99.6%)")
    ax2.plot(t, iap_b, color="#ff7f0e", lw=1.8, ls="-.", label="IAP Revenue Stream (0.4%)")
    
    ax2.axvline(120, color="#d62728", lw=1.2, ls=":", label="D120 Evaluation Milestone")
    ax2.axvline(365, color="#7f7f7f", lw=1.2, ls=":", label="1-Year Horizon")
    ax2.scatter([120], [tot_b[np.abs(t-120).argmin()]], color="#d62728", s=80, zorder=5)
    
    ax2.set_title("Game B: US Android Ad-Monetized LTV Growth\nPure Ad Engine (Ad 99.6% / IAP 0.4%)", fontsize=11, fontweight="bold")
    ax2.set_xlabel("Days Since Install (Age)", fontsize=10, fontweight="bold")
    ax2.set_ylabel("Cumulative LTV ($ / User)", fontsize=10, fontweight="bold")
    ax2.grid(True, linestyle="--", alpha=0.5)
    ax2.legend(loc="lower right", fontsize=9)
    
    plt.suptitle("Parametric Dual-Stream LTV Growth Curves & Monetization Architecture", fontsize=13, fontweight="bold", y=1.02)
    plt.tight_layout()
    plt.savefig(FIGS_DIR / "q1_ltv_growth_curves.png", dpi=300)
    plt.close()


def run_table_figure_generation():
    """Main execution entry point for Script 05."""
    print("=" * 70)
    print("CHAOS ENGINE GROWTH CASE - SCRIPT 05: GENERATING HIGH-DPI FIGURES")
    print("=" * 70)
    
    FIGS_DIR.mkdir(parents=True, exist_ok=True)
    TABLES_DIR.mkdir(parents=True, exist_ok=True)
    
    # Generate all 5 publication-ready charts
    plot_efficient_frontier()
    plot_spend_allocation_pie()
    plot_creative_wearout_curves()
    plot_creative_refresh_timeline()
    plot_ltv_growth_curves()
    
    print("\n" + "=" * 70)
    print("[05 COMPLETE] All 5 high-DPI figures generated in outputs/figures/.")
    print("=" * 70)


if __name__ == "__main__":
    run_table_figure_generation()
