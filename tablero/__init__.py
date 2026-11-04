"""R-03 tablero-seguimiento: registro de indicadores del PHVA y de eventos de seguridad del hogar."""
from __future__ import annotations

import os
import secrets
from datetime import timedelta

from flask import Flask, redirect, session, url_for

from . import auth, db, paneles, seguridad

ENTORNOS = ("desarrollo", "prueba", "produccion")


def create_app(config: dict | None = None) -> Flask:
    app = Flask(__name__)
    entorno = os.environ.get("ENTORNO", "desarrollo")
    if entorno not in ENTORNOS:
        raise RuntimeError(f"ENTORNO inválido: {entorno}")

    clave = os.environ.get("TABLERO_SECRET_KEY")
    if not clave:
        if entorno == "produccion":
            raise RuntimeError("En producción TABLERO_SECRET_KEY es obligatoria")
        clave = secrets.token_hex(32)

    app.config.update(
        SECRET_KEY=clave,
        ENTORNO=entorno,
        DEBUG=entorno == "desarrollo",
        DATABASE=os.environ.get("TABLERO_DB", os.path.join(app.instance_path, f"tablero_{entorno}.db")),
        BITACORA=os.environ.get("TABLERO_BITACORA", os.path.join(app.instance_path, f"seguridad_{entorno}.log")),
        MAX_INTENTOS=int(os.environ.get("TABLERO_MAX_INTENTOS", "3")),
        BLOQUEO_MINUTOS=int(os.environ.get("TABLERO_BLOQUEO_MINUTOS", "15")),
        SESSION_COOKIE_NAME="tablero_sesion",
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
        PERMANENT_SESSION_LIFETIME=timedelta(minutes=30),
    )
    if config:
        app.config.update(config)
    os.makedirs(app.instance_path, exist_ok=True)

    db.init_app(app)
    seguridad.init_app(app)
    app.register_blueprint(auth.bp)
    app.register_blueprint(paneles.bp)

    @app.get("/")
    def inicio():
        if session.get("usuario"):
            return redirect(url_for("paneles.indicadores"))
        return redirect(url_for("auth.login"))

    return app
