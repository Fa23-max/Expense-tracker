from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    full_name: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class ExpenseBase(BaseModel):
    description: str
    amount: float
    category: str = "Other"

class ExpenseCreate(ExpenseBase):
    pass

class ExpenseUpdate(BaseModel):
    description: Optional[str] = None
    amount: Optional[float] = None
    category: Optional[str] = None

class ExpenseResponse(ExpenseBase):
    id: int
    date: datetime
    owner_id: int
    
    class Config:
        from_attributes = True

class BudgetBase(BaseModel):
    month: int
    year: int
    amount: float
    category: str = "General"

class BudgetCreate(BudgetBase):
    pass

class BudgetResponse(BudgetBase):
    id: int
    owner_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class ExpenseSummary(BaseModel):
    total_expenses: float
    total_count: int
    month: Optional[int] = None
    year: Optional[int] = None
    category_breakdown: dict = {}
    budget_warning: Optional[str] = None

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None

class PasswordChange(BaseModel):
    current_password: str
    new_password: str

class PasswordResetRequest(BaseModel):
    email: EmailStr

class PasswordResetVerify(BaseModel):
    email: EmailStr
    reset_key: str
    new_password: str
