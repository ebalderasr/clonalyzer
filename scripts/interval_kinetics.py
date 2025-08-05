#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
interval_kinetics.py
~~~~~~~~~~~~~~~~~~~~
Interval-to-interval kinetic analysis for CHO fed-batch cultures.

Workflow
--------
1. Load cleaned CHO fed-batch data from `data/data.csv` (skips metadata row).
2. Parse `is_post_feed` to identify pre- vs post-feed sampling points.
3. For each Clone × Rep:
   • Compute growth rate (μ, h⁻¹)
   • Estimate integrated viable cell density (IVCD, cell·h)
   • Calculate dX, dGlc, dLac, yields, and specific rates (qS)
4. Save enriched DataFrame to `outputs/interval_kinetics.csv`.

Outputs
-------
CSV with new kinetic columns in `./outputs/`.

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
OUTFILE   = Path("outputs/interval_kinetics.csv")

MM_GLUCOSE = 180.156  # g/mol
MM_LACTATE = 90.080   # g/mol

KIN_COLS = [
    "mu", "IVCD_tot", "dX", "dG", "dL",
    "Y_XG", "Y_XL", "q_G", "q_L"
]

# ───── Load data ───────────────────────────────────────────────────────── #
if not DATA_FILE.exists():
    raise FileNotFoundError(f"❌ Input file not found:\n  {DATA_FILE}")

df = (
    pd.read_csv(DATA_FILE, skiprows=1)
      .assign(
          t_hr  = lambda d: pd.to_numeric(d["t_hr"], errors="coerce"),
          Rep   = lambda d: pd.Categorical(
                     pd.to_numeric(d["Rep"], errors="coerce"),
                     categories=[1, 2, 3], ordered=True),
          Clone = lambda d: d["Clone"].astype("category"),
          Notes = lambda d: d["Notes"].astype(str).str.strip(),
          Date  = lambda d: pd.to_datetime(d["Date"], format="%d/%m/%Y", errors="coerce"),
          Timestamp = lambda d: d["Timestamp"].astype(str).str.strip(),
          is_post_feed = lambda d: (
              d["is_post_feed"]
                .fillna(False)
                .apply(lambda x: str(x).strip().lower() in {"true", "t", "1"})
          )
      )
      .sort_values(["Clone", "Rep", "t_hr"], ignore_index=True)
)

# ───── Unit conversions ─────────────────────────────────────────────────── #
df["Glc_mM"]          = df["Glc_g_L"] / MM_GLUCOSE * 1e3
df["Lac_mM"]          = df["Lac_g_L"] / MM_LACTATE * 1e3
df["Glucose_mol_mL"]  = df["Glc_mM"] * 1e-6
df["Lactate_mol_mL"]  = df["Lac_mM"] * 1e-6
df[KIN_COLS]          = np.nan

# ───── Kinetic calculations ─────────────────────────────────────────────── #
for (clone, rep), group in df.groupby(["Clone", "Rep"], observed=True, sort=False):
    g = group.sort_values("t_hr").reset_index()
    idx_df = g["index"]

    for i in range(1, len(g)):
        t1 = g.loc[i]

        if t1["t_hr"] <= 72:  # batch phase
            t0 = g.loc[i - 1]

        elif not t1["is_post_feed"]:  # pre-feed
            pre_feed = g[(g["t_hr"] < t1["t_hr"]) & g["is_post_feed"]]
            if pre_feed.empty:
                continue
            t0 = pre_feed.iloc[-1]

        else:  # post-feed → skip
            continue

        Δt = t1["t_hr"] - t0["t_hr"]
        if Δt <= 0:
            continue

        # Growth rate
        mu = (np.log(t1["VCD"]) - np.log(t0["VCD"])) / Δt

        # Total balances
        dX = t1["VCD"] * t1["Vol_mL"] - t0["VCD"] * t0["Vol_mL"]
        dG = t0["Glucose_mol_mL"] * t0["Vol_mL"] - t1["Glucose_mol_mL"] * t1["Vol_mL"]
        dL = t1["Lactate_mol_mL"] * t1["Vol_mL"] - t0["Lactate_mol_mL"] * t0["Vol_mL"]

        # Yields
        Y_XG = dX / dG if dG else np.nan
        Y_XL = dX / dL if dL else np.nan

        # Integrated viable cell density
        ivc_mL   = ((t0["VCD"] + t1["VCD"]) / 2) * Δt
        IVCD_tot = ivc_mL * ((t0["Vol_mL"] + t1["Vol_mL"]) / 2)

        # Specific rates
        q_G = (dG * 1e12) / IVCD_tot if IVCD_tot else np.nan
        q_L = (dL * 1e12) / IVCD_tot if IVCD_tot else np.nan

        df.loc[idx_df[i], KIN_COLS] = [
            mu, IVCD_tot, dX, dG, dL, Y_XG, Y_XL, q_G, q_L
        ]

# ───── Save and summary ─────────────────────────────────────────────────── #
OUTFILE.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(OUTFILE, index=False)

if __name__ == "__main__":
    n_valid = df["mu"].notna().sum()
    print(f"\n✓ Intervals analyzed: {n_valid}")
    print(f"✓ Kinetic file saved to:\n  {OUTFILE}")
