# Full-Stack Vercel Deployment Guide

## 🚀 Quick Deployment Steps

### 1. Prepare Your Repository
Your project is now configured for full-stack Vercel deployment with:
- ✅ `vercel.json` - Main configuration
- ✅ `backend/api/index.py` - Serverless function entry point
- ✅ Frontend configured for relative API paths
- ✅ Backend optimized for serverless

### 2. Deploy to Vercel

#### Option A: Vercel CLI (Recommended)
```bash
# Install Vercel CLI
npm i -g vercel

# Login to Vercel
vercel login

# Deploy from project root
vercel

# Follow the prompts:
# - Set up and deploy? Yes
# - Which scope? (your account)
# - Link to existing project? No
# - Project name: outfit-project
# - Directory: ./
# - Override settings? No
```

#### Option B: Vercel Dashboard
1. Go to [Vercel.com](https://vercel.com)
2. Click "New Project"
3. Import your GitHub repository
4. **Keep Root Directory as `.` (root)**
5. Vercel will automatically detect the `vercel.json` configuration
6. Click "Deploy"

### 3. Your App Will Be Available At:
- **Frontend**: `https://outfit-project.vercel.app`
- **API**: `https://outfit-project.vercel.app/api/weather`

## 📁 Project Structure

```
outfit-project/
├── vercel.json              # Main Vercel configuration
├── frontend/                # React frontend
│   ├── src/
│   ├── package.json
│   └── ...
├── backend/                 # FastAPI backend
│   ├── api/
│   │   └── index.py        # Serverless function entry point
│   ├── app/
│   │   ├── main.py         # FastAPI app
│   │   ├── schemas.py
│   │   └── services/
│   └── requirements.txt
└── ...
```

## 🔧 Configuration Details

### `vercel.json` Breakdown:
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
      "src": "backend/api/index.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "/backend/api/index.py"
    },
    {
      "src": "/(.*)",
      "dest": "/frontend/dist/$1"
    }
  ],
  "functions": {
    "backend/api/index.py": {
      "runtime": "python3.9"
    }
  }
}
```

### How It Works:
1. **Frontend Build**: Vercel builds your React app from `frontend/`
2. **Backend Function**: Python serverless function from `backend/api/index.py`
3. **Routing**: 
   - `/api/*` → Backend serverless function
   - `/*` → Frontend static files

## 🌐 Environment Variables

For this setup, you typically don't need additional environment variables since:
- Frontend uses relative API paths (`/api/weather`)
- Backend runs as serverless function on the same domain
- CORS is configured to allow all origins

## 🚀 Deployment Commands

### Local Development:
```bash
# Start backend
cd backend
uvicorn app.main:app --reload

# Start frontend (in another terminal)
cd frontend
npm run dev
```

### Production Deployment:
```bash
# Deploy to Vercel
vercel

# Or deploy with production settings
vercel --prod
```

## 🔍 Testing Your Deployment

### 1. Test Frontend:
Visit: `https://your-app.vercel.app`
- Should show your React app
- Try searching for a location

### 2. Test API Directly:
Visit: `https://your-app.vercel.app/api/weather?location=London`
- Should return JSON weather data

### 3. Check Function Logs:
- Go to Vercel Dashboard → Functions tab
- View logs for debugging

## 🛠️ Troubleshooting

### Common Issues:

1. **"Module not found" errors**:
   - Check that `backend/api/index.py` has correct imports
   - Ensure Python path is set correctly

2. **CORS errors**:
   - Backend is configured with `allow_origins=["*"]`
   - Should work automatically

3. **API not responding**:
   - Check Vercel function logs
   - Verify the route configuration in `vercel.json`

4. **Frontend not loading**:
   - Ensure `frontend/package.json` exists
   - Check build logs in Vercel dashboard

### Debug Steps:
1. Check Vercel dashboard for build logs
2. Test API endpoint directly
3. Check function logs in Vercel dashboard
4. Verify all file paths in configuration

## 📊 Performance Benefits

- ✅ **Serverless scaling**: Automatic scaling based on demand
- ✅ **Global CDN**: Fast loading worldwide
- ✅ **Zero configuration**: Works out of the box
- ✅ **Cost effective**: Pay only for usage
- ✅ **Single deployment**: Frontend and backend together

## 🔄 Updates and Redeployment

### Automatic Deployments:
- Push to your main branch → Automatic deployment
- Vercel watches your GitHub repository

### Manual Deployments:
```bash
vercel --prod
```

## 🎯 Next Steps After Deployment

1. **Test your app**: Visit the deployed URL
2. **Set up custom domain** (optional): In Vercel dashboard
3. **Monitor performance**: Check Vercel analytics
4. **Set up monitoring**: Add error tracking if needed

Your outfit project is now ready for full-stack Vercel deployment! 🎉
