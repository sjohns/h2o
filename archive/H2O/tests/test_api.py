from fastapi.testclient import TestClient

from api_backend.app import app


client = TestClient(app)


def test_skus_endpoint_returns_data():
    response = client.get("/skus")
    assert response.status_code == 200
    payload = response.json()
    assert "skus" in payload
    assert len(payload["skus"]) > 0


def test_order_pack_get_flow():
    skus = client.get("/skus").json()["skus"]
    selected = [skus[0]["skuId"], skus[1]["skuId"]]

    created = client.post("/orders", json={"skuIds": selected})
    assert created.status_code == 200
    order = created.json()
    assert order["status"] == "created"

    packed = client.post("/pack", json={"orderId": order["orderId"]})
    assert packed.status_code == 200
    packed_payload = packed.json()
    assert packed_payload["result"]["solution"]

    fetched = client.get(f"/orders/{order['orderId']}")
    assert fetched.status_code == 200
    fetched_order = fetched.json()
    assert fetched_order["status"] == "packed"
    assert fetched_order["result"]["solution"]


def test_order_validation_rejects_unknown_sku():
    response = client.post("/orders", json={"skuIds": ["skuId_does_not_exist"]})
    assert response.status_code == 400
