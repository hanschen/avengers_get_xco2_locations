#!/usr/bin/env -S uv run --script
"""Read in observation coverage, concatenate, and convert to 0 or 1.

This is done because the current observation coverage does not account for
variable grid cell area in WRF, which erronously results in some areas being
less than 1.
"""

from datetime import timedelta
from pathlib import Path

import xarray as xr

import utils
from config import config

DATA_DIR = Path("/data0/data/avengers/wrf_co2m")
INPUT_FILE = "{date:%Y%m%d}_wrf_obs_coverage.nc"


config.output_dir.mkdir(exist_ok=True, parents=True)

vars_list = []

for date in utils.daterange(
    config.start_date, config.end_date, timedelta(days=1)
):
    input_file = INPUT_FILE.format(date=date)

    ds = xr.open_dataset(DATA_DIR / input_file)
    obs_area_frac = ds["obs_area_frac"]

    vars_list.append(obs_area_frac)
    ds.close()

combined = xr.concat(vars_list, dim="time")

# Exclude soundings in domain margins
margin = config.margin
if margin > 0:
    mask = xr.zeros_like(combined, dtype=bool)
    mask[:, margin:-margin, margin:-margin] = True
    combined = combined.where(mask, 0)

combined_ds = combined.to_dataset(name="obs_area_frac")
combined_ds.to_netcdf(config.output_dir / "concat_area_frac.nc")

combined_ds.close()
