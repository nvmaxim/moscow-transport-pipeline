import zipfile
from pathlib import Path

import pandas as pd


def extract_gtfs(zip_path: str, output_dir: str = "data/gtfs") -> None:
    zip_path = Path(zip_path)
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(zip_path) as z:
        z.extractall(out)

    stops = pd.read_csv(out / "stops.txt")
    print(stops.head())


if __name__ == "__main__":
    extract_gtfs("data/moscow_gtfs.zip")
