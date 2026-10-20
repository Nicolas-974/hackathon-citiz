"""Paramètres partagés par tous les notebooks du pipeline.

Principe du brief : pour changer de territoire (Nord, Sud, Guadeloupe…) ou passer
sur Fabric, on ne modifie QUE ce fichier. La logique des notebooks reste identique.
"""
from pathlib import Path

# --- Chemins ------------------------------------------------------------------
# En local : le dossier data/ du projet.
# Sur Fabric : RACINE = Path("/lakehouse/default/Files") (et BRONZE = RACINE / "Bronze").
RACINE = Path(__file__).resolve().parent.parent / "data"
BRONZE = RACINE / "bronze"
SILVER = RACINE / "silver"
GTFS_DIR = BRONZE / "gtfs"
INSEE_CSV = BRONZE / "insee" / "carreaux_200m_reun.csv"
RESULTATS_DIR = RACINE.parent / "resultats"
CARTES_DIR = RESULTATS_DIR / "cartes"

# Fond des cartes : gris clair Esri, sans clé, testé le 20/10/2026.
# Écartés : "OpenStreetMap" (403 pour les pages ouvertes en file:///, pas d'en-tête Referer)
# et "CartoDB positron" (tuile "API KEY REQUIRED").
FOND_CARTE = "Esri.WorldGrayCanvas"

# --- Périmètre étudié -----------------------------------------------------------
# Choix du périmètre, pas une règle de score : pour le Nord, on change cette liste.
TERRITOIRE = "Ouest (TCO)"
COMMUNES = {
    "97407": "Le Port",
    "97408": "La Possession",
    "97413": "Saint-Leu",
    "97415": "Saint-Paul",
    "97423": "Trois-Bassins",
}

# Réseaux GTFS pris en compte : nom affiché -> sous-dossier de GTFS_DIR.
# Un réseau dont le dossier est absent est ignoré (avec un message), pas bloquant.
RESEAUX = {
    "Kar'Ouest": "karouest",
    "Car Jaune": "car_jaune",
}

# Jour de référence pour compter les passages : un mardi ordinaire (AAAAMMJJ, format GTFS).
DATE_REF = 20261020

# --- Carreaux INSEE -------------------------------------------------------------
CRS_CARREAUX = "EPSG:2975"   # projection officielle de La Réunion, en mètres
TAILLE_CARREAU_M = 200

# --- Accessibilité au bus -------------------------------------------------------
RAYON_TERRE_M = 6_371_000
RAYON_5MIN_M = 400           # ~5 min à pied (5 km/h), à vol d'oiseau
SEUIL_ISOLE_M = 2_000        # au-delà : carreau "isolé" (indice d'absence de route, à vérifier)

# Niveaux d'offre selon les passages de bus à moins de 5 min.
# Seuils = quartiles mesurés sur l'Ouest (Kar'Ouest seul : 32 / 95 / 212 passages).
# Ils restent fixes pour pouvoir comparer réseaux et territoires entre eux.
SEUILS_OFFRE = [-1, 0, 31, 94, 211, float("inf")]
NIVEAUX_OFFRE = ["Aucun arrêt", "Très faible", "Faible", "Correcte", "Forte"]

# --- Valeur d'un emplacement ----------------------------------------------------
# Poids du besoin selon l'offre de bus actuelle : des CHOIX explicites, modifiables.
POIDS_BESOIN = {
    "Aucun arrêt": 1.0,
    "Très faible": 1.0,
    "Faible": 0.6,
    "Correcte": 0.3,
    "Forte": 0.1,
}
RAYON_STATION_M = 500        # hypothèse : distance acceptée à pied jusqu'à une voiture (à sourcer)

# --- Optimisation sous budget ---------------------------------------------------
BUDGET_EUR = 300_000
COUT_STATION_EUR = 30_000    # PROVISOIRE, NON SOURCÉ : à remplacer par le chiffrage de l'équipe
