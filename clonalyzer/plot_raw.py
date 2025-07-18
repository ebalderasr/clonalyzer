#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
plot_raw.py
~~~~~~~~~~~
Generate per-sample scatter plots (Clone × Rep) for CHO fed-batch data.

Plots include:
• Time-course scatter plots (raw values)
• Kinetic parameter trends
• Correlation plots

Assumes `outputs/interval_kinetics.csv` has been generated by
`interval_kinetics.py`.

Outputs
-------
Figures saved in:
• outputs/figures_raw/time/
• outputs/figures_raw/kinetics/
• outputs/figures_raw/corr/

Author
------
Emiliano Balderas R. | 16 Jul 2025
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# ───── Configuration ───────────────────────────────────────────────────── #
CSV_PATH = Path("outputs/interval_kinetics.csv")
FIGURE_DIR = Path("outputs/figures_raw")
SUBFOLDERS = ["time", "kinetics", "corr"]
FIGSIZE = (8, 6)
DPI = 300
PALETTE = "tab10"
AXES_RECT = [0.15, 0.15, 0.78, 0.78]

sns.set_style("whitegrid")

SHAPE_MAP = {1: "o", 2: "s", 3: "D"}  # markers by replicate

# ───── Load data ───────────────────────────────────────────────────────── #
if not CSV_PATH.exists():
    raise FileNotFoundError(f"❌ File not found:\n  {CSV_PATH}")

df = pd.read_csv(CSV_PATH)

# ───── Set up output folders ───────────────────────────────────────────── #
for sub in SUBFOLDERS:
    (FIGURE_DIR / sub).mkdir(parents=True, exist_ok=True)

# ───── Color palette by clone ──────────────────────────────────────────── #
clones = df["Clone"].unique().tolist()
colors = sns.color_palette(PALETTE, len(clones))
COLOR = dict(zip(clones, colors))

# ───── Helper: scatter plot by clone × rep ────────────────────────────── #
def scatter_by_rep(ax, data, x, y):
    for cl, g_cl in data.groupby("Clone", observed=True, sort=False):
        for rp, g_rp in g_cl.groupby("Rep", observed=True, sort=False):
            ax.scatter(
                g_rp[x], g_rp[y],
                color=COLOR[cl],
                marker=SHAPE_MAP.get(rp, "o"),
                s=65, edgecolor="white", linewidth=0.4,
                label=f"{cl}-rep{rp}" if ax.get_legend() is None else "",
            )

# ───── 1. Raw time-course plots ───────────────────────────────────────── #
PLOT_TIME = [
    ("VCD",       r'VCD (cells·mL$^{-1}$)',      "Viable Cell Density"),
    ("Viab_pct",  r'Viability (%)',              "Cell Viability"),
    ("Glc_mM",    r'Glucose (mM)',               "Glucose Concentration"),
    ("Lac_mM",    r'Lactate (mM)',               "Lactate Concentration"),
    ("Gln_mM",    r'Glutamine (mM)',             "Glutamine Concentration"),
    ("Glu_mM",    r'Glutamate (mM)',             "Glutamate Concentration"),
    ("GFP_mean",  r'GFP (a.u.)',                 "GFP Mean Fluorescence"),
    ("TMRM_mean", r'TMRM (a.u.)',                "TMRM Mean Fluorescence"),
]

for var, ylab, title in PLOT_TIME:
    if var not in df.columns:
        print(f"⚠️  '{var}' not found; skipping.")
        continue

    fig = plt.figure(figsize=FIGSIZE, dpi=DPI)
    ax = fig.add_axes(AXES_RECT)

    scatter_by_rep(ax, df, "t_hr", var)
    ax.set_xlabel("Time (h)")
    ax.set_ylabel(ylab)
    ax.set_title(title)
    ax.set_xlim(left=0)
    ax.legend(title="Clone–Rep", fontsize=8)

    fig.tight_layout()
    fig.savefig(FIGURE_DIR / "time" / f"{var}_raw.png")
    plt.close(fig)

