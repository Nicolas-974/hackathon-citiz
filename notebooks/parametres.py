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
INSEE_CSV = BRONZE / "insee" / "carreaux_200m_reun.csv"   # même fichier : il couvre toute l'île
RESULTATS_DIR = RACINE.parent / "resultats"
CARTES_DIR = RESULTATS_DIR / "cartes"

# Fond des cartes : gris clair Esri, sans clé, testé le 20/10/2026.
# Écartés : "OpenStreetMap" (403 pour les pages ouvertes en file:///, pas d'en-tête Referer)
# et "CartoDB positron" (tuile "API KEY REQUIRED").
FOND_CARTE = "Esri.WorldGrayCanvas"

# --- Périmètre étudié -----------------------------------------------------------
# Choix du périmètre, pas une règle de score.
# Toute l'île : les 24 communes. Pour revenir à un zoom, ne garder que les communes voulues
# (Ouest/TCO : 97407, 97408, 97413, 97415, 97423).
TERRITOIRE = "La Réunion (île entière)"
COMMUNES = {
    # Nord - CINOR
    "97411": "Saint-Denis",
    "97418": "Sainte-Marie",
    "97420": "Sainte-Suzanne",
    # Est - CIREST
    "97402": "Bras-Panon",
    "97406": "La Plaine-des-Palmistes",
    "97409": "Saint-André",
    "97410": "Saint-Benoît",
    "97419": "Sainte-Rose",
    "97421": "Salazie",
    # Ouest - TCO
    "97407": "Le Port",
    "97408": "La Possession",
    "97413": "Saint-Leu",
    "97415": "Saint-Paul",
    "97423": "Trois-Bassins",
    # Sud-Ouest - CIVIS
    "97401": "Les Avirons",
    "97404": "L'Étang-Salé",
    "97405": "Petite-Île",
    "97414": "Saint-Louis",
    "97416": "Saint-Pierre",
    "97424": "Cilaos",
    # Sud - CASUD
    "97403": "Entre-Deux",
    "97412": "Saint-Joseph",
    "97417": "Saint-Philippe",
    "97422": "Le Tampon",
}

# Réseaux GTFS pris en compte : nom affiché -> sous-dossier de GTFS_DIR.
# Un réseau dont le dossier est absent est ignoré (avec un message), pas bloquant.
# Un seul dossier par réseau : seuls les dossiers listés ici sont lus, donc l'ancienne
# copie manuelle "karouest" peut rester sur le disque sans être comptée deux fois.
RESEAUX = {
    "Car Jaune": "car_jaune",                         # interurbain, toute l'île
    "Kar'Ouest": "kar_ouest",                         # TCO (version téléchargée automatiquement)
    "Citalis": "citalis_bus",                         # CINOR
    "Téléphérique Citalis": "citalis_telepherique",   # CINOR (Papang, Saint-Denis)
    "Estival": "estival",                             # CIREST
    "Alternéo": "alterneo",                           # CIVIS
    "Car Sud": "car_sud",                             # CASUD
}

# Jour de référence pour compter les passages : un mardi ordinaire (AAAAMMJJ, format GTFS).
# ⚠️ Il doit être couvert par le calendrier des 7 réseaux : vérifier la sortie du notebook 01
# (un réseau à 0 service ferait apparaître toute son intercommunalité "sans bus").
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
# Budget inchangé (10 stations à 30 k€) : sur l'île entière, la sélection se répartit
# désormais entre les territoires. À ajuster en démo dans le notebook 05.
BUDGET_EUR = 300_000
COUT_STATION_EUR = 30_000    # PROVISOIRE, NON SOURCÉ : à remplacer par le chiffrage de l'équipe