from app.config import settings
from sqlalchemy import create_engine, Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

class Database:
    def __init__(self):
        self.engine = self.create_engine()
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
    
    def create_engine(self) -> Engine:
        print("Creating DB connection...")
        try:
            engine = create_engine(
                url=settings.DATABASE_URL
            )
            return engine
        except Exception as e:
            print(f"Failed to create DB engine: {e}")
            raise

database = Database()
Base = declarative_base()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()