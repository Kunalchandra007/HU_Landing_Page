# Vercel Environment Variable Setup

To make the deployed site work properly, you need to set the environment variable in Vercel:

## Steps:

1. Go to https://vercel.com/dashboard
2. Select your project (hu-final)
3. Go to "Settings" tab
4. Click on "Environment Variables" in the left sidebar
5. Add the following environment variable:
   - **Name**: `REACT_APP_API_URL`
   - **Value**: `https://web-production-bd5a.up.railway.app/api`
   - **Environment**: Select all (Production, Preview, Development)
6. Click "Save"
7. Go to "Deployments" tab
8. Click the three dots (...) on the latest deployment
9. Click "Redeploy"

This will ensure the frontend uses the correct Railway backend URL in production.

## Alternative: Use Vercel CLI

If you have Vercel CLI installed, you can run:

```bash
vercel env add REACT_APP_API_URL
# Enter: https://web-production-bd5a.up.railway.app/api
# Select: Production, Preview, Development

vercel --prod
```

## Current Issue

The frontend is currently hardcoded to use `http://localhost:5000/api` which only works locally.
After setting the environment variable in Vercel, the deployed site will use the Railway backend.
