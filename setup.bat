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
pip install --quiet requests pytz pymodbus
echo   OK: requests, pytz, pymodbus
echo.

echo ============================================================
echo   SETUP TERMINE!
echo ============================================================
echo.
echo   Pour demarrer le serveur: start.bat
echo.
pause
