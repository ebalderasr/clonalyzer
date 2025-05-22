---

# CHO Cell Culture Kinetic Analysis

This repository contains a Python script designed to analyze fed-batch CHO (Chinese Hamster Ovary) cell culture kinetic data. It automates the process of data cleaning, visualization, and the calculation of key bioprocess parameters, providing insights into clone performance.

## 🚀 Getting Started

To run this script, you'll need **Python 3.11.11** installed along with the specific versions of libraries listed in the `requirements.txt` file.

---

### Prerequisites: Setting Up Your Python Environment

It's highly recommended to use a virtual environment (like `conda` or `venv`) to manage your project's dependencies. This ensures that you have the exact Python version and library versions used during development, preventing potential conflicts with other projects.

1.  **Create a New Environment:**
    * **Using `conda` (Recommended if you have Anaconda/Miniconda):**
        ```bash
        conda create -n cho_kinetics_env python=3.11.11
        ```
    * **Using `venv` (Standard Python virtual environment):**
        ```bash
        python3.11 -m venv cho_kinetics_env
        ```
        (Ensure `python3.11` points to your Python 3.11 installation if you have multiple versions).

2.  **Activate Your Environment:**
    * **Using `conda`:**
        ```bash
        conda activate cho_kinetics_env
        ```
    * **Using `venv`:**
        * **Windows:**
            ```bash
            .\cho_kinetics_env\Scripts\activate
            ```
        * **macOS/Linux:**
            ```bash
            source cho_kinetics_env/bin/activate
            ```
    You'll see `(cho_kinetics_env)` preceding your terminal prompt when the environment is active.

3.  **Install Required Packages:**
    With your environment active, navigate to the root directory of this repository (where `requirements.txt` is located) and install all dependencies:
    ```bash
    pip install -r requirements.txt
    ```

---

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

**Example:** Your CSV might look something like this (the `rep` column is crucial for distinguishing replicates):

| Clone     | T | G   | Gln | Xv      | Xd | L   | Glu | V  | MAb | rP  | rep |
| :-------- | :- | :-- | :-- | :------ | :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| Clone A   | 0 | 5.0 | 4.0 | 0.5e6   | 0  | 0.1 | 0.1 | 99 | 0   | 0   | 1   |
| Clone A   | 1 | 4.5 | 3.8 | 1.0e6   | 0  | 0.2 | 0.1 | 98 | 0.1 | 0.01| 1   |
| Clone A   | 0 | 4.9 | 3.9 | 0.5e6   | 0  | 0.1 | 0.1 | 99 | 0   | 0   | 2   |
| ...       |    |     |     |         |    |     |     |    |     |     |     |

---

### Running the Script

1.  **Save your data:** Ensure your kinetic data is saved as a `.csv` file (e.g., `2024-05-18_Clones_B_C_Kinetics.csv`) inside a `data/` folder in the same directory as the script.
    * **Note:** The script currently expects the data file path to be hardcoded as `DATASET_PATH = 'data/2024-05-18_Clones_B_C_Kinetics.csv'` at the top of the script. Future updates will introduce a GUI for file selection.
2.  **Define Exponential Phase:** Open the Python script and set `TIME_START` and `TIME_END` variables (in Section 5) to define the time range for your exponential growth phase. This is critical for accurate kinetic calculations.
3.  **Run the Python script:** Execute the main Python script from your terminal (with your environment active):
    ```bash
    python your_script_name.py
    ```
    (Replace `your_script_name.py` with the actual name of your Python file).

---

## 📊 How the Script Works

The script follows a clear, step-by-step process to analyze your cell culture data:

---

### 1. Data Loading and Cleaning

**What happens here?** This initial phase reads your raw `.csv` file and performs essential cleaning and preparation steps to ensure data quality and consistency for subsequent analysis.

