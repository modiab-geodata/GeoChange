from pathlib import Path
import geopandas as gpd
from pyogrio.errors import DataSourceError

FORMATS_SUPPORTES = [
    ".geojson",
    ".shp",
    ".gpkg"
]


def load_file(path):

    extension = path.suffix.lower()

    if extension not in FORMATS_SUPPORTES:
        print(f"Format non supporté : {extension}")
        return None

    try:
        gdf = gpd.read_file(path)

    except DataSourceError:
        print(f"Impossible de lire le fichier : {path}")
        return None

    return gdf