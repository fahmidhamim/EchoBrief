# EchoBrief AI - API Specification

## Base URL

```
http://localhost:8000/api
```

## Authentication

All endpoints (except `/auth/register` and `/auth/login`) require JWT token in Authorization header:

```
Authorization: Bearer <token>
```

## Response Format

All responses are JSON with the following structure:

```json
{
  "data": {},
  "error": null,
  "status": "success"
}
```

## Endpoints

### Authentication

#### Register User

```http
POST /auth/register
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "SecurePassword123"
}
```

**Response (201):**
```json
{
  "access_token": "eyJhbGc...",
  "token_type": "bearer",
  "user": {
    "id": "uuid",
    "name": "John Doe",
    "email": "john@example.com",
    "avatar_url": null,
    "is_admin": false,
    "created_at": "2024-01-01T00:00:00"
  }
}
```

#### Login

```http
POST /auth/login
Content-Type: application/json

{
  "email": "john@example.com",
  "password": "SecurePassword123"
}
```

**Response (200):**
```json
{
  "access_token": "eyJhbGc...",
  "token_type": "bearer",
  "user": {
    "id": "uuid",
    "name": "John Doe",
    "email": "john@example.com",
    "avatar_url": null,
    "is_admin": false,
    "created_at": "2024-01-01T00:00:00"
  }
}
```

#### Get Current User

```http
GET /auth/me
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "id": "uuid",
  "name": "John Doe",
  "email": "john@example.com",
  "avatar_url": null,
  "is_admin": false,
  "created_at": "2024-01-01T00:00:00"
}
```

### Meetings

#### Create Meeting

```http
POST /meetings/create
Authorization: Bearer <token>
Content-Type: application/json

{
  "meeting_title": "Q1 Planning",
  "description": "Quarterly planning meeting",
  "max_participants": 20
}
```

**Response (201):**
```json
{
  "id": "uuid",
  "host_id": "uuid",
  "meeting_title": "Q1 Planning",
  "description": "Quarterly planning meeting",
  "status": "scheduled",
  "max_participants": 20,
  "created_at": "2024-01-01T00:00:00",
  "started_at": null,
  "ended_at": null
}
```

#### Get Meeting Details

```http
GET /meetings/{meeting_id}
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "id": "uuid",
  "host_id": "uuid",
  "meeting_title": "Q1 Planning",
  "description": "Quarterly planning meeting",
  "status": "in_progress",
  "max_participants": 20,
  "created_at": "2024-01-01T00:00:00",
  "started_at": "2024-01-01T10:00:00",
  "ended_at": null,
  "participants_count": 5,
  "transcript_count": 12,
  "has_summary": false
}
```

#### Get User Meetings

```http
GET /meetings/user/{user_id}
Authorization: Bearer <token>
```

**Response (200):**
```json
[
  {
    "id": "uuid",
    "host_id": "uuid",
    "meeting_title": "Q1 Planning",
    "status": "completed",
    "created_at": "2024-01-01T00:00:00",
    "started_at": "2024-01-01T10:00:00",
    "ended_at": "2024-01-01T11:00:00"
  }
]
```

#### Join Meeting

```http
POST /meetings/join
Authorization: Bearer <token>
Content-Type: application/json

{
  "meeting_id": "uuid"
}
```

**Response (200):**
```json
{
  "status": "joined",
  "participant_id": "uuid"
}
```

#### Leave Meeting

```http
POST /meetings/{meeting_id}/leave
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "status": "left"
}
```

#### End Meeting

```http
POST /meetings/{meeting_id}/end
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "id": "uuid",
  "host_id": "uuid",
  "meeting_title": "Q1 Planning",
  "status": "completed",
  "created_at": "2024-01-01T00:00:00",
  "started_at": "2024-01-01T10:00:00",
  "ended_at": "2024-01-01T11:00:00"
}
```

#### Get Meeting Transcripts

```http
GET /meetings/{meeting_id}/transcripts
Authorization: Bearer <token>
```

**Response (200):**
```json
[
  {
    "id": "uuid",
    "meeting_id": "uuid",
    "speaker_name": "John Doe",
    "transcript_text": "Let's discuss the Q1 goals...",
    "timestamp_seconds": 0,
    "confidence": 0.95,
    "created_at": "2024-01-01T10:00:00"
  }
]
```

### Audio

