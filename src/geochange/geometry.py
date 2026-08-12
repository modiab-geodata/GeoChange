def geometries_modifiees(gdf_old, gdf_new, colonne_id):
    geometry_colonne = gdf_old.geometry.name

    ancien = gdf_old[[colonne_id, geometry_colonne]]
    nouveau = gdf_new[[colonne_id, geometry_colonne]]

    comparaison = ancien.merge(
        nouveau,
        on= colonne_id,
        suffixes = ("_old", "_new")
    )

    geometries_differentes = ~comparaison.apply(
        lambda ligne: ligne[f"{geometry_colonne}_old"].equals(
            ligne[f"{geometry_colonne}_new"]
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