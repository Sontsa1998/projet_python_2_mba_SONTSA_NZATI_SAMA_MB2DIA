"""Setup configuration for Transaction API."""

from setuptools import setup, find_packages

setup(
    name="transaction-api",
    version="1.0.0",
    description="FastAPI application for transaction analysis",
    author="Christian - Stéphane - Brenda",
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=[
        "fastapi==0.104.1",
        "uvicorn==0.24.0",
        "pydantic==2.5.0",
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
        ],
    },
)