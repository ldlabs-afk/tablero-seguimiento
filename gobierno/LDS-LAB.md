# LDS-LAB – Regla de desarrollo seguro de las herramientas internas del hogar

| Campo | Valor |
|---|---|
| Versión | 1.0 |
| Estado | Aprobada |
| Aprobada por | Padre – Jefe de hogar, dueño de la información (cuenta `Xhirukai`; la aprobación queda en el commit que incorpora este documento) |
| Elaborada por | Hijo – Líder tecnológico (cuenta `ldlabs-afk`) |
| Revisión | Anual, o antes si ocurre un incidente o cambia el proceso (sección 13) |

> **Escenario de laboratorio.** El hogar no desarrolla software. Esta regla forma parte de un ejercicio académico
> representativo: describe cómo se gobernaría el desarrollo si el líder tecnológico construyera herramientas internas
> para ejecutar los planes de tratamiento de la matriz de riesgos. Todos los datos son ficticios.

## 1. Objeto y alcance

Establecer las normas de desarrollo seguro (NTC-ISO/IEC 27001:2022, control A.8.25) para las herramientas internas del hogar:

| ID | Repositorio | Función | Riesgo que trata |
|---|---|---|---|
| R-01 | `depurador-adjuntos` | Aplica la regla de conservación de adjuntos | R2 |
| R-02 | `revisor-red` | Compara los dispositivos conectados con el inventario autorizado | R5 |
| R-03 | `tablero-seguimiento` | Registra los indicadores de la fase Verificar y los eventos de seguridad | Fase Verificar del PHVA |

## 2. Roles y responsabilidades

| Rol | Persona | Responsabilidades |
|---|---|---|
| Dueño de la información y aprobador | Padre – Jefe de hogar (`padre-aprobador`) | Aprueba esta regla, los requisitos y cada cambio; ejecuta R-01 en producción |
| Desarrollador y líder tecnológico | Hijo (`hijo-dev`) | Desarrolla, prueba, mantiene el pipeline y registra las revisiones |
| Administrador del equipo de laboratorio | Cuenta `adminlab` | Despliega en producción las versiones etiquetadas y aprobadas |

Quien desarrolla no aprueba sus propios cambios ni tiene acceso a producción (segregación de funciones, A.5.3).

## 3. Ciclo de vida y puntos de control

| Fase | Qué se exige | Evidencia |
|---|---|---|
| Requisitos | Requisitos de seguridad con ID, origen y prueba asociada, aprobados por el dueño | `REQUISITOS.md` |
| Diseño | Aplicación de los principios de la sección 8 | `DISENO.md` |
| Codificación | Codificación segura (sección 4 y sección 8) | Código revisado en el PR |
| Pruebas | Pipeline de la sección 5 en verde | Ejecuciones de GitHub Actions |
| Cambios | Procedimiento de la sección 9 | Issue, PR, aprobación, `CHANGELOG.md` |
| Despliegue | Solo versiones etiquetadas y aprobadas, por el administrador (sección 7) | Etiqueta `vX.Y.Z` y registro de despliegue |

## 4. Gestión de secretos

1. Ninguna credencial, clave o token se escribe en el código ni en archivos versionados.
2. Las credenciales se leen de variables de entorno definidas en archivos `.env` locales, excluidos por `.gitignore`.
3. Si un secreto llega a un repositorio, aunque luego se borre del código, **se considera expuesto**: debe cambiarse
   (rotarse) en máximo 24 horas y registrarse en `gobierno/REGISTRO-REVISIONES.md`.

## 5. Pruebas de seguridad y pipeline

Cada repositorio tiene el workflow `.github/workflows/seguridad.yml` con cuatro trabajos, todos obligatorios para integrar a `main`:

| Trabajo | Herramienta | Bloquea cuando |
|---|---|---|
| `pruebas` | pytest | Falla cualquier prueba, incluidas las pruebas negativas de seguridad |
| `semgrep` | Semgrep (`p/python`; además `p/flask` en R-03) | Hay hallazgos de severidad ERROR |
| `gitleaks` | Gitleaks | Hay secretos en los commits del cambio |
| `dependencias` | pip-audit | Hay dependencias con vulnerabilidades conocidas |

Un falso positivo solo puede excluirse con un comentario `nosemgrep` que explique la razón.

## 6. Datos de prueba

