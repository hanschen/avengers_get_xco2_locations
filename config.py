from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

EXP = "winter"


@dataclass
class Config:
    name: str
    start_date: datetime
    end_date: datetime
    cldfrac_dir: Path

    margin: int = 5  # number of grid points around domain to exclude
    cldfrac_method: str = "expran"
    thinning: int = 4

    minimum_coverage = 0.9
    use_obs: str = "land_nadir"

    debug: bool = True
    output_dir_base: Path = Path("output")

    @property
    def output_dir(self):
        return self.output_dir_base / self.name


CLDFRAC_DIR_BASE = Path("/data0/output/concatenate_output")

CONFIGS = {
    "summer": Config(
        name="summer",
        start_date=datetime(2025, 6, 17),
        end_date=datetime(2025, 8, 1),
        cldfrac_dir=CLDFRAC_DIR_BASE / "wp2_summer",
    ),
    "winter": Config(
        name="winter",
        start_date=datetime(2025, 1, 18),
        end_date=datetime(2025, 3, 1),
        cldfrac_dir=CLDFRAC_DIR_BASE / "wp2_winter",
    ),
}

config = CONFIGS[EXP]
