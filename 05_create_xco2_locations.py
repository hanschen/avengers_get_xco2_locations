#!/usr/bin/env -S uv run --script
"""Create files with XCO2 locations."""

import numpy as np
import pandas as pd
import xarray as xr

from config import config

REF_YEAR = 2021

ds = xr.load_dataset(config.output_dir / f"{config.use_obs}.nc")

ds_wrf = xr.load_dataset("input/wrfinput_d01")
lats = ds_wrf["XLAT"].isel(Time=0)
lons = ds_wrf["XLONG"].isel(Time=0)
ds_wrf.close()

output_dir = config.output_dir / "xco2"
output_dir.mkdir(exist_ok=True, parents=True)

for t, time in enumerate(ds.time.values):
    obs = ds["obs_area_frac"][t]
    if not np.any(obs):
        continue

    dt = pd.Timestamp(time)
    dt = dt.replace(year=REF_YEAR)  # type: ignore
    out_file = output_dir / f"{dt:sounding_%Y-%m-%d_%H:%M:%S}.dat"

    j_indices, i_indices = np.where(obs >= config.minimum_coverage)
    with open(out_file, "w") as f:
        f.write("# name,lat,lon\n")

        for j, i in zip(j_indices, i_indices, strict=True):
            name = f"sounding_{j:03d}_{i:03d}"
            lat = lats[j, i].values
            lon = lons[j, i].values

            f.write(f"{name},{lat:.5f},{lon:.5f}\n")
