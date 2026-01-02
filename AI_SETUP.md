# 🤖 AI Features Setup Guide

## Overview

EchoBrief AI supports two AI services for meeting summarization:
1. **Groq** (Free, Fast, Recommended)
2. **OpenAI** (Paid, GPT-3.5/GPT-4)

You only need to configure ONE of them.

---

## 🚀 Option 1: Groq (Recommended - Free & Fast)

### Step 1: Get Groq API Key

1. Go to https://console.groq.com/keys
2. Click "Sign Up" or "Sign In"
3. Create a free account
4. Go to API Keys section
5. Click "Create API Key"
6. Copy the key (starts with `gsk_`)

### Step 2: Add to .env File

1. Open `/backend/.env`
2. Find the line: `GROQ_API_KEY=`
3. Paste your key:
```
GROQ_API_KEY=gsk_your_actual_key_here
```
4. Save the file

### Step 3: Restart Backend

The backend will automatically reload and use the new key.

---

## 💳 Option 2: OpenAI (Paid)

### Step 1: Get OpenAI API Key

1. Go to https://platform.openai.com/api-keys
2. Sign up or login
3. Click "Create new secret key"
4. Copy the key (starts with `sk-`)

### Step 2: Add to .env File

1. Open `/backend/.env`
2. Find the line: `OPENAI_API_KEY=`
3. Paste your key:
```
OPENAI_API_KEY=sk_your_actual_key_here
```
4. Save the file

### Step 3: Restart Backend

The backend will automatically reload and use the new key.

---

## ✅ Verify Setup

### Test Summarization

1. Go to http://localhost:8000/docs
2. Make sure you're authorized (click 🔒 Authorize)
3. Find `POST /api/ai/summarize`
4. Click "Try it out"
5. Fill in:
```json
{
  "meeting_id": "YOUR_MEETING_ID",
  "max_length": 500
}
```
6. Click "Execute"
7. Should return summary with action items and keywords ✅

---

## 🔧 Troubleshooting

### Error: "No AI service configured"
- Make sure you added the API key to `.env`
- Make sure the backend restarted after editing `.env`
- Check that the key is not empty

### Error: "Invalid API key"
- Double-check the key is correct
- Make sure you copied the entire key
- Try generating a new key

### Error: "API rate limit exceeded"
- You've made too many requests
- Wait a few minutes and try again
- Consider upgrading your plan

---

## 📊 AI Features Available

Once configured, you can use:

### 1. Meeting Summarization
```
POST /api/ai/summarize
```
- Generates concise summary
- Extracts action items
- Identifies keywords

### 2. Get Summary
```
GET /api/ai/summary/{meeting_id}
```
- Retrieve saved summary
- View action items
- See keywords

---

## 🎯 Groq vs OpenAI

| Feature | Groq | OpenAI |
|---------|------|--------|
| **Cost** | Free | Paid |
| **Speed** | Very Fast | Fast |
| **Quality** | Good | Excellent |
| **Model** | Mixtral 8x7B | GPT-3.5/GPT-4 |
| **Setup** | Easy | Easy |
| **Recommended** | ✅ Yes | For better quality |

---

## 📝 Current Configuration

Your `.env` file is located at:
```
/Applications/PostgreSQL 18/EchoBrief/backend/.env
```

Lines to update:
```
# Line 12: Add Groq key
GROQ_API_KEY=gsk_your_key_here

# OR Line 15: Add OpenAI key
OPENAI_API_KEY=sk_your_key_here
```

---

## 🔐 Security Notes

- Never commit `.env` file to git
- Never share your API keys
- Keep keys confidential
- Rotate keys regularly
- Monitor API usage

---

## 🚀 Next Steps

1. Choose Groq or OpenAI
2. Get your API key
3. Add to `.env` file
4. Restart backend
5. Test summarization in Swagger UI
6. Use in frontend application

---

## 📞 Support

If you encounter issues:
1. Check the error message
2. Verify API key is correct
3. Ensure backend restarted
4. Check API service status
5. Review logs in terminal

---

**Ready to enable AI features?** 🤖