6.1. Está **prohibido** copiar información operativa (correos, adjuntos, datos de propietarios o residentes) en los
repositorios o en los entornos de desarrollo y prueba.

6.2. Los datos de prueba son **ficticios**, llevan la marca `FICTICIO` y se generan con un generador versionado en el repositorio.

6.3. Si de manera excepcional se necesitara información operativa, se requiere autorización escrita del dueño de la
información, registro de la copia, enmascaramiento de los datos personales y borrado al terminar la prueba (A.8.33).

## 7. Entornos

| Entorno | R-01 | R-03 | Quién opera |
|---|---|---|---|
| Desarrollo | Copia de trabajo en `/home/hijo-dev/repos` | `ENTORNO=desarrollo` | hijo-dev |
| Prueba | Carpeta `datos_prueba/` (por defecto) | `ENTORNO=prueba`, puerto 5000, base de datos de prueba | hijo-dev y auditores |
| Producción | `/home/padre/Adjuntos_Copropiedad` | `ENTORNO=produccion`, puerto 8000, base de datos de producción | padre; despliegue por `adminlab` |

- El desarrollador **no tiene privilegios de administrador** (sudo) ni acceso de escritura a producción.
- Las pruebas nunca se ejecutan sobre producción.
- Solo se despliegan versiones etiquetadas (`vX.Y.Z`) cuyo PR fue aprobado.

## 8. Principios de ingeniería segura (A.8.27) y requisitos mínimos

1. **Mínimo privilegio:** cada herramienta corre con el usuario y los permisos estrictamente necesarios.
2. **Valores seguros por defecto:** sin configuración explícita, la herramienta no causa daño (por ejemplo, modo simulación).
3. **Defensa en profundidad:** más de un control protege cada operación sensible.
4. **Fallo seguro:** ante un error, la herramienta se detiene sin acciones parciales y sin revelar detalles internos.
5. **Separación de funciones:** quien desarrolla no aprueba ni despliega.

Requisitos mínimos para R-03: contraseñas de al menos 12 caracteres almacenadas con función de derivación adaptativa;
bloqueo tras 3 intentos fallidos; sesión de 30 minutos; cookies `HttpOnly` y `SameSite`; token anti-CSRF en formularios;
cabeceras `Content-Security-Policy`, `X-Content-Type-Options`, `X-Frame-Options` y `Referrer-Policy`; modo depuración solo en desarrollo.

## 9. Gestión de cambios (A.8.32)

1. Todo cambio nace de un **issue** que explica el motivo.
2. Se trabaja en una rama y se abre un **PR** que referencia el issue (`Closes #n`).
3. El PR requiere **aprobación de `padre-aprobador`** y el **pipeline en verde**; la rama `main` está protegida, incluso para administradores.
4. Se actualiza `CHANGELOG.md` con la versión.
5. Para producción se crea la etiqueta `vX.Y.Z`. La reversión se hace con `git revert` y un nuevo PR.

## 10. Dependencias (A.8.8)

1. Todas las dependencias, incluidas las transitivas, se fijan con `==` en `requirements.txt`.
2. En cada mantenimiento trimestral, el líder tecnológico ejecuta manualmente `pip-audit` y registra el resultado en
   `gobierno/REGISTRO-REVISIONES.md`.
3. Plazos de corrección: CVSS ≥ 7,0, antes de integrar o en 7 días; CVSS 4,0–6,9, 30 días; CVSS < 4,0, próximo mantenimiento.

## 11. Hallazgos e incidentes

- Cada hallazgo confirmado de una herramienta se registra como issue con responsable y plazo (sección 10.3).
- Cada bloqueo de cuenta en R-03 debe tener una **acción registrada** en el panel de eventos (verificación del usuario por
  otro canal y desbloqueo), con responsable y fecha.
- Un problema de seguridad se avisa al líder tecnológico y al dueño de la información por un canal directo.

## 12. Criterios de aceptación por herramienta

| Herramienta | Criterio para pasar a producción |
|---|---|
| R-01 | Pruebas de REQ-01-01 a REQ-01-07 en verde; ejecución por defecto sin borrado |
| R-02 | Credencial fuera del código; pruebas en verde |
| R-03 | Pruebas de REQ-03-01 a REQ-03-10 en verde; sin alertas altas de ZAP confirmadas |

## 13. Revisión de esta regla

Se revisa una vez al año o después de un incidente. Cada cambio genera una nueva versión aprobada por el dueño de la información.
