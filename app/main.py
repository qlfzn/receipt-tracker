from fastapi import FastAPI
from contextlib import asynccontextmanager
import uvicorn
from app.api.routes import router
from app.db import Database

@asynccontextmanager
async def lifespan(app: FastAPI):
    db = Database().db
    conn = db.connect()
    print("Connected to database!")
    app.state.db = conn
    yield
    conn.close()

app = FastAPI(
    title="Receipt Tracker API",
    description="API for parsing and tracking receipts",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(router, prefix="/api/v1")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)