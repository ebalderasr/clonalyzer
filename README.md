   # Clonalyzer: Kinetics Data Analysis for CHO Cell Clones

   ## Overview
   **Clonalyzer** is a Python-based tool designed to clean, process, and visualize kinetic data from CHO (Chinese Hamster Ovary) cell clones. It is optimized for experiments involving multiple clones and replicates, allowing users to analyze and compare performance across different experimental conditions.

   Currently, Clonalyzer focuses on data cleaning and previewing the results to ensure data integrity and usability. Future updates will include automated graph generation, key kinetic and stoichiometric parameter calculations (e.g., growth rates, substrate uptake rates, and product yields), and their visualization.

   This tool is ideal for researchers working in biopharmaceutical development, enabling streamlined analysis of CHO cell cultures and clone optimization.


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
   │   └── Datos_cinetica_18may2024.csv  # Example dataset
   │
   ├── scripts/              # Python scripts for data analysis
   │   └── clonalyzer.py      # Main script for data processing
   │
   └── README.md             # Documentation for the project
   ```

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

   ## Data Requirements
   The script processes kinetic data from a CSV file. Below are the required data format and structure:

   ### File Format
   - The input data must be a **CSV** file with a header row.

   ### Data Format
   The input dataset must be a CSV file with the following structure:

   ### Columns
   | **Column Name**        | **Description**                                   | **Units**         | **Example**       |
   |-------------------------|---------------------------------------------------|-------------------|-------------------|
   | `Clone`                | Identifier for the CHO cell clone.               | -                 | `Clone_A`, `C1`   |
   | `rep`                  | Replicate number for each clone.                 | Integer           | `1`, `2`, `3`     |
   | `T`                    | Timepoints for measurements.                     | Days              | `0`, `1`, `2`     |
   | `G`                    | Glucose concentration.                           | g/L               | `6.5`, `5.9`      |
   | `Gln`                  | Glutamine concentration.                         | mmol/L            | `2.5`, `3.1`      |
   | `Xv`                   | Viable cell density.                             | cells/mL          | `1.2e6`, `2.5e6`  |
   | `Xd`                   | Dead cell density.                               | cells/mL          | `5.0e4`, `3.0e5`  |
   | `L`                    | Lactate concentration.                           | g/L               | `0.5`, `1.2`      |
   | `V`                    | Viability as a percentage.                       | %                 | `95`, `98`        |
   | `MAb`                  | Monoclonal antibody concentration.               | mg/mL             | `0.8`, `1.5`      |
   | `rP`                   | Recombinant protein concentration.               | mg/mL             | `0.5`, `0.9`      |

   ### Example Dataset
   | Clone  | rep | T   | G   | Gln | Xv      | Xd      | L   | V  | MAb | rP  |
   |--------|-----|-----|-----|-----|---------|---------|-----|----|-----|-----|
   | Clone1 | 1   | 0.0 | 6.5 | 2.5 | 1.2e6   | 5.0e4   | 0.5 | 95 | 0.8 | 0.5 |
   | Clone1 | 2   | 1.0 | 6.2 | 2.4 | 1.8e6   | 4.5e4   | 0.6 | 98 | 1.0 | 0.6 |
   | Clone2 | 1   | 0.0 | 6.4 | 2.6 | 1.1e6   | 5.2e4   | 0.5 | 94 | 0.7 | 0.4 |
   | Clone2 | 2   | 1.0 | 6.1 | 2.3 | 1.7e6   | 4.7e4   | 0.6 | 97 | 0.9 | 0.5 |

   ---

   ## Contact
   For questions or suggestions, feel free to contact:  
   **Emiliano Balderas Ramírez**  
   PhD Student at the Instituto de Biotecnología, UNAM  
   Email: [ebalderas@live.com.mx](mailto:ebalderas@live.com.mx)  
   Phone: +52 2221075693  


