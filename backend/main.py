from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List, Optional
import pandas as pd
import io
from fastapi.responses import StreamingResponse

from database import SessionLocal, engine, get_db
from models import Base, User, Expense, Budget, PasswordReset
from email_service import send_password_reset_email
import secrets
import string
from schemas import (
    UserCreate, UserResponse, UserLogin, UserUpdate, PasswordChange,
    ExpenseCreate, ExpenseUpdate, ExpenseResponse,
    BudgetCreate, BudgetResponse, ExpenseSummary,
    PasswordResetRequest, PasswordResetVerify
)
from auth import (
    create_access_token, verify_token, get_password_hash, 
    verify_password, get_current_user
)
from crud import (
    create_user, get_user_by_email, create_expense, get_expenses,
    update_expense, delete_expense, get_expense_by_id,
    create_budget, get_budget, update_budget, get_expense_summary
)

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Expense Tracker API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Authentication endpoints
@app.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    
    hashed_password = get_password_hash(user.password)
    db_user = create_user(db, user.email, hashed_password, user.full_name)
    return db_user

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = get_user_by_email(db, email=form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

# Expense endpoints
@app.post("/expenses", response_model=ExpenseResponse)
def add_expense(
    expense: ExpenseCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_expense = create_expense(db, expense, current_user.id)
    return db_expense

@app.get("/expenses", response_model=List[ExpenseResponse])
def get_user_expenses(
    category: Optional[str] = None,
    month: Optional[int] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    expenses = get_expenses(db, current_user.id, category, month)
    return expenses

@app.get("/expenses/summary", response_model=ExpenseSummary)
def get_expense_summary_endpoint(
    month: Optional[int] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    summary = get_expense_summary(db, current_user.id, month)
    return summary

@app.get("/expenses/export/csv")
def export_expenses_csv(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    expenses = get_expenses(db, current_user.id)
    
    # Create DataFrame
    df = pd.DataFrame([{
        'id': exp.id,
        'description': exp.description,
        'amount': exp.amount,
        'category': exp.category,
        'date': exp.date.isoformat()
    } for exp in expenses])
    
    # Create CSV in memory
    output = io.StringIO()
    df.to_csv(output, index=False)
    output.seek(0)
    
    return StreamingResponse(
        io.BytesIO(output.getvalue().encode()),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=expenses.csv"}
    )

@app.get("/expenses/{expense_id}", response_model=ExpenseResponse)
def get_expense(
    expense_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    expense = get_expense_by_id(db, expense_id, current_user.id)
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense

@app.put("/expenses/{expense_id}", response_model=ExpenseResponse)
def update_expense_endpoint(
    expense_id: int,
    expense_update: ExpenseUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    expense = get_expense_by_id(db, expense_id, current_user.id)
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    
    updated_expense = update_expense(db, expense_id, expense_update, current_user.id)
    return updated_expense

@app.delete("/expenses/{expense_id}")
def delete_expense_endpoint(
    expense_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    expense = get_expense_by_id(db, expense_id, current_user.id)
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    
    delete_expense(db, expense_id, current_user.id)
    return {"message": "Expense deleted successfully"}

# Budget endpoints
@app.post("/budgets", response_model=BudgetResponse)
def create_budget_endpoint(
    budget: BudgetCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_budget = create_budget(db, budget, current_user.id)
    return db_budget

@app.get("/budgets", response_model=List[BudgetResponse])
def get_user_budgets(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    budgets = get_budget(db, current_user.id)
    return budgets

@app.put("/budgets/{budget_id}", response_model=BudgetResponse)
def update_budget_endpoint(
    budget_id: int,
    budget_update: BudgetCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    budget = update_budget(db, budget_id, budget_update, current_user.id)
    if not budget:
        raise HTTPException(status_code=404, detail="Budget not found")
    return budget

# User Profile endpoints
@app.get("/users/profile", response_model=UserResponse)
def get_user_profile(current_user: User = Depends(get_current_user)):
    return current_user

@app.put("/users/profile", response_model=UserResponse)
def update_user_profile(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if user_update.email and user_update.email != current_user.email:
        existing_user = get_user_by_email(db, user_update.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        current_user.email = user_update.email
    
    if user_update.full_name:
        current_user.full_name = user_update.full_name
    
    db.commit()
    db.refresh(current_user)
    return current_user

@app.put("/users/change-password")
def change_password(
    password_data: PasswordChange,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not verify_password(password_data.current_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="Current password is incorrect")
    
    if len(password_data.new_password) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters long")
    
    current_user.hashed_password = get_password_hash(password_data.new_password)
    db.commit()
    
    return {"message": "Password changed successfully"}

# Password Reset endpoints
def generate_reset_key(length=6):
    """Generate a random 6-character alphanumeric reset key"""
    characters = string.ascii_uppercase + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))

@app.post("/password-reset/request")
def request_password_reset(
    reset_request: PasswordResetRequest,
    db: Session = Depends(get_db)
):
    """Request a password reset - sends email with reset key"""
    user = get_user_by_email(db, reset_request.email)
    if not user:
        # Don't reveal if email exists or not for security
        return {"message": "If the email exists, a reset key has been sent"}
    
    # Generate unique reset key
    reset_key = generate_reset_key()
    
    # Create password reset record
    password_reset = PasswordReset(
        email=reset_request.email,
        reset_key=reset_key,
        expires_at=datetime.utcnow() + timedelta(hours=1),
        is_used=False
    )
    
    db.add(password_reset)
    db.commit()
    
    # Send email with reset key (also prints to console as fallback)
    send_password_reset_email(reset_request.email, reset_key)
    
    return {"message": "If the email exists, a reset key has been sent. Check your email or backend logs."}

@app.post("/password-reset/verify")
def verify_and_reset_password(
    reset_data: PasswordResetVerify,
    db: Session = Depends(get_db)
):
    """Verify reset key and update password"""
    
    # Find the reset request
    reset_request = db.query(PasswordReset).filter(
        PasswordReset.email == reset_data.email,
        PasswordReset.reset_key == reset_data.reset_key,
        PasswordReset.is_used == False
    ).first()
    
    if not reset_request:
        raise HTTPException(
            status_code=400,
            detail="Invalid or expired reset key"
        )
    
    # Check if expired
    if reset_request.expires_at < datetime.utcnow():
        raise HTTPException(
            status_code=400,
            detail="Reset key has expired. Please request a new one."
        )
    
    # Validate new password
    if len(reset_data.new_password) < 8:
        raise HTTPException(
            status_code=400,
            detail="Password must be at least 8 characters long"
        )
    
    # Get user and update password
    user = get_user_by_email(db, reset_data.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.hashed_password = get_password_hash(reset_data.new_password)
    reset_request.is_used = True
    
    db.commit()
    
    return {"message": "Password has been reset successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
