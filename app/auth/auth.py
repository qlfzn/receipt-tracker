from app.db import get_db
from sqlalchemy.orm import session

async def authenticate_user(db, email: str, password: str):
    """
    Authenticate by checking email and password
    """
