from sqlalchemy import Column, Integer, String, Numeric, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    
    receipts = relationship("Receipt", back_populates="user", cascade="all, delete-orphan")

class Receipt(Base):
    __tablename__ = "receipts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    merchant = Column(String(255))
    total = Column(Numeric(10, 2))
    receipt_date = Column(Date)
    created_at = Column(DateTime, server_default=func.now())
    
    user = relationship("User", back_populates="receipts")
    items = relationship("Item", back_populates="receipt", cascade="all, delete-orphan")

class Item(Base):
    __tablename__ = "items"
    
    id = Column(Integer, primary_key=True, index=True)
    receipt_id = Column(Integer, ForeignKey("receipts.id"), nullable=False)
    item_name = Column(String(255))
    quantity = Column(Numeric(10, 2))
    unit_price = Column(Numeric(10, 2))
    total_price = Column(Numeric(10, 2))
    
    receipt = relationship("Receipt", back_populates="items")