#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
exp_phase_kinetics.py
~~~~~~~~~~~~~~~~~~~~~
Kinetic and stoichiometric calculations for CHO fed‑batch cultures
during the exponential growth phase (Clone × Rep).

Workflow
--------
1. Ask user for exponential phase time window.
2. Load and clean CSV data (skipping metadata row).
3. Convert glucose and lactate to mol/mL.
4. For each Clone × Rep:
   • Estimate growth rate (μ, h⁻¹)
   • Integrate viable cell density (IVCD, cell·h)
   • Compute balances (dX, dGlc, dLac)
   • Compute yields and specific rates
5. Summarize results by Clone (mean ± SD).
6. Export two CSV files.

Outputs
-------
• outputs/kinetics_by_clone_rep.csv
• outputs/kinetics_by_clone.csv

Author
------
Emiliano Balderas R. | 16 Jul 2025
"""

import numpy as np
import pandas as pd
from pathlib import Path
import os

# ───── Configuration ───────────────────────────────────────────────────── #
DATA_FILE = Path("data/data.csv")
OUTFILE_REP = Path("outputs/kinetics_by_clone_rep.csv")
OUTFILE_AGG = Path("outputs/kinetics_by_clone.csv")

MM_GLC = 180.156  # g/mol
MM_LAC = 90.080   # g/mol

# ───── Ask user for phase limits (if run directly) ─────────────────────── #
def get_phase_window():
    try:
        start = int(input("Start of exponential phase (h): "))
        end = int(input("End of exponential phase (h): "))
        if start >= end:
            raise ValueError("Start must be less than end.")
    except Exception as e:
        print(f"❌ Invalid input: {e}")
        print("Using default: 0–96 h")
        start, end = 0, 96
    return start, end

if __name__ == "__main__":
    EXP_START_HR, EXP_END_HR = get_phase_window()
else:
    EXP_START_HR, EXP_END_HR = 0, 96

# ───── Load and filter data ────────────────────────────────────────────── #
if not DATA_FILE.exists():
    raise FileNotFoundError(f"❌ Input file not found:\n  {DATA_FILE}")

df = (
    pd.read_csv(DATA_FILE, skiprows=1)
      .dropna(subset=["Clone", "Rep", "t_hr", "VCD"])
      .assign(
          Clone   = lambda d: d["Clone"].astype("category"),
          Rep     = lambda d: pd.to_numeric(d["Rep"], errors="coerce").astype("Int64"),
          t_hr    = lambda d: pd.to_numeric(d["t_hr"], errors="coerce"),
          Vol_mL  = lambda d: pd.to_numeric(d["Vol_mL"], errors="coerce"),
          Glc_g_L = lambda d: pd.to_numeric(d["Glc_g_L"], errors="coerce"),
          Lac_g_L = lambda d: pd.to_numeric(d["Lac_g_L"], errors="coerce"),
      )
      .query(f"{EXP_START_HR} <= t_hr <= {EXP_END_HR}")
      .sort_values(["Clone", "Rep", "t_hr"], ignore_index=True)
)

# ───── Unit conversion (g/L → mol/mL) ───────────────────────────────────── #
df["Glc_mmol_L"] = df["Glc_g_L"] / MM_GLC * 1e3
df["Lac_mmol_L"] = df["Lac_g_L"] / MM_LAC * 1e3
df["Glc_mol_mL"] = df["Glc_mmol_L"] * 1e-6
df["Lac_mol_mL"] = df["Lac_mmol_L"] * 1e-6

# ───── Compute kinetics per Clone × Rep ─────────────────────────────────── #
def compute_kinetics(group):
    g = group.sort_values("t_hr")
    t = g["t_hr"].values
    x = g["VCD"].values
    v = g["Vol_mL"].values
    g_mol = g["Glc_mol_mL"].values
    l_mol = g["Lac_mol_mL"].values

    if len(t) < 2:
        return pd.Series(dtype="float64")

    mu   = (np.log(x[-1]) - np.log(x[0])) / (t[-1] - t[0])
    ivcd = np.trapz(x, t)

    dX = x[-1] * v[-1] - x[0] * v[0]
    dG = g_mol[0] * v[0] - g_mol[-1] * v[-1]
    dL = l_mol[-1] * v[-1] - l_mol[0] * v[0]

    Y_XG = dX / dG if dG else np.nan
    Y_XL = dX / dL if dL else np.nan

    q_G = (dG * 1e12) / ivcd if ivcd else np.nan
    q_L = (dL * 1e12) / ivcd if ivcd else np.nan

    return pd.Series({
        "mu": mu,
        "IVCD": ivcd,
        "dX": dX,
        "dG": dG,
        "dL": dL,
        "Y_XG": Y_XG,
        "Y_XL": Y_XL,
        "q_Glc": q_G,
        "q_Lac": q_L,
    })

kin_df = (
    df.groupby(["Clone", "Rep"], observed=True)
      .apply(compute_kinetics)
      .reset_index()
)

# ───── Save Clone × Rep output ──────────────────────────────────────────── #
OUTFILE_REP.parent.mkdir(parents=True, exist_ok=True)
kin_df.to_csv(OUTFILE_REP, index=False)
print(f"\n✓ Saved kinetics by Clone × Rep to:\n  {OUTFILE_REP}")

# ───── Aggregate (Clone-level) summary ──────────────────────────────────── #
agg_df = (
    kin_df.groupby("Clone", observed=True)
          .agg(["mean", "std"])
          .reset_index()
)

agg_df.columns = ["Clone"] + [f"{col}_{stat}" for col, stat in agg_df.columns[1:]]
agg_df.to_csv(OUTFILE_AGG, index=False)
print(f"✓ Saved kinetics summary by Clone to:\n  {OUTFILE_AGG}")

# ───── Console summary ──────────────────────────────────────────────────── #
if __name__ == "__main__":
    print("\n=== Exponential-phase kinetics complete ===")
    print(f"Phase range: {EXP_START_HR}–{EXP_END_HR} h")
    print(f"Clones processed      : {kin_df['Clone'].nunique()}")
    print(f"Clone × Rep entries   : {kin_df.shape[0]}")
