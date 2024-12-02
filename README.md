# Clonalyzer: Kinetics Data Analysis for CHO Cell Clones

## Overview
**Clonalyzer** is a Python-based tool designed to clean, process, and analyze kinetic data from CHO (Chinese Hamster Ovary) cell clones. It supports experiments involving multiple clones and replicates, enabling users to evaluate performance across various experimental conditions systematically.

### Current Features
1. **Data Cleaning**:
   - Removes inconsistencies and ensures the dataset is ready for analysis.
   - Handles missing values using user-defined strategies (e.g., mean, median, or zero filling).
   
2. **Data Preview**:
   - Provides statistical summaries (`describe`) and basic information (`info`) of the dataset to facilitate exploration.

3. **Visualization**:
   - Automatically generates key plots, such as:
     - Time vs. individual parameters (e.g., Viable Cells, Glucose, Glutamine).
     - Combined plots for parameters with similar units (e.g., Glucose and Glutamine).
   - Saves all plots in a dedicated `figures` directory.

   **Examples of Generated Visualizations**:
   - **Glucose and Glutamine vs Time**:
     ![Glucose and Glutamine vs Time](figures/Glucose_and_Glutamine_vs_Time.png)
   - **Kinetic Parameter Comparison**:
     ![Kinetic Parameter Comparison](figures/kinetic_parameters_comparison.png)

4. **Kinetic and Stoichiometric Parameter Calculation**:
   - Calculates key parameters such as:
     - Specific growth rates (\( \mu \)).
     - Substrate uptake rates (\( q \)).
     - Biomass yields (\( Y \)).
   - Outputs results as a consolidated DataFrame for easy interpretation and visualization.

### Future Development
Planned features include:
- Advanced visualizations for kinetic and stoichiometric parameter comparisons across clones.
- Automated identification of the exponential growth phase.
- Expanded support for additional culture parameters (e.g., recombinant protein production).

This tool is ideal for researchers in biopharmaceutical development, streamlining the analysis of CHO cell cultures for clone optimization and process improvement.

---

## Authors
**Emiliano Balderas Ramírez**  
PhD Student at the Instituto de Biotecnología, UNAM  
Email: [ebalderas@live.com.mx](mailto:ebalderas@live.com.mx)  
Phone: +52 2221075693  

**Dr. Octavio Tonatiuh Ramírez Reivich**  
Principal Investigator, Instituto de Biotecnología, UNAM  
Email: [tonatiuh.ramirez@ibt.unam.mx](mailto:tonatiuh.ramirez@ibt.unam.mx)  

---

## Repository Structure
The repository is organized as follows:

```plaintext
clonalyzer/
│
├── data/                 # Contains input datasets (CSV files)
│   └── 2024-05-18_Clones_B_C_Kinetics.csv  # Example dataset
│
├── figures/              # Contains generated figures from the analysis
│   └── Glucose_and_Glutamine_vs_Time.png  # Example plot
│   └── kinetic_parameters_comparison.png # Example plot
│
├── clonalyzer.py         # Main script for data processing
├── README.md             # Documentation for the project
└── LICENSE               # License for the repository
```

---

## Requirements
To run the notebook, ensure you have Python 3.8+ and the following packages installed:

- `pandas`
- `numpy`
- `matplotlib`
- `seaborn`
- `scipy`

Install these packages using pip:
```plaintext
pip install pandas numpy matplotlib seaborn scipy
```

---

## Usage
1. **Prepare your dataset**:
   - Place your kinetic data in the `data/` folder. The dataset should be a CSV file formatted as described below.

2. **Run the notebook**:
   - Open the Jupyter Notebook `clonalyzer.ipynb` in the `script/` folder using JupyterLab or Jupyter Notebook:
     ```
     jupyter notebook script/clonalyzer.ipynb
     ```
   - Follow the cells in the notebook to preprocess, clean, and analyze the data.

3. **Outputs**:
   - The notebook generates cleaned datasets and visualizations (e.g., time-series plots, scatter plots).  

---

## Contact
For questions or suggestions, feel free to contact:  
**Emiliano Balderas Ramírez**  
PhD Student at the Instituto de Biotecnología, UNAM  
Email: [ebalderas@live.com.mx](mailto:ebalderas@live.com.mx)  
Phone: +52 2221075693  