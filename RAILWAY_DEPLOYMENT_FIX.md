# Railway Deployment Fix - FINAL

## Problem
Railway deployment was crashing with error: "The executable 'cd' could not be found"

## Root Cause
The CMD in Dockerfile was using shell variable expansion without proper shell invocation.

## Solution Applied

### ✅ 1. Fixed Dockerfile CMD
Changed from:
```dockerfile
CMD gunicorn -w 4 -b 0.0.0.0:$PORT backend.app:app
```

To:
```dockerfile
CMD ["sh", "-c", "gunicorn -w 4 -b 0.0.0.0:${PORT} backend.app:app"]
```

This properly invokes a shell to handle the PORT environment variable.

### ✅ 2. Added railway.json
Created explicit Railway configuration to force Dockerfile usage:
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "DOCKERFILE",
    "dockerfilePath": "Dockerfile"
  }
}
```

### ✅ 3. Created .dockerignore
Added proper .dockerignore to exclude unnecessary files from build.

### ✅ 4. Removed Procfile
Deleted Procfile to avoid conflicts with Dockerfile.

### ✅ 5. Set Default PORT
Added `ENV PORT=8080` as fallback in Dockerfile.

## Files Modified

1. **Dockerfile** - Fixed CMD to use shell array format
2. **railway.json** - Created to force Dockerfile builder
3. **.dockerignore** - Created to optimize build
4. **Procfile** - Removed to avoid conflicts

## Final Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY backend/requirements.txt backend/requirements.txt
RUN pip install --no-cache-dir -r backend/requirements.txt

COPY . .

RUN mkdir -p backend/instance

ENV PYTHONUNBUFFERED=1
ENV PORT=8080

CMD ["sh", "-c", "gunicorn -w 4 -b 0.0.0.0:${PORT} backend.app:app"]
```

## Next Steps

1. Commit and push:
   ```bash
   git add Dockerfile railway.json .dockerignore
   git add -u
   git commit -m "Fix Railway deployment - proper shell CMD format"
   git push
   ```

2. Railway will automatically redeploy

3. The container should now start successfully

## Why This Works

- `CMD ["sh", "-c", "..."]` properly invokes a shell to expand ${PORT}
- railway.json explicitly tells Railway to use Dockerfile (not nixpacks)
- Default PORT=8080 ensures fallback if Railway doesn't set it
- .dockerignore optimizes build by excluding unnecessary files

## Environment Variables in Railway

Railway automatically sets:
- `PORT` - The port your app should listen on

You should set:
- `SECRET_KEY` - Flask secret key
- `FLASK_ENV` - Set to "production"
