
from pathlib import Path
from geochange.loader import load_file

path = Path("data/input/iris_old.geojson")
gdf = load_file(path)


print(len(gdf))