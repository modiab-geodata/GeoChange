def verifier_crs(gdf):
    """Vérifie que la couche possède un CRS."""

    if gdf.crs is None:
        print("La couche ne contient pas de CRS.")
        return False

    print(f"CRS : {gdf.crs}")
    return True


def verifier_geometrie_active(gdf):
    """Vérifie qu'une géométrie active est définie."""

    if gdf.active_geometry_name is None:
        print("La couche ne possède pas de géométrie active.")
        return False

    print(f"Géométrie active : {gdf.active_geometry_name}")
    return True


def verifier_geometries_invalides(gdf):
    """Vérifie que toutes les géométries sont valides."""

    geometries_valides = gdf.geometry.is_valid

    if geometries_valides.all():
        print("Toutes les géométries sont valides.")
        return True

    nombre_invalides = (~geometries_valides).sum()

    print(
        f"La couche contient "
        f"{nombre_invalides} géométrie(s) invalide(s)."
    )

    return False


def verifier_geometries_vides(gdf):
    """Vérifie que la couche ne contient pas de géométrie vide."""

    geometries_vides = gdf.geometry.is_empty

    if geometries_vides.any():
        nombre_vides = geometries_vides.sum()

        print(
            f"La couche contient "
            f"{nombre_vides} géométrie(s) vide(s)."
        )

        return False

    print("La couche ne contient aucune géométrie vide.")
    return True


def verifier_colonnes(gdf):
    """Vérifie que la couche contient au moins une colonne."""

    nombre_colonnes = len(gdf.columns)

    if nombre_colonnes == 0:
        print("La couche ne contient aucune colonne.")
        return False

    print(f"Nombre de colonnes : {nombre_colonnes}")
    print(f"   Colonnes : {list(gdf.columns)}")

    return True


def verifier_cle_primaire(gdf, colonne):
    """Vérifie qu'une colonne peut servir de clé primaire."""

    if colonne not in gdf.columns:
        print(f"La colonne '{colonne}' n'existe pas.")
        return False

    if gdf[colonne].isna().any():
        print(
            f"La clé primaire '{colonne}' "
            f"contient des valeurs nulles."
        )
        return False

    if not gdf[colonne].is_unique:
        print(
            f"La clé primaire '{colonne}' "
            f"contient des doublons."
        )
        return False

    print(f"La colonne '{colonne}' peut servir de clé primaire.")
    return True

