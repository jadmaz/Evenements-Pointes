"""
Gestion du mapping persistant entre les offres et les Unit IDs Modbus
"""

import json
from datetime import datetime
import pytz

from config import MAPPING_FILE, TIMEZONE


def load_persistent_mapping():
    """
    Charge le mapping persistant depuis le fichier JSON.
    Format: {"offre_name": unit_id, ...}
    """
    try:
        with open(MAPPING_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("mapping", {})
    except FileNotFoundError:
        return {}


def save_persistent_mapping(mapping):
    """
    Sauvegarde le mapping persistant.
    """
    data = {
        "timestamp": datetime.now(pytz.timezone(TIMEZONE)).isoformat(),
        "mapping": mapping,
        "description": "Mapping persistant Unit ID <-> Offre (ne change jamais)"
    }
    with open(MAPPING_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def update_mapping(offres_actuelles):
    """
    Met à jour le mapping en ajoutant uniquement les nouvelles offres.
    Ne supprime JAMAIS les anciennes.
    Retourne: (mapping complet, set des offres actives)
    """
    mapping = load_persistent_mapping()
    offres_actives = set(offres_actuelles)
    
    # Trouver le prochain Unit ID disponible
    if mapping:
        next_unit_id = max(mapping.values()) + 1
    else:
        next_unit_id = 1
    
    # Ajouter les nouvelles offres uniquement
    for offre in offres_actuelles:
        if offre not in mapping:
            mapping[offre] = next_unit_id
            next_unit_id += 1
    
    save_persistent_mapping(mapping)
    return mapping, offres_actives
