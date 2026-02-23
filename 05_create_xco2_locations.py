#!/usr/bin/env -S uv run --script
"""Create files with XCO2 locations."""

from pathlib import Path

import numpy as np
import pandas as pd
import xarray as xr

REF_YEAR = 2021
OUTPUT_DIR = Path("output/xco2")

ds = xr.load_dataset("output/thinned.nc")

ds_wrf = xr.load_dataset("input/wrfinput_d01")
lats = ds_wrf["XLAT"].isel(Time=0)
lons = ds_wrf["XLONG"].isel(Time=0)
ds_wrf.close()

OUTPUT_DIR.mkdir(exist_ok=True, parents=True)

for t, time in enumerate(ds.time.values):
    obs = ds["obs_area_frac"][t]
    if not np.any(obs):
        continue

    dt = pd.Timestamp(time)
    dt = dt.replace(year=REF_YEAR)  # type: ignore
    out_file = OUTPUT_DIR / f"{dt:sounding_%Y-%m-%d_%H:%M:%S}.dat"

    j_indices, i_indices = np.where(obs == 1)
    with open(out_file, "w") as f:
        f.write("# name,lat,lon\n")

        for j, i in zip(j_indices, i_indices, strict=True):
            name = f"sounding_{j:03d}_{i:03d}"
            lat = lats[j, i].values
            lon = lons[j, i].values

            f.write(f"{name},{lat:.5f},{lon:.5f}\n")
