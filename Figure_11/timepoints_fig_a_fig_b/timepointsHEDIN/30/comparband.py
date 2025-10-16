#!/usr/bin/env python3
import os, re, argparse
import numpy as np

def read_cp2k_band(filepath, column=2):
    """
    Read CP2K BANDSTRUCTURE file and return array (nkpt, nband).
    Default column=2 → DFT+SOC (3rd column in file).
    Use column=3 for G0W0+SOC.
    """
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    bands_per_k = []
    current_bands = []

    for line in lines:
        if line.strip().startswith("kpoint:"):
            if current_bands:
                bands_per_k.append(current_bands)
                current_bands = []
        elif re.match(r"^\s*\d+", line):
            parts = line.split()
            if len(parts) > column:
                try:
                    energy = float(parts[column])
                    current_bands.append(energy)
                except ValueError:
                    continue

    if current_bands:
        bands_per_k.append(current_bands)

    nkpt = len(bands_per_k)
    if nkpt == 0:
        raise ValueError(f"No k-points parsed from {filepath}")
    nband = len(bands_per_k[0])

    arr = np.array(bands_per_k, dtype=float).reshape(nkpt, nband)
    return arr

def compute_mad(arr1, arr2, emin=None, emax=None):
    """Mean absolute deviation, optionally restricted to an energy window."""
    if arr1.shape != arr2.shape:
        raise ValueError(f"Shape mismatch: {arr1.shape} vs {arr2.shape}")

    mask = np.ones_like(arr1, dtype=bool)
    if emin is not None:
        mask &= (arr1 >= emin)
    if emax is not None:
        mask &= (arr1 <= emax)

    if not np.any(mask):
        raise ValueError("No eigenvalues found inside the requested energy window")

    diff = np.abs(arr1 - arr2)
    return np.mean(diff[mask])

def main(normal_path, highcut_path, column, emin, emax):
    arr_normal = read_cp2k_band(normal_path, column=column)
    arr_high = read_cp2k_band(highcut_path, column=column)
    mad = compute_mad(arr_normal, arr_high, emin=emin, emax=emax)
    if emin is not None or emax is not None:
        print(f"MAD = {mad:.6f} eV  (restricted to {emin} – {emax} eV)")
    else:
        print(f"MAD = {mad:.6f} eV")

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Compute MAD between normal and highcutoff CP2K bandstructures")
    ap.add_argument("normal", help="Path to normal BANDSTRUCTURE file")
    ap.add_argument("highcut", help="Path to highcutoff BANDSTRUCTURE file")
    ap.add_argument("--column", "-c", type=int, default=2,
                    help="Which column to use: 2=DFT+SOC, 3=G0W0+SOC (default=2)")
    ap.add_argument("--emin", type=float, default=None, help="Minimum energy to include")
    ap.add_argument("--emax", type=float, default=None, help="Maximum energy to include")
    args = ap.parse_args()
    main(args.normal, args.highcut, args.column, args.emin, args.emax)

