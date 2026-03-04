"""
Analyse temporelle des événements de pointe
"""

from datetime import datetime, timedelta
import pytz

from config import TIMEZONE


def analyse_evenements_par_offre(evenements, offres_affaires):
    """
    Analyse les événements pour chaque type d'offre.
    Détecte les événements selon la plage horaire (AM ou PM) du jour de l'événement.
    - AM : actif de 00h00 à 11h59
    - PM : actif de 12h00 à 23h59
    Retourne un dictionnaire: {offre: (actif, liste_futurs_2jours)}
    Max 4 événements futurs.
    """
    tz = pytz.timezone(TIMEZONE)
    now = datetime.now(tz)
    
    # Limite : 2 jours dans le futur
    limite_futur = now + timedelta(days=2)

    resultats = {}

    for offre in offres_affaires:
        actif = None
        futurs = []  # Liste des événements futurs

        for e in evenements:
            if e.get("offre") != offre:
                continue

            try:
                debut = datetime.fromisoformat(e["datedebut"]).astimezone(tz)
                plage = e.get("plagehoraire", "")
            except Exception:
                continue

            # Vérifier si on est le jour de l'événement
            if debut.date() == now.date():
                # Détection selon la plage horaire
                if plage == "AM":
                    # AM : actif si maintenant entre 00h00 et 11h59
                    if 0 <= now.hour < 12:
                        actif = e
                        break
                elif plage == "PM":
                    # PM : actif si maintenant entre 12h00 et 23h59
                    if 12 <= now.hour < 24:
                        actif = e
                        break

            # Collecter les événements futurs dans les 2 prochains jours
            if debut > now and debut <= limite_futur:
                futurs.append(e)
        
        # Trier les événements futurs par date de début
        futurs.sort(key=lambda x: datetime.fromisoformat(x["datedebut"]))
        
        # Garder max 4 événements futurs
        futurs = futurs[:4]

        resultats[offre] = (actif, futurs)

    return resultats
