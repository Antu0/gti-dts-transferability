"""Generate a small synthetic two-well dataset with the same columns and the same
qualitative behaviour as the confidential Bengal Basin logs.

Well-1: DT-DTS slope is flat above 2088 m and steeper below it (regime mixing).
Well-2: starts at 2088 m, steeper slope, shifted log distributions.
All values are random. They do not describe any real well.

Usage: python scripts/make_synthetic_data.py [output_dir]
"""
import sys, os
import numpy as np, pandas as pd

SEED = 7
DEEP_TOP = 2088.0


def ar1(n, rho, sd, rng):
    e = rng.normal(0, sd * np.sqrt(1 - rho ** 2), n); x = np.zeros(n)
    for i in range(1, n):
        x[i] = rho * x[i - 1] + e[i]
    return x


def make_well(md, kind, rng):
    n = len(md); z = (md - 200) / 3300
    dt = 145 - 80 * z ** 0.8 + ar1(n, 0.995, 6, rng) + rng.normal(0, 1.5, n)
    nphi = np.clip(0.50 - 0.38 * z + 0.004 * (dt - 100) + ar1(n, 0.99, 0.04, rng) + rng.normal(0, 0.01, n), 0.05, 0.58)
    rhob = np.clip(1.95 + 0.75 * z - 0.002 * (dt - 100) + ar1(n, 0.99, 0.04, rng) + rng.normal(0, 0.015, n), 1.7, 2.9)
    gr = np.clip(80 + ar1(n, 0.998, 22, rng) + rng.normal(0, 4, n), 25, 220)
    res = np.exp(1.5 + 0.8 * z + ar1(n, 0.99, 0.5, rng) + rng.normal(0, 0.05, n))
    if kind == "well1":
        shallow = md < DEEP_TOP
        dts = np.where(shallow, 150 + 0.55 * (dt - 84), 150 + 1.50 * (dt - 84))
    else:
        dts = 144 + 1.85 * (dt - 80)
    dts = dts + 14 * (nphi - 0.3) + ar1(n, 0.9, 3.0, rng) + rng.normal(0, 1.5, n)
    cal = 8.5 + rng.normal(0, 0.15, n); bit = np.full(n, 8.5)
    return pd.DataFrame({"MD": md, "BIT": bit, "CAL": cal, "GR": gr, "DT": dt, "DTS": np.clip(dts, 70, 380),
                         "NPHI": nphi, "RHOB": rhob, "RES_DEEP": res})


def main(out="data/synthetic"):
    rng = np.random.default_rng(SEED); os.makedirs(out, exist_ok=True)
    w1 = make_well(np.arange(200, 3470, 0.8), "well1", rng)
    w2 = make_well(np.arange(DEEP_TOP, 3500, 0.6), "well2", rng)
    w2["NPHI"] = np.clip(w2.NPHI - 0.08, 0.05, 0.45); w2["RES_DEEP"] *= 0.4; w2["GR"] = np.clip(w2.GR + 12, 25, 220)
    w1.round(4).to_csv(os.path.join(out, "Well-1.csv"), index=False)
    w2.round(4).to_csv(os.path.join(out, "Well-2.csv"), index=False)
    print("Well-1:", w1.shape, "Well-2:", w2.shape)


if __name__ == "__main__":
    main(*sys.argv[1:2])
