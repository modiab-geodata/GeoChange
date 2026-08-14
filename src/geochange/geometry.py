def _geometries_sont_differentes(geom_old, geom_new):
 
    try:
        old_est_vide = (
            geom_old is None
            or (isinstance(geom_old, float) and geom_old != geom_old)
        )
        new_est_vide = (
            geom_new is None
            or (isinstance(geom_new, float) and geom_new != geom_new)
        )

        if old_est_vide and new_est_vide:
            return False

        if old_est_vide or new_est_vide:
            return True

        return not geom_old.equals(geom_new)

    except Exception:

        try:
            return geom_old.wkt != geom_new.wkt
        except Exception:
            try:
                return str(geom_old) != str(geom_new)
            except Exception:
                return True


def geometries_modifiees(gdf_old, gdf_new, colonne_id):
    geometry_colonne = gdf_old.geometry.name

    ancien = gdf_old[[colonne_id, geometry_colonne]]
    nouveau = gdf_new[[colonne_id, geometry_colonne]]

    comparaison = ancien.merge(
        nouveau,
        on=colonne_id,
        suffixes=("_old", "_new")
    )

    geometries_differentes = comparaison.apply(
        lambda ligne: _geometries_sont_differentes(
            ligne[f"{geometry_colonne}_old"],
            ligne[f"{geometry_colonne}_new"],
        ),
        axis=1
    )

    lignes_modifiees = comparaison[geometries_differentes]
    modifications = []

    for _, ligne in lignes_modifiees.iterrows():
        modifications.append({
            "id": ligne[colonne_id],
            "ancienne_geometrie": ligne[f"{geometry_colonne}_old"],
            "nouvelle_geometrie": ligne[f"{geometry_colonne}_new"]
        })
    return modifications