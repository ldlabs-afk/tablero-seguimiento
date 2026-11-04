"""Acceso a la base de datos SQLite. Todas las consultas son parametrizadas (REQ-03-04)."""
from __future__ import annotations

import sqlite3

import click
from flask import current_app, g

ESQUEMA = """
CREATE TABLE IF NOT EXISTS usuarios (
    usuario TEXT PRIMARY KEY,
    hash_clave TEXT NOT NULL,
    rol TEXT NOT NULL CHECK (rol IN ('dueno', 'lider', 'consulta')),
    intentos_fallidos INTEGER NOT NULL DEFAULT 0,
    bloqueado_hasta REAL NOT NULL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS indicadores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    periodo TEXT NOT NULL,
    nombre TEXT NOT NULL,
    valor REAL NOT NULL,
    meta TEXT NOT NULL,
    registrado_por TEXT NOT NULL,
    fecha_registro TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
);
CREATE TABLE IF NOT EXISTS eventos_seguridad (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
    tipo TEXT NOT NULL,
    usuario TEXT,
    ip TEXT,
    detalle TEXT,
    accion TEXT,
    responsable_accion TEXT,
    fecha_accion TEXT
);
"""


def conexion() -> sqlite3.Connection:
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
    return g.db


def cerrar(_error=None) -> None:
    base = g.pop("db", None)
    if base is not None:
        base.close()


def inicializar() -> None:
    conexion().executescript(ESQUEMA)
    conexion().commit()


def init_app(app) -> None:
    app.teardown_appcontext(cerrar)

    @app.cli.command("init-db")
    def init_db_comando():
        """Crea las tablas si no existen."""
        inicializar()
        click.echo("Base de datos inicializada")
