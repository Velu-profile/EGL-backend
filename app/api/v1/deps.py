# from fastapi import Depends
# from supabase import Client

# from app.core.security import get_current_user
from app.services.budget import BudgetService
from app.services.expense import ExpenseService
# from app.core.config import settings

def get_budget_service() -> BudgetService:
    from app.main import supabase
    return BudgetService(supabase)

def get_expense_service() -> ExpenseService:
    from app.main import supabase
    return ExpenseService(supabase)