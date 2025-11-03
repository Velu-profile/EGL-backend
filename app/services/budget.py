from typing import List, Optional
from uuid import UUID
from supabase import Client
from fastapi import HTTPException, status

from app.models.budget import Budget, BudgetCreate, BudgetUpdate

class BudgetService:
    def __init__(self, supabase: Client):
        self.supabase = supabase
    
    async def get_budgets(self, user_id: str, skip: int = 0, limit: int = 100) -> List[Budget]:
        response = (
            self.supabase.table("budgets")
            .select("*")
            .eq("user_id", user_id)
            .range(skip, skip + limit - 1)
            .execute()
        )
        return [Budget(**item) for item in response.data]
    
    async def get_budget(self, user_id: str, budget_id: UUID) -> Optional[Budget]:
        response = (
            self.supabase.table("budgets")
            .select("*")
            .eq("id", budget_id)
            .eq("user_id", user_id)
            .execute()
        )
        
        if not response.data:
            return None
        
        return Budget(**response.data[0])
    
    async def create_budget(self, user_id: str, budget: BudgetCreate) -> Budget:
        budget_data = budget.dict()
        budget_data["user_id"] = user_id
        
        response = (
            self.supabase.table("budgets")
            .insert(budget_data)
            .execute()
        )
        
        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to create budget"
            )
        
        return Budget(**response.data[0])
    
    async def update_budget(self, user_id: str, budget_id: UUID, budget: BudgetUpdate) -> Optional[Budget]:
        # First verify the budget belongs to the user
        existing_budget = await self.get_budget(user_id, budget_id)
        if not existing_budget:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Budget not found"
            )
        
        update_data = budget.dict(exclude_unset=True)
        
        response = (
            self.supabase.table("budgets")
            .update(update_data)
            .eq("id", budget_id)
            .eq("user_id", user_id)
            .execute()
        )
        
        if not response.data:
            return None
        
        return Budget(**response.data[0])
    
    async def delete_budget(self, user_id: str, budget_id: UUID) -> bool:
        # First verify the budget belongs to the user
        existing_budget = await self.get_budget(user_id, budget_id)
        if not existing_budget:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Budget not found"
            )
        
        response = (
            self.supabase.table("budgets")
            .delete()
            .eq("id", budget_id)
            .eq("user_id", user_id)
            .execute()
        )
        
        return len(response.data) > 0