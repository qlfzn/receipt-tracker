import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

class Database:
    def __init__(self):
        self.engine = self.create_engine()
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
    
    def create_engine(self) -> Engine:
        print("Creating DB connection...")
        try:
            DB_HOST = os.getenv("POSTGRES_HOST")
            DB_NAME = os.getenv("POSTGRES_DB")
            DB_USER = os.getenv("POSTGRES_USER")
            DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
            DB_PORT = os.getenv("POSTGRES_PORT")

            engine = create_engine(
                url=f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
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