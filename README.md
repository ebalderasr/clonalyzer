---

# CHO Cell Culture Kinetic Analysis

This repository contains a Python script designed to analyze fed-batch CHO (Chinese Hamster Ovary) cell culture kinetic data. It automates the process of data cleaning, visualization, and the calculation of key bioprocess parameters, providing insights into clone performance.

## 🚀 Getting Started

To run this script, you'll need Python installed along with the libraries listed in the `requirements.txt` (or shown below).

### Prerequisites

Make sure you have these Python libraries installed:

* `pandas`
* `numpy`
* `matplotlib`
* `seaborn`
* `scipy`

You can install them via pip:
```bash
pip install pandas numpy matplotlib seaborn scipy
```

### Data Structure

Place your raw kinetic data in a `.csv` file. The script expects the following columns (case and exact naming as shown are important in the raw file, though the script renames them for internal use):

| Raw Column Name | Description               | Example Units        |
| :-------------- | :------------------------ | :------------------- |
| `Clone`         | Identifier for cell clone | `Clone A`, `Clone B` |
| `T`             | Time point                | `days`               |
| `G`             | Glucose concentration     | `g/L`                |
| `Gln`           | Glutamine concentration   | `mmol/L`             |
| `Xv`            | Viable Cell Density (VCD) | `cells/mL`           |
| `Xd`            | Dead Cell Density         | `cells/mL`           |
| `L`             | Lactate concentration     | `g/L`                |
| `Glu`           | Glutamate concentration   | `mmol/L`             |
| `V`             | Viability                 | `%`                  |
| `MAb`           | Antibody Concentration    | `mg/mL`              |
| `rP`            | Recombinant Protein       | `mg/mL`              |
| `rep`           | Replicate number          | `1`, `2`, `3`        |

