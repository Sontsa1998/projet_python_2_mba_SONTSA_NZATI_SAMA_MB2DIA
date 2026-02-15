@echo off
REM Script d'installation pour Transaction API (Windows)
REM Usage: install.bat [option]
REM Options: dev, ui, all, clean

setlocal enabledelayedexpansion

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║         Installation de Transaction API                   ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

REM Vérifier Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Erreur: Python n'est pas installé ou n'est pas dans le PATH
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✓ Python %PYTHON_VERSION% détecté
echo.

REM Déterminer l'option d'installation
set INSTALL_OPTION=%1
if "%INSTALL_OPTION%"=="" set INSTALL_OPTION=default

if "%INSTALL_OPTION%"=="dev" (
    echo 📦 Installation avec dépendances de développement...
    pip install -e ".[dev]"
    echo ✓ Installation complète avec dev
) else if "%INSTALL_OPTION%"=="ui" (
    echo 📦 Installation avec interface utilisateur...
    pip install -e ".[ui]"
    echo ✓ Installation complète avec UI
) else if "%INSTALL_OPTION%"=="all" (
    echo 📦 Installation complète (dev + ui)...
    pip install -e ".[dev,ui]"
    echo ✓ Installation complète
) else if "%INSTALL_OPTION%"=="clean" (
    echo 🧹 Nettoyage des fichiers générés...
    for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
    for /d /r . %%d in (.pytest_cache) do @if exist "%%d" rd /s /q "%%d"
    for /d /r . %%d in (.mypy_cache) do @if exist "%%d" rd /s /q "%%d"
    for /d /r . %%d in (htmlcov) do @if exist "%%d" rd /s /q "%%d"
    del /s /q .coverage >nul 2>&1
    del /s /q *.pyc >nul 2>&1
    del /s /q *.pyo >nul 2>&1
    if exist build rd /s /q build
    if exist dist rd /s /q dist
    for /d %%d in (*.egg-info) do rd /s /q "%%d"
    echo ✓ Nettoyage terminé
) else (
    echo 📦 Installation standard...
    pip install -e .
    echo ✓ Installation standard complète
)

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║              Installation réussie! ✓                       ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo Prochaines étapes:
echo   1. Démarrer l'API:      uvicorn transaction_api.main:app --reload
echo   2. Lancer l'interface:  streamlit run app.py
echo   3. Exécuter les tests:  pytest
echo.
echo Pour plus d'informations, consultez INSTALLATION.md
echo.
pause
