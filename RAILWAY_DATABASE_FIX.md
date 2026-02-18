# Railway Database Fix - Make Glimpse Image Optional

## Problem
The Railway database still has the `image_path` column as NOT NULL, preventing glimpses from being added without images.

## Solution Options

### Option 1: Wait for Automatic Migration (Recommended)
The backend code now includes automatic migration on startup. Railway should run this automatically on the next deployment.

**To trigger a new deployment:**
1. Go to Railway dashboard: https://railway.app/
2. Select your project
3. Click on the backend service
4. Click "Deploy" or "Redeploy"
5. Wait for deployment to complete
6. Check the logs to confirm migration ran

### Option 2: Manual Database Fix via Railway CLI

If you have Railway CLI installed:

```bash
# Install Railway CLI if needed
npm install -g @railway/cli

# Login
railway login

# Link to your project
railway link

# Connect to database
railway run python -c "
import sqlite3
import os

db_path = 'backend/instance/university.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create new table with nullable image_path
cursor.execute('''
    CREATE TABLE glimpse_new (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title VARCHAR(200) NOT NULL,
        description TEXT NOT NULL,
        image_path VARCHAR(300),
        video_url VARCHAR(500) NOT NULL,
        hashtags VARCHAR(500),
        is_active BOOLEAN DEFAULT 1,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
''')

# Copy data
cursor.execute('INSERT INTO glimpse_new SELECT * FROM glimpse')

# Replace table
cursor.execute('DROP TABLE glimpse')
cursor.execute('ALTER TABLE glimpse_new RENAME TO glimpse')

conn.commit()
conn.close()
print('Migration completed!')
"
```

### Option 3: Force Redeploy with Empty Commit

```bash
git commit --allow-empty -m "Trigger Railway redeploy for database migration"
git push origin main
```

Then check Railway logs to confirm the migration ran.

## Verify Migration Worked

After migration, test by adding a glimpse without an image through the admin panel.

## Current Status

- ✅ Backend code updated with automatic migration
- ✅ Frontend updated to make image optional
- ✅ Models updated to allow NULL image_path
- ⏳ Waiting for Railway to run migration on next deployment

## Next Steps

1. Trigger Railway redeployment (Option 1 or 3)
2. Check Railway logs for "Migration completed!" message
3. Test adding glimpse without image on deployed site
