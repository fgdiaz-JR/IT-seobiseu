from collections.abc import Generator
import sqlite3

import oracledb
from fastapi import HTTPException, status

from app.core.config import get_settings

settings = get_settings()
pool: oracledb.ConnectionPool | None = None

if not settings.use_sqlite and all(
    (settings.oracle_user, settings.oracle_password, settings.oracle_dsn)
):
    pool = oracledb.create_pool(
        user=settings.oracle_user,
        password=settings.oracle_password,
        dsn=settings.oracle_dsn,
        config_dir=settings.oracle_wallet_dir or None,
        min=1,
        max=5,
        increment=1,
    )


def get_sqlite_connection() -> sqlite3.Connection:
    connection = sqlite3.connect(settings.sqlite_path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def get_connection() -> Generator[sqlite3.Connection | oracledb.Connection, None, None]:
    if settings.use_sqlite:
        connection = get_sqlite_connection()
        try:
            yield connection
        finally:
            connection.close()
        return

    if pool is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Oracle no está configurado o no se pudo abrir el pool.",
        )

    with pool.acquire() as connection:
        yield connection
