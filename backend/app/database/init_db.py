from pathlib import Path

from pwdlib import PasswordHash

from app.core.config import get_settings
from app.database.connection import get_sqlite_connection

password_hash = PasswordHash.recommended()


def init_sqlite() -> None:
    settings = get_settings()
    if not settings.use_sqlite:
        return
    connection = get_sqlite_connection()
    connection.executescript(
        """
        CREATE TABLE IF NOT EXISTS roles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL UNIQUE
        );
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rol_id INTEGER NOT NULL,
            nombre TEXT NOT NULL,
            correo TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            activo INTEGER NOT NULL DEFAULT 1,
            FOREIGN KEY (rol_id) REFERENCES roles(id)
        );
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            razon_social TEXT NOT NULL,
            identificacion_fiscal TEXT NOT NULL UNIQUE,
            correo_contacto TEXT,
            telefono TEXT,
            estado TEXT NOT NULL DEFAULT 'ACTIVO'
        );
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER NOT NULL,
            creado_por INTEGER NOT NULL,
            tipo_requerimiento TEXT NOT NULL,
            prioridad TEXT NOT NULL,
            estado TEXT NOT NULL DEFAULT 'ABIERTO',
            asunto TEXT NOT NULL,
            descripcion TEXT NOT NULL,
            FOREIGN KEY (cliente_id) REFERENCES clientes(id),
            FOREIGN KEY (creado_por) REFERENCES usuarios(id)
        );
        CREATE TABLE IF NOT EXISTS inventario (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sku TEXT NOT NULL UNIQUE,
            nombre TEXT NOT NULL,
            categoria TEXT NOT NULL,
            stock INTEGER NOT NULL DEFAULT 0,
            stock_minimo INTEGER NOT NULL DEFAULT 0,
            precio_unitario REAL NOT NULL DEFAULT 0,
            ubicacion TEXT,
            activo INTEGER NOT NULL DEFAULT 1
        );
        CREATE TABLE IF NOT EXISTS ordenes_trabajo (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticket_id INTEGER,
            cliente_id INTEGER NOT NULL,
            tecnico_id INTEGER,
            equipo TEXT,
            prioridad TEXT NOT NULL,
            estado TEXT NOT NULL DEFAULT 'PENDIENTE',
            diagnostico TEXT,
            FOREIGN KEY (ticket_id) REFERENCES tickets(id),
            FOREIGN KEY (cliente_id) REFERENCES clientes(id),
            FOREIGN KEY (tecnico_id) REFERENCES usuarios(id)
        );
        """
    )
    roles = ("ADMINISTRADOR", "SUPERVISOR", "TECNICO", "CLIENTE")
    connection.executemany("INSERT OR IGNORE INTO roles (nombre) VALUES (?)", ((role,) for role in roles))
    role_id = connection.execute(
        "SELECT id FROM roles WHERE nombre = 'ADMINISTRADOR'"
    ).fetchone()["id"]
    connection.execute(
        """
        INSERT OR IGNORE INTO usuarios (rol_id, nombre, correo, password_hash)
        VALUES (?, ?, ?, ?)
        """,
        (
            role_id,
            "Administrador local",
            settings.seed_admin_email,
            password_hash.hash(settings.seed_admin_password),
        ),
    )
    connection.commit()
    connection.close()
