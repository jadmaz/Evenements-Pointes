"""
Utilitaires pour la conversion de données Modbus
"""


def datetime_to_registers(dt):
    """
    Convertit un datetime en composants séparés (date seulement) :
    [jour, mois, année]
    """
    if dt is None:
        return [0, 0, 0]
    
    return [
        dt.day,      # 1-31
        dt.month,    # 1-12
        dt.year      # 2025, 2026...
    ]
