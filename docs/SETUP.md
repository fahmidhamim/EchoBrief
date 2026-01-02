# EchoBrief AI - Complete Setup Guide

## Prerequisites

- Node.js 18+ ([Download](https://nodejs.org))
- Python 3.10+ ([Download](https://www.python.org))
- PostgreSQL 14+ ([Download](https://www.postgresql.org))
- Git ([Download](https://git-scm.com))

## Step 1: Database Setup

### Create Database

```bash
# Connect to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE echobriefdb;

# Exit psql
\q
```

### Load Schema

```bash
# From project root
psql -U postgres -d echobriefdb -f database/schema.sql
```

## Step 2: Backend Setup

### Install Dependencies

```bash
cd backend
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

### Configure Environment

```bash
# Copy example env file
cp .env.example .env

# Edit .env with your settings
nano .env
```

**Required environment variables:**
- `DATABASE_URL` - PostgreSQL connection string
- `JWT_SECRET` - Random secret key for JWT tokens
- `OPENAI_API_KEY` or `GROQ_API_KEY` - AI service API key

### Run Backend

```bash
# From backend directory
uvicorn app.main:app --reload --port 8000
```

Backend will be available at: `http://localhost:8000`
API Docs at: `http://localhost:8000/docs`

## Step 3: Frontend Setup

### Install Dependencies

```bash
cd frontend
npm install
```

### Configure Environment

```bash
# Create .env.local file
cat > .env.local << EOF
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000
EOF
```

### Run Frontend

```bash
# From frontend directory
npm run dev
```

Frontend will be available at: `http://localhost:3000`

## Step 4: Verify Installation

### Test Backend API

```bash
# Health check
curl http://localhost:8000/health

# Should return:
# {"status":"healthy","service":"EchoBrief AI API","version":"1.0.0"}
```

### Test Frontend

1. Open `http://localhost:3000` in your browser
2. You should see the landing page
3. Click "Get Started Free" to create an account

## Troubleshooting

### Database Connection Error

```
Error: could not connect to server: Connection refused
```

**Solution:**
- Ensure PostgreSQL is running
- Check DATABASE_URL in .env
- Verify database exists: `psql -U postgres -l`

### Port Already in Use

```
Address already in use
```

**Solution:**
- Backend: Change port in .env or use `--port 8001`
- Frontend: Use `npm run dev -- -p 3001`

### Module Not Found

```
ModuleNotFoundError: No module named 'fastapi'
```

**Solution:**
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt` again

### CORS Errors

```
Access to XMLHttpRequest blocked by CORS policy
```

**Solution:**
- Check CORS_ORIGINS in backend .env
- Ensure frontend URL is included
- Restart backend server

## Development Workflow

### Making Changes

1. **Backend Changes:**
   - Edit files in `backend/app/`
   - Server auto-reloads with `--reload` flag
   - Check `http://localhost:8000/docs` for updated API

2. **Frontend Changes:**
   - Edit files in `frontend/app/` or `frontend/components/`
   - Page auto-refreshes in browser
   - Check browser console for errors

### Database Migrations

```bash
# Create migration
alembic revision --autogenerate -m "Add new table"

# Apply migration
alembic upgrade head
```

## Deployment

### Backend (Docker)

```bash
# Build image
docker build -t echobriefai-backend ./backend

# Run container
docker run -p 8000:8000 --env-file .env echobriefai-backend
```

### Frontend (Vercel)

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
vercel
```

## Next Steps

1. Create a user account at `http://localhost:3000/auth`
2. Create a meeting in the dashboard
3. Test the meeting room interface
4. Generate AI summaries

## Support

For issues:
1. Check error messages in console
2. Review logs in backend terminal
3. Check database with: `psql -U postgres -d echobriefdb`
4. Open an issue on GitHub

## Additional Resources

- [FastAPI Docs](https://fastapi.tiangolo.com)
- [Next.js Docs](https://nextjs.org/docs)
- [PostgreSQL Docs](https://www.postgresql.org/docs)
- [Whisper Docs](https://github.com/openai/whisper)
