# SoA-LAB – Complemento de la declaración de aplicabilidad para el laboratorio de desarrollo

Versión 1.0 · Aprobado por: Padre – Jefe de hogar · Complementa la declaración de aplicabilidad de la matriz de riesgos del hogar,
donde los controles de desarrollo no se evaluaron porque el hogar no desarrolla software. **Aplica solo al escenario de laboratorio.**

| Control | Nombre | Aplicabilidad | Justificación | Implementación |
|---|---|---|---|---|
| A.8.4 | Acceso al código fuente | Aplica | El código de R-01 actúa sobre información reservada; la escritura se limita a cuentas autorizadas | Repositorios con 2 cuentas; `gobierno/ACCESOS-AUTORIZADOS.md` |
| A.8.25 | Ciclo de vida de desarrollo seguro | Aplica | El hogar construye herramientas para ejecutar tratamientos de riesgo | LDS-LAB |
| A.8.26 | Requisitos de seguridad de las aplicaciones | Aplica | Cada herramienta tiene requisitos derivados de la matriz de riesgos | `REQUISITOS.md` de R-01 y R-03 |
| A.8.27 | Arquitectura de sistemas seguros y principios de ingeniería | Aplica | Los principios limitan el daño de una falla de R-01 o R-03 | LDS-LAB 8; `DISENO.md` |
| A.8.28 | Codificación segura | Aplica | Las fallas de código podrían borrar o exponer información | LDS-LAB 4 y 8; Semgrep |
| A.8.29 | Pruebas de seguridad en el desarrollo y aceptación | Aplica | Las pruebas deben detener un cambio inseguro antes de producción | Pipeline (LDS-LAB 5) |
| A.8.30 | Desarrollo externalizado | **No aplica** | No se contrata desarrollo con terceros; todo lo desarrolla el líder tecnológico | — |
| A.8.31 | Separación de entornos de desarrollo, prueba y producción | Aplica | R-01 borra archivos; probar sobre producción pondría en riesgo la información del empleador | LDS-LAB 7 |
| A.8.32 | Gestión del cambio | Aplica | Los cambios a R-01 afectan la información del dueño | LDS-LAB 9; protección de rama |
| A.8.33 | Información de prueba | Aplica | R-01 se prueba con archivos que imitan adjuntos con datos personales | LDS-LAB 6 |
| A.8.8 | Gestión de vulnerabilidades técnicas | Aplica | Las herramientas usan librerías de terceros | LDS-LAB 10; pip-audit |
| A.5.17 | Información de autenticación | Aplica | R-02 usa la clave de administración del router | LDS-LAB 4 |
| A.8.15 | Registros | Aplica | R-01 y R-03 registran operaciones y eventos de seguridad | Bitácoras de R-01 y R-03 |
