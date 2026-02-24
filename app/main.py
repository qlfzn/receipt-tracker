from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn
from app.api.routes import router
from app.db import models


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Database ready")
    yield
    print("Application shutdown")


app = FastAPI(
    title="Bank Statement Processing API",
    description="API for scanning and processing bank statement",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/v1")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
