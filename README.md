# GTI-DTS: geological transferability index for cross-well shear-wave slowness prediction

Code for the manuscript "A geological transferability index for cross-well uncertainty in shear-wave slowness prediction" (submitted to *Geomechanics for Energy and the Environment*).

The code trains random forest, XGBoost and neural network models for shear-wave slowness (DTS) on one well, applies them to a second well without refitting, and computes the Geological Transferability Index (GTI) with block-bootstrap uncertainty. It also reproduces the statistical tests, the accuracy-loss analysis, the calibration experiments and the geomechanical propagation.

## Data availability

The original logs of Well-1 (Kailashtila) and Well-2 (Srikail/Bangora) belong to Petrobangla and cannot be shared. The repository contains a **synthetic dataset** (`data/synthetic`) with the same columns, units and qualitative behaviour (a depth-dependent DT-DTS slope in Well-1, a steeper slope and shifted distributions in Well-2). The synthetic values are random and do not describe any real well. Running the code on them shows that the pipeline works. The numbers differ from those in the paper. People with their own two-well data can run the same notebook on it.

## Repository layout

| Path | Content |
|---|---|
| `notebooks/GTI_transferability.ipynb` | The full analysis, organised as the manuscript sections |
| `data/synthetic/` | `Well-1.csv` and `Well-2.csv` (synthetic) |
| `scripts/make_synthetic_data.py` | Generator for the synthetic data (fixed seed) |
| `docs/USER_GUIDE.md` | Inputs, outputs, options and expected behaviour |
| `docs/TUTORIAL.md` | Step-by-step use cases |
| `tests/test_smoke.py` | Checks on the synthetic data |
| `requirements.txt` | Python dependencies |

## Installation

Python 3.10 or newer is needed.

```bash
git clone https://github.com/YOUR-USER/gti-dts-transferability.git
cd gti-dts-transferability
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Quick start

```bash
jupyter lab notebooks/GTI_transferability.ipynb
```

Run all cells. The notebook reads `data/synthetic/Well-1.csv` and `Well-2.csv` by default. To use your own logs, change `DATA_DIR` in the setup cell. To check the setup quickly, set `FAST = True` in the same cell.

Run without opening Jupyter:

```bash
jupyter nbconvert --to notebook --execute notebooks/GTI_transferability.ipynb --output run.ipynb
```

Google Colab: upload the repository folder, mount it, set `DATA_DIR` to the folder with the two CSV files and run all cells.

## Computational requirements

| Data | `FAST = False` |
|---|---|
| Synthetic (6,400 rows) | about 4 minutes |
| Original size (45,000 rows) | about 30 minutes |

`FAST = True` finishes in a few minutes on either.

Tested on a CPU machine with 4 cores and 16 GB of memory. No GPU is needed. All random seeds are fixed at 42, so results repeat on the same software versions. Small differences between versions of TensorFlow, scikit-learn and SHAP are expected.

## Reproducing the paper

The paper results come from the confidential logs. The notebook sections map to the paper as follows.

| Notebook section | Manuscript item |
|---|---|
| 1 Study wells and quality control | Tables 1 and 2 |
| 4.1 Distribution shift | Tables 3 and 4 |
| 4.3 Slope inference | Table 7, Figure 7 |
| 3.2 and 4.2 Models | Tables 5 and 6 |
| 3.3 The interpretation term I | Figures 5 and 6 |
| 3.3 and 4.4 GTI | Table 8, Figure 8 |
| 4.5 GTI and accuracy loss | Table 9, Figure 9 |
| 4.6 Algorithm spread | Table 10 |
| 4.7 Calibration and transfer learning | Tables 11, Figures 10 and 11 |
| 4.8 Geomechanical propagation | Table 12 |

Values in the paper for the original data: I = 0.90, GTI = 0.617 (pooled) and 0.861 (depth-matched).

## Limitations

- The class limits 0.5 and 0.8 of the GTI are provisional and not calibrated on a third well.
- By default the ANN early stopping monitors the held-out 20 % split, as in the paper. Set `ANN_VALIDATION = "train"` to monitor a validation part of the training data.

## Citation

See `CITATION.cff`. Please cite the paper once it is published.

## License

MIT. See `LICENSE`.
