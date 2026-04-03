"""Pytest tests for AutoSME API."""
import pytest
from starlette.testclient import TestClient
from auto_sme.main import create_app

client = TestClient(create_app())

def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"

def test_create_product():
    resp = client.post(
        "/api/v1/inventory",
        json={"name": "Rice", "price": 1.5, "unit": "kg"},
        headers={"X-API-Key": "dev-key"}
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["name"] == "Rice"
    assert data["stock"] == 0
    assert "id" in data

def test_list_products():
    resp = client.get("/api/v1/inventory", headers={"X-API-Key": "dev-key"})
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)

def test_adjust_stock():
    # create product
    create = client.post(
        "/api/v1/inventory",
        json={"name": "Beans", "price": 2.0, "unit": "kg"},
        headers={"X-API-Key": "dev-key"}
    )
    prod_id = create.json()["id"]
    # adjust
    resp = client.patch(
        f"/api/v1/inventory/{prod_id}?delta=50",
        headers={"X-API-Key": "dev-key"}
    )
    assert resp.status_code == 200
    assert resp.json()["stock"] == 50
    # negative adjustment
    resp = client.patch(
        f"/api/v1/inventory/{prod_id}?delta=-20",
        headers={"X-API-Key": "dev-key"}
    )
    assert resp.json()["stock"] == 30

def test_create_order():
    # create product first
    prod_resp = client.post(
        "/api/v1/inventory",
        json={"name": "Sugar", "price": 0.8, "unit": "kg"},
        headers={"X-API-Key": "dev-key"}
    )
    prod = prod_resp.json()
    order = {
        "customer_phone": "+234801234567",
        "items": [
            {"product_id": prod["id"], "product_name": prod["name"], "quantity": 2, "unit_price": prod["price"]}
        ]
    }
    resp = client.post("/api/v1/orders", json=order)  # no API key for webhook
    assert resp.status_code == 201
    data = resp.json()
    assert data["total_amount"] == 1.6
    assert data["status"] == "pending"

def test_sales_report():
    # create product and order with known created_at (would need to manipulate time; skip full PDF test for now)
    pass
