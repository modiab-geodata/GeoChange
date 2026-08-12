def statistiques_colonnes_ajoutees(resultat):
    statistiques = {
        "Nombre_colonnes_ajoutees": len(resultat)
    }
    return statistiques

def statistiques_colonnes_supprimees(resultat):
    statistiques = {
        "Nombre_colonnes_supprimees": len(resultat)
    }
    return statistiques

def statistiques_entites(resultat):
    nombre_old, nombre_new, difference = resultat

    statistiques = {
        "Nombre_entites_old": nombre_old,
        "Nombre_entites_new": nombre_new,
        "difference": difference
    }

    return statistiques

def statistiques_modifications(resultat):
    statistiques = {
        "nombre_modifications": len(resultat)
    }
    return statistiques


def statistiques_entites_ajoutes(resultat):
    statistiques = {
        "nombre_entites_ajoutes": len(resultat)
    }
    return statistiques

def statistiques_entites_supprimes(resultat):
    statistiques = {
        "nombre_entites_supprimes": len(resultat)
    }
    return statistiques

def statistiques_geometries_modifiees(resultat):
    statistiques = {
        "nombre_geometries_modifiees": len(resultat)
    }

    return statistiques