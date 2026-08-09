from pathlib import Path
from geochange.loader import load_file
import geopandas as gpd
from geochange.validator import (
    verifier_crs,
    verifier_geometrie_active,
    verifier_geometries_invalides,
    verifier_geometries_vides,
    verifier_colonnes,
    verifier_cle_primaire,
)

fonctions = [
    verifier_crs,
    verifier_geometrie_active,
    verifier_geometries_invalides,
    verifier_geometries_vides,
    verifier_colonnes,
]


path = Path("data/input/iris.geojson")
gdf = load_file(path)

for fonction in fonctions:
    resultat = fonction(gdf)
    print(f"{fonction.__name__} : {resultat}")
resultat_cle_primaine = verifier_cle_primaire(gdf, "dep")
print(resultat_cle_primaine)