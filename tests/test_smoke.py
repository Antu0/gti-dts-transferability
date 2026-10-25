"""Checks that the synthetic data are valid and have the regime structure the notebook needs."""
import subprocess, sys, pathlib
import numpy as np, pandas as pd

ROOT = pathlib.Path(__file__).resolve().parents[1]
COLS = ["MD", "BIT", "CAL", "GR", "DT", "DTS", "NPHI", "RHOB", "RES_DEEP"]


def test_generator_runs(tmp_path):
    subprocess.run([sys.executable, str(ROOT / "scripts" / "make_synthetic_data.py"), str(tmp_path)], check=True)
    for f in ["Well-1.csv", "Well-2.csv"]:
        d = pd.read_csv(tmp_path / f)
        assert list(d.columns) == COLS and len(d) > 1000 and not d.isna().any().any()


def test_regime_mixing():
    w1 = pd.read_csv(ROOT / "data" / "synthetic" / "Well-1.csv")
    w2 = pd.read_csv(ROOT / "data" / "synthetic" / "Well-2.csv")
    slope = lambda d: np.polyfit(d.DT, d.DTS, 1)[0]
    deep = w1[w1.MD >= w2.MD.min()]
    assert slope(w1) < slope(deep) < slope(w2) * 1.1
