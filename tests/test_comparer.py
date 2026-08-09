from pathlib import Path
from geochange.loader import load_file
from geochange.comparer import (
    colonnes_ajoutees, 
    colonnes_supprimees, 
    types_donnees_modifies, 
    crs_different,
    nombre_entites
    )

path1 = Path("data/input/iris.geojson")

path2 = Path("data/input/iris.geojson")

gdf_old = load_file(path1)
gdf_new = load_file(path1)

fonctions = [
    colonnes_ajoutees, 
    colonnes_supprimees, 
    types_donnees_modifies, 
    crs_different,
    nombre_entites
]

for fonction in fonctions:
    resultat = fonction(gdf_old, gdf_new)
    print(f"{fonction.__name__} : {resultat}")


