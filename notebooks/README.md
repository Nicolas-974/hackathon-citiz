# Pipeline local — accessibilité et implantation Citiz

Six notebooks, à lancer **dans l'ordre**. Chacun lit le résultat du précédent dans `data/silver/` : on ne relance que l'étape qu'on modifie.

| # | Notebook | Lit | Produit |
|---|---|---|---|
| 01 | `01_offre_bus` | GTFS (`data/bronze/gtfs/`) | `silver/offre_arrets.parquet` |
| 02 | `02_population` | INSEE (`data/bronze/insee/`) | `silver/carreaux.parquet` |
| 03 | `03_accessibilite` | 01 + 02 | `silver/carreaux_acces.parquet` |
| 04 | `04_valeur_emplacements` | 03 | `silver/emplacements.parquet` |
| 05 | `05_optimisation_budget` | 04 | `silver/selection.parquet`, `resultats/selection_stations.csv` |
| 06 | `06_cartes` | 01, 04, 05 | `resultats/cartes/*.html` |

Tous les réglages (périmètre, réseaux, date, rayons, poids, budget, coût) sont dans **`parametres.py`**. Les notebooks n'en contiennent aucun.

## Cas d'usage

- **Changer les poids du besoin** → `parametres.py`, puis relancer 04, 05, 06.
- **Changer le budget (démo jury)** → cellule 2 du notebook 05, puis relancer 05 (et 06 pour la carte).
- **Ajouter un réseau** → déposer son GTFS dans `data/bronze/gtfs/<dossier>/`, l'ajouter dans `RESEAUX`, puis tout relancer.
- **Autre territoire** → changer `COMMUNES` (et `INSEE_CSV` / `CRS_CARREAUX` hors Réunion), puis tout relancer.

## Données

- `data/bronze/` : fichiers bruts, **jamais modifiés** (copies de `gtfs-koa1808/` et du CSV INSEE).
- `data/bronze/gtfs/car_jaune/` : **vide pour l'instant**. À remplir avec le dossier `Bronze/gtfs/car_jaune` du Lakehouse. Tant qu'il est vide, le réseau est ignoré avec un message.

## Passer sur Fabric

1. Notebook en noyau **Python** (pas PySpark) : volumes faibles, beaucoup moins de capacité consommée.
2. Coller le contenu de `parametres.py` dans la première cellule, avec `RACINE = Path("/lakehouse/default/Files")` et `BRONZE = RACINE / "Bronze"`.
3. ⚠️ `Silver/` du Lakehouse est **partagé** : décider en équipe avant d'y écrire.
