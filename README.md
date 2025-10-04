# Outfit Project (FastAPI + React)

This repository contains a FastAPI backend and a Vite + React frontend.

## Quick start (development)

1. Run backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
# copy .env.example to .env and set OPENWEATHER_KEY
uvicorn app.main:app --reload --port 8000
```

2. Run frontend

```bash
cd frontend
npm install
npm run dev
```

Open the frontend at `http://localhost:5173` and use the search box. The frontend proxies `/api` to the backend.

## Production

Build the frontend (`npm run build`) and copy the `dist/` contents into `backend/app/static`. Then run the backend (uvicorn) to serve both the API and the static frontend.
