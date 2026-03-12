import zipfile
import pandas as pd

# После скачивания moscow_gtfs.zip
with zipfile.ZipFile("moscow_gtfs.zip", "r") as z:
    z.extractall("moscow_gtfs/")

stops = pd.read_csv("moscow_gtfs/stops.txt")
stop_times = pd.read_csv("moscow_gtfs/stop_times.txt")
routes = pd.read_csv("moscow_gtfs/routes.txt")

print(stops.head())
