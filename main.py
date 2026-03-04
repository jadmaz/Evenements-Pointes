"""
Point d'entrée principal pour le serveur Modbus Hydro-Québec Affaires
"""

from modbus_server import HydroAffairesModbus


def main():
    """Lance le serveur Modbus"""
    print("\n==============================================")
    print(" HYDRO-QUÉBEC – CLIENTÈLE AFFAIRES → MODBUS ")
    print("==============================================")
    print("Ctrl+C pour arrêter\n")

    server = HydroAffairesModbus()
    server.start()


if __name__ == "__main__":
    main()
