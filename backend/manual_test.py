"""
Manual API Testing Script
Run this to test all endpoints manually
"""
import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

def print_response(title, response):
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except:
        print(f"Response: {response.text}")
    print()

def test_registration():
    """Test user registration"""
    print("\n🔍 TESTING REGISTRATION ENDPOINT")
    
    user_data = {
        "email": f"testuser_{datetime.now().timestamp()}@example.com",
        "password": "testpassword123",
        "full_name": "Test User"
    }
    
    response = requests.post(f"{BASE_URL}/register", json=user_data)
    print_response("✓ Registration Test", response)
    
    if response.status_code == 200:
        print("✅ Registration PASSED")
        return user_data
    else:
        print("❌ Registration FAILED")
        return None

def test_login(user_data):
    """Test user login"""
    print("\n🔍 TESTING LOGIN ENDPOINT")
    
    if not user_data:
        print("⚠️ Skipping login test - no user data")
        return None
    
    login_data = {
        "username": user_data["email"],
        "password": user_data["password"]
    }
    
    response = requests.post(f"{BASE_URL}/login", data=login_data)
    print_response("✓ Login Test", response)
    
    if response.status_code == 200:
        print("✅ Login PASSED")
        return response.json()["access_token"]
    else:
        print("❌ Login FAILED")
        return None

def test_create_expense(token):
    """Test creating an expense"""
    print("\n🔍 TESTING CREATE EXPENSE ENDPOINT")
    
    if not token:
        print("⚠️ Skipping expense test - no auth token")
        return None
    
    headers = {"Authorization": f"Bearer {token}"}
    expense_data = {
        "description": "Test Grocery Shopping",
        "amount": 125.50,
        "category": "Food"
    }
    
    response = requests.post(f"{BASE_URL}/expenses", json=expense_data, headers=headers)
    print_response("✓ Create Expense Test", response)
    
    if response.status_code == 200:
        print("✅ Create Expense PASSED")
        return response.json()["id"]
    else:
        print("❌ Create Expense FAILED")
        return None

def test_get_expenses(token):
    """Test getting all expenses"""
    print("\n🔍 TESTING GET EXPENSES ENDPOINT")
    
    if not token:
        print("⚠️ Skipping get expenses test - no auth token")
        return
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/expenses", headers=headers)
    print_response("✓ Get Expenses Test", response)
    
    if response.status_code == 200:
        print("✅ Get Expenses PASSED")
    else:
        print("❌ Get Expenses FAILED")

def test_update_expense(token, expense_id):
    """Test updating an expense"""
    print("\n🔍 TESTING UPDATE EXPENSE ENDPOINT")
    
    if not token or not expense_id:
        print("⚠️ Skipping update expense test - no auth token or expense ID")
        return
    
    headers = {"Authorization": f"Bearer {token}"}
    update_data = {
        "description": "Updated Grocery Shopping",
        "amount": 150.00
    }
    
    response = requests.put(f"{BASE_URL}/expenses/{expense_id}", json=update_data, headers=headers)
    print_response("✓ Update Expense Test", response)
    
    if response.status_code == 200:
        print("✅ Update Expense PASSED")
    else:
        print("❌ Update Expense FAILED")

def test_create_budget(token):
    """Test creating a budget"""
    print("\n🔍 TESTING CREATE BUDGET ENDPOINT")
    
    if not token:
        print("⚠️ Skipping budget test - no auth token")
        return
    
    headers = {"Authorization": f"Bearer {token}"}
    budget_data = {
        "month": 10,
        "year": 2025,
        "amount": 1000.00,
        "category": "Food"
    }
    
    response = requests.post(f"{BASE_URL}/budgets", json=budget_data, headers=headers)
    print_response("✓ Create Budget Test", response)
    
    if response.status_code == 200:
        print("✅ Create Budget PASSED")
    else:
        print("❌ Create Budget FAILED")

def test_get_budgets(token):
    """Test getting all budgets"""
    print("\n🔍 TESTING GET BUDGETS ENDPOINT")
    
    if not token:
        print("⚠️ Skipping get budgets test - no auth token")
        return
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/budgets", headers=headers)
    print_response("✓ Get Budgets Test", response)
    
    if response.status_code == 200:
        print("✅ Get Budgets PASSED")
    else:
        print("❌ Get Budgets FAILED")

def test_delete_expense(token, expense_id):
    """Test deleting an expense"""
    print("\n🔍 TESTING DELETE EXPENSE ENDPOINT")
    
    if not token or not expense_id:
        print("⚠️ Skipping delete expense test - no auth token or expense ID")
        return
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.delete(f"{BASE_URL}/expenses/{expense_id}", headers=headers)
    print_response("✓ Delete Expense Test", response)
    
    if response.status_code == 200:
        print("✅ Delete Expense PASSED")
    else:
        print("❌ Delete Expense FAILED")

def main():
    print("\n" + "="*60)
    print("🚀 EXPENSE TRACKER API - MANUAL ENDPOINT TESTING")
    print("="*60)
    print(f"Testing API at: {BASE_URL}")
    print()
    
    try:
        # Test health check
        response = requests.get(BASE_URL)
        print(f"✓ API is reachable")
    except Exception as e:
        print(f"❌ Cannot reach API at {BASE_URL}")
        print(f"Error: {e}")
        print("\nMake sure Docker containers are running:")
        print("  docker-compose up -d")
        return
    
    # Run tests in sequence
    user_data = test_registration()
    token = test_login(user_data)
    expense_id = test_create_expense(token)
    test_get_expenses(token)
    test_update_expense(token, expense_id)
    test_create_budget(token)
    test_get_budgets(token)
    test_delete_expense(token, expense_id)
    
    print("\n" + "="*60)
    print("✅ ALL TESTS COMPLETED")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
