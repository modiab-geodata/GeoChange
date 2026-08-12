from pathlib import Path
import json

from pathlib import Path
from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)


def exporter_json(resultat, chemin_sortie):
    chemin_sortie = Path(chemin_sortie)

    chemin_sortie.parent.mkdir(parents=True, exist_ok=True)

    with open(chemin_sortie, "w", encoding="utf-8") as fichier:
        json.dump(
            resultat,
            fichier,
            indent=4,
            ensure_ascii=False,
            default=str
        )

    print(f"Rapport JSON exporté : {chemin_sortie}")

# ==========================================
# PALETTE / CONSTANTES DE STYLE
# ==========================================

COULEUR_PRIMAIRE = colors.HexColor("#1F3864")   # bleu foncé
COULEUR_SECONDAIRE = colors.HexColor("#2E75B6") # bleu moyen
COULEUR_FOND_ALT = colors.HexColor("#F2F5F9")   # gris-bleu très clair
COULEUR_TEXTE = colors.HexColor("#2B2B2B")
COULEUR_BORDURE = colors.HexColor("#D9D9D9")


def _construire_styles():
    """Construit un jeu de styles dédié, sans modifier le stylesheet global."""
    base = getSampleStyleSheet()

    styles = {
        "titre": ParagraphStyle(
            "TitreRapport",
            parent=base["Title"],
            fontName="Helvetica-Bold",
            fontSize=20,
            textColor=COULEUR_PRIMAIRE,
            alignment=TA_CENTER,
            spaceAfter=4,
        ),
        "sous_titre_doc": ParagraphStyle(
            "SousTitreDoc",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=11,
            textColor=colors.HexColor("#666666"),
            alignment=TA_CENTER,
            spaceAfter=18,
        ),
        "section": ParagraphStyle(
            "Section",
            parent=base["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=13,
            textColor=COULEUR_PRIMAIRE,
            spaceBefore=16,
            spaceAfter=8,
        ),
        "texte": ParagraphStyle(
            "TexteCorps",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=10,
            textColor=COULEUR_TEXTE,
            leading=15,
            alignment=TA_LEFT,
            spaceAfter=6,
        ),
        "label": ParagraphStyle(
            "Label",
            parent=base["BodyText"],
            fontName="Helvetica-Bold",
            fontSize=10,
            textColor=COULEUR_TEXTE,
        ),
    }
    return styles


def _entete_pied_page(canvas, document):
    """Dessine l'en-tête et le pied de page sur chaque page."""
    canvas.saveState()

    largeur, hauteur = A4

    # --- En-tête : bandeau de couleur + titre court ---
    canvas.setFillColor(COULEUR_PRIMAIRE)
    canvas.rect(0, hauteur - 18 * mm, largeur, 18 * mm, fill=1, stroke=0)

    canvas.setFillColor(colors.white)
    canvas.setFont("Helvetica-Bold", 11)
    canvas.drawString(20 * mm, hauteur - 12 * mm, "Rapport GeoChange")

    canvas.setFont("Helvetica", 9)
    canvas.drawRightString(
        largeur - 20 * mm,
        hauteur - 12 * mm,
        datetime.now().strftime("%d/%m/%Y")
    )

    # --- Pied de page : ligne fine + numéro de page ---
    canvas.setStrokeColor(COULEUR_BORDURE)
    canvas.setLineWidth(0.5)
    canvas.line(20 * mm, 15 * mm, largeur - 20 * mm, 15 * mm)

    canvas.setFillColor(colors.HexColor("#888888"))
    canvas.setFont("Helvetica", 8)
    canvas.drawCentredString(largeur / 2, 10 * mm, f"Page {document.page}")

    canvas.restoreState()


def exporter_pdf(resultat, chemin_sortie):
    chemin_sortie = Path(chemin_sortie)
    chemin_sortie.parent.mkdir(parents=True, exist_ok=True)

    document = SimpleDocTemplate(
        str(chemin_sortie),
        pagesize=A4,
        topMargin=28 * mm,
        bottomMargin=22 * mm,
        leftMargin=20 * mm,
        rightMargin=20 * mm,
    )

    styles = _construire_styles()
    contenu = []

    # ==========================================
    # TITRE
    # ==========================================

    contenu.append(Paragraph("Rapport de comparaison GeoChange", styles["titre"]))
    contenu.append(
        Paragraph(
            "Analyse des écarts entre l'ancienne et la nouvelle couche géographique",
            styles["sous_titre_doc"],
        )
    )
    contenu.append(HRFlowable(width="100%", thickness=1, color=COULEUR_BORDURE, spaceAfter=14))

    # ==========================================
    # STATISTIQUES
    # ==========================================

    contenu.append(Paragraph("Synthèse", styles["section"]))

    statistiques = resultat["statistiques"]

    tableau = [
        ["Indicateur", "Valeur"],
        ["Colonnes ajoutées", statistiques["Nombre_colonnes_ajoutees"]],
        ["Colonnes supprimées", statistiques["Nombre_colonnes_supprimees"]],
        ["Entités - ancienne couche", statistiques["Nombre_entites_old"]],
        ["Entités - nouvelle couche", statistiques["Nombre_entites_new"]],
        ["Entités ajoutées", statistiques["nombre_entites_ajoutes"]],
        ["Entités supprimées", statistiques["nombre_entites_supprimes"]],
        ["Attributs modifiés", statistiques["nombre_modifications"]],
        ["Géométries modifiées", statistiques["nombre_geometries_modifiees"]],
    ]

    table = Table(tableau, colWidths=[110 * mm, 50 * mm], hAlign="CENTER")

    style_table = [
        ("BACKGROUND", (0, 0), (-1, 0), COULEUR_PRIMAIRE),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 10),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 1), (-1, -1), 9.5),
        ("TEXTCOLOR", (0, 1), (-1, -1), COULEUR_TEXTE),
        ("ALIGN", (1, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LINEBELOW", (0, 0), (-1, 0), 1, COULEUR_PRIMAIRE),
        ("LINEBELOW", (0, -1), (-1, -1), 0.5, COULEUR_BORDURE),
        ("BOX", (0, 0), (-1, -1), 0.75, COULEUR_BORDURE),
    ]

    # Lignes alternées (zébrage) pour la lisibilité
    for i in range(1, len(tableau)):
        if i % 2 == 0:
            style_table.append(("BACKGROUND", (0, i), (-1, i), COULEUR_FOND_ALT))

    table.setStyle(TableStyle(style_table))

    contenu.append(table)
    contenu.append(Spacer(1, 10 * mm))

    # ==========================================
    # COMPARAISONS
    # ==========================================

    contenu.append(Paragraph("Détails des comparaisons", styles["section"]))

    comparaisons = resultat["comparaisons"]

    lignes_details = [
        ("Colonnes ajoutées", comparaisons["colonnes_ajoutees"]),
        ("Colonnes supprimées", comparaisons["colonnes_supprimees"]),
        ("Types modifiés", comparaisons["types_modifies"]),
        ("CRS", comparaisons["crs"]),
        ("Entités ajoutées", comparaisons["entites_ajoutees"]),
        ("Entités supprimées", comparaisons["entites_supprimees"]),
        ("Attributs modifiés", comparaisons["modifications"]),
        ("Géométries modifiées", comparaisons["geometries_modifiees"]),
    ]

    for label, valeur in lignes_details:
        contenu.append(
            Paragraph(
                f'<font color="#1F3864"><b>{label} : </b></font>{valeur}',
                styles["texte"],
            )
        )

    document.build(
        contenu,
        onFirstPage=_entete_pied_page,
        onLaterPages=_entete_pied_page,
    )

    print(f"Rapport PDF exporté : {chemin_sortie}")