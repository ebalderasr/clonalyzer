#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
plot_grouped.py
~~~~~~~~~~~~~~~
Generate mean ± SD line plots from CHO fed-batch data
aggregated by Clone × Time (`grouped_kinetics.py`).

Outputs
-------
Figures saved in:
• outputs/figures_agg/time/
• outputs/figures_agg/kinetics/
• outputs/figures_agg/corr/

Author
------
Emiliano Balderas R. | 16 Jul 2025
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# ───── Configuration ───────────────────────────────────────────────────── #
CSV_PATH = Path("outputs/results_agg_by_clone_time.csv")
FIGURE_DIR = Path("outputs/figures_agg")
SUBFOLDERS = ["time", "kinetics", "corr"]
FIGSIZE, DPI = (8, 6), 300
AXES_RECT = [0.15, 0.15, 0.78, 0.78]
PALETTE = "tab10"

sns.set_style("whitegrid")

# ───── Load aggregated data ────────────────────────────────────────────── #
if not CSV_PATH.exists():
    raise FileNotFoundError(
        f"❌ Aggregated file not found:\n  {CSV_PATH}\n"
        "Please run `grouped_kinetics.py` first."
    )

agg_df = pd.read_csv(CSV_PATH)

# ───── Set up output folders ───────────────────────────────────────────── #
for sub in SUBFOLDERS:
    (FIGURE_DIR / sub).mkdir(parents=True, exist_ok=True)

# ───── Color palette by clone ──────────────────────────────────────────── #
clones = agg_df["Clone"].unique().tolist()
colors = sns.color_palette(PALETTE, len(clones))
COLOR = dict(zip(clones, colors))

# ───── Helper: plot with error bars ────────────────────────────────────── #
def plot_line_with_error(ax, x, y, yerr, label, color):
    ax.errorbar(x, y, yerr=yerr, label=label,
                fmt="-o", color=color, capsize=3, lw=1.5, markersize=5)

# ───── 1. Time-course trends ───────────────────────────────────────────── #
PLOT_TIME = [
    ("VCD",       r'VCD (cells·mL$^{-1}$)',      "Viable Cell Density"),
    ("Glc_mM",    r'Glucose (mM)',               "Glucose Concentration"),
    ("Lac_mM",    r'Lactate (mM)',               "Lactate Concentration"),
    ("Gln_mM",    r'Glutamine (mM)',             "Glutamine Concentration"),
    ("Glu_mM",    r'Glutamate (mM)',             "Glutamate Concentration"),
    ("Viab_pct",  r'Viability (%)',              "Cell Viability"),
    ("GFP_mean",  r'GFP (a.u.)',                 "GFP Mean Fluorescence"),
    ("TMRM_mean", r'TMRM (a.u.)',                "TMRM Mean Fluorescence"),
]

for var, ylab, title in PLOT_TIME:
    avg, sd = f"{var}_avg", f"{var}_sd"
    if {avg, sd}.difference(agg_df.columns): continue

    fig, ax = plt.subplots(figsize=FIGSIZE, dpi=DPI)
    for cl in clones:
        g = agg_df[agg_df["Clone"] == cl]
        plot_line_with_error(ax, g["t_hr"], g[avg], g[sd], cl, COLOR[cl])

    ax.set_xlabel("Time (h)")
    ax.set_ylabel(ylab)
    ax.set_title(title)
    ax.legend(title="Clone")
    ax.set_xlim(left=0)
    fig.tight_layout()
    fig.savefig(FIGURE_DIR / "time" / f"{var}_avg_sd.png")
    plt.close(fig)

print("✓ Time trends saved in ./outputs/figures_agg/time")

