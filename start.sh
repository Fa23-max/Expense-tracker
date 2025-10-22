#!/bin/bash

echo "🚀 Starting Expense Tracker Application..."
echo "=========================================="

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

echo "✅ Docker and Docker Compose are available"

# Build and start the application
echo "🔨 Building and starting containers..."
docker-compose up --build -d

echo ""
echo "🎉 Application is starting up!"
echo ""
echo "📱 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:8000"
echo "📚 API Documentation: http://localhost:8000/docs"
echo ""
echo "⏳ Please wait a moment for all services to be ready..."
echo ""

# Wait for services to be ready
echo "🔍 Checking if services are ready..."

# Function to check if a service is ready
check_service() {
    local url=$1
    local name=$2
    local max_attempts=30
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        if curl -s "$url" > /dev/null 2>&1; then
            echo "✅ $name is ready!"
            return 0
        fi
        echo "⏳ Waiting for $name... (attempt $attempt/$max_attempts)"
        sleep 2
        attempt=$((attempt + 1))
    done
    
    echo "❌ $name failed to start after $max_attempts attempts"
    return 1
}

# Check backend
check_service "http://localhost:8000/docs" "Backend API"

# Check frontend
check_service "http://localhost:3000" "Frontend"

echo ""
echo "🎊 All services are ready!"
echo ""
echo "📖 Quick Start Guide:"
echo "1. Open http://localhost:3000 in your browser"
echo "2. Click 'Sign up' to create a new account"
echo "3. Login with your credentials"
echo "4. Start adding your expenses!"
echo ""
echo "🛑 To stop the application, run: docker-compose down"
echo ""
