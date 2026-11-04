# Diseño de R-03 – aplicación de los principios de ingeniería segura (LDS-LAB 8)

| Principio | Cómo se aplica en R-03 |
|---|---|
| Mínimo privilegio | Roles dueño, líder y consulta; solo dueño y líder gestionan eventos. Servicio escucha solo en 127.0.0.1 |
| Valores seguros por defecto | Entorno de desarrollo por defecto; en producción no arranca sin clave secreta; datos ficticios bloqueados en producción |
| Defensa en profundidad | Contraseña adaptativa + bloqueo + registro + acción documentada; CSRF + SameSite + CSP |
| Fallo seguro | Errores con mensajes genéricos; modo depuración desactivado fuera de desarrollo |
| Separación de funciones | Quien registra la acción frente a un bloqueo queda identificado; el despliegue lo hace `adminlab` |

Componentes: `tablero/auth.py` (autenticación y bloqueo), `tablero/seguridad.py` (CSRF, cabeceras, eventos),
`tablero/paneles.py` (indicadores y eventos), `tablero/db.py` (SQLite parametrizado), `servir.py` (Waitress).
