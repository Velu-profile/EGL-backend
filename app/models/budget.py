from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID

class BudgetBase(BaseModel):
    client_name: str
    annual_budget: float
    reduced_budget: Optional[float] = None
    budget_received_date: Optional[datetime] = None
    budget_from: Optional[str] = None

class BudgetCreate(BudgetBase):
    pass

class BudgetUpdate(BaseModel):
    client_name: Optional[str] = None
    annual_budget: Optional[float] = None
    reduced_budget: Optional[float] = None
    budget_received_date: Optional[datetime] = None
    budget_from: Optional[str] = None

class Budget(BudgetBase):
    id: UUID
    user_id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class EmployeeRole(BaseModel):
    description: str
    hours_per_week: float
    hourly_rate: float
    weekly_pay: float

class Contractor(BaseModel):
    description: str
    hours_per_week: float
    hourly_rate: float
    weekly_pay: float

class PurchaseItem(BaseModel):
    purchased_from: str
    purpose: str
    value: float
    gst_included: bool
    annual_cost: float