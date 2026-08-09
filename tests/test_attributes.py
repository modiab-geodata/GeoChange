from pathlib import Path

from geochange.loader import load_file
from geochange.attributes import modifications_valeurs


path_old = Path("data/input/iris_old.geojson")
path_new = Path("data/input/iris.geojson")

gdf_old = load_file(path_old)
gdf_new = load_file(path_new)

# Modification pour tester la fonction

gdf_new.loc[gdf_old.index[0], "nom_iris"] = "TEST MODIFICATION"


resultat = modifications_valeurs(
    gdf_old,
    gdf_new,
    "code_iris"
)

print(resultat)