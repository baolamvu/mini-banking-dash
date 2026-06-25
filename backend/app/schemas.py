from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class TransactionCreate(BaseModel):
    type: Literal["credit", "debit", "transfer"]
    amount: float = Field(gt=0)
    description: str = Field(min_length=1, max_length=255)
    account_from: str = Field(min_length=1, max_length=50)
    account_to: str = Field(min_length=1, max_length=50)


class TransactionResponse(BaseModel):
    id: int
    type: str
    amount: float
    description: str
    account_from: str
    account_to: str
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}


class StatsResponse(BaseModel):
    total_transactions: int
    total_credit: float
    total_debit: float
    net_balance: float
