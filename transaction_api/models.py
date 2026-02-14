"""Pydantic models for the Transaction API."""

from datetime import date as date_type
from datetime import datetime
from typing import Generic, List, Optional, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


