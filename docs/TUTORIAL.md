# Tutorials

## 1. Run the pipeline on the synthetic data

1. Install the requirements (see `README.md`).
2. Generate the data again if wanted: `python scripts/make_synthetic_data.py data/synthetic`.
3. Open `notebooks/GTI_transferability.ipynb` and run all cells.
4. Read the GTI table in section 3.3 and 4.4. Pooled and depth-matched rows show how regime mixing lowers R.

## 2. Use your own two wells

1. Export both wells as CSV with the columns listed in `docs/USER_GUIDE.md`.
2. Put them in a folder outside the repository, for example `private_data/Well-1.csv` and `private_data/Well-2.csv`.
3. Set `DATA_DIR = "../private_data"` in the setup cell.
4. `DEEP_TOP` is derived from the shallowest Well-2 depth, so no change is needed.
5. Run all cells. Keep the private folder out of version control. The `.gitignore` already blocks `Well-1.csv` and `Well-2.csv` outside `data/synthetic`.

## 3. Check the setup quickly

Set `FAST = True`. The run finishes in minutes. Use it after changing library versions.

## 4. Change the GTI weights or block length

- Block length: change `BLOCK_M`, or read the block-length table in section 3.3 and 4.4.
- Weight sensitivity: the class-share table in the same section lists the share of weight triples in each class.

## 5. Add a third well

Load a third file with `load(...)`, then call `gti_bootstrap(w1, I_obs)` after replacing `w2` by the new well. This gives a first test of the provisional class limits.
