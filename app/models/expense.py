from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID
from enum import Enum

class ExpenseCategory(str, Enum):
    PAYROLL = "Payroll"
    MILEAGE = "Mileage"
    EXTRAS = "Extras"
    HOST_FEE = "Host Fee"

class GSTStatus(str, Enum):
    INCLUSIVE = "Inc"
    EXCLUSIVE = "Excl"

class ExpenseBase(BaseModel):
    date: datetime
    comment: str
    category: ExpenseCategory
    cost: float
    gst_status: GSTStatus
    total: float

class ExpenseCreate(ExpenseBase):
    budget_id: UUID

class ExpenseUpdate(BaseModel):
    date: Optional[datetime] = None
    comment: Optional[str] = None
    category: Optional[ExpenseCategory] = None
    cost: Optional[float] = None
    gst_status: Optional[GSTStatus] = None
    total: Optional[float] = None

class Expense(ExpenseBase):
    id: UUID
    user_id: str
    budget_id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True