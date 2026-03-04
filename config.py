"""
Configuration centralisée pour le serveur Modbus Hydro-Québec Affaires
"""
# CONFIGURATION GÉNÉRALE
# ============================================================
TIMEZONE = "America/Montreal"
MODBUS_HOST = "0.0.0.0"
MODBUS_PORT = 5020
POLLING_INTERVAL = 300  # 5 minutes

# ============================================================
# URLS API HYDRO-QUÉBEC
# ============================================================
API_EVENTS = (
    "https://donnees.hydroquebec.com/api/explore/v2.1/"
    "catalog/datasets/evenements-pointe/records"
)

API_OFFRES = (
    "https://donnees.hydroquebec.com/api/explore/v2.1/"
    "catalog/datasets/evenements-de-pointe-offres-disponibles/records"
)

# ============================================================
# FICHIER DE MAPPING
# ============================================================
MAPPING_FILE = "modbus_mapping.json"
