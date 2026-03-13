# DeepSeek Chat

A full-stack AI chat application built with FastAPI + Vue 3, powered by DeepSeek API.

## Features

- User registration and login with JWT authentication
- Multi-conversation management (create, rename, delete)
- Real-time streaming responses via SSE
- Markdown rendering with syntax-highlighted code blocks
- One-click code copy
- Responsive dark-themed UI

## Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+
- A DeepSeek API key ([get one here](https://platform.deepseek.com/))

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
# Edit .env and set your DEEPSEEK_API_KEY
uvicorn app.main:app --reload --port 8000
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173 in your browser.

## Tech Stack

- **Backend**: FastAPI, SQLAlchemy (async), SQLite, python-jose (JWT), OpenAI SDK
- **Frontend**: Vue 3, Vite, Pinia, Vue Router, markdown-it, highlight.js
