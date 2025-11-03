from typing import List, Optional
from uuid import UUID
from supabase import Client
from fastapi import HTTPException, status

from app.models.expense import Expense, ExpenseCreate, ExpenseUpdate

class ExpenseService:
    def __init__(self, supabase: Client):
        self.supabase = supabase
    
    async def get_expenses(
        self, 
        user_id: str, 
        budget_id: Optional[UUID] = None,
        skip: int = 0, 
        limit: int = 100
    ) -> List[Expense]:
        query = (
            self.supabase.table("expenses")
            .select("*")
            .eq("user_id", user_id)
        )
        
        if budget_id:
            query = query.eq("budget_id", budget_id)
        
        response = query.range(skip, skip + limit - 1).execute()
        return [Expense(**item) for item in response.data]
    
    async def get_expense(self, user_id: str, expense_id: UUID) -> Optional[Expense]:
        response = (
            self.supabase.table("expenses")
            .select("*")
            .eq("id", expense_id)
            .eq("user_id", user_id)
            .execute()
        )
        
        if not response.data:
            return None
        
        return Expense(**response.data[0])
    
    async def create_expense(self, user_id: str, expense: ExpenseCreate) -> Expense:
        expense_data = expense.dict()
        expense_data["user_id"] = user_id
        
        response = (
            self.supabase.table("expenses")
            .insert(expense_data)
            .execute()
        )
        
        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to create expense"
            )
        
        return Expense(**response.data[0])
    
    async def update_expense(
        self, 
        user_id: str, 
        expense_id: UUID, 
        expense: ExpenseUpdate
    ) -> Optional[Expense]:
        existing_expense = await self.get_expense(user_id, expense_id)
        if not existing_expense:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Expense not found"
            )
        
        update_data = expense.dict(exclude_unset=True)
        
        response = (
            self.supabase.table("expenses")
            .update(update_data)
            .eq("id", expense_id)
            .eq("user_id", user_id)
            .execute()
        )
        
        if not response.data:
            return None
        
        return Expense(**response.data[0])
    
    async def delete_expense(self, user_id: str, expense_id: UUID) -> bool:
        existing_expense = await self.get_expense(user_id, expense_id)
        if not existing_expense:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Expense not found"
            )
        
        response = (
            self.supabase.table("expenses")
            .delete()
            .eq("id", expense_id)
            .eq("user_id", user_id)
            .execute()
        )
        
        return len(response.data) > 0