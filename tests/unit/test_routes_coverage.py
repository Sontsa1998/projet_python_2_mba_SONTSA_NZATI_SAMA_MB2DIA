"""Unit tests to improve route coverage."""

import pytest
from fastapi.testclient import TestClient
from transaction_api.main import app
from transaction_api import app_context
from transaction_api.repository import TransactionRepository