# ───── 2. Kinetic parameters vs time ────────────────────────────────────── #
PLOT_KIN = [
    ("mu",       r'μ (h$^{-1}$)',                     "Specific Growth Rate"),
    ("IVCD_tot", r'IVCD (cells·h)',                   "Integral Viable Cell Density"),
    ("dX",       r'ΔX (cells)',                       "Net Cell Change"),
    ("dG",       r'ΔGlucose (mol)',                   "Net Glucose Consumption"),
    ("dL",       r'ΔLactate (mol)',                   "Net Lactate Production"),
    ("q_G",      r'q$_G$ (pmol·cell$^{-1}$·h$^{-1}$)',"Specific Glucose Consumption"),
    ("q_L",      r'q$_L$ (pmol·cell$^{-1}$·h$^{-1}$)',"Specific Lactate Production"),
    ("Y_XG",     r'Y$_{X/G}$ (cells·mol$^{-1}$)',     "Yield on Glucose"),
    ("Y_XL",     r'Y$_{X/L}$ (cells·mol$^{-1}$)',     "Yield on Lactate"),
]

for var, ylab, title in PLOT_KIN:
    avg, sd = f"{var}_avg", f"{var}_sd"
    if {avg, sd}.difference(agg_df.columns): continue

    fig, ax = plt.subplots(figsize=FIGSIZE, dpi=DPI)
    for cl in clones:
        g = agg_df[(agg_df["Clone"] == cl) & (~agg_df[avg].isna())]
        if g.empty: continue
        plot_line_with_error(ax, g["t_hr"], g[avg], g[sd], cl, COLOR[cl])

    ax.set_xlabel("Time (h)")
    ax.set_ylabel(ylab)
    ax.set_title(title)
    ax.legend(title="Clone")
    ax.set_xlim(left=0)
    fig.tight_layout()
    fig.savefig(FIGURE_DIR / "kinetics" / f"{var}_avg_sd.png")
    plt.close(fig)

print("✓ Kinetics saved in ./outputs/figures_agg/kinetics")

# ───── 3. Correlation plots (mean ± SD) ─────────────────────────────────── #
PLOT_CORR = [
    ("mu",  "q_G",        r'μ (h$^{-1}$)',                     r'q$_G$ (pmol·cell$^{-1}$·h$^{-1}$)', "μ vs. q$_G$"),
    ("mu",  "q_L",        r'μ (h$^{-1}$)',                     r'q$_L$ (pmol·cell$^{-1}$·h$^{-1}$)', "μ vs. q$_L$"),
    ("mu",  "GFP_mean",   r'μ (h$^{-1}$)',                     r'GFP (a.u.)',                       "μ vs. GFP"),
    ("mu",  "TMRM_mean",  r'μ (h$^{-1}$)',                     r'TMRM (a.u.)',                      "μ vs. TMRM"),
    ("q_G", "q_L",        r'q$_G$ (pmol·cell$^{-1}$·h$^{-1}$)',r'q$_L$ (pmol·cell$^{-1}$·h$^{-1}$)', "q$_G$ vs. q$_L$"),
]

for x, y, xl, yl, title in PLOT_CORR:
    xm, xs, ym, ys = f"{x}_avg", f"{x}_sd", f"{y}_avg", f"{y}_sd"
    if {xm, xs, ym, ys}.difference(agg_df.columns): continue

    fig, ax = plt.subplots(figsize=FIGSIZE, dpi=DPI)
    for cl in clones:
        g = agg_df[agg_df["Clone"] == cl]
        ax.errorbar(g[xm], g[ym], xerr=g[xs], yerr=g[ys],
                    fmt="o", capsize=3, label=cl, color=COLOR[cl])

    ax.set_xlabel(xl)
    ax.set_ylabel(yl)
    ax.set_title(title)
    if x in {"mu", "q_G", "q_L"}:
        ax.set_xlim(left=0)
    if y in {"mu", "q_G", "q_L"}:
        ax.set_ylim(bottom=0)
    ax.legend(title="Clone")
    fig.tight_layout()
    fig.savefig(FIGURE_DIR / "corr" / f"{x}_vs_{y}_avg_sd.png")
    plt.close(fig)

print("✓ Correlations saved in ./outputs/figures_agg/corr")
