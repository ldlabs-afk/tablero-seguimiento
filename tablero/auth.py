"""Autenticación: inicio de sesión, cierre y bloqueo por intentos fallidos (REQ-03-01 a REQ-03-03)."""
from __future__ import annotations

import time
from functools import wraps

from flask import Blueprint, current_app, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash

from . import db
from .seguridad import registrar_evento

bp = Blueprint("auth", __name__)

MENSAJE_FALLO = "Usuario o contraseña incorrectos."
MENSAJE_BLOQUEO = "Cuenta bloqueada temporalmente por intentos fallidos. Contacte al líder tecnológico."


def requiere_sesion(vista):
    @wraps(vista)
    def envoltura(*args, **kwargs):
        if not session.get("usuario"):
            return redirect(url_for("auth.login"))
        return vista(*args, **kwargs)
    return envoltura


def requiere_rol(*roles):
    def decorador(vista):
        @wraps(vista)
        def envoltura(*args, **kwargs):
            if session.get("rol") not in roles:
                return render_template("error.html", mensaje="No tiene permiso para esta acción."), 403
            return vista(*args, **kwargs)
        return requiere_sesion(envoltura)
    return decorador


def _bloquear_si_corresponde(usuario: str, intentos: int) -> bool:
    maximo = current_app.config["MAX_INTENTOS"]
    if intentos < maximo:
        return False
    hasta = time.time() + current_app.config["BLOQUEO_MINUTOS"] * 60
    base = db.conexion()
    base.execute("UPDATE usuarios SET bloqueado_hasta = ? WHERE usuario = ?", (hasta, usuario))
    base.commit()
    registrar_evento("BLOQUEO_CUENTA", usuario, f"Cuenta bloqueada tras {intentos} intentos fallidos")
    return True


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    usuario = request.form.get("usuario", "").strip()
    clave = request.form.get("clave", "")
    base = db.conexion()
    fila = base.execute(
        "SELECT usuario, hash_clave, rol, intentos_fallidos, bloqueado_hasta FROM usuarios WHERE usuario = ?",
        (usuario,),
    ).fetchone()

    if fila is not None and fila["bloqueado_hasta"] > time.time():
        registrar_evento("INTENTO_CUENTA_BLOQUEADA", usuario, "Intento de acceso a una cuenta bloqueada")
        return render_template("login.html", error=MENSAJE_BLOQUEO), 423

    if fila is None or not check_password_hash(fila["hash_clave"], clave):
        registrar_evento("LOGIN_FALLIDO", usuario or None, "Credenciales incorrectas")
        if fila is not None:
            intentos = fila["intentos_fallidos"] + 1
            base.execute("UPDATE usuarios SET intentos_fallidos = ? WHERE usuario = ?", (intentos, usuario))
            base.commit()
            if _bloquear_si_corresponde(usuario, intentos):
                return render_template("login.html", error=MENSAJE_BLOQUEO), 423
        return render_template("login.html", error=MENSAJE_FALLO), 401

    base.execute("UPDATE usuarios SET intentos_fallidos = 0, bloqueado_hasta = 0 WHERE usuario = ?", (usuario,))
    base.commit()
    session.clear()
    session.permanent = True
    session["usuario"] = fila["usuario"]
    session["rol"] = fila["rol"]
    registrar_evento("LOGIN_EXITOSO", usuario, "Inicio de sesión")
    return redirect(url_for("paneles.indicadores"))


@bp.post("/logout")
def logout():
    usuario = session.get("usuario")
    session.clear()
    if usuario:
        registrar_evento("LOGOUT", usuario, "Cierre de sesión")
    return redirect(url_for("auth.login"))
