# 🚀 COMPLETE SE ASSIGNMENT DEPLOYMENT GUIDE (Vercel + Render)

## 🎯 PROJECT OVERVIEW
- **Frontend:** HTML/CSS/JS → Vercel
- **Backend:** FastAPI (Python) → Render
- **Database:** PostgreSQL (already configured)
- **Authentication:** JWT with PyJWT

---

# � DEPLOYMENT PROGRESS TRACKER

**Current Status:** Edit this section as you complete each step

```
STEPS (7 TOTAL)

✅ [x] Prepare backend for deployment (IN VS CODE)
✅ [x] Configure CORS in backend (IN VS CODE)
✅ [x] Commit & push to GitHub (IN VS CODE)
⏳ [ ] Deploy backend to Render (OUTSIDE VS CODE)
⏳ [ ] Deploy frontend to Vercel (OUTSIDE VS CODE)
⏳ [ ] Connect frontend to backend (IN VS CODE)
⏳ [ ] Test deployed system (IN BROWSER)
```

**Legend:**
- ✅ = Completed
- ⏳ = In Progress
- ⭕ = Not Started

---

# 🎯 QUICK STATUS

| What | Status | When |
|------|--------|------|
| Backend Code | ✅ Ready | Done in VS Code |
| Backend URL | ⏳ Pending | Will get from Render |
| Frontend Code | ⏳ Ready | Just need to update API URL |
| Frontend URL | ⏳ Pending | Will get from Vercel |
| CORS Config | ✅ Done | Already configured with PyJWT |
| Testing | ⏳ Pending | After both deployed |

---

# �📁 PROJECT STRUCTURE
```
SE/
├── Backend/
│   ├── requirements.txt (Python dependencies)
│   ├── app/
│   │   ├── main.py (FastAPI app)
│   │   ├── config.py (Settings & env vars)
│   │   ├── auth/jwt.py (JWT authentication)
│   │   ├── models/ (Database models)
│   │   ├── routes/ (API endpoints)
│   │   └── schemas/ (Data validation)
│   └── docker-compose.yml
├── Frontend/
│   ├── index.html
│   ├── app.js (Main JavaScript)
│   ├── styles.css
│   └── product-data.js
└── tasks/
    └── deployment.md (This file)
```

---

# ⚙️ STEP 1: PREPARE BACKEND FOR DEPLOYMENT (IN VS CODE)

## 1.1 Backend Dependencies

**File:** [Backend/requirements.txt](../Backend/requirements.txt)

```
fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
PyJWT==2.8.1
python-multipart==0.0.6
python-dotenv==1.0.0
alembic==1.12.1
pydantic==2.5.0
cryptography==41.0.7
passlib==1.7.4
bcrypt==4.1.1
```

**Why PyJWT?** - Pre-built wheels, no Rust compilation needed. Avoids Render build errors.

## 1.2 CORS Configuration

**File:** [Backend/app/config.py](../Backend/app/config.py)

```python
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://user:Lhw4bJEg8rCvMIm7d7gcY9uTesrDkqdr@dpg-d42gdhngi27c73c50650-a/ecommerce_w12z")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "5d0254f31c923e14d56914bd09441ae31fad7892fbc562d53497773eb24b698f")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:5173,http://localhost:3000")

settings = Settings()
```

## 1.3 JWT Configuration

**File:** [Backend/app/auth/jwt.py](../Backend/app/auth/jwt.py)

```python
from datetime import datetime, timedelta
import jwt
from jwt import InvalidTokenError
from fastapi import HTTPException, status
import bcrypt
from app.config import settings

def verify_password(plain_password, hashed_password):
    try:
        if isinstance(plain_password, str):
            plain_password = plain_password.encode('utf-8')
        if isinstance(hashed_password, str):
            hashed_password = hashed_password.encode('utf-8')
        return bcrypt.checkpw(plain_password, hashed_password)
    except ValueError:
        return False

def get_password_hash(password):
    if isinstance(password, str):
        password = password.encode('utf-8')
    return bcrypt.hashpw(password, bcrypt.gensalt()).decode('utf-8')

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """Generate JWT token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    """Decode JWT and return payload dict."""
    try:
        if token.startswith("Bearer "):
            token = token.split(" ")[1]
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
```

