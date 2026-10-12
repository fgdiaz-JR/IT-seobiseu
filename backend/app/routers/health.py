from fastapi import APIRouter

from app.database.connection import pool
from app.schemas.health import HealthResponse

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    return HealthResponse(
        status="ok",
        database="configured" if pool is not None else "not_configured",
    )

