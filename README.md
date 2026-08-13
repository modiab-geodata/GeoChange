# 🗺️ GeoChange

## Détection et analyse des changements entre deux versions d'une couche géographique

GeoChange est une application développée en **Python** permettant de comparer automatiquement deux versions d'une même couche géographique afin d'identifier les évolutions de sa structure, de ses attributs et de ses géométries.

L'application permet de charger deux couches SIG, de contrôler leur qualité avant comparaison, de sélectionner une **colonne d'identification unique adaptée aux données**, puis d'analyser les différences entre les deux versions.

GeoChange fournit également une **interface web interactive développée avec Streamlit**, permettant de visualiser les données, les résultats de comparaison et les informations géographiques directement dans une interface cartographique.

Les résultats peuvent être exportés sous différents formats afin de conserver une trace exploitable de l'analyse.

**Application en ligne : []**

---

# Objectifs

Dans de nombreux projets SIG, les données géographiques sont régulièrement mises à jour.

Il peut alors être nécessaire de déterminer rapidement :

* quelles colonnes ont été ajoutées ou supprimées ;
* quels types de données ont évolué ;
* combien d'entités ont été ajoutées ou supprimées ;
* quelles valeurs attributaires ont été modifiées ;
* quelles géométries ont été modifiées ;
* si le système de coordonnées a changé ;
* si les données présentent des problèmes avant la comparaison.

GeoChange a pour objectif d'automatiser cette analyse afin de faciliter le **suivi des évolutions de données géographiques**.

---

# Fonctionnalités

## Chargement des données

GeoChange permet de comparer deux couches géographiques :

* une **couche ancienne** ;
* une **couche nouvelle**.

Formats actuellement pris en charge :

* GeoJSON ;
* GeoPackage ;
* Shapefile.

Les fichiers peuvent être chargés directement depuis l'interface Streamlit.

---

## Validation des couches

Avant de lancer la comparaison, GeoChange effectue plusieurs contrôles sur les deux couches.

### Système de coordonnées

L'application vérifie la présence du CRS et permet de comparer le système de coordonnées des deux versions.

### Géométrie active

GeoChange vérifie qu'une géométrie active est définie pour chaque GeoDataFrame.

### Validité des géométries

L'application détecte les géométries invalides.

### Géométries vides

Les géométries vides sont également contrôlées avant la comparaison.

### Structure des données

GeoChange analyse notamment :

* le nombre de colonnes ;
* les noms des colonnes ;
* la structure générale des couches.

---

# Identification des entités

Pour comparer les entités présentes dans les deux versions, GeoChange permet à l'utilisateur de sélectionner une **colonne d'identification unique**.

Cette approche permet de ne pas dépendre d'un nom de colonne spécifique comme `code_iris`.

Par exemple, selon les données utilisées, la colonne d'identification peut être :

```text
code_iris
id
objectid
fid
code
identifiant
```

La colonne sélectionnée doit idéalement :

* exister dans les deux couches ;
* ne pas contenir de valeurs NULL ;
* ne pas contenir de doublons.

Cette identification permet ensuite de déterminer les entités ajoutées, supprimées et les modifications associées.

---

# Comparaison de la structure

GeoChange compare automatiquement la structure des deux couches.

L'application détecte :

* les colonnes ajoutées ;
* les colonnes supprimées ;
* les changements de types de données.

Exemple :

```text
Couche ancienne
----------------
id
nom
population

Couche nouvelle
----------------
id
nom
population
densite
```

GeoChange identifie alors :

```text
Colonne ajoutée :
densite
```

---

# Comparaison du CRS

Le système de coordonnées des deux couches est comparé automatiquement.

GeoChange permet ainsi d'identifier les situations dans lesquelles :

```text
Couche ancienne : EPSG:4326
Couche nouvelle : EPSG:2154
```

ou lorsque les deux couches utilisent le même système de coordonnées.

---

# Comparaison des entités

GeoChange identifie les différences entre les entités des deux versions à partir de la colonne d'identification sélectionnée.

L'application détecte :

* les entités ajoutées ;
* les entités supprimées ;
* l'évolution du nombre total d'entités.

Exemple :

```text
Ancienne couche : 1 000 entités
Nouvelle couche : 1 025 entités

Entités ajoutées : 25
Entités supprimées : 0
```

---

# Comparaison des attributs

Pour les entités présentes dans les deux versions, GeoChange compare les valeurs attributaires.

L'application identifie notamment :

* le champ concerné ;
* l'ancienne valeur ;
* la nouvelle valeur ;
* l'identifiant de l'entité concernée.

