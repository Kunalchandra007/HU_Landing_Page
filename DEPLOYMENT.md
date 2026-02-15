# Deployment Guide

## Current Setup (Temporary)
The app is currently using SQLite with `/tmp` storage on Vercel. **This is temporary and data will be lost on each deployment.**

## Recommended: Use PostgreSQL with Supabase (Free)

### Step 1: Create Supabase Account
1. Go to https://supabase.com
2. Sign up for a free account
3. Create a new project

### Step 2: Get Database URL
1. In your Supabase project dashboard, go to Settings → Database
2. Copy the "Connection string" (URI format)
3. It will look like: `postgresql://postgres:[YOUR-PASSWORD]@[HOST]:5432/postgres`

### Step 3: Update Vercel Environment Variables
1. Go to your Vercel project settings
2. Navigate to Environment Variables
3. Add a new variable:
   - Name: `DATABASE_URL`
   - Value: Your Supabase connection string
4. Redeploy your project

### Step 4: Install PostgreSQL Driver
Add to requirements.txt:
```
psycopg2-binary
```

### Alternative: Railway.app PostgreSQL (Also Free)
1. Go to https://railway.app
2. Create a new PostgreSQL database
3. Copy the connection string
4. Add to Vercel environment variables

## Important Notes
- SQLite with `/tmp` will reset on every deployment
- Use a cloud database for production
- Update `DATABASE_URL` environment variable in Vercel
- The app will automatically create tables on startup
- Default admin credentials: username=admin, password=admin123

## Local Development
For local development, the app uses `sqlite:///university.db` which persists data locally.
