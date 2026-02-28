import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from app.api.routes import router

load_dotenv()

ALLOW_ORIGINS = os.getenv("VITE_APP")

app = FastAPI(
    title="Bank Statement Processing API",
    description="API for scanning and processing bank statement",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[ALLOW_ORIGINS],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/v1")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