* **File Loading:** The script loads the `.csv` data into a pandas DataFrame, including robust error handling for file not found scenarios.
* **Column Validation:** It rigorously checks for the presence of all expected raw columns (`T`, `G`, `Xv`, `rep`, etc.), raising an error if any critical column is missing.
* **Column Renaming:** Raw, often abbreviated, column names (e.g., `T`, `G`, `Xv`, `rep`) are systematically renamed to more descriptive and user-friendly labels (e.g., `Time (days)`, `Glucose (g/L)`, `Viable Cells (cells/mL)`, `Replicate`).
* **Data Type Conversion:** All relevant columns (excluding `Clone` and `Replicate` which are handled separately) are converted to appropriate numerical data types. A robust method is employed to handle potential non-numeric entries (e.g., typos, characters), replacing them with `NaN` (Not a Number) to prevent script crashes and allow for missing data.
* **Categorical Conversion:** The `Clone` and `Replicate` columns are explicitly converted to a categorical data type. This is more memory-efficient and optimizes grouping and plotting operations in pandas and seaborn.

---

### 2. Analysis of Raw Data (Mean ± Standard Deviation)

**This section provides a crucial first look at the raw experimental variability.** Your experiments typically include multiple replicates for each clone. To understand general trends and variability, the script visualizes the raw data with statistical summaries.

* **Replicate Averaging:** For each measured parameter (e.g., `Viable Cells (cells/mL)`, `Glucose (g/L)`), the script groups the data by **`Time (days)`** and **`Clone`**.
* **Mean and Standard Deviation Calculation:** Within each group (i.e., for a specific clone at a specific time point across all its replicates), the script calculates the **mean** value and the **standard deviation** of the parameter. The standard deviation quantifies the variability or spread of your replicate data around the mean at each time point.
* **Time-Series Plots:** For each major kinetic parameter, a separate line plot is generated. These plots display the **mean** value over time, with **error bars** (or shaded regions) representing the **standard deviation** of the replicates at each time point. This gives a clear initial picture of clone performance and experimental variability.
* **Output:** All generated plots are saved as `.png` images in the `output_kinetics_analysis/` directory.

---

### 3. Normalization and Visualization of Cell Growth

**This step focuses on comparing growth profiles relative to initial conditions.**

* **Normalization:** Viable cell density (VCD) for each individual replicate is normalized by its VCD at time 0. This allows for a direct comparison of relative growth trends, even if initial cell densities varied slightly between experiments.
* **Statistical Analysis:** Similar to raw data, the mean and standard deviation of these normalized VCDs are calculated per clone per time point.
* **Normalized Growth Plot:** A time-series plot displays the mean normalized viable cell growth, with standard deviation error bars, providing a clear visual of relative growth dynamics across clones.
* **Output:** The normalized growth plot is saved as a `.png` image in the `output_kinetics_analysis/` directory.

---

### 4. Combined Kinetic Plots (Dual Y-axis)

**This section helps in identifying interrelationships between different kinetic parameters over time.**

* **Dual-Axis Visualization:** The script generates plots that display two different kinetic variables against time on a single graph, each utilizing its own Y-axis for appropriate scaling. This is particularly useful for observing dependencies, such as substrate consumption coupled with product formation.
* **Mean and Standard Deviation:** Both primary and secondary Y-axis variables are plotted with their mean values and standard deviation error bars (calculated from the replicate data), offering a comprehensive view of trends and variability.
* **Plot Configurations:** The script is set up to generate specific combinations like Glucose vs. Lactate, Glutamine vs. Glutamate, and Glucose vs. Glutamine, which are common relationships of interest in cell culture.
* **Output:** All generated combined plots are saved as `.png` images in the `output_kinetics_analysis/` directory.

---

### 5. Calculation of Kinetic and Stoichiometric Parameters

**This is the core of the quantitative analysis, deriving key performance indicators for each clone from replicate data.**

This section calculates crucial bioprocess parameters, focusing on the **exponential growth phase** (defined by `TIME_START` and `TIME_END` variables in the script). Critically, these calculations are performed **for each individual replicate first**, and then aggregated to provide a mean and standard deviation for each clone.