Exemple :

```text
ID : 750560101
Champ : population
Ancienne valeur : 1520
Nouvelle valeur : 1634
```

La comparaison prend également en compte différents types de valeurs, y compris certaines structures complexes.

---

# Comparaison des géométries

GeoChange compare les géométries des entités présentes dans les deux versions.

L'application permet d'identifier :

* les entités dont la géométrie a changé ;
* l'ancienne géométrie ;
* la nouvelle géométrie ;
* l'identifiant de l'entité concernée.

Cette fonctionnalité permet notamment de suivre l'évolution de contours géographiques entre deux versions d'une même donnée.

---

# Statistiques

Les résultats détaillés sont accompagnés de statistiques synthétiques.

GeoChange calcule notamment :

* nombre de colonnes ajoutées ;
* nombre de colonnes supprimées ;
* nombre d'entités dans l'ancienne couche ;
* nombre d'entités dans la nouvelle couche ;
* différence du nombre d'entités ;
* nombre d'entités ajoutées ;
* nombre d'entités supprimées ;
* nombre de modifications attributaires ;
* nombre de géométries modifiées.

Ces statistiques sont également affichées directement dans l'interface Streamlit.

---

# Interface Streamlit

GeoChange dispose d'une interface web permettant d'utiliser l'application sans avoir à manipuler directement le code Python.

L'interface permet notamment de :

* charger les deux couches ;
* sélectionner la colonne d'identification ;
* consulter les informations générales ;
* visualiser les données attributaires ;
* consulter les résultats de comparaison ;
* consulter les statistiques ;
* visualiser les couches sur une carte interactive ;
* télécharger les rapports générés.

L'objectif est de fournir une interface simple permettant à un utilisateur SIG ou Data d'effectuer une comparaison sans devoir exécuter manuellement chaque fonction du moteur.

---

# Visualisation cartographique

Une interface cartographique interactive permet de visualiser les deux versions des données.

Les deux couches peuvent être affichées simultanément afin de faciliter la comparaison visuelle.

La carte permet notamment de :

* afficher la couche ancienne ;
* afficher la couche nouvelle ;
* activer ou désactiver les couches ;
* naviguer sur la carte ;
* consulter les informations des entités ;
* comparer visuellement les géométries.

La visualisation cartographique utilise **Folium** et est intégrée à **Streamlit**.

---

# Génération de rapports

Après l'analyse, GeoChange génère automatiquement des rapports dans le dossier `reports/`.

## Rapport JSON

Le rapport JSON contient les résultats structurés de la comparaison :

```json
{
    "configuration": {},
    "comparaisons": {},
    "statistiques": {}
}
```

Ce format peut notamment être utilisé pour une exploitation automatisée des résultats.

## Rapport PDF

Un rapport PDF est également généré afin de disposer d'une version facilement consultable et partageable des résultats.

Les rapports contiennent notamment :

* la configuration de la comparaison ;
* les résultats de comparaison ;
* les statistiques ;
* les modifications détectées.

---

# Architecture

L'application repose sur une architecture séparant les différentes responsabilités du projet.

```text
                         +----------------------+
                         |      Utilisateur     |
                         +----------+-----------+
                                    |
                                    v
                         +----------------------+
                         |      Streamlit       |
                         |   Interface Web      |
                         +----------+-----------+
                                    |
                                    v
                         +----------------------+
                         |   Moteur GeoChange   |
                         +----------+-----------+
                                    |
              +---------------------+---------------------+
              |                     |                     |
              v                     v                     v
       Validation              Comparaison          Statistiques
              |                     |                     |
              +---------------------+---------------------+
                                    |
                                    v
                         +----------------------+
                         |      Résultats       |
                         +----------+-----------+
                                    |
                         +----------+----------+
                         |                     |
                         v                     v
                  Rapport JSON           Rapport PDF
```

---

# Stack technique

| Domaine                        | Technologies                         |
| ------------------------------ | ------------------------------------ |
| Langage                        | Python 3                             |
| Analyse de données             | Pandas                               |
| Données géographiques          | GeoPandas                            |
| Géométries                     | Shapely                              |
| Interface web                  | Streamlit                            |
| Cartographie                   | Folium                               |
| Intégration Folium / Streamlit | streamlit-folium                     |
| Rapports PDF                   | ReportLab                            |
| Format de données              | GeoJSON, GeoPackage, Shapefile |
| Gestion des fichiers           | pathlib                              |
| Versionnement                  | Git / GitHub                         |

---

# Structure du projet

