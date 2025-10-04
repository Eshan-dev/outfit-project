# Vercel Deployment Guide for Outfit Project

## 🚀 Quick Start

### Option 1: Frontend on Vercel + Backend on Railway (Recommended)

#### Step 1: Deploy Backend to Railway
1. Go to [Railway.app](https://railway.app)
2. Connect your GitHub repository
3. Select the `backend` folder
4. Railway will automatically detect Python and install dependencies
5. Copy your Railway URL (e.g., `https://outfit-backend-production.up.railway.app`)

#### Step 2: Deploy Frontend to Vercel
1. Go to [Vercel.com](https://vercel.com)
2. Import your GitHub repository
3. Set the **Root Directory** to `frontend`
4. Add Environment Variable:
   - **Name**: `VITE_API_URL`
   - **Value**: `https://your-railway-backend-url.railway.app`
5. Deploy!

### Option 2: Full-Stack on Vercel (Serverless)

#### Deploy Everything to Vercel
1. Go to [Vercel.com](https://vercel.com)
2. Import your GitHub repository
3. Keep the **Root Directory** as `.` (root)
4. Vercel will automatically detect the configuration from `vercel.json`
5. Deploy!

## 📁 Project Structure for Vercel

```
outfit-project/
├── frontend/                 # React frontend
│   ├── vercel.json         # Frontend-only config
│   └── ...
├── backend/                 # FastAPI backend
│   ├── api/
│   │   └── index.py        # Vercel serverless entry point
│   └── ...
├── vercel.json             # Full-stack config
└── ...
```

## 🔧 Configuration Files

### Frontend-only Vercel Config (`frontend/vercel.json`)
```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "framework": "vite",
  "env": {
    "VITE_API_URL": "@vite_api_url"
  }
}
```

### Full-stack Vercel Config (`vercel.json`)
```json
{
  "version": 2,
  "builds": [
    {
      "src": "frontend/package.json",
      "use": "@vercel/static-build",
      "config": {
        "distDir": "dist"
      }
    },
    {
      "src": "backend/app/main.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "/backend/app/main.py"
    },
    {
      "src": "/(.*)",
      "dest": "/frontend/dist/$1"
    }
  ]
}
```

## 🌐 Environment Variables

### For Option 1 (Frontend + External Backend)
In Vercel dashboard, add:
- `VITE_API_URL` = `https://your-railway-backend.railway.app`

### For Option 2 (Full-stack on Vercel)
No additional environment variables needed - uses relative paths.

## 🚀 Deployment Commands

### Option 1: Separate Deployment
```bash
# Deploy backend to Railway
cd backend
# Railway handles deployment automatically

# Deploy frontend to Vercel
cd frontend
# Vercel handles deployment automatically
```

### Option 2: Full-stack Deployment
```bash
# Deploy everything to Vercel
# Vercel handles both frontend and backend automatically
```

## 🔍 Troubleshooting

### Common Issues:

1. **CORS Errors**: Make sure your backend has proper CORS configuration
2. **API Not Found**: Check that your backend URL is correct in environment variables
3. **Build Failures**: Ensure all dependencies are in `package.json` and `requirements.txt`

### Debug Steps:
1. Check Vercel function logs in the dashboard
2. Verify environment variables are set correctly
3. Test API endpoints directly: `https://your-app.vercel.app/api/weather?location=London`

## 📊 Performance Tips

- **Option 1**: Better for development, easier to debug
- **Option 2**: Better for production, single deployment, serverless scaling

## 🔗 Example URLs

After deployment, your app will be available at:
- **Option 1**: `https://outfit-project.vercel.app`
- **Option 2**: `https://outfit-project.vercel.app`

API endpoints:
- **Option 1**: `https://your-railway-backend.railway.app/api/weather`
- **Option 2**: `https://outfit-project.vercel.app/api/weather`
