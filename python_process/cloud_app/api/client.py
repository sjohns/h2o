from fastapi import APIRouter, HTTPException

from python_process.cloud_app.core.solver import solve
from python_process.cloud_app.data.repository import load_skus
from python_process.cloud_app.data.versioning import get_current_version
from python_process.cloud_app.schemas.models import CalculateRequest, CalculateResponse

router = APIRouter()


@router.post("/calculate", response_model=CalculateResponse)
def calculate(request: CalculateRequest) -> CalculateResponse:
    try:
        version = get_current_version()
        sku_df = load_skus(version)
        result = solve(
            sku_df=sku_df,
            selected_sku_ids=request.selected_sku_ids,
            truck_fill_ratio=request.truck_fill_ratio,
            fixed_bundles=request.fixed_bundles,
            min_bundles=request.min_bundles,
            max_bundles=request.max_bundles,
        )
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    payload = CalculateResponse(version=version, **result)
    return payload
