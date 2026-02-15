.PHONY: help install install-dev install-ui install-all clean test test-cov lint format type run run-ui docs

help:
	@echo "Transaction API - Commandes disponibles"
	@echo "========================================"
	@echo "make install          - Installer le package"
	@echo "make install-dev      - Installer avec les dépendances de développement"
	@echo "make install-ui       - Installer avec les dépendances de l'interface"
	@echo "make install-all      - Installer avec toutes les dépendances"
	@echo "make clean            - Nettoyer les fichiers générés"
	@echo "make test             - Exécuter les tests"
	@echo "make test-cov         - Exécuter les tests avec couverture"
	@echo "make lint             - Vérifier la qualité du code"
	@echo "make format           - Formater le code"
	@echo "make type             - Vérifier les types"
	@echo "make run              - Démarrer l'API"
	@echo "make run-ui           - Démarrer l'interface Streamlit"
	@echo "make docs             - Générer la documentation"

install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"

install-ui:
	pip install -e ".[ui]"

install-all:
	pip install -e ".[dev,ui]"

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .mypy_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name htmlcov -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .tox -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name .coverage -delete
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	rm -rf build/ dist/ *.egg-info/

test:
	pytest tests/

test-cov:
	pytest --cov=transaction_api --cov-report=html --cov-report=term-missing tests/

lint:
	flake8 transaction_api tests
	black --check transaction_api tests
	isort --check-only transaction_api tests

format:
	black transaction_api tests
	isort transaction_api tests

type:
	mypy transaction_api

run:
	uvicorn transaction_api.main:app --reload --host 0.0.0.0 --port 8000

run-ui:
	streamlit run app.py

docs:
	@echo "Génération de la documentation..."
	@echo "Documentation disponible dans le README.md"
