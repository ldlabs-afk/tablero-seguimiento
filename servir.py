#!/usr/bin/env python3
"""Sirve el tablero con Waitress (servidor WSGI de producción). Escucha solo en la interfaz configurada."""
import os

from waitress import serve

from tablero import create_app

if __name__ == "__main__":
    app = create_app()
    host = os.environ.get("TABLERO_HOST", "127.0.0.1")
    puerto = int(os.environ.get("TABLERO_PUERTO", "5000"))
    print(f"Tablero ({app.config['ENTORNO']}) en http://{host}:{puerto}")
    serve(app, host=host, port=puerto)
