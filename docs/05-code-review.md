# 05 - Code review profesional

## Checklist técnico

| # | Criterio | Resultado | Observación |
|---|---|---|---|
| 1 | El código compila / arranca sin errores | ✅ Cumple | `uvicorn main:app` y `npm run build` OK |
| 2 | Todas las pruebas pasan | ✅ Cumple | 65/65 |
| 3 | El comportamiento externo se conserva | ✅ Cumple | 29 pruebas de caracterización sin cambios |
| 4 | Sin consultas SQL armadas con strings | ✅ Cumple | ORM con parámetros |
| 5 | Sin `except` vacíos ni errores silenciados | ✅ Cumple | Errores de dominio + handler central |
| 6 | Cada módulo tiene una única responsabilidad (SRP) | ✅ Cumple | |
| 7 | Dependencias hacia abstracciones (DIP) | ✅ Cumple | `Protocol` + `Depends` |
| 8 | Nombres expresivos, sin abreviaturas crípticas | ✅ Cumple | |
| 9 | Funciones ≤ 20 líneas | ✅ Cumple | Máx. 17 |
| 10 | Sin código duplicado relevante | ✅ Cumple | |
| 11 | Sin strings mágicos de dominio | ⚠️ Parcial | Ver CR-06 |
| 12 | Entrada validada con DTO y salida con Response Model | ✅ Cumple | |
| 13 | Configuración segura (CORS, secretos) | ❌ → ✅ | CR-04 corregido en commit `fix(code-review)` |
| 14 | Datos personales sintéticos | ✅ Cumple | `@example.com` |
| 15 | README y documentación actualizados | ✅ Cumple | |
| 16 | Commits pequeños y con mensaje claro | ✅ Cumple | Un commit por refactoring |

## Hallazgos y feedback

| ID | Severidad | Hallazgo | Feedback (objetivo, sobre el código) | Acción | Estado |
|---|---|---|---|---|---|
| CR-01 | Menor | `CambioEstadoRequest.estado` es `str` y no `Estado` | Sugiero documentar por qué: si fuera enum, Pydantic respondería 400 antes de verificar que la solicitud exista y cambiaría el orden 404→400 de la v1 | Comentario agregado en el schema | ✅ Aceptado |
| CR-02 | Menor | En POST, un tipo inválido con estudiante inexistente ahora responde 400 (antes 404) | Es consecuencia de validar formato primero ("rechazo temprano"). No rompe ningún caso de uso real | Documentado como cambio consciente | ✅ Aceptado |
| CR-03 | Media | La base por defecto pasa a `sgsa.db` con otro esquema | Evitar que la v2 abra una base de la v1 con columnas distintas | Documentado en README; migración fuera de alcance | ✅ Aceptado |
| CR-04 | Mayor | `CORSMiddleware(allow_origins=["*"])` | Con el proxy de Vite ya no hace falta abrir a cualquier origen | Lista configurable `SGSA_CORS_ORIGINS` | ✅ Corregido (commit `fix(code-review)`) |
| CR-05 | Info | Warning de deprecación de `starlette.testclient` | Es del tooling, no del código | Ninguna | ✅ Aceptado |
| CR-06 | Menor | El modelo persiste `tipo/estado/prioridad` como `str` | La conversión a enum ocurre en `estado_actual`. Aceptable; a futuro usar columnas `Enum` | Mejora futura | 🕒 Pendiente |
| CR-07 | Menor | El listado no pagina | Con volumen real puede crecer | Mejora futura | 🕒 Pendiente |
| CR-08 | Info | El frontend no tiene pruebas automatizadas | Agregar Vitest + Testing Library | Mejora futura | 🕒 Pendiente |

## Criterios de aceptación técnica

- [x] 100% de pruebas de caracterización en verde sin modificarlas.
- [x] Ningún hallazgo **Mayor** abierto.
- [x] Cobertura ≥ 80% en `backend/app` (obtenida: 99%).
- [x] Los 8 code smells prioritarios (CS-01 a CS-08) resueltos.
- [x] Al menos 4 refactorings documentados con antes/después.

**Dictamen:** Aprobado con observaciones menores (CR-06, CR-07, CR-08 quedan como mejoras futuras).
