from fastapi import APIRouter, HTTPException, Request

from ...replacement import compute_solution_for_selected_skus_with_constraints
from ..data.audit import append_audit_event
from ..data.repository import load_skus
from ..data.versioning import get_current_version
from ..schemas.models import CalculateRequest, CalculateResponse

router = APIRouter()


@router.post("/calculate", response_model=CalculateResponse)
def calculate(request: CalculateRequest, http_request: Request) -> CalculateResponse:
    try:
        version = get_current_version()
        sku_data_frame = load_skus(version)
        selected_sku_identifiers = request.selected_sku_ids
        available_sku_identifiers = set(sku_data_frame["sku_id"].astype(str).tolist())
        filtered_selected_sku_identifiers = [
            sku_identifier
            for sku_identifier in selected_sku_identifiers
            if sku_identifier in available_sku_identifiers
        ]
        result = compute_solution_for_selected_skus_with_constraints(
            selected_sku_identifiers=filtered_selected_sku_identifiers,
            fixed_bundles_by_sku_id=request.fixed_bundles,
            minimum_bundles_by_sku_id=request.min_bundles,
            maximum_bundles_by_sku_id=request.max_bundles,
        )
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    payload = CalculateResponse(version=version, **result)
    append_audit_event(
        event_type="client.calculate",
        payload={
            "version": version,
            "client_host": http_request.client.host if http_request.client else None,
            "selected_sku_ids": request.selected_sku_ids,
            "fixed_bundles": request.fixed_bundles,
            "min_bundles": request.min_bundles,
            "max_bundles": request.max_bundles,
            "lcm": payload.lcm,
            "total_truck_size": payload.total_truck_size,
            "total_sticks": payload.total_sticks,
        },
    )
    return payload


@router.post("/calculate/replacement", response_model=CalculateResponse)
def calculate_replacement(request: CalculateRequest, http_request: Request) -> CalculateResponse:
    return calculate(request, http_request)


@router.get("/skus")
def list_current_skus() -> dict:
    try:
        version = get_current_version()
        sku_data_frame = load_skus(version)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    records = sku_data_frame.to_dict(orient="records")
    return {"version": version, "skus": records}
