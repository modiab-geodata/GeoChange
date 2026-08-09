\# GeoChange


> \*\*GeoChange\*\* est un moteur Python de comparaison de données géographiques permettant de détecter automatiquement les différences entre deux versions d'un même jeu de données vectoriel.



Le projet est conçu pour fonctionner avec \*\*n'importe quelle couche SIG\*\* (points, lignes ou polygones) et \*\*quel que soit le domaine métier\*\* (cadastre, urbanisme, réseaux, transport, environnement, OpenStreetMap, etc.).



\---



\# Pourquoi GeoChange ?



Les données géographiques évoluent continuellement.



À chaque nouvelle livraison d'un jeu de données, plusieurs questions reviennent :



\* Quelles entités ont été ajoutées ?

\* Quelles entités ont disparu ?

\* Quelles géométries ont été modifiées ?

\* Quels attributs ont changé ?

\* Combien de changements ont eu lieu ?

\* Peut-on obtenir automatiquement un rapport des évolutions ?



Aujourd'hui, ces comparaisons sont souvent réalisées :



\* manuellement dans QGIS ;

\* avec des scripts spécifiques à chaque projet ;

\* ou ne sont tout simplement pas effectuées.



GeoChange automatise entièrement ce processus.



\---



\# Objectifs



GeoChange permet de comparer automatiquement deux versions d'un même jeu de données géographique afin de :



\* détecter les nouvelles entités ;

\* détecter les entités supprimées ;

\* identifier les modifications des attributs ;

\* identifier les modifications géométriques ;

\* produire des statistiques de comparaison ;

\* générer des rapports exploitables ;

\* exporter les résultats dans plusieurs formats SIG.



\---



\# Cas d'utilisation



GeoChange est générique et peut être utilisé dans de nombreux contextes.



\## Administration



Comparer deux versions des limites administratives.



\## Urbanisme



Comparer deux versions du cadastre ou des bâtiments.



\## Réseaux



Comparer deux versions d'un réseau électrique, gaz ou télécom.



\## Mobilité



Comparer deux versions d'un réseau cyclable ou des stations Vélib.



\## Environnement



Comparer des inventaires forestiers ou des zones naturelles.



\## OpenStreetMap



Comparer deux extractions OSM afin de détecter les évolutions.



\---



\# Fonctionnalités



\## Lecture des données



\* GeoPackage

\* GeoJSON

\* Shapefile


\---



\## Validation



\* Vérification du CRS

\* Vérification de la géométrie active

\* Vérification des géométries invalides

\* Vérification des géométries vides

\* Vérification des colonnes

\* Vérification de la clé primaire



\---



\## Comparaison de structure



\* Colonnes ajoutées

\* Colonnes supprimées

\* Types de données modifiés

\* CRS différents



\---



\## Comparaison des entités



\* Entités ajoutées

\* Entités supprimées



\---



\## Comparaison des attributs



Détection automatique des modifications de valeurs.



Exemple :



| ID  | Champ | Ancienne valeur | Nouvelle valeur |

| --- | ----- | --------------- | --------------- |

| 154 | nom   | Paris           | Paris Centre    |



\---



\## Comparaison géométrique



Détection automatique :



\* géométries modifiées ;

\* surfaces modifiées ;

\* longueurs modifiées ;

\* déplacement du centroïde.



\---



\## Statistiques



Production automatique de statistiques :



\* nombre d'entités ;

\* nombre d'ajouts ;

\* nombre de suppressions ;

\* nombre de modifications ;

\* évolution des surfaces ;

\* évolution des longueurs.



\---



\## Rapports



Génération automatique :



\* rapport HTML

\* CSV

\* GeoPackage

\* GeoJSON



\---



\# Architecture du projet



```text

GeoChange/

│

├── README.md

├── requirements.txt

├── pyproject.toml

├── LICENSE

│

├── config/

│   └── compare.yaml

│

├── data/

│   ├── sample/

│   └── output/

│

├── docs/

│

├── src/

│   └── geochange/

│       ├── loader.py

│       ├── validator.py

│       ├── comparer.py

│       ├── geometry.py

│       ├── attributes.py

│       ├── statistics.py

│       ├── exporter.py

│       ├── report.py

│       ├── cli.py

│       └── utils.py

│

├── tests/

│

└── examples/

```



\---



\# Workflow



```text

Lecture

&#x20;   │

&#x20;   ▼

Validation

&#x20;   │

&#x20;   ▼

Comparaison de structure

&#x20;   │

&#x20;   ▼

Comparaison des entités

&#x20;   │

&#x20;   ▼

Comparaison des attributs

&#x20;   │

&#x20;   ▼

Comparaison géométrique

&#x20;   │

&#x20;   ▼

Statistiques

&#x20;   │

&#x20;   ▼

Rapport

&#x20;   │

&#x20;   ▼

Export

```



\---



\# Configuration



GeoChange est piloté par un fichier YAML.



Exemple :



```yaml

input:

&#x20; old: data/old.gpkg

&#x20; new: data/new.gpkg



primary\_key: id



compare:

&#x20; structure: true

&#x20; attributes: true

&#x20; geometry: true



output:

&#x20; folder: output

&#x20; formats:

&#x20;   - html

&#x20;   - gpkg

&#x20;   - csv

```



Aucune modification du code n'est nécessaire pour comparer un nouveau jeu de données.



\---



\# Installation



```bash

git clone https://github.com/<votre-utilisateur>/GeoChange.git



cd GeoChange



python -m venv .venv



source .venv/bin/activate

```



Windows :



```bash

.venv\\Scripts\\activate

```



Installation des dépendances :



```bash

pip install -r requirements.txt

```



\---



\# Utilisation



Lancer la comparaison :



```bash

python -m geochange compare config/compare.yaml

```



\---



\# Résultats générés



GeoChange produit automatiquement :



```text

output/



├── report.html

├── summary.csv

├── added\_entities.gpkg

├── removed\_entities.gpkg

├── modified\_entities.gpkg

├── statistics.csv

└── maps/

```



\---


\* Package Python installable



\---



\# Stack technique  



\* Python

\* GeoPandas

\* Pandas

\* Shapely

\* PyProj

\* Fiona

\* NumPy

\* PyYAML

\* Matplotlib

\* pytest



\---



\# Contributions



Les contributions sont les bienvenues.



N'hésitez pas à ouvrir une \*Issue\* ou une \*Pull Request\* afin de proposer une amélioration.



\---



\# Licence



Projet distribué sous licence MIT.



