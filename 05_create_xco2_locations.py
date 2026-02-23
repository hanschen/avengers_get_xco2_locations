#!/usr/bin/env -S uv run --script
"""Create files with XCO2 locations."""

import numpy as np
import pandas as pd
import xarray as xr


ds = xr.load_dataset("output/thinned.nc")

ds_wrf = xr.load_dataset("input/wrfinput_d01")
lats = ds_wrf["XLAT"].isel(Time=0)
lons = ds_wrf["XLONG"].isel(Time=0)
ds_wrf.close()

for t, time in enumerate(ds.time.values):
    obs = ds["obs_area_frac"][t]
    if not np.any(obs):
        continue

    dt = pd.Timestamp(time)
    out_file = f"output/xco2/{dt:sounding_%Y-%m-%d_%H:%M:%S}.dat"

    j_indices, i_indices = np.where(obs == 1)
    with open(out_file, "w") as f:
        f.write("# name,lat,lon\n")

        for j, i in zip(j_indices, i_indices, strict=True):
            name = f"sounding_{j:03d}_{i:03d}"
            lat = lats[j, i].values
            lon = lons[j, i].values

            f.write(f"{name},{lat:.5f},{lon:.5f}\n")
