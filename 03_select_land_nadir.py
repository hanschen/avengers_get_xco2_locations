#!/usr/bin/env -S uv run --script
"""Select only XCO2 soundings over land (nadir)."""

import xarray as xr


ds = xr.open_dataset("output/cloud_filtered.nc")
ds_wrf = xr.open_dataset("input/wrfinput_d01")
ds_out = ds.copy(deep=True)

land = xr.where(ds_wrf["XLAND"][0] == 1, 1, 0)

obs_area_frac = ds["obs_area_frac"]
ds_out["obs_area_frac"] = obs_area_frac * land

ds_out.to_netcdf("output/land_nadir.nc")

ds.close()
ds_wrf.close()
ds_out.close()
