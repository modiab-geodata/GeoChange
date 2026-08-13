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


def main(path_old, path_new, colonne_id=None):

    print("==============================")
    print("Démarrage GeoChange")
    print("==============================")

    # ==========================================
    # 1. Chargement des couches
    # ==========================================

    print("\n===== CHARGEMENT DES COUCHES =====")

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

    # ==========================================
    # 3. Validation de la clé d'identification
    # ==========================================

    print("\n===== IDENTIFICATION DES ENTITÉS =====")

    cle_valide = False

    if colonne_id is None:
        print(
            "Aucune clé d'identification n'a été définie."
        )
        print(
            "Les analyses nécessitant une correspondance "
            "entre entités seront désactivées."
        )

    else:

        print(
            f"Clé d'identification sélectionnée : "
            f"'{colonne_id}'"
        )

        cle_old_valide = verifier_cle_primaire(
            gdf_old,
            colonne_id
        )

        cle_new_valide = verifier_cle_primaire(
            gdf_new,
            colonne_id
        )

        if cle_old_valide and cle_new_valide:

            cle_valide = True

            print(
                f"La clé '{colonne_id}' est valide "
                "pour les deux couches."
            )

        else:

            print(
                f"La clé '{colonne_id}' ne peut pas être utilisée "
                "pour identifier les entités."
            )

            print(
                "Les analyses nécessitant une correspondance "
                "entre entités seront désactivées."
            )

    # ==========================================
    # 4. Comparaison structurelle
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

    # ==========================================
    # 5. Comparaisons par entité
    # ==========================================

    if cle_valide:

        print("\n===== COMPARAISON PAR ENTITÉ =====")

        entites_ajoutees_resultat = entites_ajoutees(
            gdf_old,
            gdf_new,
            colonne_id
        )

        entites_supprimees_resultat = entites_supprimees(
            gdf_old,
            gdf_new,
            colonne_id
        )

        modifications_resultat = modifications_valeurs(
            gdf_old,
            gdf_new,
            colonne_id
        )

        geometries_modifiees_resultat = geometries_modifiees(
            gdf_old,
            gdf_new,
            colonne_id
        )

    else:

        print(
            "\n===== COMPARAISON PAR ENTITÉ ====="
        )

        print(
            "Analyses par entité ignorées : "
            "aucune clé d'identification valide."
        )

        entites_ajoutees_resultat = None
        entites_supprimees_resultat = None
        modifications_resultat = None
        geometries_modifiees_resultat = None

    # ==========================================
    # 6. Résultats des comparaisons
    # ==========================================

    print("\n===== RÉSULTATS DES COMPARAISONS =====")

    print(
        "Clé d'identification :",
        colonne_id if cle_valide else "Aucune"
    )

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

    if cle_valide:

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

    else:

        print(
            "Entités ajoutées : non calculées"
        )

        print(
            "Entités supprimées : non calculées"
        )

        print(
            "Modifications : non calculées"
        )

        print(
            "Géométries modifiées : non calculées"
        )

    # ==========================================
    # 7. Production des statistiques générales
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

    statistiques_entites_resultat = (
        statistiques_entites(
            nombre_entites_resultat
        )
    )

    # ==========================================
    # 8. Statistiques dépendantes de la clé
    # ==========================================

    if cle_valide:

        statistiques_modifications_resultat = (
            statistiques_modifications(
                modifications_resultat
            )
        )

        statistiques_entites_ajoutes_resultat = (
            statistiques_entites_ajoutes(
                entites_ajoutees_resultat
            )
        )

        statistiques_entites_supprimes_resultat = (
            statistiques_entites_supprimes(
                entites_supprimees_resultat
            )
        )

        statistiques_geometries_modifiees_resultat = (
            statistiques_geometries_modifiees(
                geometries_modifiees_resultat
            )
        )

    else:

        statistiques_modifications_resultat = {
            "nombre_modifications": None
        }

        statistiques_entites_ajoutes_resultat = {
            "nombre_entites_ajoutes": None
        }

        statistiques_entites_supprimes_resultat = {
            "nombre_entites_supprimes": None
        }

        statistiques_geometries_modifiees_resultat = {
            "nombre_geometries_modifiees": None
        }

    # ==========================================
    # 9. Construction du résultat complet
    # ==========================================

    resultats = {

        "configuration": {

            "colonne_id": (
                colonne_id
                if cle_valide
                else None
            ),

            "analyses_par_entite": cle_valide
        },

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

            "entites_ajoutees": (
                list(entites_ajoutees_resultat)
                if entites_ajoutees_resultat is not None
                else None
            ),

            "entites_supprimees": (
                list(entites_supprimees_resultat)
                if entites_supprimees_resultat is not None
                else None
            ),

            "modifications": (
                modifications_resultat
                if modifications_resultat is not None
                else None
            ),

            "geometries_modifiees": (
                geometries_modifiees_resultat
                if geometries_modifiees_resultat is not None
                else None
            )
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
    # 10. Affichage des statistiques
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
    # 11. Export des rapports
    # ==========================================

    print("\n===== EXPORT DES RAPPORTS =====")

    exporter_json(
        resultats,
        "reports/rapport.json"
    )

    exporter_pdf(
        resultats,
        "reports/rapport.pdf"
    )

    # ==========================================
    # 12. Résultat complet
    # ==========================================

    print("\n===== RÉSULTATS COMPLETS =====")

    print(resultats)

    print("\n==============================")
    print("GeoChange terminé")
    print("==============================")

    return resultats


# ==============================================
# Exécution directe du programme
# ==============================================

if __name__ == "__main__":

    path_old = Path(
        "data/input/iris_old.geojson"
    )

    path_new = Path(
        "data/input/iris.geojson"
    )

    # Pour une exécution sans clé :
    #
    # resultats = main(
    #     path_old,
    #     path_new
    # )

    # Pour une exécution avec une clé :
    colonne_id = "code_iris"

    resultats = main(
        path_old,
        path_new,
        colonne_id
    )