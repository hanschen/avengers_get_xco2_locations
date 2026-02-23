#!/usr/bin/env python
"""Apply cloud mask to observation coverage."""

from pathlib import Path

import xarray as xr
import pandas as pd

CLDFRAC_DIR = Path("/data0/output/concatenate_output")

CLFRAC_METHOD = "expran"

OUTPUT_DIR = Path("output")

DEBUG = True


ds = xr.open_dataset("output/concat_area_frac.nc")

ds_cldfrac = xr.open_dataset(CLDFRAC_DIR / "cldfrac.nc")
ref_date = pd.Timestamp(ds_cldfrac["time"].values[0])

ds_out = ds.copy(deep=True)

for t, time in enumerate(ds.time.values):
    dt = pd.Timestamp(time)
    dt_cldfrac = dt.replace(year=ref_date.year)  # type: ignore

    try:
        cldfrac = ds_cldfrac[f"CLDFRAC_{CLFRAC_METHOD}"].sel(time=dt_cldfrac)
    except KeyError:
        if DEBUG:
            print(f"no cloud fraction for date, skipping: {dt_cldfrac}")
        ds_out["obs_area_frac"][t] = 0
        continue

    cld_obs_area_frac = ds["obs_area_frac"].sel(time=dt) * cldfrac
    ds_out["obs_area_frac"][t] = cld_obs_area_frac

OUTPUT_DIR.mkdir(exist_ok=True, parents=True)
ds_out.to_netcdf(OUTPUT_DIR / "cloud_filtered.nc")

ds.close()
ds_cldfrac.close()
ds_out.close()