```text
GeoChange/
│
├── data/
│   └── input/
│       ├── iris_old.geojson
│       └── iris.geojson
│
├── reports/
│   ├── rapport.json
│   └── rapport.pdf
|
├── config/
│   ├── compare.yaml
│   └── default.yaml
│
|
├── doc/
│   ├── architecture.md
|   ├── examples.md
│   └── workflow.md
|
├── examples/
│   ├── compare_communes.py
|   ├── compare_roads.py
│   └── compares_buildings.py
|
├── tests/
│   ├── test_loader.py
|   ├── test_validator.py
│   └── test_geometry.py
|   ├── test_comparer.py
|   ├── test_attributes.py
|   ├── test_stats.py

├── src/
│   ├── geochange/
│   │   ├── __init__.py
│   │   ├── comparer.py
│   │   ├── comparer.py
│   │   ├── attributes.py
│   │   ├── geometry.py
│   │   ├── loader.py
│   │   ├── stats.py
│   │   └── validator.py
│   │   └── utils.py
│   │
│   └── main.py
│
├── app.py
├── requirements.txt
├── README.md
├── pyproject.toml
├── LICENCE
├── .gitignore
└── ...
```

---

# Installation

## 1. Cloner le dépôt

```bash
git clone https://github.com/modiab-geodata/GeoChange.git

cd GeoChange
```

---

## 2. Créer un environnement virtuel

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

---

# Exécution

## Mode ligne de commande

Le moteur GeoChange peut être exécuté directement depuis Python :

```bash
python src/main.py
```

Cette exécution permet de lancer l'ensemble du processus :

```text
Chargement
    ↓
Validation
    ↓
Comparaison
    ↓
Statistiques
    ↓
Export JSON
    ↓
Export PDF
```

Les rapports sont générés dans :

```text
reports/
```

---

# Interface web

Pour lancer l'application Streamlit :

```bash
streamlit run app.py
```

Puis ouvrir dans le navigateur :

```text
http://localhost:8501
```

---

# Utilisation

## 1. Charger les données

Depuis la barre latérale :

* sélectionner la couche ancienne ;
* sélectionner la couche nouvelle.

---

## 2. Sélectionner la colonne d'identification

Choisir la colonne permettant d'identifier de manière unique les entités.

Cette étape permet à GeoChange de fonctionner avec différents types de données géographiques sans dépendre d'un nom de colonne prédéfini.

---

## 3. Consulter les informations

L'interface présente les principales informations des deux couches :

* nom du fichier ;
* nombre d'entités ;
* nombre de colonnes ;
* CRS ;
* structure des données.

---

## 4. Consulter la comparaison

GeoChange présente les différences détectées :

* structure ;
* CRS ;
* entités ;
* attributs ;
* géométries.

---

## 5. Explorer les données sur la carte

Les deux versions de la couche peuvent être affichées simultanément sur la carte interactive afin de faciliter l'analyse visuelle des changements.

---

## 6. Consulter les statistiques

Les indicateurs synthétiques permettent d'obtenir rapidement une vue globale des changements détectés.

---

## 7. Générer les rapports

Les résultats peuvent être conservés sous forme de :

```text
rapport.json
rapport.pdf
```

dans le dossier :

```text
reports/
```

---

# Évolutions futures

Les évolutions envisagées pour GeoChange sont notamment :

* amélioration de la détection automatique des colonnes d'identification ;
* possibilité de comparer des couches ne possédant pas de clé unique ;
* amélioration de la visualisation cartographique des entités modifiées ;
* filtrage des entités ajoutées, supprimées et modifiées directement sur la carte ;
* amélioration du rapport PDF ;
* export des entités modifiées dans de nouveaux fichiers SIG ;
* prise en charge de formats SIG supplémentaires ;
* amélioration de l'interface utilisateur ;
* ajout de tests automatisés ;
* conteneurisation avec Docker ;
* intégration d'une CI/CD ;
* déploiement Cloud.

---

# Contribution

Les contributions sont les bienvenues.

Pour contribuer :

1. Forker le projet.
2. Créer une branche dédiée à la fonctionnalité :

```bash
git checkout -b feature/nouvelle-fonctionnalite
```

3. Développer et tester les modifications.
4. Committer les changements :

```bash
git commit -m "Add nouvelle fonctionnalité"
```

5. Pousser la branche :

```bash
git push origin feature/nouvelle-fonctionnalite
```

6. Créer une Pull Request.

---

# Auteur

**Moussa DIABY**

Ingénieur SIG • Consultant Data & Géomatique

GitHub : [modiab-geodata](https://github.com/modiab-geodata)
