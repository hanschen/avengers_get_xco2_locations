#!/usr/bin/env python
"""Apply cloud mask to observation coverage."""

import pandas as pd
import xarray as xr

from config import config

ds = xr.open_dataset(config.output_dir / "concat_area_frac.nc")

ds_cldfrac = xr.open_dataset(config.cldfrac_dir / "cldfrac.nc")
ref_date = pd.Timestamp(ds_cldfrac["time"].values[0])

ds_out = ds.copy(deep=True)

for t, time in enumerate(ds.time.values):
    dt = pd.Timestamp(time)
    dt_cldfrac = dt.replace(year=ref_date.year)  # type: ignore

    cldfrac_method = config.cldfrac_method
    try:
        cldfrac = ds_cldfrac[f"CLDFRAC_{cldfrac_method}"].sel(time=dt_cldfrac)
    except KeyError:
        if config.debug:
            print(f"no cloud fraction for date, skipping: {dt_cldfrac}")
        ds_out["obs_area_frac"][t] = 0
        continue

    cld_obs_area_frac = ds["obs_area_frac"].sel(time=dt) * (1 - cldfrac)
    ds_out["obs_area_frac"][t] = cld_obs_area_frac

ds_out.to_netcdf(config.output_dir / "cloud_filtered.nc")

ds.close()
ds_cldfrac.close()
ds_out.close()
