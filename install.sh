#!/bin/bash

# Script d'installation pour Transaction API
# Usage: ./install.sh [option]
# Options: dev, ui, all, clean

set -e

echo "╔════════════════════════════════════════════════════════════╗"
echo "║         Installation de Transaction API                   ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Vérifier Python
if ! command -v python3 &> /dev/null; then
    echo " Erreur: Python 3 n'est pas installé"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "✓ Python $PYTHON_VERSION détecté"

# Vérifier pip
if ! command -v pip &> /dev/null; then
    echo "Erreur: pip n'est pas installé"
    exit 1
fi

echo "✓ pip détecté"
echo ""

# Déterminer l'option d'installation
INSTALL_OPTION="${1:-default}"

case $INSTALL_OPTION in
    dev)
        echo "📦 Installation avec dépendances de développement..."
        pip install -e ".[dev]"
        echo "✓ Installation complète avec dev"
        ;;
    ui)
        echo "📦 Installation avec interface utilisateur..."
        pip install -e ".[ui]"
        echo "✓ Installation complète avec UI"
        ;;
    all)
        echo "📦 Installation complète (dev + ui)..."
        pip install -e ".[dev,ui]"
        echo "✓ Installation complète"
        ;;
    clean)
        echo "🧹 Nettoyage des fichiers générés..."
        find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
        find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
        find . -type d -name .mypy_cache -exec rm -rf {} + 2>/dev/null || true
        find . -type d -name htmlcov -exec rm -rf {} + 2>/dev/null || true
        find . -type f -name .coverage -delete
        find . -type f -name "*.pyc" -delete
        rm -rf build/ dist/ *.egg-info/
        echo "✓ Nettoyage terminé"
        ;;
    *)
        echo "📦 Installation standard..."
        pip install -e .
        echo "✓ Installation standard complète"
        ;;
esac

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║              Installation réussie! ✓                       ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "Prochaines étapes:"
echo "  1. Démarrer l'API:      uvicorn transaction_api.main:app --reload"
echo "  2. Lancer l'interface:  streamlit run app.py"
echo "  3. Exécuter les tests:  pytest"
echo ""
echo "Pour plus d'informations, consultez INSTALLATION.md"
