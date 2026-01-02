# 📝 EchoBrief AI - Command Reference

## 🚀 Quick Start Commands

### Start Everything (First Time)

```bash
# Terminal 1 - Backend
cd /Applications/PostgreSQL\ 18/EchoBrief/backend
source venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

```bash
# Terminal 2 - Frontend
cd /Applications/PostgreSQL\ 18/EchoBrief/frontend
npm run dev
```

---

## 🔧 Backend Commands

### Setup Backend

```bash
# Navigate to backend
cd /Applications/PostgreSQL\ 18/EchoBrief/backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env
```

### Run Backend

```bash
# Activate virtual environment
source venv/bin/activate

# Start development server
uvicorn app.main:app --reload --port 8000

# Start production server
uvicorn app.main:app --port 8000

# Start on different port
uvicorn app.main:app --reload --port 8001
```

### Backend Maintenance

```bash
# Activate virtual environment
source venv/bin/activate

# Update dependencies
pip install -r requirements.txt --upgrade

# Check installed packages
pip list

# Freeze current dependencies
pip freeze > requirements.txt

# Run tests
pytest

# Run specific test
pytest tests/test_auth.py

# Run with coverage
pytest --cov=app
```

### Backend Debugging

```bash
# Check if port 8000 is in use
lsof -i :8000

# Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# View backend logs
tail -f backend.log

# Test API health
curl http://localhost:8000/health

# Test API with JSON
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","email":"test@example.com","password":"password123"}'
```

---

## 🎨 Frontend Commands

### Setup Frontend

```bash
# Navigate to frontend
cd /Applications/PostgreSQL\ 18/EchoBrief/frontend

# Install dependencies
npm install

# Update dependencies
npm update

# Check for vulnerabilities
npm audit

# Fix vulnerabilities
npm audit fix
```

### Run Frontend

```bash
# Start development server
npm run dev

# Start on different port
npm run dev -- -p 3001

# Build for production
npm run build

# Start production server
npm start

# Run linter
npm run lint

# Run tests
npm test

# Run tests in watch mode
npm test -- --watch
```

### Frontend Maintenance

```bash
# Clear npm cache
npm cache clean --force

# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install

# Check outdated packages
npm outdated

# Update all packages
npm update

# Install specific package
npm install package-name

# Remove package
npm uninstall package-name

# Check bundle size
npm run build && npm run analyze
```

### Frontend Debugging

```bash
# Check if port 3000 is in use
lsof -i :3000

# Kill process on port 3000
lsof -ti:3000 | xargs kill -9

# View frontend logs
tail -f frontend.log

# Test frontend build
npm run build

# Analyze build
npm run build -- --analyze
```

---

## 🗄️ Database Commands

### PostgreSQL Management

```bash
# Check if PostgreSQL is running
pg_isready

# Start PostgreSQL (macOS)
open -a Postgres

# Connect to database
psql -d echobriefdb

# List all databases
psql -l

# List all tables
psql -d echobriefdb -c "\dt"

# Describe table
psql -d echobriefdb -c "\d users"

# Run SQL file
psql -d echobriefdb -f database/schema.sql

# Backup database
pg_dump echobriefdb > backup.sql

# Restore database
psql echobriefdb < backup.sql

# Drop database
dropdb echobriefdb

# Create database
createdb echobriefdb
```

### Database Queries

```bash
# Connect to database
psql -d echobriefdb

# Inside psql:

# Show all users
SELECT * FROM users;

# Show all meetings
SELECT * FROM meetings;

# Show all transcripts
SELECT * FROM transcripts;

# Count records
SELECT COUNT(*) FROM users;

# Delete all data (careful!)
DELETE FROM users;

# Exit psql
\q
```

---

## 🔌 API Commands

### Test API Endpoints

```bash
# Health check
curl http://localhost:8000/health

# Get API docs
curl http://localhost:8000/openapi.json

# Register user
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "password123"
  }'

# Login user
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "password123"
  }'

# Get current user (replace TOKEN)
curl -H "Authorization: Bearer TOKEN" \
  http://localhost:8000/api/auth/me

# Create meeting
curl -X POST http://localhost:8000/api/meetings/create \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "meeting_title": "Team Meeting",
    "description": "Weekly sync",
    "max_participants": 20
  }'

# Get meetings
curl -H "Authorization: Bearer TOKEN" \
  http://localhost:8000/api/meetings/user/USER_ID

# Get admin metrics
curl -H "Authorization: Bearer TOKEN" \
  http://localhost:8000/api/admin/metrics
```

---

## 🛠️ Development Workflow

### Initialize Project

```bash
# Clone/setup project
cd /Applications/PostgreSQL\ 18/EchoBrief

# Setup database
createdb echobriefdb
psql -d echobriefdb -f database/schema.sql

# Setup backend
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env

# Setup frontend
cd ../frontend
npm install

# Start servers
# Terminal 1
cd backend && source venv/bin/activate && uvicorn app.main:app --reload --port 8000

