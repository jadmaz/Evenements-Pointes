"""
Serveur Modbus TCP pour Hydro-Québec Affaires
"""

import threading
import time
from datetime import datetime
import pytz

from pymodbus.server import StartTcpServer
from pymodbus.datastore import (
    ModbusSequentialDataBlock,
    ModbusServerContext,
    ModbusDeviceContext
)

from config import MODBUS_HOST, MODBUS_PORT, POLLING_INTERVAL, TIMEZONE
from api_client import fetch_offres_affaires, fetch_evenements
from mapping import update_mapping
from event_analyzer import analyse_evenements_par_offre
from modbus_utils import datetime_to_registers


class HydroAffairesModbus:
    """
    Serveur Modbus qui gère les événements de pointe Hydro-Québec pour la clientèle Affaires
    """

    def __init__(self):
        self.running = False

        # Chargé au démarrage
        offres_actuelles = fetch_offres_affaires()
        
        # Charger/mettre à jour le mapping persistant
        self.offre_to_unit, self.offres_actives = update_mapping(offres_actuelles)

        # Créer les devices Modbus pour TOUTES les offres (actuelles ET historiques)
        devices = {}
        for offre, unit_id in self.offre_to_unit.items():
            devices[unit_id] = ModbusDeviceContext(
                hr=ModbusSequentialDataBlock(0, [0] * 40),
                ir=ModbusSequentialDataBlock(0, [0] * 40)
            )

        self.context = ModbusServerContext(
            devices=devices,
            single=False
        )

    def update_registers(self):
        """
        Met à jour les registres Modbus avec les données des événements
        """
        tz = pytz.timezone(TIMEZONE)
        now = datetime.now(tz)

        try:
            evenements = fetch_evenements()
            # Analyser uniquement les offres actives
            resultats = analyse_evenements_par_offre(
                evenements, list(self.offres_actives)
            )
        except Exception:
            resultats = {}

        # Mise à jour de chaque Unit ID (TOUS, même les inactifs)
        for offre, unit_id in self.offre_to_unit.items():
            # Vérifier si l'offre existe encore dans l'API
            offre_existe = 0 if offre in self.offres_actives else 1
            
            # Récupérer les données seulement si l'offre est active
            if offre_existe == 0:
                actif, futurs = resultats.get(offre, (None, []))
            else:
                actif, futurs = None, []

            # Registre 0 – État de pointe (AM/PM selon plage horaire)
            etat = 1 if actif else 0
            
            # Registre 1 – Offre existe dans l'API (0=oui, 1=non)
            existe = offre_existe
            
            # Registre 2 – Nombre d'événements futurs (0-4)
            nb_futurs = len(futurs)

            # Registres 3-5 – Date événement actuel (si actif)
            debut_dt = None
            plage_actuel = 0  # 0=aucun, 1=AM, 2=PM
            if actif:
                debut_dt = datetime.fromisoformat(actif["datedebut"]).astimezone(tz)
                plage_str = actif.get("plagehoraire", "")
                plage_actuel = 1 if plage_str == "AM" else 2 if plage_str == "PM" else 0
            date_regs = datetime_to_registers(debut_dt)
            
            values = [etat, existe, nb_futurs] + date_regs + [plage_actuel]
            
            # Ajouter les événements futurs (max 4) - date + plage
            for futur in futurs:
                debut_futur = datetime.fromisoformat(futur["datedebut"]).astimezone(tz)
                plage_str = futur.get("plagehoraire", "")
                plage_futur = 1 if plage_str == "AM" else 2 if plage_str == "PM" else 0
                values += datetime_to_registers(debut_futur) + [plage_futur]
            
            # Compléter avec des zéros si moins de 4 événements
            # 3 + 3 + 1 + (4 futurs × 4 registres) = 23 registres
            while len(values) < 23:
                values.append(0)

            # Mise à jour HR (3) et IR (4)
            device = self.context[unit_id]
            device.setValues(3, 0, values)
            device.setValues(4, 0, values)

    def loop(self):
        """
        Boucle de mise à jour périodique des registres
        """
        while self.running:
            self.update_registers()
            time.sleep(POLLING_INTERVAL)

    def start(self):
        """
        Démarre le serveur Modbus et la boucle de mise à jour
        """
        self.running = True
        self.update_registers()

        threading.Thread(target=self.loop, daemon=True).start()

        StartTcpServer(
            context=self.context,
            address=(MODBUS_HOST, MODBUS_PORT)
        )