## 1.4 Main FastAPI App

**File:** [Backend/app/main.py](../Backend/app/main.py)

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.models import user, product, order
from app.routes import auth, product as product_routes, order as order_routes
from app.config import settings

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="E-Commerce API",
    description="A complete e-commerce backend with authentication",
    version="1.0.0"
)

# CORS middleware - Production ready
allowed_origins = settings.FRONTEND_URL.split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(product_routes.router, prefix="/products", tags=["Products"])
app.include_router(order_routes.router, prefix="/orders", tags=["Orders"])

@app.get("/")
def root():
    return {"message": "E-Commerce API is running!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

---

# 🔥 STEP 2: COMMIT & PUSH TO GITHUB

Run these commands in terminal:

```powershell
cd c:\Users\KRRISH\Software Engineering\Assignment\SE
git add .
git commit -m "Prepare backend for production deployment"
git push
```

**Expected output:**
```
[main xxxxx] Prepare backend for production deployment
 X files changed, X insertions(+)
```

---

# 🌐 STEP 3: DEPLOY BACKEND TO RENDER (OUTSIDE VS CODE)

## 3.1 Create Render Account

1. Go to **https://render.com**
2. Click **"Sign Up"** → Select **"Sign up with GitHub"**
3. Authorize your GitHub account

## 3.2 Create Web Service

1. Click **"New"** → **"Web Service"**
2. Authorize Render to access your GitHub
3. Select repository: **`Krrish1506/SE`**
4. Click **"Connect"**

## 3.3 Fill Service Details

| Field | Value |
|-------|-------|
| **Name** | `se-ecommerce-backend` |
| **Environment** | `Python 3` |
| **Region** | `Singapore (Southeast Asia)` |
| **Branch** | `main` |
| **Root Directory** | `Backend` |

## 3.4 Build Command

```
pip install -r requirements.txt
```

**⚠️ IMPORTANT:** Do NOT include `Backend/` prefix (you're already in Backend directory)

## 3.5 Start Command

```
uvicorn app.main:app --host 0.0.0.0 --port 10000
```

**⚠️ IMPORTANT:** Do NOT use `cd Backend` (you're already in Backend directory)

## 3.6 Environment Variables

Scroll down to **"Advanced"** → Click **"Add Environment Variable"**

Add these 3 variables:

| Key | Value |
|-----|-------|
| `DATABASE_URL` | `postgresql://user:Lhw4bJEg8rCvMIm7d7gcY9uTesrDkqdr@dpg-d42gdhngi27c73c50650-a/ecommerce_w12z` |
| `SECRET_KEY` | `5d0254f31c923e14d56914bd09441ae31fad7892fbc562d53497773eb24b698f` |
| `FRONTEND_URL` | `http://localhost:5173` |

**Note:** You'll update `FRONTEND_URL` after deploying to Vercel

## 3.7 Instance Type

- **Plan:** Free (or Starter)
- **Instance Type:** Standard

## 3.8 Deploy

1. Scroll to bottom
2. Click **"Create Web Service"**
3. Wait 5-10 minutes for deployment
4. Watch logs in real-time

## 3.9 Verify Deployment

When deployment succeeds:
- You'll see a URL: `https://se-ecommerce-backend-xxxxx.onrender.com`
- Test in browser: Visit that URL → Should see:
```json
{"message": "E-Commerce API is running!"}
```

**⏹️ SAVE THIS URL FOR STEP 5!**

---

# 🛠️ TROUBLESHOOTING BACKEND DEPLOYMENT

### Error: "No such file or directory: 'Backend/requirements.txt'"
**Cause:** Build command includes `Backend/` prefix but root directory is already `Backend`
**Fix:** Build Command should be: `pip install -r requirements.txt`

### Error: "Rust compilation error" or "maturin failed"
**Cause:** Using `python-jose[cryptography]` which requires Rust compilation
**Fix:** Use `PyJWT==2.8.1` instead (has pre-built wheels)

### Error: "Read-only file system"
**Cause:** Render's file system conflict during build
**Fix:** Upgrade all dependencies to latest stable versions with pre-built wheels

### Backend not running
**Fix:**
1. Check logs in Render dashboard
2. Verify all environment variables are set correctly
3. Ensure database URL is valid
4. Manual deploy: Click "Redeploy latest commit"

---

# 🌐 STEP 4: DEPLOY FRONTEND TO VERCEL (OUTSIDE VS CODE)

## 4.1 Create Vercel Account

1. Go to **https://vercel.com**
2. Click **"Sign Up"** → Select **"Continue with GitHub"**
3. Authorize Vercel to access GitHub

## 4.2 Create Frontend Project

1. Click **"Add New..."** → **"Project"**
2. Select repository: **`Krrish1506/SE`**
3. Click **"Import"**

## 4.3 Configure Project

| Setting | Value |
|---------|-------|
| **Project Name** | `stark-avenue` (or any name) |
| **Framework Preset** | `Other` (not a Node.js framework) |
| **Root Directory** | `Frontend` |
| **Build Command** | Leave empty (static files) |
| **Output Directory** | Leave empty |

## 4.4 Add Environment Variable (Important!)

Click **"Environment Variables"** and add:

| Key | Value |
|-----|-------|
| `VITE_API_URL` | `https://se-ecommerce-backend-xxxxx.onrender.com` |

(Replace with your actual Render backend URL from Step 3)

## 4.5 Deploy

1. Click **"Deploy"**
2. Wait 2-3 minutes
3. You'll get a URL: `https://stark-avenue-xxxxx.vercel.app`

**⏹️ SAVE THIS URL!**

---

# 🔗 STEP 5: CONNECT FRONTEND TO BACKEND (IN VS CODE)

## 5.1 Update Frontend API URL

**File:** [Frontend/app.js](../Frontend/app.js)

Find this line:
```js
const API_BASE = 'http://localhost:5000/api';
```

**IF IT EXISTS**, replace with:
```js
const API_BASE = 'https://se-ecommerce-backend-xxxxx.onrender.com/api';
```

(Replace with your actual Render URL)

## 5.2 Search for all API calls

Search in [Frontend/app.js](../Frontend/app.js) for:
- `fetch(` 
- `http://localhost`
- `localhost:5000`

Replace all localhost API urls with your Render backend URL.

## 5.3 Alternative: Use Environment Variable

If your frontend uses Vite or environment variables:

```js
const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:5000/api';
```

But static HTML/JS won't automatically use Vercel env vars, so direct replacement is better.

## 5.4 Commit & Push

```powershell
cd c:\Users\KRRISH\Software Engineering\Assignment\SE
git add Frontend/app.js
git commit -m "Update API URL to production backend"
git push
```

---

# 🔐 STEP 6: UPDATE RENDER CORS (AFTER VERCEL DEPLOY)

Now that you have your Vercel frontend URL, update Render CORS:

1. Go to **https://render.com** → Your service: `se-ecommerce-backend`
2. Click **"Settings"** → **"Environment Variables"**
3. Update `FRONTEND_URL`:
   - **Old:** `http://localhost:5173`
   - **New:** `https://stark-avenue-xxxxx.vercel.app`

4. Click **"Save"** → Render auto-redeploys

---

# 🧪 STEP 7: TESTING CHECKLIST

### Frontend Test
- ✅ Visit Vercel URL in browser
- ✅ Page loads without errors
- ✅ No 404 errors in console
- ✅ All images/CSS load

### Backend Test
- ✅ Visit Render URL: `https://se-ecommerce-backend-xxxxx.onrender.com`
- ✅ Should see: `{"message": "E-Commerce API is running!"}`

### API Connection Test
- ✅ Open browser DevTools (F12)
- ✅ Go to "Network" tab
- ✅ Click any button that calls API (login, products, etc.)
- ✅ Should see API requests to Render backend
- ✅ No CORS errors in console
- ✅ Requests return data successfully

### Full Flow Test
1. Load frontend
2. Register/Login
3. Browse products
4. Add to cart
5. Checkout
6. Check database for new order

---

# ❌ COMMON ERRORS & FIXES

## CORS ERROR: "Blocked by CORS policy"
```
Access to XMLHttpRequest at 'https://...' from origin 'https://...' 
has been blocked by CORS policy
```

**Fixes:**
1. Check Render `FRONTEND_URL` environment variable matches your Vercel URL exactly
2. Wait 5 minutes after updating CORS for Render to redeploy
3. Clear browser cache: Ctrl+Shift+Delete
4. Hard refresh: Ctrl+Shift+R

## 404 Error: "Cannot GET /api/..."
**Cause:** API endpoint doesn't exist or wrong path
**Fix:**
- Check backend logs in Render
- Verify endpoint exists in [Backend/app/routes/](../Backend/app/routes/)
- Check API URL in frontend is correct

## "Cannot read property 'xxx' of undefined"
**Cause:** API not returning expected data
**Fixes:**
- Check backend is responding
- Verify database is populated
- Check frontend is parsing response correctly

## 504 Gateway Timeout or 503 Service Unavailable
**Cause:** Render app crashed or is starting up
**Fixes:**
1. Wait 1-2 minutes (Render might be restarting)
2. Go to Render dashboard, click "Manual Deploy"
3. Check logs for errors

## Blank Page on Vercel
**Cause:** JavaScript errors or missing files
**Fixes:**
1. Open DevTools (F12)
2. Check Console tab for errors
3. Check Network tab - all files loading?
4. Verify `Frontend/index.html` exists

---

# 📊 ARCHITECTURE DIAGRAM

```
┌─────────────────────────────────────────────────────────┐
│                    User's Browser                        │
└────────────────────┬────────────────────────────────────┘
                     │ (HTTPS)
                     ↓
┌─────────────────────────────────────────────────────────┐
│           Vercel (Frontend)                              │
│   - HTML/CSS/JS (Static Files)                           │
│   - URL: https://stark-avenue-xxxxx.vercel.app         │
│   - Makes API calls to backend                           │
└────────────────────┬────────────────────────────────────┘
                     │ API Requests (HTTPS)
                     ↓
┌─────────────────────────────────────────────────────────┐
│           Render (Backend)                               │
│   - FastAPI Application                                  │
│   - URL: https://se-ecommerce-backend-xxxxx.onrender.com│
│   - CORS enabled for Vercel URL                          │
│   - JWT authentication                                   │
└────────────────────┬────────────────────────────────────┘
                     │ SQL Queries
                     ↓
┌─────────────────────────────────────────────────────────┐
│        PostgreSQL Database                               │
│   - User accounts, products, orders                      │
└─────────────────────────────────────────────────────────┘
```

---

# ✅ FINAL DEPLOYMENT CHECKLIST

**UPDATE THIS SECTION AS YOU COMPLETE EACH TASK:**

```
BACKEND SETUP (IN VS CODE)
✅ [x] Backend code configured
✅ [x] requirements.txt with PyJWT
✅ [x] CORS configured in main.py
✅ [x] Config.py environment variables set
✅ [x] JWT authentication setup
✅ [x] Code committed to GitHub

RENDER DEPLOYMENT (OUTSIDE VS CODE)
⏳ [ ] Render account created
⏳ [ ] New Web Service created
⏳ [ ] Service name: se-ecommerce-backend
⏳ [ ] Root Directory set to: Backend
⏳ [ ] Region: Singapore
⏳ [ ] Build Command: pip install -r requirements.txt
⏳ [ ] Start Command: uvicorn app.main:app --host 0.0.0.0 --port 10000
⏳ [ ] Environment Variables added (3):
      - DATABASE_URL
      - SECRET_KEY
      - FRONTEND_URL
⏳ [ ] Deployment successful
⏳ [ ] Backend URL working: https://se-ecommerce-backend-xxxxx.onrender.com
⏳ [ ] Backend URL saved for later use

VERCEL DEPLOYMENT (OUTSIDE VS CODE)
⏳ [ ] Vercel account created
⏳ [ ] New Project created
⏳ [ ] Root Directory set to: Frontend
⏳ [ ] Project deployed successfully
⏳ [ ] Frontend URL working: https://stark-avenue-xxxxx.vercel.app
⏳ [ ] Frontend URL saved for later use

FRONTEND CONFIGURATION (IN VS CODE)
⏳ [ ] app.js API URL updated with Render backend URL
⏳ [ ] All localhost API calls replaced
⏳ [ ] Code committed to GitHub
⏳ [ ] Vercel auto-redeployed

RENDER CORS UPDATE (OUTSIDE VS CODE)
⏳ [ ] Render "se-ecommerce-backend" service opened
⏳ [ ] Environment Variables → FRONTEND_URL updated
⏳ [ ] Changed from: http://localhost:5173
⏳ [ ] Changed to: https://stark-avenue-xxxxx.vercel.app
⏳ [ ] Saved changes (auto-redeploy starts)

TESTING (IN BROWSER)
⏳ [ ] Frontend loads without errors
⏳ [ ] DevTools Console → No JavaScript errors
⏳ [ ] Backend URL test successful
⏳ [ ] API calls working (check Network tab)
⏳ [ ] No CORS errors in console
⏳ [ ] Login functionality works
⏳ [ ] Products load correctly
⏳ [ ] Add to cart works
⏳ [ ] Checkout process works
⏳ [ ] Order saved to database
⏳ [ ] Full end-to-end flow successful
```

**SAVE THESE URLS:**

```
Render Backend:    https://se-ecommerce-backend-xxxxx.onrender.com
Vercel Frontend:   https://stark-avenue-xxxxx.vercel.app
Backend API Base:  https://se-ecommerce-backend-xxxxx.onrender.com/api
Backend Swagger:   https://se-ecommerce-backend-xxxxx.onrender.com/docs
```

---

# 📊 DEPLOYMENT PROGRESS TABLE

| Step | Task | Status | Time | Location |
|------|------|--------|------|----------|
| 1 | Prepare backend code | ✅ Done | Already done | VS Code |
| 2 | Configure CORS & JWT | ✅ Done | Already done | VS Code |
| 3 | Push to GitHub | ✅ Done | Already done | Terminal |
| 4 | Deploy backend | ⏳ TODO | ~10 min | Render.com |
| 5 | Deploy frontend | ⏳ TODO | ~3 min | Vercel.com |
| 6 | Update frontend URLs | ⏳ TODO | ~5 min | VS Code |
| 7 | Update Render CORS | ⏳ TODO | ~2 min | Render.com |
| 8 | Test everything | ⏳ TODO | ~10 min | Browser |

---

# 💾 CURRENT STATUS SUMMARY

- Backend code prepared (CORS, JWT, config)
- requirements.txt updated (PyJWT, no Rust deps)
- Code pushed to GitHub
- ⏳ **NEXT:** Deploy backend on Render
- ⏳ **THEN:** Deploy frontend on Vercel
- ⏳ **THEN:** Connect frontend to backend
- ⏳ **FINALLY:** Test system end-to-end

---

# 📞 QUICK REFERENCE

| Component | URL | Notes |
|-----------|-----|-------|
| **Frontend** | `https://stark-avenue-xxxxx.vercel.app` | Static site |
| **Backend** | `https://se-ecommerce-backend-xxxxx.onrender.com` | FastAPI app |
| **Backend API** | `https://se-ecommerce-backend-xxxxx.onrender.com/api` | Root for API calls |
| **Backend Docs** | `https://se-ecommerce-backend-xxxxx.onrender.com/docs` | FastAPI Swagger UI |
| **Database** | PostgreSQL (configured in Render env) | Managed externally |

---

# 🎯 NEXT STEPS IF ISSUES OCCUR

1. **Check Render Logs:** Dashboard → Service → Logs
2. **Check Vercel Logs:** Dashboard → Deployments → Recent
3. **Check Browser DevTools:** F12 → Network tab
4. **Verify Environment Variables:** Are they set correctly?
5. **Test Backend URL in Browser:** Visit it directly
6. **Manual Redeploy:** Click "Redeploy" in Render/Vercel dashboard

---

# 🚀 YOU'RE DONE!
Your SE assignment is now fully deployed and publicly accessible!
