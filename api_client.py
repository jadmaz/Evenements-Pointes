"""
Client API pour récupérer les offres et événements Hydro-Québec
"""

import requests
from datetime import date

from config import API_EVENTS, API_OFFRES


# ============================================================
# API HYDRO – OFFRES
# ============================================================

def fetch_offres_affaires():
    """
    Retourne la liste des codes d'offres applicables
    à la clientèle AFFAIRES pour la date courante.
    Retourne: liste de noms d'offres (ordre stable pour mapping Unit ID)
    """
    today = date.today()
    offres_affaires = []

    r = requests.get(API_OFFRES, params={"limit": -1}, timeout=20)
    r.raise_for_status()

    for o in r.json().get("results", []):
        if o.get("type_clientele") != "affaires":
            continue

        debut = date.fromisoformat(o["debut"])
        fin = date.fromisoformat(o["fin"])

        if debut <= today <= fin:
            offre_nom = o["offresdisponibles"]
            if offre_nom not in offres_affaires:
                offres_affaires.append(offre_nom)

    # Tri alphabétique pour stabilité
    offres_affaires.sort()
    return offres_affaires


# ============================================================
# API HYDRO – ÉVÉNEMENTS
# ============================================================

def fetch_evenements():
    """
    Récupère tous les événements de pointe
    """
    r = requests.get(API_EVENTS, params={"limit": -1}, timeout=20)
    r.raise_for_status()
    return r.json().get("results", [])
