# Deployment Guide for Outfit Project

## Current Setup
- **Frontend**: React + Vite (port 5173)
- **Backend**: FastAPI (port 8000)
- **API Endpoint**: `/api/weather`

## Deployment Options

### Option 1: Deploy Backend and Frontend Separately

#### Backend Deployment
Deploy your FastAPI backend to services like:
- **Heroku**: `https://your-app-name.herokuapp.com`
- **Railway**: `https://your-app-name.railway.app`
- **Render**: `https://your-app-name.onrender.com`
- **DigitalOcean App Platform**: `https://your-app-name.ondigitalocean.app`

#### Frontend Deployment
Deploy your React frontend to:
- **Vercel**: `https://your-app-name.vercel.app`
- **Netlify**: `https://your-app-name.netlify.app`
- **GitHub Pages**: `https://yourusername.github.io/your-repo`

#### Configuration
1. **Backend**: Set environment variables:
   ```bash
   ALLOWED_ORIGINS=https://your-frontend-domain.com
   ```

2. **Frontend**: Create `.env` file:
   ```bash
   VITE_API_URL=https://your-backend-domain.com
   ```

### Option 2: Deploy as Single Application

#### Using the Built-in Static File Serving
Your backend is already configured to serve static files from `./app/static`.

1. **Build the frontend**:
   ```bash
   cd frontend
   npm run build
   ```

2. **Copy build files to backend**:
   ```bash
   # Copy the dist folder contents to backend/app/static
   cp -r frontend/dist/* backend/app/static/
   ```

3. **Deploy only the backend** - it will serve both API and frontend

#### Environment Variables for Backend
```bash
ALLOWED_ORIGINS=*
# or for production:
ALLOWED_ORIGINS=https://your-domain.com
```

## Example URLs for Different Hosting Services

### Heroku
- Backend: `https://outfit-backend-123.herokuapp.com`
- Frontend: `https://outfit-frontend-456.herokuapp.com`
- Set `VITE_API_URL=https://outfit-backend-123.herokuapp.com`

### Vercel + Railway
- Backend (Railway): `https://outfit-backend-production.up.railway.app`
- Frontend (Vercel): `https://outfit-frontend.vercel.app`
- Set `VITE_API_URL=https://outfit-backend-production.up.railway.app`

### Single App Deployment
- Full App: `https://outfit-app-123.herokuapp.com`
- No environment variables needed (uses relative paths)

## Quick Start Commands

### For Separate Deployment:
```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port $PORT

# Frontend
cd frontend
npm install
npm run build
# Deploy the dist folder to your hosting service
```

### For Single App Deployment:
```bash
# Build frontend
cd frontend
npm run build

# Copy to backend
mkdir -p backend/app/static
cp -r frontend/dist/* backend/app/static/

# Deploy backend only
cd backend
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

## Environment Variables Summary

| Variable | Purpose | Example |
|----------|---------|---------|
| `VITE_API_URL` | Frontend API URL | `https://api.yourdomain.com` |
| `ALLOWED_ORIGINS` | Backend CORS origins | `https://yourdomain.com` |
