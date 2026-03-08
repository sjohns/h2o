import asyncio

import httpx

from api.app import app


async def _request(method: str, path: str, **kwargs):
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
        return await client.request(method, path, **kwargs)


def request(method: str, path: str, **kwargs):
    return asyncio.run(_request(method, path, **kwargs))


def test_get_skus_returns_list():
    response = request("GET", "/skus")
    assert response.status_code == 200
    payload = response.json()
    assert payload["count"] > 0
    assert len(payload["skus"]) == payload["count"]
    assert "skuId" in payload["skus"][0]


def test_create_order_and_get_order():
    skus = request("GET", "/skus").json()["skus"]
    create_response = request(
        "POST",
        "/orders",
        json={
            "items": [
                {"sku_id": skus[0]["skuId"], "quantity": 2},
                {"sku_id": skus[1]["skuId"], "quantity": 1},
            ]
        },
    )
    assert create_response.status_code == 200
    created = create_response.json()
    assert "order_id" in created

    fetch_response = request("GET", f"/orders/{created['order_id']}")
    assert fetch_response.status_code == 200
    order = fetch_response.json()
    assert order["status"] == "created"
    assert len(order["items"]) == 2
    assert order["packing_result"] is None


def test_pack_returns_canonical_frontend_shape_and_persists():
    skus = request("GET", "/skus").json()["skus"]
    selected = [skus[0]["skuId"], skus[1]["skuId"]]
    create_response = request(
        "POST",
        "/orders",
        json={"items": [{"sku_id": selected[0], "quantity": 3}, {"sku_id": selected[1], "quantity": 1}]},
    )
    order_id = create_response.json()["order_id"]

    pack_response = request("POST", "/pack", json={"order_id": order_id})
    assert pack_response.status_code == 200
    payload = pack_response.json()

    assert set(payload.keys()) == {"order_id", "packing_result"}
    assert payload["order_id"] == order_id

    result = payload["packing_result"]
    expected_result_keys = {
        "skus",
        "solution",
        "lcmValue",
        "minTruckSize",
        "maxTruckSize",
        "totalSize",
        "totalSticks",
        "differenceSum",
    }
    assert set(result.keys()) == expected_result_keys

    assert isinstance(result["skus"], dict)
    assert set(result["skus"].keys()) == set(selected)
    for sku_id in selected:
        sku = result["skus"][sku_id]
        assert sku["skuId"] == sku_id
        assert "calculatedBundlesPerTruckload" in sku
        assert "calculatedBundleSize" in sku

    assert isinstance(result["solution"], list)
    assert len(result["solution"]) == 2
    assert result["solution"][0]["skuId"] in selected
    assert "numberOfBundles" in result["solution"][0]

    assert isinstance(result["lcmValue"], int)
    assert isinstance(result["totalSize"], int)
    assert isinstance(result["totalSticks"], int)
    assert isinstance(result["differenceSum"], int)
    assert result["differenceSum"] >= 0

    order_response = request("GET", f"/orders/{order_id}")
    assert order_response.status_code == 200
    order = order_response.json()
    assert order["status"] == "packed"
    assert order["packing_result"] is not None
    assert order["packing_result"]["solution"] == result["solution"]


def test_order_validation_for_unknown_sku():
    response = request("POST", "/orders", json={"items": [{"sku_id": "bad_sku", "quantity": 1}]})
    assert response.status_code == 400


def test_pack_unknown_order_returns_404():
    response = request("POST", "/pack", json={"order_id": "missing"})
    assert response.status_code == 404


def test_pack_single_sku():
    skus = request("GET", "/skus").json()["skus"]
    selected_id = skus[0]["skuId"]
    create_response = request(
        "POST",
        "/orders",
        json={"items": [{"sku_id": selected_id, "quantity": 1}]},
    )
    assert create_response.status_code == 200
    order_id = create_response.json()["order_id"]

    pack_response = request("POST", "/pack", json={"order_id": order_id})
    assert pack_response.status_code == 200
    result = pack_response.json()["packing_result"]
    assert len(result["solution"]) == 1
    assert result["solution"][0]["skuId"] == selected_id
    assert result["totalSize"] > 0


def test_pack_with_bundle_constraints():
    skus = request("GET", "/skus").json()["skus"]
    selected = [skus[0]["skuId"], skus[1]["skuId"]]
    order_id = request(
        "POST",
        "/orders",
        json={"items": [{"sku_id": selected[0], "quantity": 1}, {"sku_id": selected[1], "quantity": 1}]},
    ).json()["order_id"]

    # First do an unconstrained solve to get the initial result
    unconstrained = request("POST", "/pack", json={"order_id": order_id}).json()["packing_result"]
    sku0_bundles = next(s["numberOfBundles"] for s in unconstrained["solution"] if s["skuId"] == selected[0])
    max0 = unconstrained["skus"][selected[0]]["calculatedBundlesPerTruckload"]

    # Constrain sku0 to exactly sku0_bundles
    constraints = {
        selected[0]: {"min_bundles": sku0_bundles, "max_bundles": sku0_bundles},
        selected[1]: {"min_bundles": 1, "max_bundles": max0},
    }
    constrained = request(
        "POST",
        "/pack",
        json={"orderId": order_id, "bundleConstraints": constraints},
    ).json()["packing_result"]

    assert constrained["solution"] is not None
    sku0_constrained = next(s["numberOfBundles"] for s in constrained["solution"] if s["skuId"] == selected[0])
    assert sku0_constrained == sku0_bundles
