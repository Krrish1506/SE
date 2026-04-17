# 🚀 FULL AUTOMATED DEPLOYMENT GUIDE (Vercel + Render)

## 🎯 OBJECTIVE
Deploy:
- Frontend → Vercel
- Backend → Render
- Connect both using API + CORS

---

# 📁 STEP 0: ASSUMPTIONS

Project structure:

```
root/
├── frontend/
└── backend/
```

---

# ⚙️ STEP 1: DEPLOY BACKEND (Render)

## ACTIONS

1. Open https://render.com
2. Login with GitHub
3. Click "New" → "Web Service"
4. Select your repository

---

## CONFIGURATION

### Node.js Backend

```
Build Command: npm install
Start Command: node server.js
```

### Python Backend

```
Build Command: pip install -r requirements.txt
Start Command: uvicorn main:app --host 0.0.0.0 --port 10000
```

---

## OUTPUT

After deployment, store:

```
BACKEND_URL=https://your-backend.onrender.com
```

---

# 🔥 STEP 2: ENABLE CORS (CRITICAL)

## WHY

Frontend and backend are on different domains.  
Browsers block requests unless CORS is enabled.

---

## NODE.JS SETUP

Install:

```
npm install cors
```

Add in backend:

```js
import cors from "cors";

app.use(cors({
  origin: "https://your-frontend.vercel.app",
  credentials: true
}));
```

---

## ALTERNATIVE (OPEN ACCESS)

```js
app.use(cors());
```

---

## IMPORTANT

- Origin must exactly match frontend URL
- CORS is controlled by backend
- Required header:

```
Access-Control-Allow-Origin
```

---

# 🌐 STEP 3: DEPLOY FRONTEND (Vercel)

## ACTIONS

1. Open https://vercel.com
2. Login with GitHub
3. Click "Add New Project"
4. Import your repository

---

## CONFIGURATION

### React / Vite

```
Build Command: npm run build
Output Directory: dist
```

### Create React App

```
Build Command: npm run build
Output Directory: build
```

---

## OUTPUT

```
FRONTEND_URL=https://your-project.vercel.app
```

---

# 🔗 STEP 4: CONNECT FRONTEND TO BACKEND

## UPDATE API URL

### BEFORE

```js
http://localhost:5000/api
```

### AFTER

```js
https://your-backend.onrender.com/api
```

---

## ENVIRONMENT VARIABLE (RECOMMENDED)

### In Vercel

Add:

```
VITE_API_URL=https://your-backend.onrender.com
```

---

### USE IN CODE

```js
const API = import.meta.env.VITE_API_URL;

fetch(`${API}/api/data`);
```

---

# 🔐 STEP 5: AUTH CONFIG (OPTIONAL)

```js
res.cookie("token", token, {
  httpOnly: true,
  secure: true,
  sameSite: "none"
});
```

---

# 🧪 STEP 6: TESTING CHECKLIST

- Frontend loads
- API calls work
- No CORS errors
- Backend running

---

# ❌ COMMON ERRORS

## CORS ERROR

```
Blocked by CORS policy
```

### FIX

- Check backend CORS config
- Ensure correct origin
- Restart backend

---

## API NOT WORKING

### FIX

- Check endpoint path
- Verify BACKEND_URL

---

## COOKIE ISSUE

Ensure:

```
credentials: true
sameSite: none
secure: true
```

---

# 🧠 ARCHITECTURE

```
User
 ↓
Frontend (Vercel)
 ↓ API CALL
Backend (Render)
 ↓
Database
```

---

# 🤖 AI EXECUTION SUMMARY

1. Deploy backend on Render
2. Save BACKEND_URL
3. Enable CORS
4. Deploy frontend on Vercel
5. Save FRONTEND_URL
6. Replace API URLs
7. Add environment variables
8. Test system

---

# ✅ DEPLOYMENT COMPLETE