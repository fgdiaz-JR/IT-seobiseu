from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.routers.health import router as health_router

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="API REST para la gestión de soporte y operaciones TI.",
)

if settings.origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(health_router, prefix=settings.api_prefix)
