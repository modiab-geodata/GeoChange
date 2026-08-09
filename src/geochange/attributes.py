def modifications_valeurs(gdf_old, gdf_new, colonne_id):

    colonnes_communes = gdf_old.columns.intersection(gdf_new.columns)

    colonnes_a_comparer = colonnes_communes.difference(
        [colonne_id, gdf_old.geometry.name]
    )

    ancien = gdf_old[[colonne_id] + list(colonnes_a_comparer)]
    nouveau = gdf_new[[colonne_id] + list(colonnes_a_comparer)]

    comparaison = ancien.merge(
        nouveau,
        on=colonne_id,
        suffixes=("_old", "_new")
    )

    modifications = []

    for colonne in colonnes_a_comparer:

        valeurs_differentes = comparaison[f"{colonne}_old"] != comparaison[f"{colonne}_new"]

        lignes_modifiees = comparaison[valeurs_differentes]

        for _, ligne in lignes_modifiees.iterrows():

            modifications.append({
                "id": ligne[colonne_id],
                "champ": colonne,
                "ancienne_valeur": ligne[f"{colonne}_old"],
                "nouvelle_valeur": ligne[f"{colonne}_new"]
            })

    return modifications
