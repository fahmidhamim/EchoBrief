# EchoBrief AI - Quick Start Guide

## ✅ Setup Complete!

Your EchoBrief AI project is now fully set up. Follow these steps to run it.

---

## 🚀 Running the Application

### Terminal 1: Start Backend

```bash
cd /Applications/PostgreSQL\ 18/EchoBrief/backend
source venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

**Expected Output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

✅ Backend is ready at: **http://localhost:8000**  
📚 API Docs at: **http://localhost:8000/docs**

---

### Terminal 2: Start Frontend

```bash
cd /Applications/PostgreSQL\ 18/EchoBrief/frontend
npm run dev
```

**Expected Output:**
```
> echobriefai-frontend@1.0.0 dev
> next dev

  ▲ Next.js 14.0.0
  - Local:        http://localhost:3000
```

✅ Frontend is ready at: **http://localhost:3000**

---

## 📋 What's Been Set Up

### ✅ Database
- PostgreSQL database: `echobriefdb`
- All tables created and indexed
- Ready for data

### ✅ Backend
- FastAPI server with 19 REST endpoints
- 1 WebSocket endpoint for real-time transcription
- JWT authentication
- Rate limiting
- All dependencies installed

### ✅ Frontend
- Next.js React application
- 6 pages (landing, auth, dashboard, meeting, summary)
- UI components (button, card, input)
- Tailwind CSS styling
- Dark/light mode support

---

## 🔑 Environment Configuration

### Backend (.env)

Update `/Applications/PostgreSQL 18/EchoBrief/backend/.env` with:

```env
# Database (already configured)
DATABASE_URL=postgresql://fahmidhamim@localhost:5432/echobriefdb

# JWT
JWT_SECRET=your-super-secret-key-change-this

# AI Services (choose one)
OPENAI_API_KEY=sk-...
# OR
GROQ_API_KEY=gsk-...

# Server
SERVER_HOST=0.0.0.0
SERVER_PORT=8000
DEBUG=False

# CORS
CORS_ORIGINS=http://localhost:3000

# File Upload
MAX_FILE_SIZE=104857600
UPLOAD_DIR=./uploads
```

### Frontend (.env.local)

Create `/Applications/PostgreSQL 18/EchoBrief/frontend/.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000
```

---

## 🧪 Testing the Application

### 1. Test Backend API

```bash
# Health check
curl http://localhost:8000/health

# API Documentation
open http://localhost:8000/docs
```

### 2. Test Frontend

1. Open http://localhost:3000 in your browser
2. Click "Get Started Free"
3. Create an account
4. Create a meeting
5. Join the meeting

---

## 📊 Project Structure

```
/Applications/PostgreSQL 18/EchoBrief/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── main.py         # Main FastAPI app
│   │   ├── api/            # API endpoints
│   │   ├── models/         # Database models
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── services/       # Business logic
│   │   └── middleware/     # Auth & rate limiting
│   ├── venv/               # Virtual environment
│   ├── requirements.txt    # Python dependencies
│   └── .env                # Environment variables
│
├── frontend/               # Next.js frontend
│   ├── app/               # Pages
│   ├── components/        # React components
│   ├── lib/               # Utilities
│   ├── node_modules/      # NPM packages
│   └── package.json       # Dependencies
│
├── database/
│   └── schema.sql         # PostgreSQL schema
│
└── docs/
    ├── SETUP.md           # Detailed setup guide
    └── API.md             # API specification
```

---

## 🔗 Useful Links

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Docs (Swagger):** http://localhost:8000/docs
- **API Docs (ReDoc):** http://localhost:8000/redoc
- **Health Check:** http://localhost:8000/health

---

## 🐛 Troubleshooting

### Backend won't start

```bash
# Check if port 8000 is in use
lsof -i :8000

# Kill the process if needed
kill -9 <PID>

# Try a different port
uvicorn app.main:app --reload --port 8001
```

### Frontend won't start

```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install

# Try a different port
npm run dev -- -p 3001
```

### Database connection error

```bash
# Check if PostgreSQL is running
pg_isready

# Check database exists
psql -l | grep echobriefdb

# Recreate database if needed
dropdb echobriefdb
createdb echobriefdb
psql -d echobriefdb -f database/schema.sql
```

---

## 📝 Next Steps

1. **Update .env files** with your API keys
2. **Test the API** at http://localhost:8000/docs
3. **Create an account** at http://localhost:3000
4. **Create a meeting** and test the features
5. **Review documentation** in `/docs` folder

---

## 🎯 Key Features to Try

✅ **User Authentication** - Sign up and log in  
✅ **Create Meetings** - Start a new meeting  
✅ **Join Meetings** - Participate in meetings  
✅ **Live Transcription** - See real-time transcripts  
✅ **AI Summaries** - Generate meeting summaries  
✅ **Admin Dashboard** - View system metrics  
✅ **Dark Mode** - Toggle theme in navbar  

---

## 📞 Support

- Check `docs/SETUP.md` for detailed setup instructions
- Check `docs/API.md` for API endpoint documentation
- Review code comments in source files
- Check browser console for frontend errors
- Check terminal for backend errors

---

## 🎉 You're All Set!

Your EchoBrief AI MVP is ready to use. Start the backend and frontend servers and begin building!

**Happy coding! 🚀**
