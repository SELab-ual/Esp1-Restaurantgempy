from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy import create_engine, Column, Integer, String, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import os
import time

# --- Database Setup ---
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/rmos_db")

# Retry logic for DB connection
engine = None
for i in range(10):
    try:
        engine = create_engine(DATABASE_URL)
        connection = engine.connect()
        print("Database connected!")
        connection.close()
        break
    except Exception:
        print("Waiting for Database...")
        time.sleep(2)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- Models ---
class OrderModel(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    table_id = Column(Integer)
    status = Column(String, default="Sent to Kitchen")
    items = Column(JSON) # Storing list of items as JSON for simplicity in Sprint 1

# Create Tables
Base.metadata.create_all(bind=engine)

# --- Pydantic Schemas ---
class OrderCreate(BaseModel):
    table_id: int
    items: List[str]

class OrderRead(OrderCreate):
    id: int
    status: str

    class Config:
        orm_mode = True

# --- API ---
app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 1. MENU ENDPOINT (Sprint 1 Requirement C05)
@app.get("/menu")
def get_menu():
    return [
        {"id": 1, "name": "Steak Frites", "price": 25.00, "category": "Main"},
        {"id": 2, "name": "Caesar Salad", "price": 12.00, "category": "Starter"},
        {"id": 3, "name": "Chocolate Cake", "price": 8.50, "category": "Dessert"},
        {"id": 4, "name": "Soda", "price": 3.00, "category": "Drink"},
    ]

# 2. PLACE ORDER (Sprint 1 Requirement C10)
@app.post("/orders/", response_model=OrderRead)
def place_order(order: OrderCreate, db: Session = Depends(get_db)):
    db_order = OrderModel(table_id=order.table_id, items=order.items)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

# 3. GET ORDERS (Sprint 1 Requirement W06 - For Waiter/Kitchen)
@app.get("/orders/", response_model=List[OrderRead])
def read_orders(db: Session = Depends(get_db)):
    return db.query(OrderModel).all()