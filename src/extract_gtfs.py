from pathlib import Path
import zipfile
import pandas as pd


def extract_gtfs_zip(zip_path: str, output_dir: str = "data/gtfs") -> None:
    zip_path = Path(zip_path)
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(zip_path) as z:
        z.extractall(out)


def load_gtfs_frames(input_dir: str = "data/gtfs") -> dict[str, pd.DataFrame]:
    input_path = Path(input_dir)
    tables = {}

    for name in ["stops", "routes", "trips", "stop_times", "calendar"]:
        path = input_path / f"{name}.txt"
        if path.exists():
            tables[name] = pd.read_csv(path)

    return tables


if __name__ == "__main__":
    extract_gtfs_zip("data/improved-gtfs-moscow-official.zip")
    tables = load_gtfs_frames("data/gtfs")
    print(tables["stops"].head())
