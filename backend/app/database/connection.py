from collections.abc import Iterator

import oracledb
from fastapi import HTTPException, status

from app.core.config import get_settings


def create_pool() -> oracledb.ConnectionPool | None:
    settings = get_settings()
    if not all((settings.oracle_user, settings.oracle_password, settings.oracle_dsn)):
        return None
    return oracledb.create_pool(
        user=settings.oracle_user,
        password=settings.oracle_password,
        dsn=settings.oracle_dsn,
        min=1,
        max=5,
        increment=1,
    )


pool = create_pool()


def get_connection() -> Iterator[oracledb.Connection]:
    if pool is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="La base de datos no está configurada.",
        )
    with pool.acquire() as connection:
        yield connection

