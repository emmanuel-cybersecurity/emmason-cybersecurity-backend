from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import Base, engine
from app.api.routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown lifecycle."""
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Emmason Cyber Security API",
    description=(
        "Backend API for Emmason Cyber Security. "
        "Provides secure services and API endpoints."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)


# --------------------------------------------------
# CORS
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# API ROUTES
# --------------------------------------------------

app.include_router(
    router,
    prefix="/api",
)


# --------------------------------------------------
# HEALTH CHECK
# --------------------------------------------------

@app.get(
    "/health",
    tags=["System"],
    summary="Health check",
)
def health():
    return {
        "status": "ok",
        "service": "Emmason Cyber Security API",
        "version": "1.0.0",
    }


# --------------------------------------------------
# ROOT ENDPOINT
# --------------------------------------------------

@app.get(
    "/",
    tags=["System"],
    summary="API information",
)
def root():
    return {
        "name": "Emmason Cyber Security API",
        "status": "online",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
    }
