# CI / GitLab CI

Ce fichier décrit les variables CI et l'utilisation du pipeline défini dans `.gitlab-ci.yml`.

Jobs principaux
- `test`: installe les dépendances et lance `pytest` (génère `reports/junit.xml`).
- `build`: construit et pousse l'image Docker vers le registre GitLab (`$CI_REGISTRY_IMAGE`).


Variables CI attendues (à définir dans Settings → CI / CD → Variables)
- `CI_REGISTRY_USER`: (souvent configuré automatiquement) nom d'utilisateur du registre.
- `CI_REGISTRY_PASSWORD`: mot de passe du registre (ou token). Utilisé pour `docker login`.
- `CI_REGISTRY_IMAGE`: nom complet de l'image (ex: `registry.gitlab.com/<group>/<project>`). Défini automatiquement si vous utilisez le Container Registry.
- `PROD_SSH_PRIVATE_KEY`: clé privée SSH (format PEM) pour se connecter au serveur de production. Marquer comme `Protected` et `Masked`.
- `PROD_SERVER`: adresse IP ou hostname du serveur de production.
- `PROD_SSH_USER`: utilisateur SSH sur le serveur de production.
- `PROD_SSH_PORT`: port SSH si différent de 22 (optionnel).


Tester localement
- Exécuter les tests unitaires localement:

```bash
python -m venv .venv
source .venv/bin/activate  # ou .venv\Scripts\activate sur Windows
pip install -r requirements.txt
pytest -q
```

Sécurité
- Ne stockez jamais la clé privée dans le dépôt. Utilisez les Variables GitLab protégées.
- Restreignez le déploiement (`when: manual`) et protégez la branche `main`/`master`.

Si vous voulez, j'adapte le chemin `docker-compose` et les commandes SSH à votre configuration serveur; fournissez le `PROD_SERVER` et le chemin cible.
