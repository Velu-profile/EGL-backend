from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query

from app.models.expense import Expense, ExpenseCreate, ExpenseUpdate
from app.services.expense import ExpenseService
from app.api.v1.deps import get_expense_service
from app.core.security import get_current_user

router = APIRouter()

@router.get("/", response_model=List[Expense])
async def read_expenses(
    budget_id: Optional[UUID] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user = Depends(get_current_user),
    expense_service: ExpenseService = Depends(get_expense_service)
):
    """
    Retrieve expenses for the current user.
    """
    return await expense_service.get_expenses(
        user_id=current_user.id,
        budget_id=budget_id,
        skip=skip,
        limit=limit
    )

@router.get("/{expense_id}", response_model=Expense)
async def read_expense(
    expense_id: UUID,
    current_user = Depends(get_current_user),
    expense_service: ExpenseService = Depends(get_expense_service)
):
    """
    Get a specific expense by ID.
    """
    expense = await expense_service.get_expense(current_user.id, expense_id)
    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found"
        )
    return expense

@router.post("/", response_model=Expense, status_code=status.HTTP_201_CREATED)
async def create_expense(
    expense: ExpenseCreate,
    current_user = Depends(get_current_user),
    expense_service: ExpenseService = Depends(get_expense_service)
):
    """
    Create a new expense.
    """
    return await expense_service.create_expense(current_user.id, expense)

@router.put("/{expense_id}", response_model=Expense)
async def update_expense(
    expense_id: UUID,
    expense: ExpenseUpdate,
    current_user = Depends(get_current_user),
    expense_service: ExpenseService = Depends(get_expense_service)
):
    """
    Update an expense.
    """
    updated_expense = await expense_service.update_expense(
        current_user.id, expense_id, expense
    )
    if not updated_expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found"
        )
    return updated_expense

@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_expense(
    expense_id: UUID,
    current_user = Depends(get_current_user),
    expense_service: ExpenseService = Depends(get_expense_service)
):
    """
    Delete an expense.
    """
    success = await expense_service.delete_expense(current_user.id, expense_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found"
        )