#### Upload Audio File

```http
POST /audio/upload
Authorization: Bearer <token>
Content-Type: multipart/form-data

meeting_id: uuid
file: <audio_file>
```

**Response (200):**
```json
{
  "status": "uploaded",
  "file_path": "/uploads/uuid_audio.mp3",
  "file_size": 5242880,
  "filename": "audio.mp3"
}
```

### AI & Summarization

#### Generate Summary

```http
POST /ai/summarize
Authorization: Bearer <token>
Content-Type: application/json

{
  "meeting_id": "uuid",
  "transcript_text": null,
  "max_length": 500
}
```

**Response (200):**
```json
{
  "id": "uuid",
  "meeting_id": "uuid",
  "summary_text": "The meeting discussed Q1 goals and objectives...",
  "action_items": [
    "Complete project proposal by Friday",
    "Schedule follow-up meeting",
    "Send meeting notes to team"
  ],
  "keywords": ["Q1", "goals", "planning", "timeline"],
  "duration_seconds": 3600,
  "word_count": 450,
  "generated_at": "2024-01-01T11:00:00"
}
```

#### Get Meeting Summary

```http
GET /ai/summary/{meeting_id}
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "id": "uuid",
  "meeting_id": "uuid",
  "summary_text": "The meeting discussed Q1 goals and objectives...",
  "action_items": [
    "Complete project proposal by Friday",
    "Schedule follow-up meeting",
    "Send meeting notes to team"
  ],
  "keywords": ["Q1", "goals", "planning", "timeline"],
  "duration_seconds": 3600,
  "word_count": 450,
  "generated_at": "2024-01-01T11:00:00"
}
```

### Admin

#### Get System Metrics

```http
GET /admin/metrics
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "total_users": 150,
  "total_meetings": 450,
  "completed_meetings": 420,
  "total_participants": 1200,
  "total_summaries": 400,
  "active_meetings": 30
}
```

#### Get All Users

```http
GET /admin/users?limit=100&offset=0
Authorization: Bearer <token>
```

**Response (200):**
```json
[
  {
    "id": "uuid",
    "name": "John Doe",
    "email": "john@example.com",
    "is_admin": false,
    "created_at": "2024-01-01T00:00:00"
  }
]
```

#### Get All Meetings

```http
GET /admin/meetings?limit=100&offset=0
Authorization: Bearer <token>
```

**Response (200):**
```json
[
  {
    "id": "uuid",
    "title": "Q1 Planning",
    "host_id": "uuid",
    "status": "completed",
    "participants_count": 5,
    "created_at": "2024-01-01T00:00:00",
    "ended_at": "2024-01-01T11:00:00"
  }
]
```

## Error Responses

### 400 Bad Request

```json
{
  "detail": "Invalid request parameters"
}
```

### 401 Unauthorized

```json
{
  "detail": "Invalid or expired token"
}
```

### 403 Forbidden

```json
{
  "detail": "Admin access required"
}
```

### 404 Not Found

```json
{
  "detail": "Resource not found"
}
```

### 429 Too Many Requests

```json
{
  "detail": "Rate limit exceeded"
}
```

### 500 Internal Server Error

```json
{
  "detail": "Internal server error",
  "error": "Error message"
}
```

## Rate Limiting

- **Limit:** 100 requests per minute per IP
- **Headers:** `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`

## WebSocket

### Real-time Transcription

```
ws://localhost:8000/ws/transcription?meeting_id=uuid&token=<token>
```

**Message Format:**
```json
{
  "type": "transcript",
  "speaker": "John Doe",
  "text": "Let's discuss the Q1 goals...",
  "timestamp": 0,
  "confidence": 0.95
}
```

## Pagination

Endpoints that return lists support pagination:

- `limit` - Number of items per page (default: 50, max: 100)
- `offset` - Number of items to skip (default: 0)

Example:
```
GET /admin/users?limit=20&offset=40
```

## Timestamps

All timestamps are in ISO 8601 format (UTC):
```
2024-01-01T12:00:00
```

## Rate Limits by Endpoint

| Endpoint | Limit |
|----------|-------|
| `/auth/register` | 5 per hour per IP |
| `/auth/login` | 10 per hour per IP |
| `/meetings/create` | 100 per hour per user |
| `/ai/summarize` | 50 per hour per user |
| Other endpoints | 100 per minute per IP |
