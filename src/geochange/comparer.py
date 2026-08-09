def colonnes_ajoutees(gdf_old, gdf_new):
    colonnes_ajoutees = gdf_new.columns.difference(gdf_old.columns)
    if len(colonnes_ajoutees) == 0:
        print("Aucune colonne(s) n'a été ajouté(s)")
        return colonnes_ajoutees
    else:
        print(f"Colonne(s) ajoutée(s) : {list(colonnes_ajoutees)}")
        return colonnes_ajoutees


def colonnes_supprimees (gdf_old, gdf_new):
    colonnes_supprimees =gdf_old.columns.difference(gdf_new.columns)
    if len(colonnes_supprimees) == 0:
        print("Aucune colonne(s) n'a été supprimée(s)")
        return colonnes_supprimees
    else:
        print(f"Colonne(s) supprimée(s) : {list(colonnes_supprimees)}")
        return colonnes_supprimees

def types_donnees_modifies(gdf_old, gdf_new):
    colonnes_communes = gdf_old.columns.intersection(gdf_new.columns)

    types_modifies = {}

    for colonne in colonnes_communes:
        type_old = gdf_old[colonne].dtype
        type_new = gdf_new[colonne].dtype

        if type_old != type_new:
            types_modifies[colonne] = (type_old, type_new)

    if len(types_modifies) == 0:
        print("Aucun type de données n'a été modifié.")
        return types_modifies

    print("Type(s) de données modifié(s) :")

    for colonne, types in types_modifies.items():
        print(f" - {colonne} : {types[0]} → {types[1]}")
    return types_modifies

def crs_different(gdf_old, gdf_new):
    gdf_old_crs = gdf_old.crs.to_epsg()
    gdf_new_crs = gdf_new.crs.to_epsg()

    if gdf_old_crs != gdf_new_crs:
        print("Le CRS des deux couches est différent.")
    else:
        print("Les deux couches ont le même CRS.")
    return gdf_old_crs, gdf_new_crs

def nombre_entites(gdf_old, gdf_new):

    nombre_old = len(gdf_old)
    nombre_new = len(gdf_new)

    if nombre_old > nombre_new:
        difference = nombre_old - nombre_new
        print("L'ancienne couche contient plus d'entités que la nouvelle.")
        return nombre_old, nombre_new, difference

    elif nombre_new > nombre_old:
        difference = nombre_new - nombre_old
        print("La nouvelle couche contient plus d'entités que l'ancienne.")
        return nombre_old, nombre_new, difference

    else:
        print("Les deux couches ont le même nombre d'entités.")
        return nombre_old, nombre_new, 0









