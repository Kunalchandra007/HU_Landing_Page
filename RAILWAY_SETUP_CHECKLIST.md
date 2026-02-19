# Railway Setup Checklist ✅

## Current Problem
```
┌─────────────────────────────────────────┐
│  Railway Container (Ephemeral)         │
│                                         │
│  ┌──────────────┐  ┌─────────────┐    │
│  │ SQLite DB    │  │   Images    │    │
│  │ university.db│  │ /static/... │    │
│  └──────────────┘  └─────────────┘    │
│         ↓                  ↓            │
│    DELETED ON          DELETED ON      │
│    REDEPLOY!           REDEPLOY!       │
└─────────────────────────────────────────┘
```

## Solution
```
┌─────────────────────────────────────────┐
│  Railway Container (Ephemeral)         │
│                                         │
│  ┌──────────────────────────────────┐  │
│  │   Backend Application            │  │
│  │   (Flask API)                    │  │
│  └──────────────────────────────────┘  │
│         ↓                                │
└─────────┼────────────────────────────────┘
          ↓
┌─────────┴────────────────────────────────┐
│  PostgreSQL Database (Persistent)       │
│  ✅ Data survives redeploys              │
│  ✅ Events, Happenings, Glimpses         │
│  ✅ Admin users                          │
└──────────────────────────────────────────┘
```

---

## Setup Steps

### ☐ Step 1: Add PostgreSQL Database
**Time: 2 minutes**

1. Open Railway project dashboard
2. Click **"+ New"** button
3. Select **"Database"** → **"Add PostgreSQL"**
4. Wait for provisioning (30 seconds)

**Result:** `DATABASE_URL` environment variable is automatically added

---

### ☐ Step 2: Verify Environment Variables
**Time: 1 minute**

Go to backend service → **Variables** tab

Should see:
```
DATABASE_URL = postgresql://postgres:xxxxx@xxxxx.railway.app:5432/railway
SECRET_KEY = your-secret-key-12345
```

If `DATABASE_URL` is missing, Railway didn't auto-link. Manually add PostgreSQL.

---

### ☐ Step 3: Redeploy Backend
**Time: 2 minutes**

1. Go to backend service
2. Click **"Deploy"** → **"Redeploy"**
3. Watch the logs

**Expected logs:**
```
Using PostgreSQL database - creating tables with correct schema...
✅ PostgreSQL tables created successfully
✅ Admin user created (username: admin, password: admin123)
```

---

### ☐ Step 4: Test Data Persistence
**Time: 3 minutes**

1. Login to admin panel
   - URL: `https://your-backend.railway.app/admin`
   - Username: `admin`
   - Password: `admin123`

2. Add a test event:
   - Title: "Test Event"
   - Description: "Testing persistence"
   - Date: Any future date
   - Image: Any image

3. Go to Railway dashboard → Redeploy backend

4. Refresh admin panel → Check if "Test Event" still exists ✅

---

## Verification Checklist

After completing all steps:

- [ ] PostgreSQL database is added to Railway project
- [ ] `DATABASE_URL` environment variable exists
- [ ] Backend logs show "Using PostgreSQL database"
- [ ] Admin user can login
- [ ] Added content persists after redeploy
- [ ] Frontend displays content from database

---

## What's Fixed vs What's Not

### ✅ Fixed (Persistent)
- Events data
- Happenings data
- Glimpses data
- Admin users
- All database content

### ❌ Still Ephemeral (Temporary)
- Uploaded images
- Static files

**Why?** Railway's filesystem is ephemeral. Images need cloud storage (Cloudinary/S3).

---

## Image Storage Options

### Option 1: Accept Ephemeral Images (Current)
- **Pros:** No setup needed
- **Cons:** Re-upload images after each deploy
- **Best for:** Testing, development

### Option 2: Use Cloudinary (Recommended)
- **Pros:** Permanent storage, CDN, free tier
- **Cons:** Requires code changes (30 min setup)
- **Best for:** Production

### Option 3: Use AWS S3
- **Pros:** Scalable, reliable
- **Cons:** More complex setup, costs money
- **Best for:** Large scale production

---

## Common Issues

### Issue: Data still disappearing
**Solution:** 
- Verify PostgreSQL is added to the **same Railway project**
- Check `DATABASE_URL` in environment variables
- Check logs for "Using PostgreSQL database"

### Issue: Can't login to admin
**Solution:**
- Check logs for "Admin user created"
- Try username: `admin`, password: `admin123`
- If still fails, check database connection in logs

### Issue: Images not loading
**Solution:**
- This is expected (ephemeral filesystem)
- Images work until next redeploy
- Implement Cloudinary for permanent storage

---

## Success Criteria

You'll know it's working when:

1. ✅ You can add events/happenings/glimpses
2. ✅ Content appears on the frontend
3. ✅ After redeploying Railway, content is still there
4. ✅ Admin panel shows all your content
5. ⚠️  Images disappear after redeploy (expected until Cloudinary)

---

## Need Help?

1. Check Railway logs for errors
2. Run `python verify_database.py` locally
3. Verify `DATABASE_URL` environment variable
4. Check PostgreSQL service is running in Railway

---

## Timeline

- **Immediate:** Add PostgreSQL (5 minutes)
- **Short term:** Test and verify (5 minutes)
- **Later:** Implement Cloudinary for images (30 minutes)

**Total time to fix data persistence: 10 minutes**
