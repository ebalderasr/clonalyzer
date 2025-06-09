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

| Raw Column Name | Description                       | Example Units        |
| :-------------- | :-------------------------------- | :------------------- |
| `Clone`         | Identifier for cell clone         | `Clone A`, `Clone B` |
| `T`             | Time point                        | `hours`              |
| `G`             | Glucose concentration             | `g/L`                |
| `Gln`           | Glutamine concentration           | `mmol/L`             |
| `Xv`            | Viable Cell Density (VCD)         | `cells/mL`           |
| `Xm`            | Dead Cell Density                 | `cells/mL`           |
| `L`             | Lactate concentration             | `g/L`                |
| `Glu`           | Glutamate concentration           | `mmol/L`             |
| `V`             | Viability                         | `%`                  |
| `Mab`           | Antibody Concentration            | `mg/mL`              |
| `rP`            | Recombinant Protein Concentration | `mg/mL`              |
| `rep`           | Replicate number                  | `1`, `2`, `3`        |

**Note on other columns in `Example.csv` (e.g., `vivas`, `muertas`, `C`, `dil`):**
The script is configured to either ignore or remove these columns from the processed DataFrame if they are not explicitly listed in the expected input structure and are not used for analysis. This keeps the data clean and focused on relevant parameters.

**Example:** Your CSV might look something like this (the `rep` column is crucial for distinguishing replicates):

| Clone   | T   | G   | Gln | Xv      | Xm   | L   | Glu | V  | Mab | rP  | rep |
| :------ | :-- | :-- | :-- | :------ | :--- | :-- | :-- | :-- | :-- | :-- | :-- |
| Clone A | 0   | 5.0 | 4.0 | 0.5e6   | 0    | 0.1 | 0.1 | 99 | 0   | 0   | 1   |
| Clone A | 1   | 4.5 | 3.8 | 1.0e6   | 0    | 0.2 | 0.1 | 98 | 0.1 | 0.01| 1   |
| Clone A | 0   | 4.9 | 3.9 | 0.5e6   | 0    | 0.1 | 0.1 | 99 | 0   | 0   | 2   |
| ...     |     |     |     |         |      |     |     |    |     |     |     |

---

### Running the Script

1.  **Save your data:** Ensure your kinetic data is saved as a `.csv` file (e.g., `Example.csv`) inside a `data/` folder in the same directory as the script.
    * **Note:** The script currently expects the data file path to be hardcoded as `DATASET_PATH = 'data/Example.csv'` in the "Global Constants and User Configuration" section (0.1).
2.  **Define Exponential Phase:** Open the Python script and set `TIME_START` and `TIME_END` variables (in Section 0.2 of "Global Constants and User Configuration") to define the time range (in hours) for your exponential growth phase. This is critical for accurate kinetic calculations.
3.  **Run the Python script:** Execute the main Python script from your terminal (with your environment active):
    ```bash
    python your_script_name.py
    ```
    (Replace `your_script_name.py` with the actual name of your Python file).

---

## 📊 How the Script Works

The script follows a clear, step-by-step process to analyze your cell culture data:

---

### 0. Global Constants and User Configuration

This section centralizes all user-configurable variables (file paths, time ranges, output directories, etc.) and global constants (like molecular weights of metabolites) in one place for easy modification. It also handles initial setup such as creating the output directory and configuring the plotting aesthetic using Seaborn.

---

### 1. Helper Functions

This section defines a set of reusable utility functions crucial for data handling, statistical calculations, and file operations. These include `clean_filename` (for creating safe file names), `confirm_columns` (for validating the presence of expected data columns), `calculate_kinetics_stats` (for computing means and standard deviations for time-series data), and `normalize_column` (for scaling data to a 0-1 range).

---

### 2. Data Loading and Initial Cleaning

This initial phase is responsible for reading your raw `.csv` data, performing essential cleaning, and preparing the DataFrame for subsequent analysis.

