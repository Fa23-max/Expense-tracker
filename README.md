# Expense Tracker - Full Stack Application

A comprehensive expense tracking application built with React frontend and FastAPI backend, containerized with Docker.

## Features

### Core Functionality
- ✅ User authentication (login/signup)
- ✅ Add, edit, delete expenses
- ✅ View all expenses with filtering
- ✅ Expense summary and analytics
- ✅ Monthly expense summaries
- ✅ Budget management with warnings
- ✅ CSV export functionality
- ✅ Category-based expense organization

### Additional Features
- 🎨 Modern, responsive UI
- 📊 Interactive charts and reports
- 🔐 JWT-based authentication
- 🐳 Docker containerization
- 📱 Mobile-friendly design
- ⚡ Real-time updates

## Tech Stack

### Frontend
- React 18
- React Router
- Axios for API calls
- Recharts for data visualization
- Lucide React for icons
- React Hot Toast for notifications

### Backend
- FastAPI
- SQLAlchemy ORM
- PostgreSQL database
- JWT authentication
- Pydantic for data validation
- Pandas for CSV export

### Infrastructure
- Docker & Docker Compose
- PostgreSQL database
- Nginx (optional for production)

## Quick Start

### Prerequisites
- Docker and Docker Compose installed
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd expense-tracker
   ```

2. **Start the application**
   ```bash
   docker-compose up --build
   ```

3. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### First Time Setup

1. **Register a new account** at http://localhost:3000/register
2. **Login** with your credentials
3. **Start adding expenses** and setting budgets!

## API Endpoints

### Authentication
- `POST /register` - User registration
- `POST /login` - User login
- `POST /token` - Get access token

### Expenses
- `GET /expenses` - Get all expenses (with optional filters)
- `POST /expenses` - Add new expense
- `GET /expenses/{id}` - Get specific expense
- `PUT /expenses/{id}` - Update expense
- `DELETE /expenses/{id}` - Delete expense
- `GET /expenses/summary` - Get expense summary
- `GET /expenses/export/csv` - Export expenses to CSV

### Budgets
- `GET /budgets` - Get all budgets
- `POST /budgets` - Create new budget
- `PUT /budgets/{id}` - Update budget
- `DELETE /budgets/{id}` - Delete budget

## Usage Examples

### Command Line Interface (CLI) Style

The application provides a web interface that mimics the CLI functionality described in the requirements:

```bash
# Add expense
expense-tracker add --description "Lunch" --amount 20
# Expense added successfully (ID: 1)

# List expenses
expense-tracker list
# ID  Date       Description  Amount
# 1   2024-08-06  Lunch        $20

# Get summary
expense-tracker summary
# Total expenses: $30

# Delete expense
expense-tracker delete --id 2
# Expense deleted successfully

# Monthly summary
expense-tracker summary --month 8
# Total expenses for August: $20
```

### Web Interface Features

1. **Dashboard**: Overview of spending, recent expenses, and budget alerts
2. **Expenses**: Add, edit, delete, and filter expenses by category/month
3. **Budgets**: Set monthly budgets with category-specific limits
4. **Reports**: Visual analytics with charts and export functionality

## Development

### Running in Development Mode

1. **Backend only**
   ```bash
   cd backend
   pip install -r requirements.txt
   uvicorn main:app --reload
   ```

2. **Frontend only**
   ```bash
   cd frontend
   npm install
   npm start
   ```

### Database Management

The application uses PostgreSQL with SQLAlchemy ORM. Database migrations are handled automatically on startup.

### Environment Variables

Create a `.env` file in the backend directory:

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/expense_tracker
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Project Structure

```
expense-tracker/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── database.py          # Database configuration
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── auth.py              # Authentication logic
│   ├── crud.py              # Database operations
│   ├── requirements.txt     # Python dependencies
│   └── Dockerfile           # Backend container
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── contexts/        # React contexts
│   │   ├── App.js           # Main app component
│   │   └── index.js         # Entry point
│   ├── package.json         # Node dependencies
│   └── Dockerfile           # Frontend container
├── docker-compose.yml       # Multi-container setup
└── README.md               # This file
```

## Features Implementation

### ✅ Core Requirements
- [x] Add expense with description and amount
- [x] Update expense
- [x] Delete expense
- [x] View all expenses
- [x] View expense summary
- [x] Monthly expense summary

### ✅ Additional Features
- [x] Expense categories with filtering
- [x] Budget management with warnings
- [x] CSV export functionality
- [x] User authentication
- [x] Modern web interface
- [x] Data visualization
- [x] Responsive design

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For issues and questions, please create an issue in the repository.
