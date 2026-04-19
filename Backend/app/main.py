import sys
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # ── Startup ──────────────────────────────────────────────
    # Validate required environment variables
    missing = []
    if not settings.DATABASE_URL:
        missing.append("DATABASE_URL")
    if not settings.SECRET_KEY:
        missing.append("SECRET_KEY")
    if missing:
        logger.critical(f"STARTUP FAILED — missing required environment variables: {', '.join(missing)}")
        logger.critical("Set these in Render → Environment Variables and redeploy.")
        sys.exit(1)

    # Import models to register them with SQLAlchemy
    from app.models import user, product, order  # noqa: F401
    from app.database import Base, engine

    try:
        logger.info("Connecting to database and creating tables...")
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables ready ✓")
    except Exception as e:
        logger.critical(f"STARTUP FAILED — could not connect to database: {e}")
        logger.critical("Check your DATABASE_URL environment variable on Render.")
        sys.exit(1)

    yield
    # ── Shutdown ─────────────────────────────────────────────
    logger.info("Shutting down...")


app = FastAPI(
    title="E-Commerce API",
    description="A complete e-commerce backend with authentication",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS middleware
allowed_origins = settings.FRONTEND_URL.split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
from app.routes import auth, product as product_routes, order as order_routes  # noqa: E402
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(product_routes.router, prefix="/products", tags=["Products"])
app.include_router(order_routes.router, prefix="/orders", tags=["Orders"])


@app.get("/")
def root():
    return {"message": "E-Commerce API is running!"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
