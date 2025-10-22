from sqlalchemy.orm import Session
from sqlalchemy import and_, extract, func
from typing import List, Optional
from datetime import datetime

from models import User, Expense, Budget
from schemas import UserCreate, ExpenseCreate, ExpenseUpdate, BudgetCreate

def create_user(db: Session, email: str, hashed_password: str, full_name: str):
    db_user = User(email=email, hashed_password=hashed_password, full_name=full_name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_expense(db: Session, expense: ExpenseCreate, user_id: int):
    db_expense = Expense(**expense.dict(), owner_id=user_id)
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense

def get_expenses(db: Session, user_id: int, category: Optional[str] = None, month: Optional[int] = None):
    query = db.query(Expense).filter(Expense.owner_id == user_id)
    
    if category:
        query = query.filter(Expense.category == category)
    
    if month:
        query = query.filter(extract('month', Expense.date) == month)
    
    return query.order_by(Expense.date.desc()).all()

def get_expense_by_id(db: Session, expense_id: int, user_id: int):
    return db.query(Expense).filter(
        and_(Expense.id == expense_id, Expense.owner_id == user_id)
    ).first()

def update_expense(db: Session, expense_id: int, expense_update: ExpenseUpdate, user_id: int):
    db_expense = get_expense_by_id(db, expense_id, user_id)
    if not db_expense:
        return None
    
    update_data = expense_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_expense, field, value)
    
    db.commit()
    db.refresh(db_expense)
    return db_expense

def delete_expense(db: Session, expense_id: int, user_id: int):
    db_expense = get_expense_by_id(db, expense_id, user_id)
    if db_expense:
        db.delete(db_expense)
        db.commit()
        return True
    return False

def create_budget(db: Session, budget: BudgetCreate, user_id: int):
    db_budget = Budget(**budget.dict(), owner_id=user_id)
    db.add(db_budget)
    db.commit()
    db.refresh(db_budget)
    return db_budget

def get_budget(db: Session, user_id: int):
    return db.query(Budget).filter(Budget.owner_id == user_id).all()

def update_budget(db: Session, budget_id: int, budget_update: BudgetCreate, user_id: int):
    db_budget = db.query(Budget).filter(
        and_(Budget.id == budget_id, Budget.owner_id == user_id)
    ).first()
    
    if not db_budget:
        return None
    
    update_data = budget_update.dict()
    for field, value in update_data.items():
        setattr(db_budget, field, value)
    
    db.commit()
    db.refresh(db_budget)
    return db_budget

def get_expense_summary(db: Session, user_id: int, month: Optional[int] = None):
    query = db.query(Expense).filter(Expense.owner_id == user_id)
    
    if month:
        query = query.filter(extract('month', Expense.date) == month)
    
    expenses = query.all()
    
    total_expenses = sum(expense.amount for expense in expenses)
    total_count = len(expenses)
    
    # Category breakdown
    category_breakdown = {}
    for expense in expenses:
        category = expense.category
        if category in category_breakdown:
            category_breakdown[category] += expense.amount
        else:
            category_breakdown[category] = expense.amount
    
    # Budget warning
    budget_warning = None
    if month:
        current_year = datetime.now().year
        budget = db.query(Budget).filter(
            and_(
                Budget.owner_id == user_id,
                Budget.month == month,
                Budget.year == current_year
            )
        ).first()
        
        if budget and total_expenses > budget.amount:
            budget_warning = f"Budget exceeded! You've spent ${total_expenses:.2f} out of ${budget.amount:.2f} budget for {month}/{current_year}"
    
    return {
        "total_expenses": total_expenses,
        "total_count": total_count,
        "month": month,
        "year": datetime.now().year if month else None,
        "category_breakdown": category_breakdown,
        "budget_warning": budget_warning
    }