# Terminal 2
cd frontend && npm run dev
```

### Daily Development

```bash
# Terminal 1 - Backend
cd /Applications/PostgreSQL\ 18/EchoBrief/backend
source venv/bin/activate
uvicorn app.main:app --reload --port 8000

# Terminal 2 - Frontend
cd /Applications/PostgreSQL\ 18/EchoBrief/frontend
npm run dev

# Terminal 3 - Optional: Database management
cd /Applications/PostgreSQL\ 18/EchoBrief
psql -d echobriefdb
```

### Before Committing

```bash
# Backend
cd backend
source venv/bin/activate
pytest
pylint app/

# Frontend
cd frontend
npm run lint
npm test
npm run build
```

---

## 🐛 Troubleshooting Commands

### Port Issues

```bash
# Find process using port
lsof -i :8000
lsof -i :3000
lsof -i :5432

# Kill process by PID
kill -9 PID

# Kill all processes on port
lsof -ti:8000 | xargs kill -9
lsof -ti:3000 | xargs kill -9
```

### Database Issues

```bash
# Check PostgreSQL status
pg_isready

# Restart PostgreSQL (macOS)
brew services restart postgresql

# Check database size
psql -d echobriefdb -c "SELECT pg_size_pretty(pg_database_size('echobriefdb'));"

# Vacuum database
psql -d echobriefdb -c "VACUUM ANALYZE;"

# Kill idle connections
psql -d echobriefdb -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = 'echobriefdb' AND pid <> pg_backend_pid();"
```

### Backend Issues

```bash
# Clear Python cache
find . -type d -name __pycache__ -exec rm -r {} +
find . -type f -name "*.pyc" -delete

# Reinstall dependencies
source venv/bin/activate
pip install -r requirements.txt --force-reinstall

# Check Python version
python --version

# Check pip version
pip --version

# Upgrade pip
pip install --upgrade pip
```

### Frontend Issues

```bash
# Clear Next.js cache
rm -rf .next

# Clear npm cache
npm cache clean --force

# Reinstall node_modules
rm -rf node_modules package-lock.json
npm install

# Check Node version
node --version

# Check npm version
npm --version
```

---

## 📊 Monitoring Commands

### View Logs

```bash
# Backend logs (real-time)
tail -f backend.log

# Frontend logs (real-time)
tail -f frontend.log

# View last 50 lines
tail -50 backend.log

# Search logs
grep "error" backend.log

# Count occurrences
grep -c "error" backend.log
```

### System Monitoring

```bash
# Check disk usage
df -h

# Check memory usage
free -h

# Check CPU usage
top

# Check network connections
netstat -an | grep LISTEN

# Monitor processes
ps aux | grep python
ps aux | grep node
```

---

## 🚀 Deployment Commands

### Build for Production

```bash
# Backend
cd backend
source venv/bin/activate
pip install -r requirements.txt
# Update .env for production

# Frontend
cd frontend
npm install
npm run build
```

### Docker Commands (Optional)

```bash
# Build Docker image
docker build -t echobriefai-backend .

# Run Docker container
docker run -p 8000:8000 echobriefai-backend

# View Docker logs
docker logs CONTAINER_ID

# Stop Docker container
docker stop CONTAINER_ID
```

---

## 📋 Environment Setup

### Create .env Files

```bash
# Backend .env
cd backend
cat > .env << EOF
DATABASE_URL=postgresql://fahmidhamim@localhost:5432/echobriefdb
JWT_SECRET=your-secret-key-change-this
JWT_ALGORITHM=HS256
SERVER_HOST=0.0.0.0
SERVER_PORT=8000
ENVIRONMENT=development
DEBUG=False
OPENAI_API_KEY=sk-...
GROQ_API_KEY=gsk-...
EOF

# Frontend .env.local
cd ../frontend
cat > .env.local << EOF
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000
EOF
```

---

## 🎯 Common Workflows

### Add New Backend Endpoint

```bash
# 1. Create schema in app/schemas/
# 2. Create service method in app/services/
# 3. Add endpoint in app/api/
# 4. Test with curl or Swagger UI
# 5. Update API.md documentation
```

### Add New Frontend Page

```bash
# 1. Create page in app/[page]/page.tsx
# 2. Add navigation link in components/navbar.tsx
# 3. Style with Tailwind CSS
# 4. Test in browser
# 5. Update documentation
```

### Add New Database Table

```bash
# 1. Create model in app/models/
# 2. Update database/schema.sql
# 3. Run migration
# 4. Create schema in app/schemas/
# 5. Create service methods
# 6. Create API endpoints
```

---

## 🔗 Useful Links

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **Health Check:** http://localhost:8000/health

---

## 📞 Quick Help

```bash
# Show this file
cat COMMANDS.md

# Search commands
grep "command" COMMANDS.md

# Copy command to clipboard (macOS)
echo "command" | pbcopy

# Run command from history
!command_name
```

---

*Last Updated: Nov 30, 2025*  
*EchoBrief AI - Command Reference Guide*
