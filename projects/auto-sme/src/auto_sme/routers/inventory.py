"""Inventory router — product CRUD and stock adjustment."""
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional
import uuid
from datetime import datetime
from auto_sme.dependencies import verify_api_key

router = APIRouter(prefix="/inventory", dependencies=[Depends(verify_api_key)])

# In-memory store
_products_db: List[dict] = []

class ProductCreate(BaseModel):
    name: str
    price: float
    unit: str
    stock: int = 0
    low_stock_threshold: int = 10

class Product(ProductCreate):
    id: str

@router.post("", response_model=Product, status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductCreate, api_key: str = Depends(lambda: None)):
    new_prod = {
        "id": str(uuid.uuid4()),
        "name": product.name,
        "price": product.price,
        "unit": product.unit,
        "stock": product.stock,
        "low_stock_threshold": product.low_stock_threshold,
    }
    _products_db.append(new_prod)
    return new_prod

@router.patch("/{product_id}")
async def adjust_stock(product_id: str, delta: int = 0, api_key: str = Depends(lambda: None)):
    for prod in _products_db:
        if prod["id"] == product_id:
            prod["stock"] += delta
            if prod["stock"] < 0:
                prod["stock"] = 0
            return prod
    raise HTTPException(status_code=404, detail="Product not found")

@router.get("", response_model=List[Product])
async def list_products(api_key: str = Depends(lambda: None)):
    return _products_db
