# Clonalyzer

**Clonalyzer** is a modular toolkit for kinetic and stoichiometric analysis of CHO fed-batch cultures. It supports per-interval, grouped, and exponential-phase analyses with high-quality visualizations.

Designed for bioprocess engineers and data scientists working with clonal cell line characterization.

## 🧬 What is Clonalyzer?

Clonalyzer is a modular Python toolkit for the kinetic and stoichiometric analysis of mammalian cell cultures, particularly designed for fed-batch bioprocesses using CHO cells. It helps quantify growth rates, nutrient consumption, metabolite production, yields, and specific rates—per replicate or per clone.

🔎 **Use cases include**:

* Comparing clone performance in early-stage screening
* Monitoring nutrient and metabolite profiles over time
* Estimating growth and productivity during the exponential phase
* Generating clean, publication-ready plots

Although Clonalyzer was designed with **fed-batch CHO processes** in mind, it is **not limited** to them. For instance:

* Block 3 (exponential-phase analysis) can be used for any batch process.
* Block 1 and 2 support general interval or time-based profiling, including perfusion or hybrid strategies.

## 🖐️ Kinetic and Stoichiometric Calculations

Clonalyzer computes the following parameters for each Clone × Replicate:

| Parameter                      | Symbol        | Units                   | Description                                           |
| ------------------------------ | ------------- | ----------------------- | ----------------------------------------------------- |
| Growth rate                    | μ             | h⁻¹                     | Calculated as slope of ln(VCD) over time              |
| Integrated viable cell density | IVCD          | cells·h·mL⁻¹ or cells·h | Area under the VCD curve over time (trapezoidal rule) |
| Cell balance                   | ∆X            | cells                   | Difference in viable cells in total volume            |
| Substrate balance              | ∆S (Glc, Lac) | mol                     | Difference in total moles in volume                   |
| Yield on substrate             | Yₓ/ₛ          | cells·mol⁻¹             | ∆X / ∆S                                               |
| Specific rate                  | qₛ            | pmol·cell⁻¹·h⁻¹         | ∆S normalized to IVCD and converted to pmol           |

For example, specific consumption of glucose (q\_Glc):

```
q_Glc = (∆Glucose in mol × 1e12) / IVCD  →  pmol/(cell·h)
```

All rates are computed using volume-normalized quantities for full mass balance integrity.

---

## 📃 Full Calculation Details

All calculations are performed per biological replicate (Clone × Rep), using volume-normalized data to maintain mass balance integrity.

### Specific Growth Rate (μ)

$$\mu = \frac{\ln X_2 - \ln X_1}{t_2 - t_1}$$

Where:

* $$X_1$$, $$X_2$$ are viable cell densities at times $$t_1$$ and $$t_2$$
* Units: cells/mL and hours
* Result: $$\mu$$ in  $$h^{-1}$$

### Integral of Viable Cell Density (IVCD)

$$\text{IVCD}_{\text{mL}} = \int_{t_1}^{t_2} X(t) dt \approx \frac{X_1 + X_2}{2} \cdot \Delta t$$

$$\text{IVCD}_{\text{tot}} = \text{IVCD}_{\text{mL}} \cdot \frac{V_1 + V_2}{2}$$

* Units: cells·h or cells·h·mL⁻¹

### Metabolite or Biomass Balance (∆S, ∆X)

$$\Delta X = X_2 V_2 - X_1 V_1
\quad\text{and}\quad
\Delta S = S_1 V_1 - S_2 V_2$$


* $$X$$: cells/mL
* $$S$$: mol/mL
* $$V$$: mL

$$\Delta S$$ is positive if the substrate was consumed, and negative if it was produced.

### Yield on Substrate ($$Y_{X/S}$$)

$$Y_{X/S} = \frac{\Delta X}{\Delta S}$$

* Units: cells/mol

### Specific Rate ($q_S$)

$$q_S = \frac{\Delta S \cdot 10^{12}}{\text{IVCD}_{\text{tot}}}$$


* $$\Delta S$$: mol
* $$IVCD_{tot}$$: cell·h
* $$q_S$$: pmol/(cell·h)

---

📄 For a detailed explanation, see the [How does Clonalyzer do the calculations.pdf](./How%20does%20Clonalyzer%20do%20the%20calculations.pdf)

---
All rates are computed using volume-normalized quantities for full mass balance integrity.
📄 For a detailed explanation of how kinetic and stoichiometric parameters are calculated, see the [How does Clonalyzer do the calculations.pdf](./How%20does%20Clonalyzer%20do%20the%20calculations.pdf) document included in this repository.

## 📄 Input Data Format

Clonalyzer expects a single CSV file in `data/data.csv` with the **first row reserved for metadata** (it will be skipped automatically).

### Required Columns (used in calculations)

