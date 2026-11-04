# Requisitos de seguridad – R-03 tablero-seguimiento

Versión 1.0 · Origen: LDS-LAB 8, OWASP ASVS 5.0 nivel 1 · Aprobados por: Padre – Jefe de hogar (dueño de la información).

| ID | Requisito | Origen | Criterio de verificación | Prueba asociada |
|---|---|---|---|---|
| REQ-03-01 | Autenticación con contraseña almacenada con función adaptativa (scrypt) y mensaje de error genérico | ASVS V6; A.8.5 | Usuario inexistente y clave errada dan la misma respuesta | `test_req03_01_*` |
| REQ-03-02 | Bloqueo de la cuenta al tercer intento fallido, incluso con la clave correcta después | ASVS V6; A.8.5 | Códigos 401, 401, 423 y luego 423 | `test_req03_02_bloqueo_al_tercer_intento` |
| REQ-03-03 | Cada bloqueo se registra sin la contraseña y exige una acción documentada con responsable | ASVS V16; A.8.15; LDS-LAB 11 | Evento en bitácora sin la clave; acción registrada | `test_req03_03_*` |
| REQ-03-04 | Consultas a la base de datos parametrizadas | ASVS V1; CWE-89 | Sin concatenación de SQL (Semgrep y revisión) | Semgrep / LC-08 |
| REQ-03-05 | Token anti-CSRF en todo formulario | ASVS V3 | POST sin token se rechaza (400) | `test_req03_05_post_sin_token_csrf_rechazado` |
| REQ-03-06 | Cabeceras de seguridad (CSP, nosniff, X-Frame-Options, Referrer-Policy) | ASVS V3, V13 | Cabeceras presentes en cada respuesta | `test_req03_06_cabeceras_de_seguridad` |
| REQ-03-07 | Cookie de sesión HttpOnly, SameSite y con expiración (30 min) | ASVS V7 | Atributos presentes en Set-Cookie | `test_req03_07_cookie_de_sesion_protegida` |
| REQ-03-08 | Solo los roles dueño y líder ven y gestionan eventos de seguridad | ASVS V8; A.5.15 | El rol consulta recibe 403 | `test_req03_08_rol_consulta_no_ve_eventos` |
| REQ-03-09 | En producción la clave secreta es obligatoria y no está en el código | ASVS V13; LDS-LAB 4 | Sin TABLERO_SECRET_KEY la aplicación no arranca | `test_req03_09_produccion_exige_clave_secreta` |
| REQ-03-10 | Modo depuración solo en desarrollo | ASVS V13; A.8.31 | DEBUG falso en prueba y producción | `test_req03_10_depuracion_solo_en_desarrollo` |
