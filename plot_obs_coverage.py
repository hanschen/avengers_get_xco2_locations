#!/usr/bin/env -S uv run --script
"""Plot observation coverage for whole time period"""

import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt

import xarray as xr

THRESHOLD = 1

# ds = xr.open_dataset("output/concat_area_frac.nc")
# ds = xr.open_dataset("output/cloud_filtered.nc")
ds = xr.open_dataset("output/land_nadir.nc")
# ds = xr.open_dataset("output/thinned.nc")

obs_area_frac = ds["obs_area_frac"]
obs_num = xr.where(obs_area_frac >= THRESHOLD, 1, 0).sum(dim="time")
ds.close()

ds_wrf = xr.open_dataset("input/wrfinput_d01")

lats = ds_wrf["XLAT"].isel(Time=0)
lons = ds_wrf["XLONG"].isel(Time=0)

truelat1 = ds_wrf.attrs["TRUELAT1"]
truelat2 = ds_wrf.attrs["TRUELAT2"]
stand_lon = ds_wrf.attrs["STAND_LON"]
cen_lat = ds_wrf.attrs["CEN_LAT"]
cen_lon = ds_wrf.attrs["CEN_LON"]

proj = ccrs.LambertConformal(
    central_longitude=stand_lon,
    central_latitude=cen_lat,
    standard_parallels=(truelat1, truelat2),
)

lon_min = lons.min()
lon_max = lons.max()
lat_min = lats.min()
lat_max = lats.max()


fig, ax = plt.subplots(figsize=(12, 9), subplot_kw={"projection": proj})

# Add features
ax.add_feature(cfeature.COASTLINE.with_scale("50m"))
ax.add_feature(cfeature.BORDERS.with_scale("50m"))

cf = ax.pcolormesh(
    lons,
    lats,
    obs_num,
    cmap="viridis",
    transform=ccrs.PlateCarree(),
)

fig.colorbar(cf)

ax.set_extent([lon_min, lon_max, lat_min, lat_max], crs=ccrs.PlateCarree())

plt.show()
