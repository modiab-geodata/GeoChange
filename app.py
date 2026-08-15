import json
import tempfile
import datetime
import decimal
from pathlib import Path

import numpy as np
import streamlit as st
import folium
from folium.plugins import Fullscreen
from streamlit_folium import st_folium

from geochange.loader import load_file

from geochange.exporter import exporter_pdf

from geochange.validator import (
    verifier_crs,
    verifier_geometrie_active,
    verifier_geometries_invalides,
    verifier_geometries_vides,
    verifier_colonnes,
    verifier_cle_primaire,
)

from geochange.comparer import (
    colonnes_ajoutees,
    colonnes_supprimees,
    types_donnees_modifies,
    crs_different,
    nombre_entites,
    entites_ajoutees,
    entites_supprimees,
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
    statistiques_geometries_modifiees,
)


# ============================================================
# CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="GeoChange",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CSS — theme-aware (s'adapte au thème clair/sombre de l'utilisateur),
# pleine largeur, rendu type dashboard de production
# ============================================================

st.markdown(
    """
    <style>

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 3rem;
        padding-left: 2.5rem;
        padding-right: 2.5rem;
        max-width: 100%;
    }

    /* Bandeau d'en-tête */
    .bandeau {
        background-color: var(--primary-color);
        padding: 1.5rem 2rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-wrap: wrap;
        gap: 12px;
    }
    .bandeau h1 {
        color: white;
        margin: 0;
        font-size: 1.5rem;
        font-weight: 600;
    }
    .bandeau p {
        color: rgba(255, 255, 255, 0.82);
        margin: 0.3rem 0 0 0;
        font-size: 0.92rem;
    }
    .bandeau-badge {
        background: rgba(255, 255, 255, 0.15);
        color: white;
        padding: 6px 14px;
        border-radius: 999px;
        font-size: 0.82rem;
        font-weight: 500;
        white-space: nowrap;
    }

    /* Titres de section homogènes */
    h2 {
        font-size: 1.15rem;
        font-weight: 600;
        margin-top: 0.2rem;
        margin-bottom: 0.3rem;
    }
    h3 {
        font-size: 1rem;
        font-weight: 600;
    }
    .sous-titre {
        color: var(--text-color);
        opacity: 0.65;
        font-size: 0.88rem;
        margin-bottom: 1.1rem;
    }

    /* Métriques */
    [data-testid="stMetric"] {
        background-color: var(--secondary-background-color);
        border: 1px solid rgba(128, 128, 128, 0.25);
        border-radius: 10px;
        padding: 14px 16px;
    }
    [data-testid="stMetricLabel"] {
        font-weight: 600;
        font-size: 0.8rem;
        opacity: 0.75;
    }
    [data-testid="stMetricValue"] {
        font-size: 1.55rem;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        border-right: 1px solid rgba(128, 128, 128, 0.2);
    }

    /* Onglets de navigation principaux : rendu plus "dashboard" */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        border-bottom: 1px solid rgba(128, 128, 128, 0.25);
    }
    .stTabs [data-baseweb="tab"] {
        height: 42px;
        padding: 0 16px;
        border-radius: 8px 8px 0 0;
        font-weight: 500;
    }

    /* Puces pour listes de colonnes */
    .chip {
        display: inline-block;
        background-color: var(--secondary-background-color);
        border: 1px solid rgba(128, 128, 128, 0.3);
        border-radius: 999px;
        padding: 3px 12px;
        margin: 3px 4px 3px 0;
        font-size: 0.82rem;
        font-family: var(--font);
    }
    .chip-add {
        border-color: rgba(46, 160, 67, 0.4);
        color: #2ea043;
    }
    .chip-del {
        border-color: rgba(224, 62, 62, 0.4);
        color: #e03e3e;
    }

    /* Légende carte */
    .legende {
        display: flex;
        gap: 20px;
        align-items: center;
        font-size: 0.88rem;
        opacity: 0.85;
        margin-bottom: 0.8rem;
    }
    .legende span {
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }
    .pastille {
        width: 10px;
        height: 10px;
        border-radius: 50%;
        display: inline-block;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SIDEBAR
# ============================================================

FORMATS_ACCEPTES = ["geojson", "gpkg"]

AIDE_UPLOAD = (
    "Formats acceptés : GeoJSON (.geojson) et GeoPackage (.gpkg)."
)

with st.sidebar:

    st.header("📂 Chargez vos données")

    st.caption(
        "Chargez deux versions d'une même couche pour lancer l'analyse."
    )

    st.markdown(
        """
        <div style="font-size:0.8rem; opacity:0.75; margin-bottom:0.6rem; line-height:1.5;">
        <b>Formats supportés</b><br>
         GeoJSON - GeoPackage
        </div>
        """,
        unsafe_allow_html=True,
    )

    fichiers_old = st.file_uploader(
        "Ancienne couche",
        type=FORMATS_ACCEPTES,
        help=AIDE_UPLOAD,
        accept_multiple_files=True,
        key="upload_old",
    )

    fichiers_new = st.file_uploader(
        "Nouvelle couche",
        type=FORMATS_ACCEPTES,
        help=AIDE_UPLOAD,
        accept_multiple_files=True,
        key="upload_new",
    )


# ============================================================
# CHARGEMENT DES FICHIERS
# ============================================================

def charger_fichier(fichiers):
    """
    Reconstruit un jeu de fichiers uploadés (Streamlit) dans un même
    dossier temporaire, puis utilise le loader de GeoChange sur le
    fichier principal.
    """

    if not fichiers:
        return None

    dossier_temp = Path(tempfile.mkdtemp())

    chemin_principal = None

    extensions_principales = {".gpkg", ".geojson"}

    for fichier in fichiers:

        chemin_fichier = dossier_temp / fichier.name

        with open(chemin_fichier, "wb") as f:
            f.write(fichier.getbuffer())

        if chemin_fichier.suffix.lower() in extensions_principales:
            chemin_principal = chemin_fichier

    if chemin_principal is None:
        return None

    return load_file(chemin_principal)


def _convertir_valeur_json_safe(valeur):
    """
    Convertit récursivement une valeur en types Python natifs
    sérialisables (JSON, Folium/GeoJSON, export...).
    """

    if valeur is None:
        return None

    if isinstance(valeur, np.ndarray):
        return [_convertir_valeur_json_safe(v) for v in valeur.tolist()]

    if isinstance(valeur, (list, tuple)):
        return [_convertir_valeur_json_safe(v) for v in valeur]

    if isinstance(valeur, dict):
        return {cle: _convertir_valeur_json_safe(v) for cle, v in valeur.items()}

    if isinstance(valeur, np.integer):
        return int(valeur)

    if isinstance(valeur, np.floating):
        return float(valeur)

    if isinstance(valeur, np.bool_):
        return bool(valeur)

    # pandas.Timestamp hérite de datetime.datetime : ce cas est
    # donc couvert par ce test, pas besoin d'importer pandas ici.
    if isinstance(valeur, (datetime.datetime, datetime.date, datetime.time)):
        return valeur.isoformat()

    if isinstance(valeur, decimal.Decimal):
        return float(valeur)

    if isinstance(valeur, bytes):
        return valeur.decode("utf-8", errors="replace")

    if isinstance(valeur, (str, int, float, bool)):
        return valeur

    # Filet de sécurité final : tout type non reconnu est converti en texte
    try:
        json.dumps(valeur)
        return valeur
    except (TypeError, ValueError):
        return str(valeur)


def _dedupliquer_colonnes(gdf):

    colonnes = list(gdf.columns)
    vus = {}
    nouvelles_colonnes = []

    for nom in colonnes:
        if nom not in vus:
            vus[nom] = 0
            nouvelles_colonnes.append(nom)
        else:
            vus[nom] += 1
            nouvelles_colonnes.append(f"{nom}_dup{vus[nom]}")

    if nouvelles_colonnes != colonnes:
        gdf = gdf.copy()
        gdf.columns = nouvelles_colonnes

    return gdf


def normaliser_attributs(gdf):
    """
    Nettoie les colonnes d'attributs (hors géométrie) du GeoDataFrame
    pour garantir des types sérialisables partout dans l'app : carte
    Folium, export JSON, comparaison des valeurs.
    """

    if gdf is None:
        return None

    gdf = gdf.copy()

    gdf = _dedupliquer_colonnes(gdf)

    # Force un index de lignes standard (0, 1, 2, ...). Certains
    # Shapefile sont chargés par pyogrio avec un index non entier
    # (basé sur le champ FID interne), ce qui fait planter pandas
    # lors de la réaffectation de colonnes via .apply() plus bas
    # (KeyError: 0 — pandas cherche l'étiquette "0" au lieu de la
    # position 0 quand l'index n'est pas un RangeIndex classique).
    gdf = gdf.reset_index(drop=True)

    colonnes_attributs = [
        colonne for colonne in gdf.columns
        if colonne != gdf.geometry.name
    ]

    for colonne in colonnes_attributs:
        gdf[colonne] = gdf[colonne].apply(_convertir_valeur_json_safe)

    return gdf


# ============================================================
# IDENTIFIANT
# ============================================================

def colonnes_identifiantes(gdf_old, gdf_new):
    """
    Retourne les colonnes communes aux deux couches
    pouvant potentiellement servir d'identifiant.
    """

    colonnes_old = set(gdf_old.columns)
    colonnes_new = set(gdf_new.columns)

    communes = colonnes_old.intersection(colonnes_new)

    return [
        colonne
        for colonne in gdf_old.columns
        if colonne in communes
        and colonne != gdf_old.geometry.name
    ]


def verifier_identifiant(gdf, colonne):
    """
    Vérifie qu'une colonne peut servir d'identifiant unique.
    """

    if colonne not in gdf.columns:
        return False, "Colonne inexistante."

    valeurs_nulles = gdf[colonne].isna().sum()

    doublons = gdf[colonne].duplicated().sum()

    if valeurs_nulles > 0:
        return False, f"{valeurs_nulles} valeur(s) nulle(s)."

    if doublons > 0:
        masque_doublons = gdf[colonne].duplicated(keep=False)
        nb_lignes_concernees = int(masque_doublons.sum())
        nb_valeurs_dupliquees = int(
            gdf.loc[masque_doublons, colonne].nunique()
        )
        return False, (
            f"{nb_valeurs_dupliquees} valeur(s) dupliquée(s) "
            f"({nb_lignes_concernees} ligne(s) concernée(s))."
        )

    return True, "Identifiant unique valide."


# ============================================================
# ANALYSE COMPLETE
# ============================================================

def analyser_couches(gdf_old, gdf_new, colonne_id=None):

    # --------------------------------------------------------
    # Validation
    # --------------------------------------------------------

    validations = {
        "old": {},
        "new": {},
    }

    validations["old"]["crs"] = gdf_old.crs
    validations["new"]["crs"] = gdf_new.crs

    validations["old"]["geometrie_active"] = gdf_old.geometry.name
    validations["new"]["geometrie_active"] = gdf_new.geometry.name

    validations["old"]["geometries_invalides"] = int(
        (~gdf_old.geometry.is_valid).sum()
    )

    validations["new"]["geometries_invalides"] = int(
        (~gdf_new.geometry.is_valid).sum()
    )

    validations["old"]["geometries_vides"] = int(
        gdf_old.geometry.is_empty.sum()
    )

    validations["new"]["geometries_vides"] = int(
        gdf_new.geometry.is_empty.sum()
    )

    validations["old"]["colonnes"] = list(gdf_old.columns)
    validations["new"]["colonnes"] = list(gdf_new.columns)

    # --------------------------------------------------------
    # Comparaison structurelle — toujours calculée, ne dépend
    # pas de l'identifiant
    # --------------------------------------------------------

    colonnes_ajoutees_resultat = colonnes_ajoutees(
        gdf_old,
        gdf_new,
    )

    colonnes_supprimees_resultat = colonnes_supprimees(
        gdf_old,
        gdf_new,
    )

    types_modifies_resultat = types_donnees_modifies(
        gdf_old,
        gdf_new,
    )

    crs_different_resultat = crs_different(
        gdf_old,
        gdf_new,
    )

    nombre_entites_resultat = nombre_entites(
        gdf_old,
        gdf_new,
    )

    # --------------------------------------------------------
    # Comparaisons par entité — uniquement si un identifiant
    # valide a été fourni, comme dans main.py
    # --------------------------------------------------------

    cle_valide = colonne_id is not None

    if cle_valide:

        entites_ajoutees_resultat = entites_ajoutees(
            gdf_old,
            gdf_new,
            colonne_id,
        )

        entites_supprimees_resultat = entites_supprimees(
            gdf_old,
            gdf_new,
            colonne_id,
        )

        modifications_resultat = modifications_valeurs(
            gdf_old,
            gdf_new,
            colonne_id,
        )

        geometries_modifiees_resultat = geometries_modifiees(
            gdf_old,
            gdf_new,
            colonne_id,
        )

    else:

        entites_ajoutees_resultat = None
        entites_supprimees_resultat = None
        modifications_resultat = None
        geometries_modifiees_resultat = None

    # --------------------------------------------------------
    # Statistiques
    # --------------------------------------------------------

    statistiques = {}

    statistiques.update(
        statistiques_colonnes_ajoutees(
            colonnes_ajoutees_resultat
        )
    )

    statistiques.update(
        statistiques_colonnes_supprimees(
            colonnes_supprimees_resultat
        )
    )

    statistiques.update(
        statistiques_entites(
            nombre_entites_resultat
        )
    )

    if cle_valide:

        statistiques.update(
            statistiques_entites_ajoutes(
                entites_ajoutees_resultat
            )
        )

        statistiques.update(
            statistiques_entites_supprimes(
                entites_supprimees_resultat
            )
        )

        statistiques.update(
            statistiques_modifications(
                modifications_resultat
            )
        )

        statistiques.update(
            statistiques_geometries_modifiees(
                geometries_modifiees_resultat
            )
        )

    else:

        statistiques.update({"nombre_entites_ajoutes": None})
        statistiques.update({"nombre_entites_supprimes": None})
        statistiques.update({"nombre_modifications": None})
        statistiques.update({"nombre_geometries_modifiees": None})

    # --------------------------------------------------------
    # Résultat complet
    # --------------------------------------------------------

    resultats = {
        "identifiant": colonne_id if cle_valide else None,

        "analyses_par_entite": cle_valide,

        "validations": validations,

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

            "modifications": modifications_resultat,

            "geometries_modifiees": geometries_modifiees_resultat,
        },

        "statistiques": statistiques,
    }

    return resultats


# ============================================================
# CARTE
# ============================================================

def construire_carte(gdf_old, gdf_new):

    old_4326 = gdf_old.to_crs(4326)
    new_4326 = gdf_new.to_crs(4326)

    bounds_old = old_4326.total_bounds
    bounds_new = new_4326.total_bounds

    minx = min(bounds_old[0], bounds_new[0])
    miny = min(bounds_old[1], bounds_new[1])
    maxx = max(bounds_old[2], bounds_new[2])
    maxy = max(bounds_old[3], bounds_new[3])

    carte = folium.Map(
        tiles="CartoDB positron",
        control_scale=True,
    )

    # Cas particulier : emprise dégénérée (un seul point, ou plusieurs
    # points identiques) — fit_bounds sur une bbox de largeur/hauteur
    # nulle peut donner un comportement de zoom imprévisible.
    emprise_degeneree = (minx == maxx) and (miny == maxy)

    if emprise_degeneree:
        carte.location = [miny, minx]
        carte.zoom_start = 15
    else:
        carte.fit_bounds(
            [
                [miny, minx],
                [maxy, maxx],
            ],
            padding=(30, 30),
            max_zoom=18,
        )

    Fullscreen(
        position="topleft"
    ).add_to(carte)

    # --------------------------------------------------------
    # Style des points : cercles vectoriels (SVG) plutôt que des
    # marqueurs "épingle" par défaut de Leaflet. 
    # --------------------------------------------------------

    # --------------------------------------------------------
    # Ancienne couche
    # --------------------------------------------------------

    champs_old = [
        colonne
        for colonne in old_4326.columns
        if colonne != old_4326.geometry.name
    ][:5]

    folium.GeoJson(
        old_4326,
        name="Ancienne couche",
        style_function=lambda feature: {
            "color": "#C0392B",
            "weight": 2,
            "fillColor": "#C0392B",
            "fillOpacity": 0.15,
        },
        highlight_function=lambda feature: {
            "weight": 4,
            "fillOpacity": 0.35,
        },
        marker=folium.CircleMarker(
            radius=6,
            color="#C0392B",
            weight=2,
            fill=True,
            fill_color="#C0392B",
            fill_opacity=0.6,
        ),
        tooltip=(
            folium.GeoJsonTooltip(
                fields=champs_old,
                sticky=True,
            )
            if champs_old
            else None
        ),
    ).add_to(carte)

    # --------------------------------------------------------
    # Nouvelle couche
    # --------------------------------------------------------

    champs_new = [
        colonne
        for colonne in new_4326.columns
        if colonne != new_4326.geometry.name
    ][:5]

    folium.GeoJson(
        new_4326,
        name="Nouvelle couche",
        style_function=lambda feature: {
            "color": "#2E75B6",
            "weight": 2,
            "fillColor": "#2E75B6",
            "fillOpacity": 0.20,
        },
        highlight_function=lambda feature: {
            "weight": 4,
            "fillOpacity": 0.40,
        },
        marker=folium.CircleMarker(
            radius=6,
            color="#2E75B6",
            weight=2,
            fill=True,
            fill_color="#2E75B6",
            fill_opacity=0.6,
        ),
        tooltip=(
            folium.GeoJsonTooltip(
                fields=champs_new,
                sticky=True,
            )
            if champs_new
            else None
        ),
    ).add_to(carte)

    folium.LayerControl(
        collapsed=False
    ).add_to(carte)

    return carte


# ============================================================
# PETITS HELPERS D'AFFICHAGE
# ============================================================

def afficher_chips(valeurs, variante=""):
    """Affiche une liste de valeurs sous forme de puces (chips)."""

    classe = f"chip {variante}".strip()

    html = "".join(
        f'<span class="{classe}">{valeur}</span>'
        for valeur in valeurs
    )

    st.markdown(html, unsafe_allow_html=True)


def types_geometrie_presents(gdf):
    """
    Renvoie la liste triée des types de géométrie présents dans la
    couche, en filtrant les valeurs manquantes (NaN) que peut renvoyer
    geom_type pour des géométries vides/invalides — sinon sorted()
    échoue en tentant de comparer un float (NaN) à une chaîne.
    """

    types = [
        t for t in gdf.geometry.geom_type.unique()
        if isinstance(t, str)
    ]

    return sorted(types)


def statut_geometries(nb, libelle_singulier, libelle_pluriel, niveau_alerte="error"):
    """Affiche un message de statut cohérent pour les contrôles géométriques."""

    if nb == 0:
        st.success(f"Aucune {libelle_singulier}.")
    else:
        message = f"{nb} {libelle_singulier if nb == 1 else libelle_pluriel} détectée(s)."
        if niveau_alerte == "error":
            st.error(message)
        else:
            st.warning(message)


# ============================================================
# TITRE
# ============================================================

st.markdown(
    """
    <div class="bandeau">
        <div>
            <h1>🗺️ GeoChange</h1>
            <p>Comparaison de deux versions d'une couche géographique : structure, attributs et géométrie.</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# APPLICATION
# ============================================================

def nom_principal(fichiers):
    """Renvoie le nom du fichier principal d'un jeu uploadé
    (le .gpkg ou .geojson), pour l'affichage."""

    if not fichiers:
        return None

    extensions_principales = {".gpkg", ".geojson"}

    for fichier in fichiers:
        if Path(fichier.name).suffix.lower() in extensions_principales:
            return fichier.name

    return fichiers[0].name


def reconcilier_colonnes_tronquees(gdf_old, gdf_new):
    colonnes_old = [
        c for c in gdf_old.columns if c != gdf_old.geometry.name
    ]
    colonnes_new = [
        c for c in gdf_new.columns if c != gdf_new.geometry.name
    ]

    colonnes_old_orphelines = set(colonnes_old) - set(colonnes_new)
    colonnes_new_orphelines = set(colonnes_new) - set(colonnes_old)

    correspondances = []
    renommage = {}

    for nom_old in colonnes_old_orphelines:

        candidats = [
            nom_new for nom_new in colonnes_new_orphelines
            if nom_old.startswith(nom_new) or nom_new.startswith(nom_old)
        ]

        if len(candidats) == 1:
            nom_new = candidats[0]
            renommage[nom_new] = nom_old
            correspondances.append((nom_old, nom_new))

    if renommage:
        gdf_new = gdf_new.rename(columns=renommage)

    return gdf_new, correspondances


if fichiers_old and fichiers_new:

    # --------------------------------------------------------
    # Chargement
    # --------------------------------------------------------

    with st.spinner("Chargement des couches..."):

        try:

            gdf_old = charger_fichier(fichiers_old)
            gdf_new = charger_fichier(fichiers_new)

            gdf_old = normaliser_attributs(gdf_old)
            gdf_new = normaliser_attributs(gdf_new)

            gdf_new, correspondances_colonnes = reconcilier_colonnes_tronquees(
                gdf_old, gdf_new
            )

        except Exception as erreur:

            import traceback

            st.error(
                f"❌ Impossible de charger les couches : {erreur}"
            )

            with st.expander("Détails techniques (pour diagnostic)"):
                st.code(traceback.format_exc())

            st.stop()

        if gdf_old is None or gdf_new is None:

            st.error(
                "❌ Une des deux couches n'a pas pu être lue. "
                "Vérifiez que le fichier est un GeoJSON (.geojson) ou "
                "un GeoPackage (.gpkg) valide."
            )

            st.stop()

    # --------------------------------------------------------
    # Choix de l'identifiant — optionnel,
    # Sans identifiant valide, les analyses par entité (Entités,
    # Modifications) sont désactivées mais le reste de l'app
    # (Vue d'ensemble, Carte, Validation, Structure) reste utilisable.
    # --------------------------------------------------------

    with st.container(border=True):

        st.subheader("🔑 Identifiant des entités (optionnel)")

        st.markdown(
            '<p class="sous-titre">Sélectionnez la colonne qui identifie de '
            "manière unique chaque entité dans les deux versions de la "
            "couche. Sans colonne unique disponible, les analyses par "
            "entité (entités ajoutées/supprimées, modifications, "
            "géométries modifiées) seront désactivées, mais la structure "
            "et la carte restent disponibles.</p>",
            unsafe_allow_html=True,
        )

        colonnes_communes = colonnes_identifiantes(
            gdf_old,
            gdf_new,
        )

        colonne_id = None
        cle_valide = False

        if not colonnes_communes:

            st.info(
                "ℹ️ Aucune colonne commune aux deux couches. "
                "Les analyses par entité seront désactivées."
            )

        else:

            # Auto-détection : on propose par défaut la première colonne
            # déjà unique dans les deux couches, si elle existe.

            colonne_par_defaut = "(Aucun)"

            for candidate in colonnes_communes:
                ok_old, _ = verifier_identifiant(gdf_old, candidate)
                ok_new, _ = verifier_identifiant(gdf_new, candidate)
                if ok_old and ok_new:
                    colonne_par_defaut = candidate
                    break

            options = ["(Aucun)"] + colonnes_communes

            colonne_choisie = st.selectbox(
                "Colonne identifiant unique",
                options,
                index=options.index(colonne_par_defaut),
            )

            if colonne_choisie == "(Aucun)":

                st.caption(
                    "ℹ️ Aucun identifiant sélectionné — les analyses par "
                    "entité seront désactivées."
                )

            else:

                col_status_old, col_status_new = st.columns(2)

                id_old_ok, message_old = verifier_identifiant(
                    gdf_old, colonne_choisie
                )
                id_new_ok, message_new = verifier_identifiant(
                    gdf_new, colonne_choisie
                )

                with col_status_old:
                    st.caption("Ancienne couche")
                    (st.success if id_old_ok else st.error)(message_old)

                with col_status_new:
                    st.caption("Nouvelle couche")
                    (st.success if id_new_ok else st.error)(message_new)

                if id_old_ok and id_new_ok:

                    colonne_id = colonne_choisie
                    cle_valide = True

                else:

                    st.warning(
                        "⚠️ Cette colonne n'est pas unique dans les deux "
                        "couches. Voici les lignes concernées, et les "
                        "analyses par entité restent désactivées :"
                    )

                    if not id_old_ok:
                        st.caption("Doublons — ancienne couche")
                        lignes_dupliquees_old = gdf_old[
                            gdf_old[colonne_choisie].duplicated(keep=False)
                        ]
                        st.dataframe(
                            lignes_dupliquees_old[[colonne_choisie]],
                            use_container_width=True,
                        )

                    if not id_new_ok:
                        st.caption("Doublons — nouvelle couche")
                        lignes_dupliquees_new = gdf_new[
                            gdf_new[colonne_choisie].duplicated(keep=False)
                        ]
                        st.dataframe(
                            lignes_dupliquees_new[[colonne_choisie]],
                            use_container_width=True,
                        )

    # --------------------------------------------------------
    # Analyse
    # --------------------------------------------------------

    with st.spinner("Analyse comparative des couches..."):

        resultats = analyser_couches(
            gdf_old,
            gdf_new,
            colonne_id,
        )

    comparaisons = resultats["comparaisons"]
    statistiques = resultats["statistiques"]
    validations = resultats["validations"]

    st.write("")

    # ========================================================
    # NAVIGATION PRINCIPALE
    # ========================================================

    (
        tab_apercu,
        tab_carte,
        tab_validation,
        tab_structure,
        tab_entites,
        tab_modifications,
        tab_donnees,
        tab_export,
    ) = st.tabs(
        [
            "📊 Vue d'ensemble",
            "🗺️ Carte",
            "🔎 Validation de données",
            "🔄 Structure de données",
            "➕➖ Entités",
            "🔍 Modifications de données",
            "📋 Table attributaire",
            "📥 Export de données",
        ]
    )

    # ========================================================
    # 1. VUE D'ENSEMBLE
    # ========================================================

    with tab_apercu:

        st.subheader("Indicateurs clés")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Nombre d'entités-ancienne couche", len(gdf_old))

        with col2:
            st.metric(
                "Nombre d'entités-nouvelle couche",
                len(gdf_new),
                #delta=len(gdf_new) - len(gdf_old),
            )

        with col3:
            st.metric(
                "Nombre d'attributs modifiés",
                statistiques["nombre_modifications"],
            )

        with col4:
            st.metric(
                "Nombre de géométries modifiées",
                statistiques["nombre_geometries_modifiees"],
            )

        col5, col6, col7, col8 = st.columns(4)

        with col5:
            st.metric("Nombre d'entités ajoutées", statistiques["nombre_entites_ajoutes"])

        with col6:
            st.metric("Nombre d'entités supprimées", statistiques["nombre_entites_supprimes"])

        with col7:
            st.metric("Nombre de colonnes ajoutées", len(comparaisons["colonnes_ajoutees"]))

        with col8:
            st.metric("Nombre de colonnes supprimées", len(comparaisons["colonnes_supprimees"]))

        st.divider()

        st.subheader("Couches comparées")

        col_a, col_b = st.columns(2)

        with col_a:
            with st.container(border=True):
                st.markdown("**🗂️ Ancienne couche**")
                st.write("**Nom :**", nom_principal(fichiers_old))
                st.write("**CRS :**", gdf_old.crs)
                st.write("**Géométrie active :**", gdf_old.geometry.name)
                st.markdown("**Types de géométrie :**")
                afficher_chips(types_geometrie_presents(gdf_old))

        with col_b:
            with st.container(border=True):
                st.markdown("**🗂️ Nouvelle couche**")
                st.write("**Nom :**", nom_principal(fichiers_new))
                st.write("**CRS :**", gdf_new.crs)
                st.write("**Géométrie active :**", gdf_new.geometry.name)
                st.markdown("**Types de géométrie :**")
                afficher_chips(types_geometrie_presents(gdf_new))

    # ========================================================
    # 2. CARTE
    # ========================================================

    with tab_carte:

        st.subheader("Visualisation cartographique")

        st.markdown(
            '<p class="sous-titre">Visualisation des deux versions de la '
            'couche. Utilisez le contrôle des couches en haut à droite pour afficher '
            'ou masquer chaque version.</p>',
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="legende">
                <span><span class="pastille" style="background:#C0392B;"></span> Ancienne couche</span>
                <span><span class="pastille" style="background:#2E75B6;"></span> Nouvelle couche</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        carte = construire_carte(gdf_old, gdf_new)

        st_folium(
            carte,
            use_container_width=True,
            height=620,
            returned_objects=[],
        )

    # ========================================================
    # 3. VALIDATION
    # ========================================================

    with tab_validation:

        st.subheader("Validation des couches")

        st.markdown(
            '<p class="sous-titre">Contrôles de cohérence sur le système de '
            'coordonnées et la géométrie de chaque couche.</p>',
            unsafe_allow_html=True,
        )

        sous_tab_old, sous_tab_new = st.tabs(["Ancienne couche", "Nouvelle couche"])

        for sous_tab, cle in [(sous_tab_old, "old"), (sous_tab_new, "new")]:

            with sous_tab:

                col1, col2 = st.columns(2)

                with col1:
                    st.caption("CRS")
                    st.success(f"{validations[cle]['crs']}")

                    st.caption("Géométrie active")
                    st.success(validations[cle]["geometrie_active"])

                with col2:
                    st.caption("Géométries invalides")
                    statut_geometries(
                        validations[cle]["geometries_invalides"],
                        "géométrie invalide",
                        "géométries invalides",
                        niveau_alerte="error",
                    )

                    st.caption("Géométries vides")
                    statut_geometries(
                        validations[cle]["geometries_vides"],
                        "géométrie vide",
                        "géométries vides",
                        niveau_alerte="warning",
                    )

    # ========================================================
    # 4. STRUCTURE
    # ========================================================

    with tab_structure:

        st.subheader("Comparaison de structure")

        col1, col2, col3 = st.columns(3)

        with col1:
            with st.container(border=True):
                st.metric("Nombre de colonnes ajoutées", len(comparaisons["colonnes_ajoutees"]))
                if comparaisons["colonnes_ajoutees"]:
                    afficher_chips(comparaisons["colonnes_ajoutees"], "chip-add")

        with col2:
            with st.container(border=True):
                st.metric("Nombre de colonnes supprimées", len(comparaisons["colonnes_supprimees"]))
                if comparaisons["colonnes_supprimees"]:
                    afficher_chips(comparaisons["colonnes_supprimees"], "chip-del")

        with col3:
            with st.container(border=True):
                st.metric("Nombre de types de données modifiés", len(comparaisons["types_modifies"]))
                if comparaisons["types_modifies"]:
                    for champ, types in comparaisons["types_modifies"].items():
                        types_lisibles = " → ".join(str(t) for t in types)
                        st.write(f"**{champ}** : {types_lisibles}")

    # ========================================================
    # 5. ENTITES
    # ========================================================

    with tab_entites:

        st.subheader("Comparaison des entités")

        if not resultats["analyses_par_entite"]:

            st.info(
                "ℹ️ Analyse non disponible : aucun identifiant unique "
                "valide n'a été défini. Configurez-en un dans la "
                "section \"🔑 Identifiant des entités\" en haut de page "
                "pour activer cette comparaison."
            )

        else:

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Nombre d'entités ajoutées", statistiques["nombre_entites_ajoutes"])

            with col2:
                st.metric("Nombre d'entités supprimées", statistiques["nombre_entites_supprimes"])

            with col3:
                st.metric("Différence totale", len(gdf_new) - len(gdf_old))

            st.divider()

            tab_ajoutees, tab_supprimees = st.tabs(
                ["Nombre d'entités ajoutées", "Nombre d'entités supprimées"]
            )

            with tab_ajoutees:
                if comparaisons["entites_ajoutees"]:
                    st.dataframe(
                        comparaisons["entites_ajoutees"],
                        use_container_width=True,
                    )
                else:
                    st.success("Aucune entité ajoutée.")

            with tab_supprimees:
                if comparaisons["entites_supprimees"]:
                    st.dataframe(
                        comparaisons["entites_supprimees"],
                        use_container_width=True,
                    )
                else:
                    st.success("Aucune entité supprimée.")

    # ========================================================
    # 6. MODIFICATIONS
    # ========================================================

    with tab_modifications:

        st.subheader("Statistiques des changements")

        if not resultats["analyses_par_entite"]:

            st.info(
                "ℹ️ Analyse non disponible : aucun identifiant unique "
                "valide n'a été défini. Configurez-en un dans la "
                "section \"🔑 Identifiant des entités\" en haut de page "
                "pour activer cette comparaison."
            )

        else:

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Nomnre d'attributs modifiés", statistiques["nombre_modifications"])

            with col2:
                st.metric("Nombre de géométries modifiées", statistiques["nombre_geometries_modifiees"])

            with col3:
                st.metric("Nom de l'identifiant utilisé", colonne_id)

            st.divider()

            st.subheader("Détails des modifications")

            modifications = comparaisons["modifications"]

            st.markdown("**📝 Modifications d'attributs**")
            if modifications:
                st.dataframe(modifications, use_container_width=True)
            else:
                st.success("Aucune modification d'attribut détectée.")

            geometries = comparaisons["geometries_modifiees"]

            st.markdown("**📐 Géométries modifiées**")
            if geometries:
                st.dataframe(geometries, use_container_width=True)
            else:
                st.success("Aucune modification géométrique détectée.")

    # ========================================================
    # 7. DONNEES BRUTES
    # ========================================================

    with tab_donnees:

        st.subheader("Aperçu des données")

        tab1, tab2 = st.tabs(["Ancienne couche", "Nouvelle couche"])

        with tab1:
            st.dataframe(
                gdf_old.drop(columns=gdf_old.geometry.name),
                use_container_width=True,
            )

        with tab2:
            st.dataframe(
                gdf_new.drop(columns=gdf_new.geometry.name),
                use_container_width=True,
            )

    # ========================================================
    # 8. EXPORT
    # ========================================================

    with tab_export:

        st.subheader("Export du rapport")

        st.markdown(
            '<p class="sous-titre">Téléchargez les résultats de l\'analyse '
            "(validations, comparaisons, statistiques) au format JSON ou "
            "sous forme de rapport PDF.</p>",
            unsafe_allow_html=True,
        )

        col_json, col_pdf = st.columns(2)

        with col_json:

            json_bytes = json.dumps(
                resultats,
                indent=4,
                ensure_ascii=False,
                default=str,
            ).encode("utf-8")

            st.download_button(
                label="📄 Télécharger le rapport JSON",
                data=json_bytes,
                file_name="rapport_geochange.json",
                mime="application/json",
                use_container_width=True,
            )

        with col_pdf:

            if st.button("📑 Générer le rapport PDF", use_container_width=True):

                with st.spinner("Génération du PDF..."):

                    try:

                        dossier_temp = Path(tempfile.mkdtemp())
                        chemin_pdf = dossier_temp / "rapport_geochange.pdf"

                        exporter_pdf(resultats, chemin_pdf)

                        with open(chemin_pdf, "rb") as fichier_pdf:
                            pdf_bytes = fichier_pdf.read()

                        st.session_state["pdf_genere"] = pdf_bytes

                    except Exception as erreur:

                        st.error(
                            f"❌ Impossible de générer le PDF : {erreur}"
                        )

            if "pdf_genere" in st.session_state:

                st.download_button(
                    label="📥 Télécharger le rapport PDF",
                    data=st.session_state["pdf_genere"],
                    file_name="rapport_geochange.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                )

else:

    st.info(
        "Chargez une ancienne couche et une nouvelle couche "
        "depuis le menu à gauche pour démarrer l'analyse."
    )