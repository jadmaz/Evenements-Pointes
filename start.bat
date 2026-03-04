@echo off
:: ============================================================
:: START - HYDRO-QUEBEC GDP MONITOR
:: ============================================================

if not exist "venv\Scripts\python.exe" (
    exit /b 1
)

venv\Scripts\python.exe main.py
