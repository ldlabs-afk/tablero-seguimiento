"""Pruebas de seguridad de R-03 (requisitos en REQUISITOS.md)."""
from conftest import CLAVE, iniciar


def test_req03_01_inicio_de_sesion_valido(cliente):
    respuesta = iniciar(cliente, "auditor-prueba", CLAVE)
    assert respuesta.status_code == 302


def test_req03_01_credenciales_invalidas_mensaje_generico(cliente):
    a = iniciar(cliente, "auditor-prueba", "errada")
    b = iniciar(cliente, "no-existe", "errada")
    assert a.status_code == b.status_code == 401
    assert "Usuario o contraseña incorrectos" in a.get_data(as_text=True)


def test_req03_02_bloqueo_al_tercer_intento(cliente):
    codigos = [iniciar(cliente, "auditor-prueba", f"errada-{i}").status_code for i in range(3)]
    assert codigos == [401, 401, 423]
    assert iniciar(cliente, "auditor-prueba", CLAVE).status_code == 423


def test_req03_03_evento_registrado_sin_contrasena(cliente, app, tmp_path):
    for i in range(3):
        iniciar(cliente, "auditor-prueba", f"ClaveSecretaErrada-{i}")
    bitacora = (tmp_path / "seguridad.log").read_text(encoding="utf-8")
    assert "BLOQUEO_CUENTA" in bitacora
    assert "ClaveSecretaErrada" not in bitacora


def test_req03_03_accion_documentada_desbloquea(cliente, app):
    for i in range(3):
        iniciar(cliente, "auditor-prueba", f"errada-{i}")
    otro = app.test_client()
    iniciar(otro, "lider-prueba", CLAVE)
    from tablero import db
    with app.app_context():
        evento = db.conexion().execute(
            "SELECT id FROM eventos_seguridad WHERE tipo = 'BLOQUEO_CUENTA'").fetchone()["id"]
    html = otro.get("/eventos").get_data(as_text=True)
    import re
    csrf = re.search(r'name="csrf_token" value="([^"]+)"', html).group(1)
    otro.post(f"/eventos/{evento}/accion",
              data={"accion": "Verificado por otro canal; se desbloquea", "desbloquear": "si", "csrf_token": csrf})
    with app.app_context():
        fila = db.conexion().execute("SELECT accion, responsable_accion FROM eventos_seguridad WHERE id = ?",
                                     (evento,)).fetchone()
    assert fila["responsable_accion"] == "lider-prueba"
    assert iniciar(cliente, "auditor-prueba", CLAVE).status_code == 302


def test_req03_05_post_sin_token_csrf_rechazado(cliente):
    respuesta = cliente.post("/login", data={"usuario": "auditor-prueba", "clave": CLAVE})
    assert respuesta.status_code == 400


def test_req03_06_cabeceras_de_seguridad(cliente):
    cabeceras = cliente.get("/login").headers
    assert "default-src 'self'" in cabeceras["Content-Security-Policy"]
    assert cabeceras["X-Content-Type-Options"] == "nosniff"
    assert cabeceras["X-Frame-Options"] == "DENY"


def test_req03_07_cookie_de_sesion_protegida(cliente):
    respuesta = iniciar(cliente, "auditor-prueba", CLAVE)
    cookie = respuesta.headers["Set-Cookie"]
    assert "HttpOnly" in cookie and "SameSite=Lax" in cookie and "Expires=" in cookie


def test_req03_08_rol_consulta_no_ve_eventos(cliente):
    iniciar(cliente, "auditor-prueba", CLAVE)
    assert cliente.get("/eventos").status_code == 403


def test_req03_09_produccion_exige_clave_secreta(monkeypatch):
    import pytest
    from tablero import create_app
    monkeypatch.setenv("ENTORNO", "produccion")
    monkeypatch.delenv("TABLERO_SECRET_KEY", raising=False)
    with pytest.raises(RuntimeError):
        create_app()


def test_req03_10_depuracion_solo_en_desarrollo(app):
    assert app.config["DEBUG"] is False
