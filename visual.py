#!/usr/bin/env python3
"""
Visualize atmospheric-noise randomness from Random.org.

What you get:
  1) A "TV static" image from true-random bytes
  2) Histogram of byte values (0-255)
  3) Bit-balance per bit position (0..7)
  4) Autocorrelation for lags 1..100

Requirements:
  pip install requests numpy matplotlib

Note:
  - Random.org has quotas; be considerate with N_BYTES and CHUNK_SIZE.
  - If fetching fails (quota/network), code can fall back to pseudorandom.
"""

import requests
import time
import sys
import numpy as np
import matplotlib.pyplot as plt

# ---------------- Configuration ----------------
# Total number of random bytes to fetch (must be a multiple of CHUNK_SIZE)
N_BYTES = 256 * 256          # 65,536 bytes → 256x256 image
CHUNK_SIZE = 10000           # Random.org GET limit per call is typically 10,000 integers
SLEEP_BETWEEN_CALLS = 0.5    # seconds (be polite)
USE_FALLBACK_IF_FAIL = True  # use numpy PRNG if Random.org fails (plots will be labeled)

# Endpoint for Random.org HTTP integers API
RNG_URL = "https://www.random.org/integers/"

def fetch_random_bytes_from_random_org(n_bytes, chunk_size=10000, sleep_between=0.5):
    """
    Fetch n_bytes of true random bytes (0..255) from Random.org using the integers API.
    Returns a numpy uint8 array of length n_bytes.
    May raise an exception if the service returns an error.
    """
    if n_bytes % chunk_size != 0:
        raise ValueError("n_bytes must be a multiple of chunk_size for this simple fetcher.")

    out = np.empty(n_bytes, dtype=np.uint8)
    written = 0

    for _ in range(n_bytes // chunk_size):
        params = {
            "num": chunk_size,
            "min": 0,
            "max": 255,
            "col": 1,
            "base": 10,
            "format": "plain",
            "rnd": "new",  # ensure fresh randomness
        }
        r = requests.get(RNG_URL, params=params, timeout=15)
        r.raise_for_status()
        text = r.text.strip()

        if text.startswith("Error:"):
            raise RuntimeError(f"Random.org error: {text}")

        # Parse integers; they are newline/space separated
        vals = [int(x) for x in text.split()]
        if len(vals) != chunk_size:
            raise RuntimeError(f"Unexpected count from Random.org: got {len(vals)} expected {chunk_size}")

        out[written:written+chunk_size] = np.array(vals, dtype=np.uint8)
        written += chunk_size
        time.sleep(sleep_between)

    return out

def compute_autocorrelation(series, max_lag=100):
    """
    Simple (biased) autocorrelation for lags 1..max_lag.
    Normalized by variance so ACF[0]≈1 (we omit lag 0 in the return).
    """
    x = series.astype(float)
    x = (x - x.mean())
    var = np.dot(x, x) / len(x)
    if var == 0:
        return np.zeros(max_lag)
    acf = []
    for lag in range(1, max_lag + 1):
        v = np.dot(x[:-lag], x[lag:]) / len(x)
        acf.append(v / var)
    return np.array(acf)

def main():
    source_label = "Random.org (atmospheric noise)"
    try:
        data = fetch_random_bytes_from_random_org(N_BYTES, CHUNK_SIZE, SLEEP_BETWEEN_CALLS)
    except Exception as e:
        if not USE_FALLBACK_IF_FAIL:
            print("Failed to fetch from Random.org:", e, file=sys.stderr)
            sys.exit(1)
        # Fallback to PRNG so visuals still appear; clearly label the source
        rng = np.random.default_rng()
        data = rng.integers(0, 256, size=N_BYTES, dtype=np.uint8)
        source_label = "Fallback: NumPy PRNG (not true randomness)"
        print("⚠️ Fallback in use (quota/network issue). Proceeding with PRNG visuals.", file=sys.stderr)

    # 1) TV static image (256x256)
    side = int(np.sqrt(len(data)))
    if side * side != len(data):
        # reshape to a near-square if N_BYTES not a perfect square
        side = int(np.floor(np.sqrt(len(data))))
        data = data[: side * side]
    img = data.reshape(side, side)

    # 2) Histogram (0..255)
    hist_counts, _ = np.histogram(data, bins=np.arange(257))  # 256 bins

    # 3) Bit-balance per bit position
    bit_counts = [(data >> b) & 1 for b in range(8)]
    ones_ratio = [bc.mean() for bc in bit_counts]  # fraction of ones in each bit

    # 4) Autocorrelation (lags 1..100)
    acf = compute_autocorrelation(data, max_lag=100)

    # ---------------- Visualization ----------------
    # Create 4 separate figures, as requested (no subplots).
    # Also, do not set any explicit colors or styles.

    # TV static
    plt.figure(figsize=(6, 6))
    plt.imshow(img, cmap="gray", vmin=0, vmax=255)  # grayscale image to "see" the noise
    plt.title(f"TV Static from {source_label}\n({img.shape[0]}x{img.shape[1]} pixels)")
    plt.axis("off")
    plt.tight_layout()

    # Histogram
    plt.figure(figsize=(7, 4))
    plt.bar(np.arange(256), hist_counts, width=1.0)
    plt.title(f"Byte Histogram (0–255) — {source_label}")
    plt.xlabel("Byte value")
    plt.ylabel("Count")
    plt.tight_layout()

    # Bit balance
    plt.figure(figsize=(6, 4))
    plt.bar(np.arange(8), ones_ratio)
    plt.title(f"Bit Balance (fraction of 1s) — {source_label}")
    plt.xlabel("Bit position (0 = LSB)")
    plt.ylabel("Fraction of ones")
    plt.ylim(0, 1)
    plt.tight_layout()

    # Autocorrelation
    plt.figure(figsize=(7, 4))
    lags = np.arange(1, len(acf) + 1)
    plt.stem(lags, acf, use_line_collection=True)
    plt.title(f"Autocorrelation (lags 1–{len(acf)}) — {source_label}")
    plt.xlabel("Lag")
    plt.ylabel("ACF")
    plt.tight_layout()

    plt.show()

if __name__ == "__main__":
    main()
