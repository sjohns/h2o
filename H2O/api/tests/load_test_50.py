import concurrent.futures
import requests
import time

BASE = "http://127.0.0.1:8000"


def run_one_user():
    start = time.time()

    r = requests.get(f"{BASE}/skus")
    r.raise_for_status()
    skus = r.json()["skus"]

    selected = [s["skuId"] for s in skus[:2]]

    for _ in range(26):
        r = requests.post(f"{BASE}/orders", json={"selectedSkus": selected})
        r.raise_for_status()
        oid = r.json()["order_id"]

        r = requests.post(f"{BASE}/pack", json={"orderId": oid})
        r.raise_for_status()

    return time.time() - start


def main():
    USERS = 50

    t0 = time.time()

    with concurrent.futures.ThreadPoolExecutor(max_workers=USERS) as ex:
        results = list(ex.map(lambda _: run_one_user(), range(USERS)))

    total = time.time() - t0

    print("Users:", USERS)
    print("Total time:", total)
    print("Avg user time:", sum(results) / len(results))
    print("Throughput orders/sec:", (USERS * 26) / total)


if __name__ == "__main__":
    main()
