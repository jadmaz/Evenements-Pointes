"""
Client API pour récupérer les offres et événements Hydro-Québec
"""

import requests
from datetime import date, datetime, timedelta
import pytz

from config import API_EVENTS, API_OFFRES, TIMEZONE, USE_MOCK_DATA


def _mock_offres_affaires():
    """
    Donnees mock pour tests hors API.
    """
    return [
        "AFFAIRES-100"
    ]


def _mock_evenements():
    """
    Donnees mock pour tests hors API.
    Format compatible avec event_analyzer.py.
    """
    tz = pytz.timezone(TIMEZONE)
    now = datetime.now(tz)
    active_plage = "AM" if now.hour < 12 else "PM"

    return [
        {
            "code": "EV101",
            "offre": "AFFAIRES-100",
            "datedebut": (now + timedelta(hours=2)).isoformat(),
            "datefin": (now + timedelta(hours=4)).isoformat(),
            "plagehoraire": "AM",
        },
        {
            "code": "EV102",
            "offre": "AFFAIRES-100",
            "datedebut": (now + timedelta(hours=6)).isoformat(),
            "datefin": (now + timedelta(hours=8)).isoformat(),
            "plagehoraire": "PM",
        },
        {
            "code": "EV103",
            "offre": "AFFAIRES-100",
            "datedebut": (now + timedelta(hours=26)).isoformat(),
            "datefin": (now + timedelta(hours=28)).isoformat(),
            "plagehoraire": "AM",
        },
        {
            "code": "EV104",
            "offre": "AFFAIRES-100",
            "datedebut": (now + timedelta(hours=46)).isoformat(),
            "datefin": (now + timedelta(hours=48)).isoformat(),
            "plagehoraire": "PM",
        },
    ]


# ============================================================
# API HYDRO – OFFRES
# ============================================================

def fetch_offres_affaires():
    """
    Retourne la liste des codes d'offres applicables
    à la clientèle AFFAIRES pour la date courante.
    Retourne: liste de noms d'offres (ordre stable pour mapping Unit ID)
    """
    if USE_MOCK_DATA:
        offres_affaires = _mock_offres_affaires()
        offres_affaires.sort()
        return offres_affaires

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
    if USE_MOCK_DATA:
        return _mock_evenements()

    r = requests.get(API_EVENTS, params={"limit": -1}, timeout=20)
    r.raise_for_status()
    return r.json().get("results", [])
