# Index de Documentation - Transaction API

##  Accès Rapide

### Pour Commencer
- **[SETUP_COMPLETE.md](SETUP_COMPLETE.md)** -  Résumé final et prochaines étapes
- **[QUICKSTART.md](QUICKSTART.md)** -  Guide de démarrage rapide
- **[PACKAGING_README.md](PACKAGING_README.md)** -  README du packaging

### Installation et Configuration
- **[INSTALLATION.md](INSTALLATION.md)** -  Guide d'installation détaillé
- **[PACKAGE_INFO.md](PACKAGE_INFO.md)** -  Information complète du package
- **[VERIFY_PACKAGING.md](VERIFY_PACKAGING.md)** - Checklist de vérification

### Déploiement et Production
- **[DEPLOYMENT.md](DEPLOYMENT.md)** -  Guide de déploiement complet
- **[PACKAGING_SUMMARY.md](PACKAGING_SUMMARY.md)** - Résumé du packaging

### Documentation Principale
- **[README.md](README.md)** -  Documentation principale du projet

## Fichiers de Configuration

### Configuration du Packaging
```
setup.py              - Configuration setuptools
pyproject.toml        - Configuration moderne PEP 517/518
MANIFEST.in           - Fichiers à inclure dans le package
tox.ini               - Configuration pour tests multi-versions
Makefile              - Commandes courantes
```

### Fichiers de Projet
```
LICENSE               - Licence MIT
requirements.txt      - Dépendances du projet
.gitignore            - Fichiers à ignorer
```

##  Commandes Courantes

### Installation
```bash
# Installation simple
pip install -e .

# Installation avec développement
pip install -e ".[dev]"

# Installation complète
pip install -e ".[dev,ui]"
```

### Tests
```bash
# Tous les tests
pytest

# Avec couverture
pytest --cov=transaction_api --cov-report=html

# Tests spécifiques
pytest tests/unit/
pytest tests/integration/
pytest tests/properties/
```

### Qualité du Code
```bash
# Linting
flake8 transaction_api tests

# Formatage
black transaction_api tests
isort transaction_api tests

# Type checking
mypy transaction_api
```

### Exécution
```bash
# Démarrer l'API
uvicorn transaction_api.main:app --reload

# Démarrer l'interface
streamlit run app.py

# Utiliser les commandes Make
make run              # Démarrer l'API
make run-ui           # Démarrer Streamlit
```

## 📚 Structure de la Documentation

### Par Cas d'Usage

#### Je veux installer le package
1. Lire: [INSTALLATION.md](INSTALLATION.md)
2. Exécuter: `pip install -e ".[dev,ui]"`
3. Vérifier: [VERIFY_PACKAGING.md](VERIFY_PACKAGING.md)

#### Je veux démarrer rapidement
1. Lire: [QUICKSTART.md](QUICKSTART.md)
2. Lire: [SETUP_COMPLETE.md](SETUP_COMPLETE.md)
3. Exécuter: `make run`


---

**Dernière mise à jour:** 2024
**Version:** 1.0.0
**Auteurs:** Christian SONTSA, Stéphane NZATI, Brenda Camélia Sama
