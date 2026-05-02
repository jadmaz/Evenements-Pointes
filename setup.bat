@echo off
:: ============================================================
:: SETUP - HYDRO-QUEBEC GDP MONITOR
:: ============================================================

echo.
echo ============================================================
echo   HYDRO-QUEBEC GDP MONITOR - SETUP
echo ============================================================
echo.

:: Vérifier Python
echo [1/3] Verification de Python...
python --version >nul 2>&1
if %errorLevel% neq 0 (
    echo.
    echo   Python n'est pas installe!
    echo   Ouverture de la page de telechargement...
    echo.
    start https://www.python.org/downloads/
    echo   Installez Python, puis relancez ce script.
    echo.
    pause
    exit /b 1
)
for /f "tokens=*" %%i in ('python --version') do echo   OK: %%i
echo.

:: Créer venv
echo [2/3] Creation de l'environnement virtuel...
if exist "venv" (
    echo   venv existe deja, skip...
) else (
    python -m venv venv
)
echo   OK
echo.

:: Installer dépendances
echo [3/3] Installation des dependances...
call venv\Scripts\activate.bat
pip install --quiet --upgrade pip
pip install --quiet -r requirements.txt
echo   OK: dependances installees depuis requirements.txt
echo.

:: Generer .env par defaut
echo [4/4] Generation du fichier .env...
if exist ".env" (
    echo   .env existe deja, skip...
) else (
    (
        echo # Configuration Hydro-Quebec Modbus
        echo TIMEZONE=America/Montreal
        echo MODBUS_HOST=0.0.0.0
        echo MODBUS_PORT=5020
        echo POLLING_INTERVAL=300
        echo USE_MOCK_DATA=true
        echo API_EVENTS=https://donnees.hydroquebec.com/api/explore/v2.1/catalog/datasets/evenements-pointe/records
        echo API_OFFRES=https://donnees.hydroquebec.com/api/explore/v2.1/catalog/datasets/evenements-de-pointe-offres-disponibles/records
        echo MAPPING_FILE=modbus_mapping.json
    ) > .env
    echo   .env cree avec configuration par defaut
)
echo.

echo ============================================================
echo   SETUP TERMINE!
echo ============================================================
echo.
echo   Pour demarrer le serveur: start.bat
echo.
pause
