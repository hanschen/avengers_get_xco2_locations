#!/usr/bin/env -S uv run --script
"""Read in observation coverage, concatenate, and convert to 0 or 1.

This is done because the current observation coverage does not account for
variable grid cell area in WRF, which erronously results in some areas being
less than 1.
"""

from datetime import datetime, timedelta
from pathlib import Path

import xarray as xr

import utils

THRESHOLD = 0.8
MARGIN = 0  # number of grid points around domain to exclude

START_DATE = datetime(2025, 6, 17)
END_DATE = datetime(2025, 8, 1)

DATA_DIR = Path("/data0/data/avengers/wrf_co2m")
INPUT_FILE = "{date:%Y%m%d}_wrf_obs_coverage.nc"

OUTPUT_DIR = Path("output")


OUTPUT_DIR.mkdir(exist_ok=True, parents=True)

vars_list = []

for date in utils.daterange(START_DATE, END_DATE, timedelta(days=1)):
    input_file = INPUT_FILE.format(date=date)

    ds = xr.open_dataset(DATA_DIR / input_file)
    obs_area_frac = ds["obs_area_frac"]
    obs_area_frac_binary = xr.where(obs_area_frac >= THRESHOLD, 1, 0)

    vars_list.append(obs_area_frac_binary)
    ds.close()

combined = xr.concat(vars_list, dim="time")

# Exclude soundings in domain margins
if MARGIN > 0:
    mask = xr.zeros_like(combined, dtype=bool)
    mask[:, MARGIN:-MARGIN, MARGIN:-MARGIN] = True
    combined = combined.where(mask, 0)

combined_ds = combined.to_dataset(name="obs_area_frac")
combined_ds.to_netcdf(OUTPUT_DIR / "concat_area_frac.nc")

combined_ds.close()
