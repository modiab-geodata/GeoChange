from pathlib import Path

from geochange.loader import load_file

from geochange.exporter import (
    exporter_json,
    exporter_pdf
)

from geochange.validator import (
    verifier_crs,
    verifier_geometrie_active,
    verifier_geometries_invalides,
    verifier_geometries_vides,
    verifier_colonnes,
    verifier_cle_primaire
)

from geochange.comparer import (
    colonnes_ajoutees,
    colonnes_supprimees,
    types_donnees_modifies,
    crs_different,
    nombre_entites,
    entites_ajoutees,
    entites_supprimees
)

from geochange.attributes import modifications_valeurs
from geochange.geometry import geometries_modifiees

from geochange.stats import (
    statistiques_colonnes_ajoutees,
    statistiques_colonnes_supprimees,
    statistiques_entites,
    statistiques_modifications,
    statistiques_entites_ajoutes,
    statistiques_entites_supprimes,
    statistiques_geometries_modifiees
)


def main(path_old, path_new):

    print("==============================")
    print("Démarrage GeoChange")
    print("==============================")

    # ==========================================
    # 1. Chargement des couches
    # ==========================================

    gdf_old = load_file(path_old)
    gdf_new = load_file(path_new)

    # ==========================================
    # 2. Validation des couches
    # ==========================================

    print("\n===== VALIDATION DES COUCHES =====")

    verifier_crs(gdf_old)
    verifier_crs(gdf_new)

    verifier_geometrie_active(gdf_old)
    verifier_geometrie_active(gdf_new)

    verifier_geometries_invalides(gdf_old)
    verifier_geometries_invalides(gdf_new)

    verifier_geometries_vides(gdf_old)
    verifier_geometries_vides(gdf_new)

    verifier_colonnes(gdf_old)
    verifier_colonnes(gdf_new)

    verifier_cle_primaire(gdf_old, "code_iris")
    verifier_cle_primaire(gdf_new, "code_iris")

    # ==========================================
    # 3. Comparaison des couches
    # ==========================================

    print("\n===== COMPARAISON DES COUCHES =====")

    colonnes_ajoutees_resultat = colonnes_ajoutees(
        gdf_old,
        gdf_new
    )

    colonnes_supprimees_resultat = colonnes_supprimees(
        gdf_old,
        gdf_new
    )

    types_modifies_resultat = types_donnees_modifies(
        gdf_old,
        gdf_new
    )

    crs_different_resultat = crs_different(
        gdf_old,
        gdf_new
    )

    nombre_entites_resultat = nombre_entites(
        gdf_old,
        gdf_new
    )

    entites_ajoutees_resultat = entites_ajoutees(
        gdf_old,
        gdf_new,
        "code_iris"
    )

    entites_supprimees_resultat = entites_supprimees(
        gdf_old,
        gdf_new,
        "code_iris"
    )

    modifications_resultat = modifications_valeurs(
        gdf_old,
        gdf_new,
        "code_iris"
    )

    geometries_modifiees_resultat = geometries_modifiees(
        gdf_old,
        gdf_new,
        "code_iris"
    )

    # ==========================================
    # 4. Affichage des résultats de comparaison
    # ==========================================

    print("\n===== RÉSULTATS DES COMPARAISONS =====")

    print(
        "Colonnes ajoutées :",
        list(colonnes_ajoutees_resultat)
    )

    print(
        "Colonnes supprimées :",
        list(colonnes_supprimees_resultat)
    )

    print(
        "Types modifiés :",
        types_modifies_resultat
    )

    print(
        "CRS :",
        crs_different_resultat
    )

    print(
        "Nombre d'entités :",
        nombre_entites_resultat
    )

    print(
        "Entités ajoutées :",
        entites_ajoutees_resultat
    )

    print(
        "Entités supprimées :",
        entites_supprimees_resultat
    )

    print(
        "Modifications :",
        modifications_resultat
    )

    print(
        "Géométries modifiées :",
        geometries_modifiees_resultat
    )

    # ==========================================
    # 5. Production des statistiques
    # ==========================================

    statistiques_colonnes_ajoutees_resultat = (
        statistiques_colonnes_ajoutees(
            colonnes_ajoutees_resultat
        )
    )

    statistiques_colonnes_supprimees_resultat = (
        statistiques_colonnes_supprimees(
            colonnes_supprimees_resultat
        )
    )

    statistiques_entites_resultat = statistiques_entites(
        nombre_entites_resultat
    )

    statistiques_modifications_resultat = statistiques_modifications(
        modifications_resultat
    )

    statistiques_entites_ajoutes_resultat = statistiques_entites_ajoutes(
        entites_ajoutees_resultat
    )

    statistiques_entites_supprimes_resultat = statistiques_entites_supprimes(
        entites_supprimees_resultat
    )

    statistiques_geometries_modifiees_resultat = (
        statistiques_geometries_modifiees(
            geometries_modifiees_resultat
        )
    )

    # ==========================================
    # 6. Construction du résultat complet
    # ==========================================

    resultats = {
        "comparaisons": {
            "colonnes_ajoutees": list(
                colonnes_ajoutees_resultat
            ),

            "colonnes_supprimees": list(
                colonnes_supprimees_resultat
            ),

            "types_modifies": types_modifies_resultat,

            "crs": crs_different_resultat,

            "nombre_entites": nombre_entites_resultat,

            "entites_ajoutees": list(
                entites_ajoutees_resultat
            ),

            "entites_supprimees": list(
                entites_supprimees_resultat
            ),

            "modifications": modifications_resultat,

            "geometries_modifiees": geometries_modifiees_resultat
        },

        "statistiques": {
            **statistiques_colonnes_ajoutees_resultat,
            **statistiques_colonnes_supprimees_resultat,
            **statistiques_entites_resultat,
            **statistiques_entites_ajoutes_resultat,
            **statistiques_entites_supprimes_resultat,
            **statistiques_modifications_resultat,
            **statistiques_geometries_modifiees_resultat
        }
    }

    # ==========================================
    # 7. Affichage des statistiques
    # ==========================================

    print("\n===== RÉSULTATS STATISTIQUES =====")

    print(
        "Colonnes ajoutées :",
        statistiques_colonnes_ajoutees_resultat
    )

    print(
        "Colonnes supprimées :",
        statistiques_colonnes_supprimees_resultat
    )

    print(
        "Entités :",
        statistiques_entites_resultat
    )

    print(
        "Entités ajoutées :",
        statistiques_entites_ajoutes_resultat
    )

    print(
        "Entités supprimées :",
        statistiques_entites_supprimes_resultat
    )

    print(
        "Modifications :",
        statistiques_modifications_resultat
    )

    print(
        "Géométries modifiées :",
        statistiques_geometries_modifiees_resultat
    )

    # ==========================================
    # 8. Export JSON
    # ==========================================

    exporter_json(
        resultats,
        "reports/rapport.json"
    )

    exporter_pdf(
        resultats,
        "reports/rapport.pdf"
    )

    # ==========================================a
    # 9. Résultat complet
    # ==========================================

    print("\n===== RÉSULTATS COMPLETS =====")
    print(resultats)

    return resultats


if __name__ == "__main__":

    path_old = Path("data/input/iris_old.geojson")
    path_new = Path("data/input/iris.geojson")

    resultats = main(
        path_old,
        path_new
    )