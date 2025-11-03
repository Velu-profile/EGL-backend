from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query

from app.models.budget import Budget, BudgetCreate, BudgetUpdate
from app.services.budget import BudgetService
from app.api.v1.deps import get_budget_service
from app.core.security import get_current_user
from supabase import Client

router = APIRouter()

@router.get("/", response_model=List[Budget])
async def read_budgets(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user = Depends(get_current_user),
    budget_service: BudgetService = Depends(get_budget_service)
):
    """
    Retrieve budgets for the current user.
    """
    return await budget_service.get_budgets(
        user_id=current_user.id,
        skip=skip,
        limit=limit
    )

@router.get("/{budget_id}", response_model=Budget)
async def read_budget(
    budget_id: UUID,
    current_user = Depends(get_current_user),
    budget_service: BudgetService = Depends(get_budget_service)
):
    """
    Get a specific budget by ID.
    """
    budget = await budget_service.get_budget(current_user.id, budget_id)
    if not budget:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Budget not found"
        )
    return budget

@router.post("/", response_model=Budget, status_code=status.HTTP_201_CREATED)
async def create_budget(
    budget: BudgetCreate,
    current_user = Depends(get_current_user),
    budget_service: BudgetService = Depends(get_budget_service)
):
    """
    Create a new budget.
    """
    return await budget_service.create_budget(current_user.id, budget)

@router.put("/{budget_id}", response_model=Budget)
async def update_budget(
    budget_id: UUID,
    budget: BudgetUpdate,
    current_user = Depends(get_current_user),
    budget_service: BudgetService = Depends(get_budget_service)
):
    """
    Update a budget.
    """
    updated_budget = await budget_service.update_budget(
        current_user.id, budget_id, budget
    )
    if not updated_budget:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Budget not found"
        )
    return updated_budget

@router.delete("/{budget_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_budget(
    budget_id: UUID,
    current_user = Depends(get_current_user),
    budget_service: BudgetService = Depends(get_budget_service)
):
    """
    Delete a budget.
    """
    success = await budget_service.delete_budget(current_user.id, budget_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Budget not found"
        )