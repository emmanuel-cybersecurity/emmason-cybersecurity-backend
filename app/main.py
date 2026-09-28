from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import Base, engine
from app.api.routes import router

@asynccontextmanager
async def lifespan(app: FastAPI):
Base.metadata.create_all(bind=engine)
yield

app = FastAPI(
title="Emmason Cyber Security API",
description="Backend API for Emmason Cyber Security.",
version="1.0.0",
docs_url="/docs",
redoc_url="/redoc",
lifespan=lifespan,
)

app.add_middleware(
CORSMiddleware,
allow_origins=settings.cors_origins,
allow_credentials=True,
allow_methods=["GET", "POST"],
allow_headers=["Authorization", "Content-Type"],
)

app.include_router(router, prefix="/api")

@app.get("/health", tags=["System"])
def health():
return {
"status": "ok",
"service": "Emmason Cyber Security API"
}
