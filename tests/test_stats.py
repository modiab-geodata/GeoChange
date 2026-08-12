from pathlib import Path

from geochange.loader import load_file
from geochange.stats import (
    statistiques_entites,
    statistiques_colonnes_ajoutees,
    statistiques_colonnes_supprimees,
    statistiques_modifications,
    statistiques_entites_ajoutes,
    statistiques_entites_supprimes
)
path_old = Path("data/input/iris_old.geojson")
path_new = Path("data/input/iris.geojson")

gdf_old = load_file(path_old)
gdf_new = load_file(path_new)

resultat4 = statistiques_modifications(gdf_old, gdf_new, "code_iris")
resultat5 = statistiques_entites_ajoutes(gdf_old, gdf_new, "code_iris")
resultat6 = statistiques_entites_supprimes(gdf_old, gdf_new, "code_iris")


fonctions = [
    statistiques_entites,
    statistiques_colonnes_ajoutees,
    statistiques_colonnes_supprimees,
]

for fonction in fonctions:
    resultat = fonction(gdf_old, gdf_new)
    print(f"{fonction.__name__} : {resultat}")

print(resultat4)
print(resultat5)
print(resultat6)
