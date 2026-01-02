# EchoBrief AI - AI-Powered Audio Meeting Platform

A complete MVP for real-time audio transcription and intelligent meeting summarization.

## 🎯 Features

- **Real-time Audio Transcription** - Live speech-to-text using Whisper
- **AI-Powered Summaries** - Automatic meeting summaries, action items, and keywords
- **Secure Authentication** - JWT-based user authentication with bcrypt hashing
- **Meeting Management** - Create, join, and track meetings (max 20 participants)
- **WebSocket Streaming** - Real-time transcript updates to all participants
- **Admin Dashboard** - Usage metrics and analytics
- **Dark/Light Mode** - Modern UI with theme support
- **PDF Export** - Download transcripts and summaries
- **Responsive Design** - Mobile and desktop optimized

## 📁 Project Structure

```
EchoBrief/
├── frontend/                 # Next.js React application
│   ├── app/                 # App router pages
│   ├── components/          # Reusable components
│   ├── lib/                 # Utilities and helpers
│   ├── public/              # Static assets
│   ├── package.json
│   └── next.config.js
├── backend/                 # FastAPI Python application
│   ├── app/
│   │   ├── api/            # API routes
│   │   ├── models/         # Database models
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── services/       # Business logic
│   │   ├── middleware/     # Auth, CORS, etc
│   │   └── main.py         # FastAPI app
│   ├── requirements.txt
│   └── .env.example
├── database/                # Database setup
│   └── schema.sql          # PostgreSQL schema
├── docs/                    # Documentation
│   ├── API.md              # API specification
│   └── SETUP.md            # Detailed setup guide
└── README.md
```

## 🚀 Quick Start

### Prerequisites

- Node.js 18+
- Python 3.10+
- PostgreSQL 14+
- Git

### 1. Database Setup

```bash
# Create database
psql -U postgres -c "CREATE DATABASE echobriefdb;"

# Load schema
psql -U postgres -d echobriefdb -f database/schema.sql
```

### 2. Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your configuration

# Run server
uvicorn app.main:app --reload --port 8000
```

Backend will be available at `http://localhost:8000`
API Docs at `http://localhost:8000/docs`

### 3. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend will be available at `http://localhost:3000`

## 🔧 Environment Variables

### Backend (.env)

```
DATABASE_URL=postgresql://postgres:password@localhost:5432/echobriefdb
JWT_SECRET=your-super-secret-key-change-this
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

# AI Services
OPENAI_API_KEY=sk-...
GROQ_API_KEY=gsk_...

# Server
SERVER_HOST=0.0.0.0
SERVER_PORT=8000
CORS_ORIGINS=http://localhost:3000

# File storage
UPLOAD_DIR=./uploads
MAX_FILE_SIZE=104857600  # 100MB
```

### Frontend (.env.local)

```
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000
```

## 📊 Database Schema

### Core Tables

- **users** - User accounts with authentication
- **meetings** - Meeting sessions with metadata
- **participants** - Meeting participants tracking
- **transcripts** - Real-time transcript segments
- **summaries** - AI-generated summaries and action items
- **audio_files** - Uploaded audio recordings
- **audit_logs** - System audit trail

See `database/schema.sql` for complete schema.

## 🔌 API Endpoints

### Authentication
- `POST /api/auth/register` - User signup
- `POST /api/auth/login` - User login
- `POST /api/auth/refresh` - Refresh JWT token
- `POST /api/auth/logout` - User logout

### Meetings
- `POST /api/meetings/create` - Create new meeting
- `POST /api/meetings/join` - Join existing meeting
- `GET /api/meetings/user/{user_id}` - Get user's meetings
- `GET /api/meetings/{meeting_id}` - Get meeting details
- `POST /api/meetings/{meeting_id}/end` - End meeting
- `DELETE /api/meetings/{meeting_id}` - Delete meeting

### Audio & Transcription
- `POST /api/audio/upload` - Upload audio file
- `GET /api/transcripts/{meeting_id}` - Get meeting transcripts
- `WS /ws/transcription` - WebSocket for real-time transcription

### AI & Summaries
- `POST /api/ai/summarize` - Generate summary
- `GET /api/ai/summary/{meeting_id}` - Get meeting summary
- `GET /api/ai/summary/{meeting_id}/pdf` - Download summary as PDF

### Admin
- `GET /api/admin/metrics` - Get usage metrics
- `GET /api/admin/users` - List all users
- `GET /api/admin/meetings` - List all meetings

## 🏗️ Architecture

### Frontend
- **Framework**: Next.js 14 with App Router
- **Styling**: Tailwind CSS + shadcn/ui components
- **State Management**: React Context + Hooks
- **Real-time**: WebSocket client for live transcription
- **Auth**: JWT stored in secure HTTP-only cookies
- **Forms**: React Hook Form with Zod validation

### Backend
- **Framework**: FastAPI with async/await
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: JWT with bcrypt password hashing
- **AI**: Faster-Whisper for transcription, Groq/OpenAI for summaries
- **Real-time**: WebSocket with asyncio
- **Rate Limiting**: Slowapi middleware
- **Validation**: Pydantic schemas

## 🔐 Security Features

- JWT token-based authentication
- Bcrypt password hashing (cost factor 12)
- CORS protection
- Rate limiting on API endpoints (100 req/min per IP)
- SQL injection prevention (SQLAlchemy ORM)
- HTTPS support ready
- Secure WebSocket (WSS) ready
- Input validation on all endpoints
- CSRF protection ready

## 📈 Scalability

- Stateless API design for horizontal scaling
- Database connection pooling
- WebSocket server can be load-balanced with sticky sessions
- Async/await for concurrent request handling
- Background task queue ready (Celery integration optional)
- Caching layer ready (Redis integration optional)

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```


## 🧬 After cloning:

```bash
🚚 Backend:
     cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

🛩️ Frontend:
cd frontend
npm install

📲 Then run the servers:
 cd backend && python -m uvicorn app.main:app --reload --port 8000
cd frontend && npm run dev -- --hostname 0.0.0.0 --port 3000
```


## 📚 Documentation

- **API Specification**: See `docs/API.md` for detailed endpoint documentation
- **Setup Guide**: See `docs/SETUP.md` for step-by-step installation
- **Database**: See `database/schema.sql` for schema details

## 🚀 Deployment

### Backend (Docker)
```bash
docker build -t echobriefai-backend ./backend
docker run -p 8000:8000 --env-file .env echobriefai-backend
```

### Frontend (Vercel)
```bash
npm install -g vercel
vercel
```

## 📝 License

MIT License - See LICENSE file for details

## 🤝 Support

For issues and questions, please open an issue on GitHub.

---

**Built with ❤️ for seamless meeting experiences**
