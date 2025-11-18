#!/usr/bin/env python3

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import uvicorn
from dotenv import load_dotenv
import os

load_dotenv()

from app.api.v1 import router as api_router
from app.core.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 VentureGuard AI starting up...")
    yield
    print("👋 VentureGuard AI shutting down...")

app = FastAPI(
    title="VentureGuard AI API",
    description="AI-Powered Business Intelligence Guardian - Predict, Protect, Prosper",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "VentureGuard AI API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "environment": settings.APP_ENV
    }

app.include_router(api_router, prefix=f"/api/{settings.API_VERSION}")

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": exc.status_code,
                "message": exc.detail
            }
        }
    )

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
