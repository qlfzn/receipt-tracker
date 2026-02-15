from fastapi import FastAPI
import uvicorn
from app.api.routes import router

app = FastAPI(
    title="Receipt Tracker API",
    description="API for parsing and tracking receipts",
    version="1.0.0"
)

app.include_router(router, prefix="/api/v1")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)