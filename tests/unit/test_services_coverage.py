"""Unit tests to improve service coverage."""

import pytest
from transaction_api.repository import TransactionRepository
from transaction_api.services.customer_service import CustomerService
from transaction_api.services.fraud_service import FraudService
from transaction_api.services.statistics_service import StatisticsService
from transaction_api.services.health_service import HealthService
from transaction_api.services.transaction_service import TransactionService
