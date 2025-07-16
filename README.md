# Clonalyzer

**Clonalyzer** is a modular toolkit for kinetic and stoichiometric analysis of CHO fed-batch cultures. It supports per-interval, grouped, and exponential-phase analyses with high-quality visualizations.

Designed for bioprocess engineers and data scientists working with clonal cell line characterization.

## 🧬 What is Clonalyzer?

Clonalyzer is a modular Python toolkit for the kinetic and stoichiometric analysis of mammalian cell cultures, particularly designed for fed-batch bioprocesses using CHO cells. It helps quantify growth rates, nutrient consumption, metabolite production, yields, and specific rates—per replicate or per clone.

🔎 **Use cases include**:
- Comparing clone performance in early-stage screening
- Monitoring nutrient and metabolite profiles over time
- Estimating growth and productivity during the exponential phase
- Generating clean, publication-ready plots

Although Clonalyzer was designed with **fed-batch CHO processes** in mind, it is **not limited** to them. For instance:
- Block 3 (exponential-phase analysis) can be used for any batch process.
- Block 1 and 2 support general interval or time-based profiling, including perfusion or hybrid strategies.

## 📐 Kinetic and Stoichiometric Calculations

Clonalyzer computes the following parameters for each Clone × Replicate:

| Parameter      | Symbol      | Units                     | Description |
|----------------|-------------|----------------------------|-------------|
| Growth rate    | μ           | h⁻¹                        | Calculated as slope of ln(VCD) over time |
| Integrated viable cell density | IVCD      | cells·h·mL⁻¹ or cells·h | Area under the VCD curve over time (trapezoidal rule) |
| Cell balance   | ΔX          | cells                     | Difference in viable cells in total volume |
| Substrate balance | ΔS (Glc, Lac) | mol                    | Difference in total moles in volume |
| Yield on substrate | Yₓ/ₛ     | cells·mol⁻¹              | ΔX / ΔS |
| Specific rate  | qₛ          | pmol·cell⁻¹·h⁻¹           | ΔS normalized to IVCD and converted to pmol |

For example, specific consumption of glucose (q_Glc):

```
q_Glc = (ΔGlucose in mol × 1e12) / IVCD  →  pmol/(cell·h)
```

All rates are computed using volume-normalized quantities for full mass balance integrity.

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

### 1. Interval-based kinetics

```bash
python -m clonalyzer.interval_kinetics
python -m clonalyzer.plot_raw
```

### 2. Aggregated kinetics

```bash
python -m clonalyzer.grouped_kinetics
python -m clonalyzer.plot_grouped
```

### 3. Exponential-phase kinetics

```bash
python -m clonalyzer.exp_phase_kinetics
python -m clonalyzer.plot_exp
```

## 📂 Outputs

All processed files and figures are saved in the `outputs/` folder.

## 👤 Author

**Emiliano Balderas R.**  
GitHub: [@ebalderasr](https://github.com/ebalderasr)

## 📄 License

MIT License.