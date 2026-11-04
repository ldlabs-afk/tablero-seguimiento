import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from gestion import crear_usuario  # noqa: E402
from tablero import create_app, db  # noqa: E402

CLAVE = "Clave-de-prueba-FICTICIA-01"


@pytest.fixture
def app(tmp_path, monkeypatch):
    monkeypatch.setenv("ENTORNO", "prueba")
    aplicacion = create_app({
        "DATABASE": str(tmp_path / "prueba.db"),
        "BITACORA": str(tmp_path / "seguridad.log"),
        "TESTING": True,
    })
    from tablero import seguridad
    seguridad.configurar_bitacora(aplicacion)
    with aplicacion.app_context():
        db.inicializar()
        crear_usuario("auditor-prueba", "consulta", CLAVE)
        crear_usuario("lider-prueba", "lider", CLAVE)
    return aplicacion


@pytest.fixture
def cliente(app):
    return app.test_client()


def token(cliente) -> str:
    html = cliente.get("/login").get_data(as_text=True)
    return re.search(r'name="csrf_token" value="([^"]+)"', html).group(1)


def iniciar(cliente, usuario, clave):
    return cliente.post("/login", data={"usuario": usuario, "clave": clave, "csrf_token": token(cliente)})
