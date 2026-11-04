# R-03 tablero-seguimiento

Herramienta interna del hogar (laboratorio académico). Registra los indicadores trimestrales de la fase **Verificar** del
PHVA y los eventos de seguridad con la acción tomada frente a cada uno. La carpeta `gobierno/` contiene la regla de
desarrollo seguro (**LDS-LAB**) y los documentos que rigen los tres repositorios.

> Escenario de laboratorio: repositorio público con datos ficticios.

```bash
python3 -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt
export ENTORNO=prueba TABLERO_PUERTO=5000
python3 gestion.py crear-usuario auditor-prueba --rol consulta
python3 gestion.py cargar-ficticios
python3 servir.py
```

| Variable | Uso | Valor por defecto |
|---|---|---|
| `ENTORNO` | desarrollo, prueba o produccion | desarrollo |
| `TABLERO_SECRET_KEY` | Clave de sesión (obligatoria en producción) | aleatoria fuera de producción |
| `TABLERO_DB` / `TABLERO_BITACORA` | Base de datos y bitácora de seguridad | carpeta `instance/` |
| `TABLERO_MAX_INTENTOS` / `TABLERO_BLOQUEO_MINUTOS` | Bloqueo por intentos fallidos | 3 / 15 |
| `TABLERO_HOST` / `TABLERO_PUERTO` | Interfaz y puerto | 127.0.0.1 / 5000 |
