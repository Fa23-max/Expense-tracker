@echo off
echo 🚀 Starting Expense Tracker Application...
echo ==========================================

REM Check if Docker is installed
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker is not installed. Please install Docker first.
    pause
    exit /b 1
)

REM Check if Docker Compose is installed
docker-compose --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker Compose is not installed. Please install Docker Compose first.
    pause
    exit /b 1
)

echo ✅ Docker and Docker Compose are available

REM Build and start the application
echo 🔨 Building and starting containers...
docker-compose up --build -d

echo.
echo 🎉 Application is starting up!
echo.
echo 📱 Frontend: http://localhost:3000
echo 🔧 Backend API: http://localhost:8000
echo 📚 API Documentation: http://localhost:8000/docs
echo.
echo ⏳ Please wait a moment for all services to be ready...
echo.

echo 🔍 Checking if services are ready...

REM Wait for services to be ready
timeout /t 10 /nobreak >nul

echo.
echo 🎊 Application should be ready!
echo.
echo 📖 Quick Start Guide:
echo 1. Open http://localhost:3000 in your browser
echo 2. Click 'Sign up' to create a new account
echo 3. Login with your credentials
echo 4. Start adding your expenses!
echo.
echo 🛑 To stop the application, run: docker-compose down
echo.
pause
