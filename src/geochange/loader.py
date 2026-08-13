from pathlib import Path

import geopandas as gpd
import pyogrio
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

    # ------------------------------------------------------------
    # Diagnostic : compare les champs réellement présents dans le
    # fichier source (lus directement via les métadonnées GDAL/pyogrio,
    # indépendamment du GeoDataFrame construit) aux champs effectivement
    # chargés. Utile en particulier pour les Shapefile, où un champ
    # peut être ignoré selon l'encodage (.cpg) ou une collision de noms
    # après troncature à 10 caractères (limite du format DBF).
    # ------------------------------------------------------------

    try:
        info = pyogrio.read_info(str(path))
        champs_source = list(info.get("fields", []))
        champs_lus = [
            colonne for colonne in gdf.columns
            if colonne != gdf.geometry.name
        ]

        champs_manquants = [
            champ for champ in champs_source
            if champ not in champs_lus
        ]

        print(f"Champs source ({len(champs_source)}) : {champs_source}")
        print(f"Champs lus     ({len(champs_lus)}) : {champs_lus}")

        if champs_manquants:
            print(
                f"⚠️ {len(champs_manquants)} champ(s) du fichier source "
                f"absent(s) après lecture : {champs_manquants}"
            )

            if extension == ".shp":
                print(
                    "→ Cause probable pour un Shapefile : collision de "
                    "noms après troncature DBF à 10 caractères, ou "
                    "encodage (.cpg) incorrect/absent empêchant le "
                    "décodage du nom de champ."
                )

    except Exception as erreur_diagnostic:
        print(f"Diagnostic des champs impossible : {erreur_diagnostic}")

    return gdf