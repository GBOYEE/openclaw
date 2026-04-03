"""Orders router — receive WhatsApp orders, track status."""
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional
import uuid
from datetime import datetime

router = APIRouter(prefix="/orders")  # no API key required for webhooks

_orders_db: List[dict] = []

class OrderItem(BaseModel):
    product_id: str
    product_name: str
    quantity: int
    unit_price: float

class OrderCreate(BaseModel):
    customer_phone: str
    customer_name: Optional[str] = None
    items: List[OrderItem]

class Order(OrderCreate):
    id: str
    total_amount: float
    status: str = "pending"
    created_at: datetime

@router.post("", response_model=Order, status_code=status.HTTP_201_CREATED)
async def create_order(order: OrderCreate):
    total = sum(item.quantity * item.unit_price for item in order.items)
    new_order = {
        "id": str(uuid.uuid4()),
        "customer_phone": order.customer_phone,
        "customer_name": order.customer_name,
        "items": [item.dict() for item in order.items],
        "total_amount": total,
        "status": "pending",
        "created_at": datetime.utcnow(),
    }
    _orders_db.append(new_order)
    # TODO: send auto-reply via Twilio
    return new_order

@router.get("", response_model=List[Order])
async def list_orders():
    return _orders_db

@router.patch("/{order_id}/status")
async def update_order_status(order_id: str, status: str = "confirmed"):
    for order in _orders_db:
        if order["id"] == order_id:
            order["status"] = status
            return order
    raise HTTPException(status_code=404, detail="Order not found")
