"""Controles transversales: token anti-CSRF, cabeceras de seguridad y registro de eventos."""
from __future__ import annotations

import hmac
import json
import logging
import secrets
import time

from flask import abort, current_app, request, session

from . import db

registro = logging.getLogger("tablero.seguridad")

CABECERAS = {
    "Content-Security-Policy": "default-src 'self'; frame-ancestors 'none'; form-action 'self'; base-uri 'self'",
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "Referrer-Policy": "no-referrer",
    "Permissions-Policy": "camera=(), microphone=(), geolocation=()",
    "Cross-Origin-Opener-Policy": "same-origin",
    "Cross-Origin-Resource-Policy": "same-origin",
    "Cross-Origin-Embedder-Policy": "require-corp",
    "Cache-Control": "no-store",
}


def token_csrf() -> str:
    if "csrf" not in session:
        session["csrf"] = secrets.token_urlsafe(32)
    return session["csrf"]


def verificar_csrf() -> None:
    if request.method != "POST":
        return
    enviado = request.form.get("csrf_token", "")
    esperado = session.get("csrf", "")
    if not esperado or not hmac.compare_digest(enviado, esperado):
        abort(400)


def poner_cabeceras(respuesta):
    for nombre, valor in CABECERAS.items():
        respuesta.headers.setdefault(nombre, valor)
    return respuesta


def registrar_evento(tipo: str, usuario: str | None, detalle: str) -> None:
    """Registra el evento en la base de datos y en la bitácora. Nunca registra contraseñas."""
    ip = request.remote_addr
    base = db.conexion()
    base.execute(
        "INSERT INTO eventos_seguridad (tipo, usuario, ip, detalle) VALUES (?, ?, ?, ?)",
        (tipo, usuario, ip, detalle),
    )
    base.commit()
    registro.warning(json.dumps({"fecha": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "tipo": tipo,
                                 "usuario": usuario, "ip": ip, "detalle": detalle}, ensure_ascii=False))


def configurar_bitacora(app) -> None:
    manejador = logging.FileHandler(app.config["BITACORA"], encoding="utf-8")
    manejador.setFormatter(logging.Formatter("%(message)s"))
    registro.handlers.clear()
    registro.addHandler(manejador)
    registro.setLevel(logging.INFO)


def init_app(app) -> None:
    configurar_bitacora(app)
    app.before_request(verificar_csrf)
    app.after_request(poner_cabeceras)
    app.jinja_env.globals["csrf_token"] = token_csrf
