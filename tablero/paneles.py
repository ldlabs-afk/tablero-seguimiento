"""Paneles del tablero: indicadores trimestrales del PHVA y eventos de seguridad con su acción."""
from __future__ import annotations

from flask import Blueprint, redirect, render_template, request, session, url_for

from . import db
from .auth import requiere_rol, requiere_sesion
from .seguridad import registrar_evento

bp = Blueprint("paneles", __name__)


@bp.get("/indicadores")
@requiere_sesion
def indicadores():
    filas = db.conexion().execute(
        "SELECT periodo, nombre, valor, meta, registrado_por, fecha_registro FROM indicadores ORDER BY id DESC"
    ).fetchall()
    return render_template("indicadores.html", indicadores=filas)


@bp.post("/indicadores")
@requiere_rol("dueno", "lider")
def agregar_indicador():
    periodo = request.form.get("periodo", "").strip()[:20]
    nombre = request.form.get("nombre", "").strip()[:120]
    meta = request.form.get("meta", "").strip()[:60]
    texto_valor = request.form.get("valor", "").strip()
    if not (texto_valor.isascii() and texto_valor.isdigit()) or len(texto_valor) > 7:
        return render_template("error.html", mensaje="El valor debe ser un número entero entre 0 y 9999999."), 400
    valor = int(texto_valor)
    if not periodo or not nombre or not meta:
        return render_template("error.html", mensaje="Todos los campos son obligatorios."), 400
    base = db.conexion()
    base.execute(
        "INSERT INTO indicadores (periodo, nombre, valor, meta, registrado_por) VALUES (?, ?, ?, ?, ?)",
        (periodo, nombre, valor, meta, session["usuario"]),
    )
    base.commit()
    return redirect(url_for("paneles.indicadores"))


@bp.get("/eventos")
@requiere_rol("dueno", "lider")
def eventos():
    filas = db.conexion().execute(
        "SELECT id, fecha, tipo, usuario, ip, detalle, accion, responsable_accion, fecha_accion "
        "FROM eventos_seguridad ORDER BY id DESC LIMIT 200"
    ).fetchall()
    return render_template("eventos.html", eventos=filas)


@bp.post("/eventos/<int:evento_id>/accion")
@requiere_rol("dueno", "lider")
def registrar_accion(evento_id: int):
    accion = request.form.get("accion", "").strip()[:500]
    desbloquear = request.form.get("desbloquear") == "si"
    if not accion:
        return render_template("error.html", mensaje="Describa la acción tomada."), 400
    base = db.conexion()
    evento = base.execute("SELECT usuario FROM eventos_seguridad WHERE id = ?", (evento_id,)).fetchone()
    if evento is None:
        return render_template("error.html", mensaje="Evento inexistente."), 404
    base.execute(
        "UPDATE eventos_seguridad SET accion = ?, responsable_accion = ?, fecha_accion = datetime('now', 'localtime') "
        "WHERE id = ?",
        (accion, session["usuario"], evento_id),
    )
    if desbloquear and evento["usuario"]:
        base.execute(
            "UPDATE usuarios SET intentos_fallidos = 0, bloqueado_hasta = 0 WHERE usuario = ?", (evento["usuario"],)
        )
    base.commit()
    registrar_evento("ACCION_REGISTRADA", session["usuario"], f"Acción sobre el evento {evento_id}")
    return redirect(url_for("paneles.eventos"))
