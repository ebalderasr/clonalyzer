# Kinetics Data Analysis for CHO Cell Clones

## Overview
This repository contains scripts and datasets for analyzing the kinetics of CHO cell clones. The analysis focuses on parameters like cell viability, glucose, glutamine, and lactate concentrations across multiple time points and replicates.

## Data Requirements
The script processes kinetic data from a CSV file. Below are the required data format and structure:

### File Format
- The input data must be a **CSV** file with a header row.

### Columns Description
| **Column Name** | **Description**                                   | **Example**      | **Data Type**          |
|------------------|---------------------------------------------------|------------------|------------------------|
| `Clone`          | Identifier for the CHO cell clone.               | `X-B7`, `C`      | Categorical (string)   |
| `T`              | Timepoints for measurements (in days).           | `0.0`, `1.0`     | Numeric (float)        |
| `V`              | Monitored parameter (e.g., viable volume).       | `166.0`          | Numeric (float)        |
| `M`              | Monitored parameter (e.g., metabolites).         | `6.0`            | Numeric (float)        |
| `C`              | Monitored parameter (e.g., cell concentration).  | `10`             | Integer                |
| `dil`            | Dilution factor or condition identifier.         | `2`              | Integer                |
| `Xv`             | Viable cell density (cells/mL).                  | `332000.0`       | Numeric (float)        |
| `Xm`             | Maximum cell density (cells/mL).                 | `12000.0`        | Numeric (float)        |
| `Viabilidad`     | Cell viability (as a percentage, string format). | `97%`, `100%`    | String (convertible)   |
| `rep`            | Replicate number for each clone.                 | `1`, `2`         | Integer                |
| `AcM`            | Monoclonal antibody concentration (g/L).         | `0.5`, `NaN`     | Numeric (float or NaN) |
| `G`              | Glucose concentration (g/L).                    | `6.2`, `5.9`     | String (convertible)   |
| `L`              | Lactate concentration (g/L).                    | `0.3`            | Numeric (float)        |
| `Gln`            | Glutamine concentration (mmol/L).               | `5.9`, `6.0`     | Numeric (float)        |
| `Glu`            | Glutamate concentration (mmol/L).               | `1.8`            | Numeric (float)        |

### Example Dataset
| Clone | T   | V     | M    | C  | dil | Xv       | Xm     | Viabilidad | rep | AcM  | G       | L     | Gln   | Glu   |
|-------|-----|-------|------|----|-----|----------|--------|------------|-----|------|---------|-------|-------|-------|
| X-B7  | 0.0 | 166.0 | 6.0  | 10 | 2   | 332000.0 | 12000.0| 97%        | 1   | NaN  | 6.2     | 0.3   | 5.9   | 1.8   |
| X-B7  | 1.0 | 150.0 | 6.5  | 10 | 2   | 320000.0 | 15000.0| 95%        | 1   | 0.5  | 6.0     | 0.4   | 5.8   | 1.9   |

---

## Usage
1. Place your dataset in the `data/` folder.
2. Run the script:
   ```bash
   python preprocess_kinetics.py
