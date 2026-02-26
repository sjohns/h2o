#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
BASE_URL = 'http://127.0.0.1:8001'


def _request_json(method: str, path: str, payload: dict | None = None) -> dict:
    url = f'{BASE_URL}{path}'
    data = None
    headers = {'Content-Type': 'application/json'}
    if payload is not None:
        data = json.dumps(payload).encode('utf-8')

    req = Request(url=url, data=data, method=method, headers=headers)
    with urlopen(req, timeout=10) as resp:
        body = resp.read().decode('utf-8')
        return json.loads(body)


def _wait_for_health(max_wait_seconds: int = 20) -> None:
    start = time.time()
    while True:
        try:
            _request_json('GET', '/health')
            return
        except (URLError, HTTPError):
            if time.time() - start > max_wait_seconds:
                raise
            time.sleep(0.25)


def main() -> None:
    proc = subprocess.Popen(
        ['python3', '-m', 'uvicorn', 'api.app:app', '--host', '127.0.0.1', '--port', '8001'],
        cwd=str(ROOT),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    try:
        _wait_for_health()

        print('[1] GET /skus')
        skus = _request_json('GET', '/skus')
        sku_ids = [skus['skus'][0]['skuId'], skus['skus'][1]['skuId']]
        print('selected:', sku_ids)

        print('[2] POST /orders')
        order = _request_json(
            'POST',
            '/orders',
            {'items': [{'sku_id': sku_ids[0], 'quantity': 2}, {'sku_id': sku_ids[1], 'quantity': 1}]},
        )
        print('order_id:', order['order_id'])

        print('[3] POST /pack')
        packed = _request_json('POST', '/pack', {'order_id': order['order_id']})
        result = packed['packing_result']
        assert 'skus' in result and 'solution' in result
        print('solution_items:', len(result['solution']))

        print('[4] GET /orders/{id}')
        fetched = _request_json('GET', f"/orders/{order['order_id']}")
        assert fetched['status'] == 'packed'
        assert fetched['packing_result'] is not None
        assert fetched['packing_result']['solution']
        print('smoke test passed')
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()


if __name__ == '__main__':
    main()
