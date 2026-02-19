# Fix Data Persistence Issue - Quick Guide

## The Problem
Your admin changes disappear because Railway uses **ephemeral storage**. Every time Railway restarts or redeploys:
- SQLite database file is deleted
- Uploaded images are deleted
- All your changes are lost

## The Solution (3 Steps)

### Step 1: Add PostgreSQL to Railway

1. Open your Railway project: https://railway.app/project/your-project
2. Click the **"+ New"** button in your project
3. Select **"Database"**
4. Choose **"Add PostgreSQL"**
5. Railway will create a PostgreSQL database and automatically link it to your backend service

**That's it!** Railway automatically sets the `DATABASE_URL` environment variable.

---

### Step 2: Redeploy Your Backend

After adding PostgreSQL:

1. Go to your backend service in Railway
2. Click **"Deploy"** → **"Redeploy"**
3. Wait for deployment to complete (check logs)

You should see in the logs:
```
Using PostgreSQL database - creating tables with correct schema...
✅ PostgreSQL tables created successfully
✅ Admin user created (username: admin, password: admin123)
```

---

### Step 3: Test Data Persistence

1. Login to admin panel: `https://your-railway-url.up.railway.app/admin`
2. Add a new event/happening/glimpse
3. Go back to Railway dashboard
4. Redeploy your backend service again
5. Check if your data is still there ✅

---

## What About Images?

### Current Status
Images are still saved to the filesystem, which means:
- ✅ Images work during the current deployment
- ❌ Images are lost when you redeploy

### Quick Fix (For Now)
After each redeploy, you'll need to re-upload images through the admin panel.

### Permanent Fix (Recommended Later)
Implement cloud storage like Cloudinary:
- Free tier: 25GB storage
- Images persist forever
- Automatic image optimization
- CDN delivery

---

## Verification

Run this command locally to check your database:
```bash
python verify_database.py
```

This will show:
- Database type (PostgreSQL or SQLite)
- Number of events, happenings, glimpses
- Admin users

---

## Important Notes

1. **PostgreSQL = Persistent Data** ✅
   - Events, happenings, glimpses will persist
   - Admin users will persist
   - Data survives redeploys

2. **Filesystem = Ephemeral** ❌
   - Uploaded images will be lost on redeploy
   - Need cloud storage for permanent images

3. **Local Development**
   - Still uses SQLite (no PostgreSQL needed locally)
   - Images saved to `frontend/public/images/`

---

## Troubleshooting

### "Data still disappearing after adding PostgreSQL"

Check Railway environment variables:
1. Go to backend service → **Variables** tab
2. Verify `DATABASE_URL` exists and starts with `postgresql://`
3. If not, manually add PostgreSQL database to project

### "Can't see PostgreSQL in Railway"

1. Make sure you added it to the **same project** as your backend
2. Railway should auto-link it
3. Check backend logs for database connection messages

### "Images not loading"

This is expected with current setup. Images are ephemeral on Railway.
- Option 1: Re-upload after each deploy
- Option 2: Implement Cloudinary (permanent solution)

---

## Next Steps

1. ✅ Add PostgreSQL to Railway (5 minutes)
2. ✅ Redeploy and test (2 minutes)
3. ⏳ Implement Cloudinary for images (optional, 30 minutes)

Your data will persist after Step 1 & 2!
