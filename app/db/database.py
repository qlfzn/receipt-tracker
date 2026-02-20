import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Engine

load_dotenv()

class Database:
    def __init__(self):
        self.db = self.create_db()
    
    def create_db(self) -> Engine:
        print("Creating DB connection...")
        try:
            DB_HOST = os.getenv("POSTGRES_HOST")
            DB_NAME = os.getenv("POSTGRES_DB")
            DB_USER = os.getenv("POSTGRES_USER")
            DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
            DB_PORT = os.getenv("POSTGRES_PORT")

            engine = create_engine(url=f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
            return engine
        except Exception as e:
            print(f"Failed to create DB engine: {e}")
            raise