print("✓ Time trends saved in ./outputs/figures_raw/time")

# ───── 2. Kinetic parameters vs. time ───────────────────────────────────── #
PLOT_KIN = [
    ("mu",        r'μ (h$^{-1}$)',                     "Specific Growth Rate"),
    ("IVCD_tot",  r'IVCD (cells·h)',                   "Integral Viable Cell Density"),
    ("dX",        r'ΔX (cells)',                       "Net Cell Change"),
    ("dG",        r'ΔGlucose (mol)',                   "Net Glucose Consumption"),
    ("dL",        r'ΔLactate (mol)',                   "Net Lactate Production"),
    ("q_G",       r'q$_G$ (pmol·cell$^{-1}$·h$^{-1}$)',"Specific Glucose Consumption"),
    ("q_L",       r'q$_L$ (pmol·cell$^{-1}$·h$^{-1}$)',"Specific Lactate Production"),
    ("Y_XG",      r'Y$_{X/G}$ (cells·mol$^{-1}$)',     "Yield on Glucose"),
    ("Y_XL",      r'Y$_{X/L}$ (cells·mol$^{-1}$)',     "Yield on Lactate"),
]

for var, ylab, title in PLOT_KIN:
    if var not in df.columns:
        continue

    fig = plt.figure(figsize=FIGSIZE, dpi=DPI)
    ax = fig.add_axes(AXES_RECT)

    scatter_by_rep(ax, df, "t_hr", var)
    ax.set_xlabel("Time (h)")
    ax.set_ylabel(ylab)
    ax.set_title(title)
    ax.set_xlim(left=0)
    ax.legend(title="Clone–Rep", fontsize=8)

    fig.tight_layout()
    fig.savefig(FIGURE_DIR / "kinetics" / f"{var}_raw.png")
    plt.close(fig)

print("✓ Kinetic plots saved in ./outputs/figures_raw/kinetics")

# ───── 3. Correlation plots ────────────────────────────────────────────── #
PAIR_CORR = [
    ("mu",  "q_G",        r'μ (h$^{-1}$)',                     r'q$_G$ (pmol·cell$^{-1}$·h$^{-1}$)', "μ vs. q$_G$"),
    ("mu",  "q_L",        r'μ (h$^{-1}$)',                     r'q$_L$ (pmol·cell$^{-1}$·h$^{-1}$)', "μ vs. q$_L$"),
    ("mu",  "GFP_mean",   r'μ (h$^{-1}$)',                     r'GFP (a.u.)',                       "μ vs. GFP"),
    ("mu",  "TMRM_mean",  r'μ (h$^{-1}$)',                     r'TMRM (a.u.)',                      "μ vs. TMRM"),
    ("q_G", "q_L",        r'q$_G$ (pmol·cell$^{-1}$·h$^{-1}$)',r'q$_L$ (pmol·cell$^{-1}$·h$^{-1}$)', "q$_G$ vs. q$_L$"),
]

for x, y, xl, yl, title in PAIR_CORR:
    if {x, y}.difference(df.columns):
        continue

    fig = plt.figure(figsize=FIGSIZE, dpi=DPI)
    ax = fig.add_axes(AXES_RECT)

    scatter_by_rep(ax, df, x, y)
    ax.set_xlabel(xl)
    ax.set_ylabel(yl)
    ax.set_title(title)

    if x in {"mu", "q_G", "q_L"}:
        ax.set_xlim(left=0)
    if y in {"mu", "q_G", "q_L"}:
        ax.set_ylim(bottom=0)

    ax.legend(title="Clone–Rep", fontsize=8)

    fig.tight_layout()
    fig.savefig(FIGURE_DIR / "corr" / f"{x}_vs_{y}_raw.png")
    plt.close(fig)

print("✓ Correlations saved in ./outputs/figures_raw/corr")
