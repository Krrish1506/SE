# 🛍️ Stark Avenue — Full-Stack E-Commerce Platform

> A premium luxury streetwear e-commerce platform built as a Software Engineering assignment. Features a pixel-perfect vanilla HTML/CSS/JS storefront connected to a production-grade FastAPI backend with JWT authentication and PostgreSQL persistence.

### 🌐 Live Demo
- **Frontend (Vercel):** [https://stark-avenue.vercel.app/](https://stark-avenue.vercel.app/)
- **Backend API (Render):** [https://se-ecommerce-backend.onrender.com/docs](https://se-ecommerce-backend.onrender.com/docs)

---

## 📋 Table of Contents

- [Project Overview](#-project-overview)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [API Reference](#-api-reference)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Backend Setup](#backend-setup-local)
  - [Frontend Setup](#frontend-setup-local)
  - [Docker Setup](#docker-setup)
- [Environment Variables](#-environment-variables)
- [Features](#-features)
- [Contributing](#-contributing)

---

## 📌 Project Overview

**Stark Avenue** is a full-stack web application for a luxury streetwear brand. It combines:

- A **rich, animated frontend** — built entirely with vanilla HTML, CSS, and JavaScript — featuring a multi-page shopping experience (home, products, cart, checkout, blog, affiliate program, SWOT, and video marketing).
- A **robust REST API backend** — built with Python's FastAPI framework — handling user authentication, product management (admin-only), inventory tracking, and order processing, all persisted to a PostgreSQL database.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    User's Browser                        │
└────────────────────┬────────────────────────────────────┘
                     │ HTTPS
                     ▼
┌─────────────────────────────────────────────────────────┐
│           Vercel  (Frontend — Static)                    │
│   HTML + CSS + Vanilla JS                                │
│   Pages: index, products, checkout, blog, about, etc.   │
└────────────────────┬────────────────────────────────────┘
                     │ REST API Calls (HTTPS + JWT)
                     ▼
┌─────────────────────────────────────────────────────────┐
│           Render  (Backend — FastAPI)                    │
│   /auth  →  Registration & Login                        │
│   /products  →  Product Catalog (Admin CRUD)            │
│   /orders  →  Order Placement & History                 │
└────────────────────┬────────────────────────────────────┘
                     │ SQL (SQLAlchemy ORM)
                     ▼
┌─────────────────────────────────────────────────────────┐
│        PostgreSQL Database                               │
│   Tables: users, products, orders                        │
└─────────────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | HTML5, CSS3 (Custom Properties, Flexbox, Grid), Vanilla JavaScript |
| **Backend** | Python 3.11, FastAPI 0.104, Uvicorn |
| **ORM** | SQLAlchemy 2.0 |
| **Database** | PostgreSQL 13 |
| **Authentication** | JWT via PyJWT 2.9, bcrypt password hashing |
| **Validation** | Pydantic v2 |
| **Migrations** | Alembic 1.12 |
| **Containerization** | Docker, Docker Compose |
| **Frontend Hosting** | Vercel |
| **Backend Hosting** | Render |

---

## 📂 Project Structure

```
SE/
├── .gitignore
├── README.md                   ← You are here
│
├── Backend/                    ← FastAPI Python backend
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── requirements.txt
│   ├── requirements-dev.txt
│   ├── .env.example
│   ├── seed.py                 ← Database seeding script
│   ├── seed.sql
│   ├── dump_sql.py
│   └── app/
│       ├── main.py             ← FastAPI app entry point & CORS config
│       ├── config.py           ← Settings & environment variable loading
│       ├── database.py         ← SQLAlchemy engine & session factory
│       ├── auth/
│       │   └── jwt.py          ← Token creation, verification, password hashing
│       ├── models/
│       │   ├── user.py         ← User ORM model
│       │   ├── product.py      ← Product ORM model
│       │   └── order.py        ← Order ORM model
│       ├── schemas/
│       │   ├── user.py         ← Pydantic schemas (UserCreate, UserResponse, Token)
│       │   ├── product.py      ← Pydantic schemas (ProductCreate, ProductResponse)
│       │   └── order.py        ← Pydantic schemas (OrderCreate, OrderResponse)
│       └── routes/
│           ├── auth.py         ← POST /auth/register, POST /auth/login
│           ├── product.py      ← GET/POST/PUT/DELETE /products/
│           └── order.py        ← POST/GET /orders/
│
├── Frontend/                   ← Static HTML/CSS/JS storefront
│   ├── index.html              ← Homepage (hero, categories, featured products)
│   ├── products.html           ← Full product catalog
│   ├── product-detail.html     ← Individual product detail page
│   ├── checkout.html           ← Checkout page (cart review, shipping, payment)
│   ├── login.html              ← Login / Registration page
│   ├── about.html              ← Brand story
│   ├── contact.html            ← Support & contact form
│   ├── blog.html               ← Blog listing
│   ├── blog-*.html             ← Individual blog article pages (5 articles)
│   ├── swot.html               ← Business SWOT analysis
│   ├── affiliate-program.html  ← Affiliate program details
│   ├── video-marketing.html    ← Video marketing showcase
│   ├── 404.html                ← Custom 404 error page
│   ├── styles.css              ← Global stylesheet (~100KB, all design tokens)
│   ├── app.js                  ← Main JS: cart state, API calls, UI interactions
│   ├── product-data.js         ← Centralized product catalog data
│   ├── manifest.json           ← PWA Web App Manifest
│   └── video/                  ← Product/brand video assets (V1–V12.mp4)
│
└── tasks/
    ├── todo.md                 ← Current development task (Checkout flow)
    ├── deployment.md           ← Step-by-step Vercel + Render deployment guide
    └── lessons.md              ← Lessons learned
```

---

## 📡 API Reference

All endpoints are available at `http://localhost:8000`. Interactive docs (Swagger UI) are auto-generated at `/docs`.

### Authentication — `/auth`

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `POST` | `/auth/register` | None | Register a new user account |
| `POST` | `/auth/login` | None | Login and receive a JWT access token |

**Register Body:**
```json
{
  "email": "user@example.com",
  "full_name": "Jane Doe",
  "password": "supersecret"
}
```

**Login Body:**
```json
{
  "email": "user@example.com",
  "password": "supersecret"
}
```

**Login Response:**
```json
{
  "access_token": "<jwt_token>",
  "token_type": "bearer"
}
```

---

### Products — `/products`

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `GET` | `/products/` | None | List all products (supports `?skip=` & `?limit=`) |
| `GET` | `/products/{id}` | None | Get a single product by ID |
| `POST` | `/products/` | 🔒 Admin JWT | Create a new product |
| `PUT` | `/products/{id}` | 🔒 Admin JWT | Update an existing product |
| `DELETE` | `/products/{id}` | 🔒 Admin JWT | Delete a product |

---

### Orders — `/orders`

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `POST` | `/orders/` | 🔑 JWT | Place a new order (validates stock server-side) |
| `GET` | `/orders/` | 🔑 JWT | Get all orders for the authenticated user |
| `GET` | `/orders/{id}` | 🔑 JWT | Get a specific order by ID |

**Create Order Body:**
```json
{
  "shipping_address": "123 Main St, City, Country",
  "items": [
    { "product_id": 1, "quantity": 2, "price": 0 },
    { "product_id": 3, "quantity": 1, "price": 0 }
  ]
}
```
> ℹ️ The `price` field is ignored — the server always uses the price from the database to prevent client-side price manipulation.

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.11+**
- **PostgreSQL 13+** (or Docker for a containerised setup)
- A modern web browser (Chrome, Firefox, Edge)

---

### Backend Setup (Local)

```powershell
# 1. Navigate to Backend directory
cd "c:\Users\KRRISH\Software Engineering\Assignment\SE\Backend"

# 2. Create and activate a virtual environment
python -m venv venv311
.\venv311\Scripts\Activate.ps1

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment variables
copy .env.example .env
# Edit .env and fill in DATABASE_URL and SECRET_KEY

# 5. (Optional) Seed the database with sample data
python seed.py

# 6. Start the development server
uvicorn app.main:app --reload --port 8000
```

The API will be available at **http://localhost:8000**  
Interactive Swagger docs: **http://localhost:8000/docs**

---

### Frontend Setup (Local)

No build step is required. Open `Frontend/index.html` directly in your browser, or use VS Code's **Live Server** extension for the best experience (avoids CORS issues with local resources).

```
# With Live Server (VS Code):
Right-click Frontend/index.html → "Open with Live Server"
# Access at: http://127.0.0.1:5500
```

> **Important:** The frontend's API URL is centrally configured in `Frontend/product-data.js` via the `API_BASE` constant. Change it to `http://localhost:8000` for local development.

---

### Docker Setup

A `docker-compose.yml` is provided to spin up both the FastAPI app and a PostgreSQL database together:

```powershell
cd "c:\Users\KRRISH\Software Engineering\Assignment\SE\Backend"

docker-compose up --build
```

| Service | Port | Description |
|---------|------|-------------|
| `web` | `8000` | FastAPI application |
| `db` | `5432` | PostgreSQL 13 database |

---

## ☁️ Production Deployment

### Backend (Render)
1. **Database:** Create a Free PostgreSQL database on Render.
2. **Web Service:** Create a new Web Service using Python 3 tied to the `Backend` directory. Set build command to `pip install -r requirements.txt` and start command to `uvicorn app.main:app --host 0.0.0.0 --port 10000`.
3. **Environment Variables:** Set `DATABASE_URL` (Internal DB URL), `SECRET_KEY`, and `FRONTEND_URL` (your deployed Vercel URL).

*(Note: The `Backend/.python-version` file pins Python to 3.11.9 to ensure compatibility with `pydantic-core` pre-built wheels and avoids failing Cargo compilation).*

### Frontend (Vercel)
1. Import the project into Vercel.
2. Set the Root Directory to `Frontend`. No build command or output directory configuration is needed.
3. Update `API_BASE` in `product-data.js` to point to the live Render backend URL before deploying.

---

## 🔑 Environment Variables

Copy `Backend/.env.example` to `Backend/.env` and populate all required values:

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@localhost:5432/ecommerce` |
| `SECRET_KEY` | Secret key for JWT signing (keep private!) | `a-strong-random-hex-string` |
| `FRONTEND_URL` | Comma-separated list of allowed CORS origins | `http://localhost:5500,https://your-app.vercel.app` |

> ⚠️ **Never commit your `.env` file.** It is listed in `.gitignore`.

---

## ✨ Features

### Frontend
- 🎨 **Premium Dark-Mode UI** — HSL-based color palette, glassmorphism effects, and micro-animations throughout
- 🛒 **Interactive Cart & Wishlist** — Flyout panels with real-time state management via vanilla JS
- 💳 **Multi-step Checkout** — Cart review, shipping form, and multiple payment methods (COD, Credit Card, UPI)
- 📱 **Fully Responsive** — Optimized for mobile, tablet, and desktop breakpoints
- 🍞 **Toast Notifications** — User feedback for cart/wishlist interactions
- 🎬 **Video Marketing Page** — Showcases 12 brand videos (V1–V12)
- 📝 **Rich Blog** — 5 individual fashion/style articles
- 🔗 **Affiliate Program Page** — Detailed commission and referral structure
- 📊 **SWOT Analysis Page** — Business strategy visualization

### Backend
- 🔐 **JWT Authentication** — Secure token-based auth with bcrypt password hashing (30 min expiry)
- 👑 **Role-Based Access** — `is_admin` flag gates all product write operations
- 📦 **Inventory Management** — Stock quantity automatically decremented on order creation
- 🛡️ **Server-Side Price Validation** — Order prices are always resolved from the database (prevents client spoofing)
- 🐳 **Docker Ready** — Single `docker-compose up --build` starts the full stack
- 📄 **Auto-Generated API Docs** — Swagger UI at `/docs`, ReDoc at `/redoc`
- 🚀 **Render/Railway Ready** — Configured for zero-downtime cloud deployment

---

## 📜 License

This project was developed as a **Software Engineering university assignment**.  
© 2026 Stark Avenue. All rights reserved.