* **File Loading:** The script loads the `.csv` data into a pandas DataFrame, including robust error handling for `FileNotFoundError` and other loading issues.
* **Column Validation & Renaming:** It rigorously checks for the presence of all expected raw columns. Raw column names (e.g., `T`, `Xv`, `Xm`, `Mab`, `rP`, `rep`) are systematically renamed to more descriptive and user-friendly labels (e.g., `Time (hours)`, `Viable Cells (cells/mL)`, `Dead Cells (cells/mL)`, `Antibody Concentration (mg/mL)`, `Recombinant Protein (mg/mL)`, `Replicate`).
* **Data Type Conversion:** All relevant columns are converted to appropriate numerical data types. A robust method handles potential non-numeric entries (e.g., typos, characters) by replacing them with `NaN` (Not a Number) to prevent script crashes.
* **Categorical Conversion:** `Clone` and `Replicate` columns are explicitly converted to a categorical data type for efficient grouping and plotting.
* **Unused Column Handling:** Columns in the raw data that are not required for analysis (e.g., `vivas`, `muertas`, `C`, `dil` from `Example.csv` if `Xm` is used for dead cells) are explicitly dropped to maintain a cleaner and more focused DataFrame.

---

### 3. Data Normalization for Visualization

This step creates a separate DataFrame with normalized data specifically for plotting purposes. The original `kinetics_data` DataFrame remains untouched to ensure that scientific calculations are performed on the raw, unscaled values.

* **Min-Max Scaling:** Numerical columns (excluding identifiers) are normalized to a 0-1 range using the Min-Max normalization method: `(value - min) / (max - min)`. Columns with constant values are normalized to 0.0.
* **Purpose:** This normalized dataset is primarily used to generate additional plots that compare relative changes between different parameters or clones, regardless of their absolute magnitudes.

---

### 4. Plotting Functions (Definitions)

This section contains the definitions for two primary plotting functions that are used throughout the script to generate various kinetic plots:

* **`save_plot_with_stats`:** Generates and saves a time-series plot for a single kinetic parameter, displaying its mean and standard deviation across replicates for each clone. It includes robust checks for missing or all-NaN data.
* **`save_combined_plot_with_stats`:** Generates and saves a combined plot with two Y-axes, allowing the comparison of two different kinetic variables against a common X-axis (Time). Both variables are plotted with their mean values and standard deviation error bars, providing a comprehensive view of trends and variability. It also includes robust data checks.

---

### 5. Generate Individual Kinetic Plots

This section utilizes the `save_plot_with_stats` function to generate time-series plots for each individual kinetic parameter.

* **Parameter-Specific Plots:** Separate line plots are created for `Viable Cells (cells/mL)`, `Viability (%)`, `Glucose (g/L)`, `Lactate (g/L)`, `Glutamine (mmol/L)`, `Glutamate (mmol/L)`, `Antibody Concentration (mg/mL)`, `Recombinant Protein (mg/mL)`, and `Dead Cells (cells/mL)`.
* **Mean and Standard Deviation:** Each plot displays the mean value over time, with error bars representing the standard deviation of the replicates at each time point, offering a clear initial picture of clone performance and experimental variability.
* **Normalized Plots (Optional):** If `GENERATE_NORMALIZED_PLOTS` is set to `True`, an additional set of plots with normalized (0-1 scaled) data is generated for comparative visualization.
* **Output:** All generated plots are saved as high-resolution `.png` images in the `figures/` directory.

---

### 6. Generate Combined Kinetic Plots (Dual Y-Axis)

This section leverages the `save_combined_plot_with_stats` function to create plots that illustrate the interrelationships between two different kinetic parameters over time.

* **Dual-Axis Visualization:** Plots are generated combining pairs of variables such as "Glucose and Lactate", "Glutamine and Glutamate", "Glucose and Glutamine", "Viable Cell Kinetics and Antibody Concentration", and "Viable Cell Kinetics and Recombinant Protein". Each variable utilizes its own Y-axis for appropriate scaling.
* **Mean and Standard Deviation:** Both primary and secondary Y-axis variables are plotted with their mean values and standard deviation error bars (calculated from the replicate data).
* **Output:** All generated combined plots are saved as high-resolution `.png` images in the `figures/` directory.

---

### 7. Calculation of Kinetic and Stoichiometric Parameters

This is the core of the quantitative analysis, deriving key performance indicators for each clone from replicate data, focusing on the **exponential growth phase** (defined by `TIME_START` and `TIME_END`).

