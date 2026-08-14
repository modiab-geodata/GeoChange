import numpy as np
import pandas as pd


def _valeurs_sont_differentes(valeur_old, valeur_new):

    old_est_multivaleur = isinstance(valeur_old, (list, tuple, np.ndarray))
    new_est_multivaleur = isinstance(valeur_new, (list, tuple, np.ndarray))

    if not old_est_multivaleur and not new_est_multivaleur:

        old_est_nulle = pd.isna(valeur_old)
        new_est_nulle = pd.isna(valeur_new)

        if old_est_nulle and new_est_nulle:
            return False

        if old_est_nulle or new_est_nulle:
            return True

    try:
        resultat = valeur_old != valeur_new

        if isinstance(resultat, (list, tuple, np.ndarray, pd.Series)):
            return bool(np.any(resultat))

        return bool(resultat)

    except (ValueError, TypeError):
        return str(valeur_old) != str(valeur_new)


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

        valeurs_differentes = comparaison.apply(
            lambda ligne: _valeurs_sont_differentes(
                ligne[f"{colonne}_old"],
                ligne[f"{colonne}_new"],
            ),
            axis=1,
        )

        lignes_modifiees = comparaison[valeurs_differentes]

        for _, ligne in lignes_modifiees.iterrows():

            modifications.append({
                "id": ligne[colonne_id],
                "champ": colonne,
                "ancienne_valeur": ligne[f"{colonne}_old"],
                "nouvelle_valeur": ligne[f"{colonne}_new"]
            })

    return modifications
