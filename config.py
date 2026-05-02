"""
Configuration centralisée pour le serveur Modbus Hydro-Québec Affaires
"""
import os

from dotenv import load_dotenv


load_dotenv()


def _get_bool_env(name, default=False):
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _get_int_env(name, default):
    value = os.getenv(name)
    if value is None:
        return default
    try:
        return int(value)
    except ValueError:
        return default


# CONFIGURATION GÉNÉRALE
# ============================================================
TIMEZONE = os.getenv("TIMEZONE", "America/Montreal")
MODBUS_HOST = os.getenv("MODBUS_HOST", "0.0.0.0")
MODBUS_PORT = _get_int_env("MODBUS_PORT", 5020)
POLLING_INTERVAL = _get_int_env("POLLING_INTERVAL", 300)  # 5 minutes
USE_MOCK_DATA = _get_bool_env("USE_MOCK_DATA", False)

# ============================================================
# URLS API HYDRO-QUÉBEC
# ============================================================
API_EVENTS = os.getenv(
    "API_EVENTS",
    "https://donnees.hydroquebec.com/api/explore/v2.1/"
    "catalog/datasets/evenements-pointe/records",
)

API_OFFRES = os.getenv(
    "API_OFFRES",
    "https://donnees.hydroquebec.com/api/explore/v2.1/"
    "catalog/datasets/evenements-de-pointe-offres-disponibles/records",
)

# ============================================================
# FICHIER DE MAPPING
# ============================================================
MAPPING_FILE = os.getenv("MAPPING_FILE", "modbus_mapping.json")
