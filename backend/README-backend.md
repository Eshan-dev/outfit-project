# Backend (FastAPI)

## Setup (dev)

1. Create virtualenv and install deps:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Create `.env` (copy `.env.example`) and set `OPENWEATHER_KEY`.

3. Run server:

```bash
uvicorn app.main:app --reload --port 8000
```

API: GET `/api/weather?location=CityName` returns JSON with `weather` and `suggestions`.

In production, copy the frontend `dist` build to `backend/app/static` so FastAPI serves it.
