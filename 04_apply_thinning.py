#!/usr/bin/env -S uv run --script
"""Apply observation thinning to observation coverage."""

import xarray as xr

THINNING = 4

ds = xr.open_dataset("output/land_nadir.nc")

mask = xr.zeros_like(ds["obs_area_frac"], dtype=bool)
mask[:, ::THINNING, ::THINNING] = True

ds_thinned = ds.where(mask, 0)

ds_thinned.to_netcdf("output/thinned.nc")
