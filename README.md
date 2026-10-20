# Hackathon Microsoft × Citiz — Où implanter des stations d'autopartage ?

Analyse de l'Ouest de La Réunion : accès au bus de chaque habitant, puis choix des meilleurs emplacements pour des stations Citiz selon un budget.

## Voir les résultats sans rien installer

Ouvrez simplement dans votre navigateur les cartes du dossier **`resultats/cartes/`** :

| Carte | Ce qu'elle montre |
|---|---|
| `carte_selection.html` | Les stations recommandées, numérotées par priorité |
| `carte_acces.html` | L'offre de bus à moins de 5 min à pied, carreau par carreau |
| `carte_arrets.html` | Les arrêts de bus, selon leur nombre de passages |
| `carte_isoles.html` | Les zones habitées très loin de tout arrêt |

La liste des stations s'ouvre aussi dans Excel : `resultats/selection_stations.csv`.

## Lancer les notebooks

### 1. Choisir le bon Python ⚠️

C'est **le point le plus important**. Un ordinateur a souvent plusieurs versions de Python installées. Les bibliothèques doivent être installées **dans le même Python** que celui choisi pour lancer les notebooks, sinon l'erreur `ModuleNotFoundError` apparaît.

- Utilisez **Python 3.10 ou plus récent** (testé avec Python 3.13).
- Dans VS Code, ouvrez un notebook, puis cliquez en **haut à droite** sur le nom du Python (« Select Kernel ») et choisissez **toujours le même**.
- Notez son emplacement (affiché dans la liste) : il servira à l'étape 2.

### 2. Installer les bibliothèques (une seule fois)

Dans un terminal ouvert dans ce dossier, avec **le même Python qu'à l'étape 1** :

```
python -m pip install -r requirements.txt
```

Si vous avez plusieurs Python, remplacez `python` par le chemin complet de celui choisi à l'étape 1 (par exemple `C:\Python313\python.exe`).

### 3. Lancer les notebooks dans l'ordre

Ils sont dans le dossier `notebooks/`. Ouvrez-les **un par un, dans l'ordre**, et cliquez sur **« Run All »** :

```
01 → 02 → 03 → 04 → 05 → 06
```

Chaque notebook utilise le résultat du précédent. Le dernier (06) régénère les cartes dans `resultats/cartes/`.

### 4. Changer un réglage

Tous les réglages (budget, poids, rayons…) sont dans **`notebooks/parametres.py`**. Après une modification : **« Restart »** puis **« Run All »** sur les notebooks concernés, sinon l'ancienne valeur reste utilisée sans message d'erreur.

Pour les détails (quel notebook relancer selon le réglage modifié), voir `notebooks/README.md`.

## Sources des données

- **Population :** INSEE, Filosofi 2021, carreaux de 200 m — https://www.insee.fr/fr/statistiques/8735162
- **Bus :** fichiers GTFS Kar'Ouest et Car Jaune (Lakehouse Fabric de l'équipe, dossier `Bronze/gtfs`)
