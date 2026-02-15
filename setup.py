"""Configuration de setup pour l'API Transaction.

Ce module configure le packaging et l'installation du module transaction_api
en tant que package Python installable avec toutes les dépendances nécessaires.
"""

from setuptools import setup, find_packages

setup(
    name="transaction-api",
    version="1.0.0",
    description="Application FastAPI pour l'analyse des transactions, la détection de fraude et les informations sur les clients",
    long_description=open("README.md", encoding="utf-8").read() if __name__ == "__main__" else "",
    long_description_content_type="text/markdown",
    author="Christian SONTSA - Stéphane NZATI - Brenda Camélia Sama",
    author_email="contact@transaction-api.local",
    url="https://github.com/yourusername/transaction-api",
    license="MIT",
    packages=find_packages(exclude=["tests", "tests.*", "*.tests"]),
    include_package_data=True,
    python_requires=">=3.10",
    install_requires=[
        "fastapi==0.128.8",
        "uvicorn==0.30.0",
        "pydantic==2.12.5",
        "pydantic-core==2.41.5",
        "starlette==0.52.1",
        "pandas==2.2.0",
        "numpy==1.26.1",
        "python-multipart==0.0.6",
        "typing-extensions==4.15.0",
        "anyio==3.7.1",
        "httpcore",
        "certifi==2024.2.2",
        "idna==3.11",
        "numpydoc",
        "pydocstyle",
        "flake8-docstrings",
        "sniffio==1.3.1",
    ],
    extras_require={
        "dev": [
            "pytest==7.4.3",
            "pytest-cov==4.1.0",
            "hypothesis==6.88.0",
            "black==23.12.0",
            "flake8==6.1.0",
            "isort==5.13.2",
            "mypy==1.7.1",
            "numpydoc",
            "pydocstyle",
            "flake8-docstrings",
        ],
        "ui": [
            "streamlit==1.40.0",
            "plotly==5.24.1",
            "requests==2.32.3",
        ],
    },
    entry_points={
        "console_scripts": [
            "transaction-api=transaction_api.main:app",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: French",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Office/Business :: Financial",
    ],
    keywords="transaction api fraud detection analytics fastapi",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/transaction-api/issues",
        "Source": "https://github.com/yourusername/transaction-api",
    },
)