| Column name   | Description                           | Units            |
|---------------|----------------------------------------|------------------|
| `t_hr`        | Time since inoculation                | hours            |
| `Clone`       | Clone identifier (e.g., A, B, C)      | string           |
| `Rep`         | Biological replicate number           | integer (1, 2, 3)|
| `VCD`         | Viable cell density                   | cells/mL         |
| `Viab_pct`    | Cell viability plot                   | %                |
| `Vol_mL`      | Culture volume at sampling time       | mL               |
| `Glc_g_L`     | Glucose concentration                 | g/L              |
| `Lac_g_L`     | Lactate concentration                 | g/L              |
| `Gln_mM`      | Glutamine concentration               | mmol/L  (mM)     |
| `Glu_mM`      | Glutamate concentration               | mmol/L  (mM)     |
| `is_post_feed`| Whether the sample is post-feeding    | TRUE or FALSE    |

### Optional Columns (used in some plots if present)

| Column name     | Example usage                    | Units         |
|------------------|----------------------------------|---------------|
| `GFP_mean`, `TMRM_mean` | Cytometry signal (GFP, mitochondrial potential) | arbitrary units |

> Columns such as `Notes`, `Glucose_Added_mL`, or `Quadrants` are **ignored**, but can coexist in your file.

### Example

| t_hr | t_day | Clone | Rep | Timestamp | Date       | is_post_feed | VCD       | DCD       | Viab_pct | Glc_g_L | Lac_g_L |
|------|-------|--------|-----|-----------|------------|--------------|-----------|-----------|----------|---------|---------|
| 0    | 0     | A     | 1   | 10:00     | 03/07/2025 | FALSE        | 3.10E+05  | 4.00E+03  | 98.73    | 6.59    | 0.00    |
| 24   | 1     | B      | 1   | 10:00     | 04/07/2025 | FALSE        | 5.20E+05  | 4.00E+03  | 99.22    | 5.88    | 0.44    |


### Flexibility for Other Measurements

Clonalyzer is designed to **gracefully handle extra columns**. This allows you to include additional data such as:
- Cell size (e.g., from a Coulter counter)
- pH, osmolarity, conductivity
- Any signal from cytometry or online sensors

You may include as many additional columns as needed—the system will ignore them unless explicitly used in plotting.

## 📁 Project Structure

```
clonalyzer/
├── interval_kinetics.py      # Interval-based kinetics (Clone × Rep × Time)
├── grouped_kinetics.py       # Aggregated kinetics (Clone × Time)
├── exp_phase_kinetics.py     # Exponential-phase kinetics (Clone × Rep)
├── plot_raw.py               # Per-sample scatter plots
├── plot_grouped.py           # Grouped line plots with error bars
├── plot_exp.py               # Bar plots per clone (exponential phase)
```

## 🚀 Quickstart

1. **Clone the repository**

```bash
git clone https://github.com/ebalderasr/Clonalyzer.git
cd Clonalyzer
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Prepare your data**

Place your CSV file inside the `data/` folder and rename it to:

```
data/data.csv
```


## 📈 Usage

Clonalyzer is organized into three independent analysis blocks. Each block includes a data processing script and a plotting script. You can run all blocks, or choose only the ones that fit your experimental design.

---

### 🔹 Block 1: Interval-based kinetics (Clone × Rep × Time)

Use this block to compute kinetics between each pair of consecutive time points per replicate (interval-by-interval). Ideal for detailed trajectory analysis.

```bash
python -m clonalyzer.interval_kinetics
```

- Calculates $$μ, IVCD, ΔX, ΔGlc, ΔLac, q_G, q_L, Y_XG, Y_XL$$ for each interval
- Input: `data/data.csv`
- Output: `outputs/interval_kinetics.csv`

```bash
python -m clonalyzer.plot_raw
```

- Generates per-sample scatter plots:
  - Raw variables (VCD, glucose, etc.)
  - Kinetic parameters per interval
  - Correlation plots

---

### 🔹 Block 2: Aggregated kinetics (Clone × Time)

Use this block to compute and visualize the average ± SD of all measurements and parameters per clone at each time point.

```bash
python -m clonalyzer.grouped_kinetics
```

- Aggregates all numeric columns by `Clone × t_hr`
- Output: `outputs/results_agg_by_clone_time.csv`

```bash
python -m clonalyzer.plot_grouped
```

- Line plots with error bars for:
  - Raw trends (glucose, lactate, viability...)
  - Kinetic variables over time
  - Correlations (mean ± SD)

---

### 🔹 Block 3: Exponential-phase kinetics (Clone × Rep)

Use this block to extract clone-level metrics only during exponential growth. You’ll be prompted to specify the start and end time of the exponential phase.

```bash
python -m clonalyzer.exp_phase_kinetics
```

- Requires user input:
  - Start time (e.g. `0`)
  - End time (e.g. `96`)
- Calculates μ, IVCD, yields, and specific rates using only data within that window
- Output:
  - `kinetics_by_clone_rep.csv` (per replicate)
  - `kinetics_by_clone.csv` (mean ± SD per clone)

```bash
python -m clonalyzer.plot_exp
```

- Bar plots (mean ± SD) for each parameter per clone
- Output: `outputs/figures_exp/`

---

Each block can be run independently. For example, if you only need clone-level performance comparisons, Block 3 is sufficient.


## 📂 Outputs

All processed files and figures are saved in the `outputs/` folder.

## 👤 Author

**Emiliano Balderas R.**  
GitHub: [@ebalderasr](https://github.com/ebalderasr)

## 📄 License

MIT License.
