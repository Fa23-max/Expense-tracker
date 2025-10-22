import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from main import app
from database import Base, get_db
from models import User, Expense, Budget

# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="function")
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(test_db):
    return TestClient(app)

@pytest.fixture
def test_user_data():
    return {
        "email": "test@example.com",
        "password": "testpassword123",
        "full_name": "Test User"
    }

@pytest.fixture
def registered_user(client, test_user_data):
    response = client.post("/register", json=test_user_data)
    return response.json()

@pytest.fixture
def auth_token(client, test_user_data, registered_user):
    response = client.post(
        "/login",
        data={"username": test_user_data["email"], "password": test_user_data["password"]}
    )
    return response.json()["access_token"]

# ==================== AUTHENTICATION TESTS ====================

def test_register_user(client, test_user_data):
    """Test user registration"""
    response = client.post("/register", json=test_user_data)
    
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == test_user_data["email"]
    assert data["full_name"] == test_user_data["full_name"]
    assert "id" in data
    assert data["is_active"] == True
    print("✓ Registration test passed")

def test_register_duplicate_email(client, test_user_data, registered_user):
    """Test registration with duplicate email"""
    response = client.post("/register", json=test_user_data)
    
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"].lower()
    print("✓ Duplicate email test passed")

def test_register_invalid_email(client):
    """Test registration with invalid email"""
    response = client.post("/register", json={
        "email": "invalid-email",
        "password": "testpass",
        "full_name": "Test"
    })
    
    assert response.status_code == 422
    print("✓ Invalid email test passed")

def test_login_success(client, test_user_data, registered_user):
    """Test successful login"""
    response = client.post(
        "/login",
        data={"username": test_user_data["email"], "password": test_user_data["password"]}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    print("✓ Login success test passed")

def test_login_wrong_password(client, test_user_data, registered_user):
    """Test login with wrong password"""
    response = client.post(
        "/login",
        data={"username": test_user_data["email"], "password": "wrongpassword"}
    )
    
    assert response.status_code == 401
    assert "incorrect" in response.json()["detail"].lower()
    print("✓ Wrong password test passed")

def test_login_nonexistent_user(client):
    """Test login with non-existent user"""
    response = client.post(
        "/login",
        data={"username": "nonexistent@example.com", "password": "password"}
    )
    
    assert response.status_code == 401
    print("✓ Non-existent user test passed")

# ==================== EXPENSE TESTS ====================

def test_create_expense(client, auth_token):
    """Test creating an expense"""
    response = client.post(
        "/expenses",
        json={
            "description": "Test Expense",
            "amount": 50.00,
            "category": "Food"
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["description"] == "Test Expense"
    assert data["amount"] == 50.00
    assert data["category"] == "Food"
    assert "id" in data
    print("✓ Create expense test passed")

def test_create_expense_unauthorized(client):
    """Test creating expense without authentication"""
    response = client.post(
        "/expenses",
        json={
            "description": "Test Expense",
            "amount": 50.00,
            "category": "Food"
        }
    )
    
    assert response.status_code == 401
    print("✓ Unauthorized expense creation test passed")

def test_get_expenses(client, auth_token):
    """Test getting all expenses"""
    # Create some expenses first
    client.post(
        "/expenses",
        json={"description": "Expense 1", "amount": 25.00, "category": "Food"},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    client.post(
        "/expenses",
        json={"description": "Expense 2", "amount": 75.00, "category": "Transport"},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    response = client.get(
        "/expenses",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    print("✓ Get expenses test passed")

def test_get_expenses_by_category(client, auth_token):
    """Test filtering expenses by category"""
    client.post(
        "/expenses",
        json={"description": "Food Expense", "amount": 25.00, "category": "Food"},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    client.post(
        "/expenses",
        json={"description": "Transport Expense", "amount": 75.00, "category": "Transport"},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    response = client.get(
        "/expenses?category=Food",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["category"] == "Food"
    print("✓ Filter expenses by category test passed")

def test_get_single_expense(client, auth_token):
    """Test getting a single expense by ID"""
    create_response = client.post(
        "/expenses",
        json={"description": "Test Expense", "amount": 50.00, "category": "Food"},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    expense_id = create_response.json()["id"]
    
    response = client.get(
        f"/expenses/{expense_id}",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == expense_id
    assert data["description"] == "Test Expense"
    print("✓ Get single expense test passed")

def test_update_expense(client, auth_token):
    """Test updating an expense"""
    create_response = client.post(
        "/expenses",
        json={"description": "Original", "amount": 50.00, "category": "Food"},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    expense_id = create_response.json()["id"]
    
    response = client.put(
        f"/expenses/{expense_id}",
        json={"description": "Updated", "amount": 75.00},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["description"] == "Updated"
    assert data["amount"] == 75.00
    print("✓ Update expense test passed")

def test_delete_expense(client, auth_token):
    """Test deleting an expense"""
    create_response = client.post(
        "/expenses",
        json={"description": "To Delete", "amount": 50.00, "category": "Food"},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    expense_id = create_response.json()["id"]
    
    response = client.delete(
        f"/expenses/{expense_id}",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    assert response.status_code == 200
    assert "deleted" in response.json()["message"].lower()
    
    # Verify it's deleted
    get_response = client.get(
        f"/expenses/{expense_id}",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert get_response.status_code == 404
    print("✓ Delete expense test passed")

# ==================== BUDGET TESTS ====================

def test_create_budget(client, auth_token):
    """Test creating a budget"""
    response = client.post(
        "/budgets",
        json={
            "month": 10,
            "year": 2025,
            "amount": 1000.00,
            "category": "Food"
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["month"] == 10
    assert data["year"] == 2025
    assert data["amount"] == 1000.00
    assert data["category"] == "Food"
    print("✓ Create budget test passed")

def test_get_budgets(client, auth_token):
    """Test getting all budgets"""
    client.post(
        "/budgets",
        json={"month": 10, "year": 2025, "amount": 1000.00, "category": "Food"},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    response = client.get(
        "/budgets",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    print("✓ Get budgets test passed")

def test_update_budget(client, auth_token):
    """Test updating a budget"""
    create_response = client.post(
        "/budgets",
        json={"month": 10, "year": 2025, "amount": 1000.00, "category": "Food"},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    budget_id = create_response.json()["id"]
    
    response = client.put(
        f"/budgets/{budget_id}",
        json={"month": 10, "year": 2025, "amount": 1500.00, "category": "Food"},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["amount"] == 1500.00
    print("✓ Update budget test passed")

# ==================== RUN ALL TESTS ====================

if __name__ == "__main__":
    print("\n" + "="*60)
    print("RUNNING EXPENSE TRACKER API TESTS")
    print("="*60 + "\n")
    pytest.main([__file__, "-v", "-s"])
