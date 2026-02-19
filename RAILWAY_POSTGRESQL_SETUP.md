# Railway PostgreSQL Setup Guide

## Problem
Railway uses an **ephemeral filesystem** - any files (SQLite database, uploaded images) are deleted when the container restarts or redeploys. This is why your admin changes disappear.

## Solution
Use PostgreSQL database and cloud storage for images.

---

## Step 1: Add PostgreSQL to Railway

1. Go to your Railway project dashboard
2. Click **"+ New"** button
3. Select **"Database"** → **"Add PostgreSQL"**
4. Railway will automatically create a PostgreSQL database
5. The `DATABASE_URL` environment variable will be automatically added to your backend service

---

## Step 2: Update Backend Requirements

The `psycopg2-binary` package is already in `backend/requirements.txt`, so no changes needed.

---

## Step 3: Verify Environment Variables

In Railway dashboard, go to your backend service → **Variables** tab:

Make sure these exist:
- `DATABASE_URL` - Should be automatically set by Railway when you add PostgreSQL
- `SECRET_KEY` - Set to a random string (e.g., `your-secret-key-12345`)

---

## Step 4: Deploy

1. Push your code to GitHub (if using GitHub deployment)
2. Or trigger a redeploy in Railway dashboard
3. Railway will:
   - Detect PostgreSQL connection
   - Create all tables automatically
   - Create admin user (username: `admin`, password: `admin123`)

---

## Step 5: Image Storage (Important!)

### Current Issue
Images are saved to the filesystem, which is ephemeral on Railway.

### Temporary Solution (Current)
Images are saved to both:
- `backend/static/images/` (for Railway backend)
- `frontend/public/images/` (for local development)

**Note:** Images will still be lost on Railway redeploy. For permanent storage, you need cloud storage.

### Permanent Solution (Recommended)
Use cloud storage like:
- **Cloudinary** (free tier: 25GB storage, 25GB bandwidth/month)
- **AWS S3**
- **Google Cloud Storage**

---

## How to Check if PostgreSQL is Working

1. Check Railway logs after deployment
2. Look for: `Using PostgreSQL database - creating tables with correct schema...`
3. Add an event/happening/glimpse through admin panel
4. Trigger a redeploy
5. Check if the data persists after redeploy

---

## Current Database Configuration

The backend automatically detects the database type:

```python
# If DATABASE_URL contains 'postgresql' → Use PostgreSQL
# If DATABASE_URL is not set → Use SQLite (local development only)
```

---

## Admin Panel Access

- URL: `https://your-railway-url.up.railway.app/admin`
- Username: `admin`
- Password: `admin123`

---

## Troubleshooting

### Data still disappearing?
- Verify PostgreSQL is added to your Railway project
- Check that `DATABASE_URL` environment variable exists
- Check Railway logs for database connection errors

### Images disappearing?
- This is expected with current setup (ephemeral filesystem)
- Implement Cloudinary or S3 for permanent image storage

### Can't connect to database?
- Check Railway logs for connection errors
- Verify PostgreSQL service is running
- Check if `DATABASE_URL` has `?sslmode=require` appended (backend does this automatically)
