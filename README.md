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
