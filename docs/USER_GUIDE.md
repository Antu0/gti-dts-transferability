# User guide

## Inputs

Two CSV files, `Well-1.csv` (source well, used for training) and `Well-2.csv` (target well, never used for fitting).

| Column | Unit | Meaning | Accepted range |
|---|---|---|---|
| MD | m | Measured depth | any |
| BIT | in | Bit size | 4 to 20 |
| CAL | in | Caliper | 4 to 20 |
| GR | API | Gamma ray | 0 to 300 |
| DT | µs/ft | Compressional slowness | 40 to 240 |
| DTS | µs/ft | Shear slowness (target) | 60 to 400 |
| NPHI | v/v | Neutron porosity | -0.05 to 0.60 |
| RHOB | g/cm³ | Bulk density | 1.65 to 2.95 |
| RES_DEEP | ohm·m | Deep resistivity | 0.01 to 2000 |

Rows outside these ranges or with missing values are removed. The files should already be depth-matched and despiked. Each file needs a regular depth step.

## Settings (setup cell)

| Name | Default | Effect |
|---|---|---|
| `DATA_DIR` | `../data/synthetic` | Folder with the two CSV files |
| `FAST` | `False` | `True` reduces bootstrap, SHAP rows, epochs and tree counts for a quick check |
| `N_BOOT` | 3000 (200 if fast) | Bootstrap resamples |
| `N_SHAP` | 2000 (300 if fast) | Depth-spaced rows explained per well |
| `BLOCK_M` | 100 | Depth-block length (m) of the bootstrap |
| `CLASS_HI`, `CLASS_LO` | 0.8, 0.5 | Provisional GTI class limits |
| `ANN_VALIDATION` | `"test"` | `"test"` uses the held-out 20 % split for early stopping, as in the paper. `"train"` uses 10 % of the training rows |
| `SEED` | 42 | Random seed |

## Outputs

The notebook prints tables and draws figures. It writes no files. To keep a table, call `df.to_csv(...)` on the variable shown below.

| Variable | Content |
|---|---|
| `t3`, `t4` | KS, PSI and shift measures |
| `MODELS` | Fitted RF, XGB and ANN |
| `w2` | Well-2 with columns `DTS_RF`, `DTS_XGB`, `DTS_ANN` and the errors |
| `rho`, `I_obs`, `I_boot` | SHAP rank correlations and the interpretation term I |
| `nested`, `bins` | GTI and accuracy drop for nested and disjoint reference sets |
| `tl` | Transfer-learning results by fraction, placement and model |

## Definitions

- D: share of Well-2 rows inside the 95 % Mahalanobis envelope of the Well-1 logs.
- R: smaller divided by larger DT-DTS slope of the two wells. R is set to 0 if a resampled slope is not positive.
- I: smallest Spearman correlation between the Well-1 and Well-2 mean |SHAP| feature ranks over the three algorithms. With five logs, I moves in steps of 0.1.
- GTI = (D · R · I)^(1/3).

## Expected behaviour

- With the synthetic data, the pooled Well-1 slope is smaller than the depth-matched slope, and R is lower for the pooled reference.
- Cluster-robust t statistics are smaller than naive ones.
- The accuracy drop is the internal R² minus the external R².
- Results repeat for a fixed seed on the same library versions.

## Common problems

| Message | Cause and fix |
|---|---|
| `Cannot take a larger sample than population` | Fewer rows than the requested sample. Lower `N_SHAP` or supply more rows |
| Very long SHAP step | Random forest SHAP is slow on deep trees. Lower `N_SHAP` |
| Missing column | Check the column names in the table above |
