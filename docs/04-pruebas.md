# 04 - Pruebas y verificación

## Estrategia

1. **Caracterización (red de seguridad):** antes de tocar el código se escribieron 29 pruebas de caja
   negra sobre la API de la versión inicial (`tests/test_caracterizacion_api.py`).
2. **Refactor en pasos chicos:** después de cada commit de refactoring se ejecutaron las mismas
   pruebas, sin modificarlas.
3. **Pruebas nuevas** que la versión inicial no permitía: unitarias de dominio y servicios con
   repositorios en memoria, y regresión de seguridad.

## Casos de prueba

| ID | Caso | Entrada | Resultado esperado |
|---|---|---|---|
| CP-01 | Listar estudiantes | GET /api/estudiantes | 200, ≥3 registros con 5 campos |
| CP-02 | Listar responsables | GET /api/responsables | 200, áreas Alumnado/Coordinación/Bedelia |
| CP-03 | Registrar solicitud válida | POST certificado | 201, PENDIENTE, BAJA, sin responsable |
| CP-04 | Prioridad por tipo y urgencia (9 combinaciones) | POST con tipo/urgente | BAJA/MEDIA/ALTA según tabla |
| CP-05 | Datos inválidos (6 variantes) | tipo, asunto, descripción, estudiante | 400 / 404 |
| CP-06 | Obtener por id | GET /api/solicitudes/{id} | 200 igual al creado; 404 si no existe |
| CP-07 | Filtrar por estado, tipo, prioridad y texto | GET con query | Sólo coincidencias; orden descendente |
| CP-08 | Asignar responsable | PATCH /responsable | 200; 404 responsable o solicitud inexistente |
| CP-09 | Flujo completo de estados | PATCH /estado | 409 sin responsable; EN_PROCESO → RESUELTA; 409 en estado final |
| CP-10 | Transiciones inválidas desde PENDIENTE | RESUELTA / PENDIENTE / CUALQUIERA | 409 / 409 / 400 |
| CP-11 | Reporte resumen | GET /api/reportes/resumen | Contadores y % se actualizan |
| CP-12 | Inyección SQL en filtros (4 variantes) | `estado="x' OR 1=1 --"` | 200 y lista vacía |

## Resultados

| Versión | Caracterización | Seguridad | Unitarias | Total |
|---|---|---|---|---|
| `estado-inicial` | 29/29 ✅ | 1/5 ❌ (4 fallan: inyección) | no aplicable (sin capas) | — |
| Cada commit de refactoring | 29/29 ✅ | — | — | — |
| `estado-refactorizado` | 29/29 ✅ | 5/5 ✅ | 31/31 ✅ | **65/65, cobertura 99%** |

Evidencias: `evidencias/pytest_estado_inicial.txt`, `evidencias/pytest_seguridad_sobre_estado_inicial.txt`,
`evidencias/pytest_estado_refactorizado.txt`, `evidencias/inyeccion_sql_estado_inicial.txt`, `evidencias/capturas/`.

## Cómo reproducir

```bash
cd backend
pip install -r requirements.txt
pytest -v --cov=app
# comparar con la version inicial
git checkout estado-inicial -- backend/main.py   # corre las pruebas de caracterizacion sobre la v1
git checkout main -- backend/main.py             # volver a la version refactorizada
```
