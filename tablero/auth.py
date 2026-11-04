"""Autenticación: inicio de sesión y cierre (REQ-03-01)."""
from __future__ import annotations

from functools import wraps

from flask import Blueprint, current_app, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash

from . import db
from .seguridad import registrar_evento

bp = Blueprint("auth", __name__)

MENSAJE_FALLO = "Usuario o contraseña incorrectos."


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

    if fila is None or not check_password_hash(fila["hash_clave"], clave):
        registrar_evento("LOGIN_FALLIDO", usuario or None, "Credenciales incorrectas")
        return render_template("login.html", error=MENSAJE_FALLO), 401

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
