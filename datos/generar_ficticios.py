"""Generador de datos FICTICIOS para los entornos de desarrollo y prueba (LDS-LAB 6.2).

Todos los registros llevan la marca FICTICIO. Nunca se copian datos operativos.
"""
import random

INDICADORES = [
    ("Cuentas con privilegios de administrador de uso diario", "0"),
    ("Adjuntos del trabajo conservados en el disco", "≤ 5"),
    ("Dispositivos desconocidos detectados en la red", "0"),
    ("Actualizaciones pendientes", "0"),
    ("Incidentes en el periodo", "0"),
]


def cargar(conexion, semilla: int = 2026) -> int:
    azar = random.Random(semilla)
    total = 0
    for periodo in ("2026-T2", "2026-T3"):
        for nombre, meta in INDICADORES:
            conexion.execute(
                "INSERT INTO indicadores (periodo, nombre, valor, meta, registrado_por) VALUES (?, ?, ?, ?, ?)",
                (periodo, f"FICTICIO – {nombre}", azar.randint(0, 6), meta, "generador-ficticio"),
            )
            total += 1
    conexion.commit()
    return total
