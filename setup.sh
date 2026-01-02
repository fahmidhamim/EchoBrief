#!/bin/bash

# EchoBrief AI - Complete Setup Script
# This script sets up the entire project

set -e  # Exit on error

echo "🚀 EchoBrief AI - Setup Script"
echo "================================"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Step 1: Check PostgreSQL
echo -e "${BLUE}Step 1: Checking PostgreSQL...${NC}"
if ! command -v psql &> /dev/null; then
    echo -e "${YELLOW}PostgreSQL not found. Please install PostgreSQL first.${NC}"
    exit 1
fi
echo -e "${GREEN}✓ PostgreSQL found${NC}"

# Step 2: Start PostgreSQL (macOS)
echo -e "${BLUE}Step 2: Starting PostgreSQL...${NC}"
if [[ "$OSTYPE" == "darwin"* ]]; then
    open -a Postgres 2>/dev/null || true
    sleep 2
fi
echo -e "${GREEN}✓ PostgreSQL started${NC}"

# Step 3: Create database and user
echo -e "${BLUE}Step 3: Setting up database...${NC}"
PSQL_PATH=$(which psql)

# Try to create database (ignore if already exists)
$PSQL_PATH -U postgres -tc "SELECT 1 FROM pg_database WHERE datname = 'echobriefdb'" | grep -q 1 || \
$PSQL_PATH -U postgres -c "CREATE DATABASE echobriefdb;" 2>/dev/null || true

echo -e "${GREEN}✓ Database created${NC}"

# Step 4: Load schema
echo -e "${BLUE}Step 4: Loading database schema...${NC}"
$PSQL_PATH -U postgres -d echobriefdb -f database/schema.sql
echo -e "${GREEN}✓ Schema loaded${NC}"

# Step 5: Setup Backend
echo -e "${BLUE}Step 5: Setting up backend...${NC}"
cd backend

# Create virtual environment
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Copy env file
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo -e "${YELLOW}⚠ Created .env file. Please update with your API keys.${NC}"
fi

cd ..
echo -e "${GREEN}✓ Backend setup complete${NC}"

# Step 6: Setup Frontend
echo -e "${BLUE}Step 6: Setting up frontend...${NC}"
cd frontend

# Install dependencies
npm install

cd ..
echo -e "${GREEN}✓ Frontend setup complete${NC}"

# Step 7: Summary
echo ""
echo -e "${GREEN}================================${NC}"
echo -e "${GREEN}✓ Setup Complete!${NC}"
echo -e "${GREEN}================================${NC}"
echo ""
echo -e "${BLUE}Next steps:${NC}"
echo ""
echo "1. Update backend/.env with your API keys:"
echo "   - OPENAI_API_KEY or GROQ_API_KEY"
echo "   - JWT_SECRET (random string)"
echo ""
echo "2. Start the backend:"
echo "   cd backend"
echo "   source venv/bin/activate"
echo "   uvicorn app.main:app --reload --port 8000"
echo ""
echo "3. Start the frontend (in another terminal):"
echo "   cd frontend"
echo "   npm run dev"
echo ""
echo "4. Open http://localhost:3000 in your browser"
echo ""
echo -e "${BLUE}API Documentation: http://localhost:8000/docs${NC}"
echo ""
