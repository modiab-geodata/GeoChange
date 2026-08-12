from pathlib import Path
import geopandas as gpd
from pyogrio.errors import DataSourceError

# Formats supportés
FORMATS_SUPPORTES = [
    ".geojson",
    ".shp",
    ".gpkg"
]


def load_file(path):

    print("")
    print("============================")
    print(f"Lecture : {path.name}")
    print("============================")

    extension = path.suffix.lower()

    # Vérification du format supporté
    if extension not in FORMATS_SUPPORTES:
        print(f"Format non supporté : {extension}")
        return None

    try:
        gdf = gpd.read_file(path)

    except DataSourceError:
        print(f"Impossible de lire le fichier : {path}")
        return None

    return gdf
