#!/usr/bin/env -S uv run --script
"""Apply observation thinning to observation coverage."""

import xarray as xr

from config import config

ds = xr.open_dataset(config.output_dir / "land_nadir.nc")

mask = xr.zeros_like(ds["obs_area_frac"], dtype=bool)
thinning = config.thinning
mask[:, ::thinning, ::thinning] = True

ds_thinned = ds.where(mask, 0)

ds_thinned.to_netcdf(config.output_dir / "thinned.nc")

ds.close()
ds_thinned.close()