* **Replicate-Level Calculation:**
    * For each clone and individual replicate, data within the user-defined exponential phase is isolated.
    * **Unit Conversions:** Glucose and Lactate concentrations are converted from `g/L` to `mmol/L`, and viable cell density from `cells/mL` to `cells/L` to ensure consistent units.
    * **Specific Growth Rate ($\mu$, d$^{-1}$):** Calculated as the slope of the linear regression of the natural logarithm of Viable Cell Density (`ln(VCD)`) versus `Time (hours)`. The result is then **converted to per day (d$^{-1}$)** by multiplying by 24 (since time is in hours).
    * **Biomass Yields ($Y_{x/s}$, cells/L/mmol):** Quantify the efficiency of converting a substrate into viable cells, calculated as `ΔX / |ΔSubstrate|`.
    * **Average Volumetric Rates ($\Delta / \Delta t$, mmol/L/day or mg/L/day):** Represent the overall rate of consumption or production of a metabolite or product over the time interval. Calculated as `ΔMetabolite / ΔTime`, and then **converted to per day** by multiplying by 24. This applies to Glucose, Glutamine, Lactate, Glutamate, Antibody Concentration, and Recombinant Protein.
    * **Specific Consumption/Production Rates (q-rates, mmol/cell·day or mg/cell·day):** Indicate the rate at which a *single cell* consumes a substrate or produces a product/byproduct, normalized by cell density. Calculated as `|Average Rate of Change| / Average Viable Cell Density`, and then **converted to per day** by multiplying by 24. This applies to Glucose, Glutamine, Lactate, Glutamate, Antibody Concentration (`qMab`), and Recombinant Protein (`qrP`).
* **Aggregation for Clones:** After calculating parameters for every individual replicate, these values are aggregated by `Clone` to compute the **mean** and **standard deviation** for each kinetic and stoichiometric parameter across its replicates.
* **Output:** The script prints two DataFrames to the console: one showing the calculated parameters for each individual replicate, and another summarizing these parameters per clone as `Mean ± Standard Deviation`.

---

### 8. Parameter Comparison Plots

This final section generates comparative visualizations to help you quickly identify trends, performance differences, and relationships between calculated parameters across different clones.

* **Consistent Coloring:** Each unique clone is assigned a specific color, used consistently across all comparison plots for easy identification.
* **Bar Plots:** Used for single key metrics (e.g., Specific Growth Rate) to show direct, side-by-side comparisons between clones, with error bars indicating the standard deviation.
* **Scatter Plots:** Used to visualize the relationship between two different calculated parameters (e.g., Biomass Yields, Specific Consumption/Production Rates). This section now includes plots comparing:
    * Specific Growth Rate vs. Specific Antibody Production ($q_{Mab}$)
    * Specific Growth Rate vs. Specific Recombinant Protein Production ($q_{rP}$)
    These plots also include X and Y error bars based on the standard deviation, helping to understand the spread of the data points.
* **Professional Labels:** Plot titles and axis labels utilize LaTeX formatting for standard scientific symbols (e.g., $\mu$, $Y_{x/G}$, $q_G$, $q_{Mab}$, $q_{rP}$, $\cdot$), enhancing the professional and scientific appearance of the figures.
* **Output:** All comparison plots are saved as high-resolution `.png` images in the `figures/` directory.

---

## 📈 Analysis & Interpretation

By examining the generated plots and the `df_results` table, you can:

* **Identify Fast Growers:** Quickly see which clones exhibit the highest specific growth rate ($\mu$) and how consistent this rate is across replicates.
* **Assess Metabolic Efficiency:** Determine which clones have high biomass yields ($Y_{x/s}$) on key substrates and potentially low specific byproduct production ($q_L$, $q_{Glu}$), indicating more efficient metabolism for biomass production.
* **Evaluate Productivity Potential:** Correlate these kinetic parameters with product (antibody and recombinant protein) production data to select optimal clones based on desired bioprocess characteristics, including specific productivity rates ($q_{Mab}$, $q_{rP}$).
* **Understand Variability:** The inclusion of standard deviations on all plots and tables provides crucial insights into the reproducibility and robustness of each clone's performance. High standard deviations might indicate a need for further investigation into experimental consistency or inherent biological heterogeneity.

This comprehensive analysis supports informed decision-making in clone selection for bioprocess development.

---