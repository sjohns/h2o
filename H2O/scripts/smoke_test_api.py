#!/usr/bin/env python3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from fastapi.testclient import TestClient

from api_backend.app import app


client = TestClient(app)


def main() -> None:
    print("[1] GET /skus")
    skus_resp = client.get("/skus")
    skus_resp.raise_for_status()
    skus = skus_resp.json()["skus"]
    sku_ids = [skus[0]["skuId"], skus[1]["skuId"], skus[2]["skuId"]]
    print(f"selected skuIds={sku_ids}")

    print("[2] POST /orders")
    order_resp = client.post("/orders", json={"skuIds": sku_ids})
    order_resp.raise_for_status()
    order = order_resp.json()
    print(f"orderId={order['orderId']}")

    print("[3] POST /pack")
    pack_resp = client.post("/pack", json={"orderId": order["orderId"]})
    pack_resp.raise_for_status()
    result = pack_resp.json()["result"]
    print(f"totalSize={result['totalSize']} totalSticks={result['totalSticks']}")

    print("[4] GET /orders/{id}")
    get_resp = client.get(f"/orders/{order['orderId']}")
    get_resp.raise_for_status()
    full = get_resp.json()
    assert full["status"] == "packed"
    assert full["result"]["solution"]
    print("smoke test passed")


if __name__ == "__main__":
    main()