* **Replicate-Level Calculation:**
    * For each clone, the script iterates through every individual replicate.
    * For each replicate, data within the user-defined `TIME_START` and `TIME_END` is isolated. This range is assumed to represent the true exponential growth phase where rates are relatively constant.
    * **Unit Conversions:** Glucose and Lactate concentrations are converted from `g/L` to `mmol/L`, and `cells/mL` to `cells/L` to ensure consistent units across all calculations.
    * **Specific Growth Rate ($\mu$, d$^{-1}$):**
        * The **natural logarithm of Viable Cell Density (`ln(VCD)`)** is calculated for the replicate.
        * A **linear regression** is performed on `ln(VCD)` vs. `Time (days)` within the exponential phase for that specific replicate.
        * The **slope** of this linear regression is the **specific growth rate ($\mu$)** for that replicate, indicating how fast cells are dividing.
    * **Total Deltas ($\Delta$)**: The total change in concentration for each metabolite (e.g., Glucose, Lactate) and viable cells ($\Delta X$) is calculated over the exponential phase for that replicate by subtracting the initial value from the final value within that phase.
    * **Biomass Yields ($Y_{x/s}$, cells/L/mmol):**
        * These parameters quantify the efficiency of converting a substrate into viable cells.
        * For each replicate, calculated as: $\Delta X / |\Delta \text{Substrate}|$ (e.g., $Y_{x/G} = \Delta X / |\Delta \text{Glucose}|$).
    * **Average Volumetric Rates ($\Delta / \Delta t$, mmol/L/day):**
        * These represent the overall rate of consumption or production of a metabolite over the time interval for that replicate.
        * Calculated as: $\Delta \text{Metabolite} / \Delta \text{Time}$.
    * **Specific Consumption/Production Rates (q-rates, mmol/cell·day):**
        * These indicate the rate at which a *single cell* consumes a substrate or produces a product/byproduct, normalized by cell density.
        * For each replicate, calculated as: $|\text{Average Rate of Change}| / \text{Average Viable Cell Density}$ (e.g., $q_G = |\Delta \text{Glucose} / \Delta t| / \text{Average X}$).
* **Aggregation for Clones:**
    * After calculating parameters for every individual replicate, all these replicate-level values are collected into a DataFrame (`df_replicate_params`). This DataFrame is displayed in the console to allow inspection of individual replicate results.
    * Finally, this `df_replicate_params` is grouped by `Clone`, and the **mean** and **standard deviation** are calculated for each kinetic and stoichiometric parameter across its replicates.
* **Output:** The script prints two DataFrames to the console: one showing the calculated parameters for each individual replicate, and another summarizing these parameters per clone as `Mean ± Standard Deviation`.

---

### 6. Parameter Comparison Plots

**This final section generates comparative visualizations to help you quickly identify trends, performance differences, and relationships between calculated parameters across different clones.**

* **Consistent Coloring:** Each unique clone is assigned a specific color, which is used consistently across all comparison plots for easy identification and comparison.
* **Bar Plots:** Used for single key metrics (e.g., Specific Growth Rate) to show direct, side-by-side comparisons between clones. **Error bars representing the standard deviation** are included to indicate the variability observed across replicates for each clone.
* **Scatter Plots:** Used to visualize the relationship between two different calculated parameters (e.g., Biomass Yield on Glucose vs. Biomass Yield on Glutamine, or Specific Glucose Consumption vs. Specific Lactate Production). These plots also include **X and Y error bars** based on the standard deviation of each parameter across replicates, helping to understand the spread of the data points.
* **Professional Labels:** Plot titles and axis labels utilize LaTeX formatting for standard scientific symbols (e.g., $\mu$, $Y_{x/G}$, $q_G$, $\cdot$), enhancing the professional and scientific appearance of the figures.
* **Output:** All comparison plots are saved as high-resolution `.png` images in the `output_kinetics_analysis/` directory.

---

## 📈 Analysis & Interpretation

By examining the generated plots and the `df_results` table, you can:

* **Identify Fast Growers:** Quickly see which clones exhibit the highest specific growth rate ($\mu$) and how consistent this rate is across replicates.
* **Assess Metabolic Efficiency:** Determine which clones have high biomass yields ($Y_{x/s}$) on key substrates and potentially low specific byproduct production ($q_L$, $q_{Glu}$), indicating more efficient metabolism for biomass production.
* **Evaluate Productivity Potential:** Correlate these kinetic parameters with recombinant protein ($rP$) or antibody ($MAb$) production data to select optimal clones based on desired bioprocess characteristics.
* **Understand Variability:** The inclusion of standard deviations on all plots and tables provides crucial insights into the reproducibility and robustness of each clone's performance. High standard deviations might indicate a need for further investigation into experimental consistency or inherent biological heterogeneity.

This comprehensive analysis supports informed decision-making in clone selection for bioprocess development.

---
