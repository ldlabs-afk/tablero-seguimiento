# Accesos autorizados – laboratorio de desarrollo (LDS-LAB 2 y 7)

## Repositorios en GitHub (R-01, R-02, R-03)

| Cuenta GitHub | Rol en el laboratorio | Permiso autorizado | Verificación en dos pasos |
|---|---|---|---|
| `ldlabs-afk` | hijo-dev – desarrollador y líder tecnológico | Propietario (administrador) | Obligatoria |
| `Xhirukai` | padre-aprobador – dueño de la información | Escritura (write); aprueba PR; sin administración | Obligatoria |

- Visibilidad: **públicos**. Decisión del laboratorio: solo contienen código y datos ficticios, y GitHub gratuito permite
  proteger ramas únicamente en repositorios públicos.
- Llaves de despliegue (deploy keys): **ninguna autorizada**.
- Tokens: solo los de sesión de GitHub CLI de cada cuenta, en el usuario Linux correspondiente.

## Usuarios del equipo de laboratorio (Ubuntu en WSL2)

| Usuario Linux | Función | Privilegios autorizados |
|---|---|---|
| `adminlab` | Administración del equipo, despliegue y auditoría | sudo |
| `hijo-dev` | Desarrollo y entorno de prueba | **Sin sudo**; sin acceso a `/home/padre` ni a producción |
| `padre` | Ejecución en producción | Sin sudo; dueño de `/home/padre/Adjuntos_Copropiedad` |