**Example:** Your CSV might look something like this (excluding the `rep` column for brevity, but it's crucial for replicates):

| Clone    | T | G   | Gln | Xv    | Xd | L   | Glu | V  | MAb | rP  |
| :------- | :- | :-- | :-- | :---- | :-- | :-- | :-- | :-- | :-- | :-- |
| Clone A | 0 | 5.0 | 4.0 | 0.5e6 | 0  | 0.1 | 0.1 | 99 | 0   | 0   |
| Clone A | 1 | 4.5 | 3.8 | 1.0e6 | 0  | 0.2 | 0.1 | 98 | 0.1 | 0.01|
| Clone A | 0 | 4.9 | 3.9 | 0.5e6 | 0  | 0.1 | 0.1 | 99 | 0   | 0   |
| ...      |   |     |     |       |    |     |     |    |     |     |

### Running the Script

1.  **Save your data:** Ensure your kinetic data is saved as a `.csv` file (e.g., `2024-05-18_Clones_B_C_Kinetics.csv`) inside a `data/` folder in the same directory as the script.
2.  **Run the Python script:** Execute the main Python script from your terminal:
    ```bash
    python your_script_name.py
    ```
    (Replace `your_script_name.py` with the actual name of your Python file).

## 📊 How the Script Works

The script follows a clear, step-by-step process to analyze your cell culture data:

---

### 1. Data Loading and Cleaning

**What happens here?** The script reads your raw `.csv` file and prepares it for analysis. This is crucial for ensuring data quality and consistency.

* **File Loading:** The `.csv` data is loaded into a pandas DataFrame. The script includes error handling to notify you if the file is not found.
* **Column Validation:** It first checks if all expected columns (`T`, `G`, `Xv`, etc.) are present in your raw data.
* **Column Renaming:** Raw column names (like `T`, `G`) are renamed to more descriptive and user-friendly names (e.g., `Time (days)`, `Glucose (g/L)`).
* **Data Type Conversion:** All relevant columns (except `Clone` and `Replicate`) are converted to numerical types. A robust method is used to handle potential non-numeric entries (e.g., typos, characters) by replacing them with `NaN` (Not a Number) to prevent crashes.
* **Categorical Conversion:** The `Clone` column is converted to a categorical data type, which is more efficient for grouping and plotting operations.

---

### 2. Data Averaging and Standard Deviation Calculation

**This is a critical step for robust analysis!** Your experiments typically include multiple replicates for each clone. To get reliable trends and reduce noise, the script averages the data for each clone at every time point.

* **Grouping by Time and Clone:** For each measured parameter (e.g., `Viable Cells (cells/mL)`, `Glucose (g/L)`), the script groups the data by **`Time (days)`** and **`Clone`**.
* **Calculating Mean and Standard Deviation:** Within each group (i.e., for a specific clone at a specific time point across all its replicates), the script calculates:
    * **`mean`**: The average value of the parameter.
    * **`std`**: The standard deviation of the parameter, which quantifies the variability or spread of your replicate data around the mean.
* **Output DataFrames:** These calculations generate intermediate DataFrames (e.g., `kinetics_stats`) which have columns like `Time (days)`, `Clone`, `mean`, and `std` for each parameter. These averaged values are then used for plotting and further calculations.

---

### 3. Kinetic Plots (Time-Series Visualizations)

**What happens here?** The script generates plots showing how different parameters change over time for each clone, visually representing the mean and variability.

* **Individual Plots:** For each major kinetic parameter (e.g., Viable Cell Density, Glucose, Lactate, Antibody Concentration), a separate line plot is generated. These plots display the **mean** value over time, with **error bars** representing the **standard deviation** of the replicates at each time point. This gives a clear picture of clone performance and experimental variability.
* **Combined Plots (Dual Y-axis):** To observe relationships between parameters (e.g., glucose consumption vs. lactate production), some plots combine two different metrics on a single graph, each with its own Y-axis for appropriate scaling. These also show means and standard deviations.
* **Output:** All generated plots are saved as `.png` images in the `figures/` directory.

---

### 4. Calculation of Kinetic and Stoichiometric Parameters

**This is where the key performance indicators are quantified!** The script calculates important bioprocess parameters, focusing on the **exponential growth phase** (defined by `TIME_START_EXP_PHASE` and `TIME_END_EXP_PHASE` at the beginning of the script).

* **Exponential Phase Selection:** For each clone, data within the user-defined `TIME_START_EXP_PHASE` and `TIME_END_EXP_PHASE` is isolated. This is crucial as most kinetic parameters are constant during this phase.
* **Unit Conversions:** Glucose and Lactate concentrations are converted from `g/L` to `mmol/L`, and `cells/mL` to `cells/L` for consistency in calculations.
* **Specific Growth Rate ($\mu$, d$^{-1}$):**
    * The **natural logarithm of Viable Cell Density (`ln(VCD)`)** is calculated.
    * A **linear regression** is performed on `ln(VCD)` vs. `Time (days)` within the exponential phase.
    * The **slope** of this linear regression is the **specific growth rate ($\mu$)**, which indicates how fast cells are dividing in a given time unit (d$^{-1}$).
* **Total Deltas ($\Delta$)**: The script calculates the total change in concentration for each metabolite and viable cells ($\Delta X$) over the exponential phase by subtracting the initial value from the final value within that phase.
* **Biomass Yields ($Y_{x/s}$, cells/L/mmol):**
    * These parameters quantify the efficiency of converting a substrate into viable cells.
    * Calculated as: $\Delta X / |\Delta \text{Substrate}|$ (e.g., $Y_{x/G} = \Delta X / |\Delta \text{Glucose}|$).
* **Average Rates of Change ($\Delta / \Delta t$, mmol/L/day):**
    * These represent the overall rate of consumption or production of a metabolite over the time interval.
    * Calculated as: $\Delta \text{Metabolite} / \Delta \text{Time}$.
* **Specific Consumption/Production Rates (q-rates, mmol/cell·day):**
    * These indicate the rate at which a *single cell* consumes a substrate or produces a product/byproduct. They are normalized by cell density.
    * Calculated as: $|\text{Average Rate of Change}| / \text{Average Viable Cell Density}$ (e.g., $q_G = |\Delta \text{Glucose} / \Delta t| / \text{Average X}$).
* **Output:** All calculated parameters for each clone are summarized in a final DataFrame, which is printed to the console.

---

### 5. Parameter Comparison Plots

**What happens here?** The script generates comparative visualizations to help you quickly identify the "best" clones based on your performance criteria.

* **Consistent Coloring:** Each clone is assigned a unique color, and this color is used consistently across all comparison plots for easy identification.
* **Bar Plots:** Used for single metrics (e.g., Specific Growth Rate) to show direct, side-by-side comparisons between clones.
* **Scatter Plots:** Used to visualize the relationship between two different calculated parameters (e.g., Biomass Yield on Glucose vs. Biomass Yield on Glutamine, or Specific Glucose Consumption vs. Specific Lactate Production). This helps in identifying trade-offs or synergistic effects.
* **Professional Labels:** Plot titles and axis labels use LaTeX formatting for scientific symbols ($\mu$, $Y_{x/G}$, $q_G$, etc.), enhancing the professional appearance of the figures.
* **Output:** All comparison plots are saved as `.png` images in the `figures/` directory.

---

## 📈 Analysis & Interpretation

By examining the generated plots and the `df_results` table, you can:

* **Identify Fast Growers:** See which clones have the highest specific growth rate ($\mu$).
* **Assess Metabolic Efficiency:** Determine which clones have high biomass yields ($Y_{x/s}$) and low specific byproduct production ($q_L$, $q_{Glu}$), indicating efficient metabolism.
* **Evaluate Productivity:** For antibody or recombinant protein, you'd correlate these kinetic parameters with the final product titer.

This analysis helps in selecting optimal clones for further development based on desired bioprocess characteristics.

---
