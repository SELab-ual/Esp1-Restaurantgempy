from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI(title="RMOS API - Sprint 1 Prototype")

# Mock DB Data for Sprint 1
MENU_ITEMS = [
    {"id": 1, "name": "Classic Burger", "price": 12.99, "category": "Mains"},
    {"id": 2, "name": "Caesar Salad", "price": 8.50, "category": "Starters"},
    {"id": 3, "name": "Craft Cola", "price": 3.00, "category": "Drinks"}
]

class LoginData(BaseModel):
    username: str
    password: str

@app.get("/")
def read_root():
    return {"status": "RMOS Backend is Running"}

@app.get("/menu")
def get_menu():
    """Satisfies C01, C05: Customer gets menu items"""
    return MENU_ITEMS

@app.post("/login")
def login(data: LoginData):
    """Satisfies W01, Y10: Waiter authentication"""
    if data.username == "waiter" and data.password == "password123":
        return {"token": "sprint1-auth-token-xyz", "role": "waiter", "name": "John Doe"}
    raise HTTPException(status_code=401, detail="Invalid credentials")