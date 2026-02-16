# Deploy Frontend to Vercel

## Step 1: Push to GitHub

```bash
git add -A
git commit -m "React frontend ready for deployment"
git push origin main
```

## Step 2: Deploy on Vercel

1. Go to https://vercel.com
2. Click "New Project"
3. Import your GitHub repository
4. Configure project:
   - **Framework Preset**: Create React App
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `build`
   - **Install Command**: `npm install`

5. Add Environment Variable:
   - Name: `REACT_APP_API_URL`
   - Value: `https://your-backend-url.com/api` (add this after deploying backend)

6. Click "Deploy"

## Step 3: Deploy Backend (Separate)

### Option A: Railway.app (Recommended)
1. Go to https://railway.app
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Set root directory to `backend`
5. Railway will auto-detect Flask
6. Add environment variables:
   - `DATABASE_URL` (get from Railway PostgreSQL)
   - `SECRET_KEY`
   - `MAIL_USERNAME`
   - `MAIL_PASSWORD`
7. Deploy!

### Option B: Render.com
1. Go to https://render.com
2. New → Web Service
3. Connect GitHub repository
4. Settings:
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn api:app`
5. Add environment variables
6. Create PostgreSQL database on Render
7. Deploy!

## Step 4: Update Frontend with Backend URL

1. Go back to Vercel project settings
2. Environment Variables
3. Update `REACT_APP_API_URL` with your backend URL
4. Redeploy frontend

## Done! 🎉

Your frontend will be live on Vercel and backend on Railway/Render.

## Important Notes

- Frontend URL: `https://your-project.vercel.app`
- Backend URL: `https://your-backend.railway.app` or `https://your-backend.onrender.com`
- Make sure CORS is configured in backend to allow your Vercel domain
- Update `REACT_APP_API_URL` in Vercel environment variables

## Troubleshooting

### 404 Error on Vercel
- Make sure root directory is set to `frontend`
- Check that `vercel.json` exists in frontend folder

### CORS Error
- Update backend `api.py` CORS origins to include your Vercel URL
- Example: `origins=["https://your-project.vercel.app"]`

### API Not Working
- Check backend is deployed and running
- Verify `REACT_APP_API_URL` is set correctly in Vercel
- Check browser console for errors
