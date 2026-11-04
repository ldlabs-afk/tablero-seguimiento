#!/usr/bin/env python3
"""Administración del tablero: inicializar la base, crear usuarios y cargar datos ficticios."""
from __future__ import annotations

import argparse
import getpass
import sys

from werkzeug.security import generate_password_hash

from tablero import create_app, db

ROLES = ("dueno", "lider", "consulta")


def crear_usuario(usuario: str, rol: str, clave: str) -> None:
    if len(clave) < 12:
        raise ValueError("La contraseña debe tener al menos 12 caracteres (LDS-LAB 8)")
    base = db.conexion()
    base.execute(
        "INSERT OR REPLACE INTO usuarios (usuario, hash_clave, rol, intentos_fallidos, bloqueado_hasta) "
        "VALUES (?, ?, ?, 0, 0)",
        (usuario, generate_password_hash(clave), rol),
    )
    base.commit()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="comando", required=True)
    sub.add_parser("init-db")
    cu = sub.add_parser("crear-usuario")
    cu.add_argument("usuario")
    cu.add_argument("--rol", choices=ROLES, required=True)
    sub.add_parser("cargar-ficticios")
    args = parser.parse_args()

    app = create_app()
    with app.app_context():
        db.inicializar()
        if args.comando == "crear-usuario":
            clave = getpass.getpass(f"Contraseña para {args.usuario}: ")
            try:
                crear_usuario(args.usuario, args.rol, clave)
            except ValueError as error:
                print(f"ERROR: {error}")
                return 2
            print(f"Usuario {args.usuario} creado con rol {args.rol} en el entorno {app.config['ENTORNO']}")
        elif args.comando == "cargar-ficticios":
            if app.config["ENTORNO"] == "produccion":
                print("ERROR: los datos ficticios no se cargan en producción")
                return 2
            from datos.generar_ficticios import cargar
            print(f"{cargar(db.conexion())} indicadores FICTICIOS cargados")
        else:
            print(f"Base de datos lista: {app.config['DATABASE']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
