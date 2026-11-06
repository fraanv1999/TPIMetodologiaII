# 01 - Diagnóstico de calidad, deuda técnica y code smells

Versión analizada: tag `estado-inicial` (`backend/main.py`, 200 líneas; `frontend/src/App.jsx`, 1 componente).

## Calidad externa (lo que ve el usuario)

| Aspecto | Observación |
|---|---|
| Funcionalidad | Las 6 operaciones funcionan: registrar, listar/filtrar, ver detalle, asignar responsable, cambiar estado, reporte. |
| Reglas de negocio | Prioridad automática por tipo + urgencia; ciclo de estados controlado. |
| Usabilidad | Una pantalla con alta, filtros, tabla y tarjetas de resumen. |
| Evidencia | 29/29 pruebas de caracterización pasan (`evidencias/pytest_estado_inicial.txt`). |

## Calidad interna (lo que ve el equipo técnico)

Todo el backend vive en un único archivo, con SQL, validaciones, reglas de negocio y armado de
respuestas mezclados. Funciona, pero cada cambio es caro y riesgoso.

## Inventario de problemas (14)

Escala: Impacto/Riesgo = Bajo · Medio · Alto · Crítico. Prioridad 1 = corregir primero.

| ID | Smell / debilidad | Ubicación | Evidencia | Impacto | Riesgo de mantenimiento | Prioridad |
|---|---|---|---|---|---|---|
| CS-01 | SQL Injection por concatenación de strings | `main.py` L96-106 `listar()` | `estado="x' OR 1=1 --"` devuelve todas las filas (`evidencias/inyeccion_sql_estado_inicial.txt`) | Crítico | Fuga de datos, consultas arbitrarias | 1 |
| CS-02 | Manejo de errores: `except:` vacío | `main.py` L107-114 | SQL mal formado responde `[]` con 200, el error se oculta | Alto | Fallas silenciosas, imposible diagnosticar | 1 |
| CS-03 | God Class / módulo dios | `main.py` completo | Endpoints + SQL + validación + reglas + reporte en 1 archivo | Alto | Todo cambio toca el mismo archivo; sin pruebas unitarias posibles | 1 |
| CS-04 | Duplicated Code | SELECT con JOIN en L90, 97, 119, 149, 169; dict de respuesta en L92, 111, 123, 151, 171 | 5 copias idénticas | Alto | Agregar un campo exige 10 ediciones coordinadas | 1 |
| CS-05 | Dependencia de implementación concreta / estado global (viola DIP) | `main.py` L11-13 `conn` y `c` globales | Endpoints usan `sqlite3` directo | Alto | No se puede sustituir persistencia ni aislar en tests | 2 |
| CS-06 | Long Method | `crear()` L57-92 (36 líneas) | Valida, calcula prioridad, persiste y arma respuesta | Alto | Difícil de leer, probar y modificar | 2 |
| CS-07 | Switch statements (viola OCP) | Prioridad L72-87; transiciones L136-145 | Cadena `if/elif` por tipo y por estado | Medio | Nuevo tipo/estado = modificar código existente | 2 |
| CS-08 | Primitive Obsession / magic strings | L64, L134, L187 y `App.jsx` | Estados, tipos y prioridades como strings repetidos | Medio | Un typo (`"PENDENTE"`) no lo detecta nadie | 2 |
| CS-09 | Long Parameter List | `guardar()` L47 (9 parámetros) | Orden posicional frágil | Medio | Intercambiar 2 argumentos no da error | 2 |
| CS-10 | Falta de contrato de entrada/salida (DTO) | `crear()`, `cambiar_estado()`, `asignar()` reciben `Request` crudo | Validación manual; Swagger no documenta el body | Medio | Validaciones inconsistentes entre endpoints | 2 |
| CS-11 | Nombres poco expresivos | `d`, `c`, `e`, `p`, `x`, `r`, `data2`, `en/el/rn`; `f1..f4` en front | — | Medio | Mayor costo de lectura | 3 |
| CS-12 | Componente dios en frontend | `App.jsx` (211 líneas, 15 `useState`) | UI, estado, red y reglas en un componente | Medio | Cambios de UI rompen lógica de red | 3 |
| CS-13 | URL base hardcodeada y fetch duplicado | `App.jsx` 7 apariciones de `http://127.0.0.1:8000` | — | Medio | Cambiar de entorno exige editar 7 lugares | 3 |
| CS-14 | Código muerto / comentado | `main.py` L195-200 `borrar()` | Además usa SQL concatenado | Bajo | Ruido, confusión | 4 |

## Priorización (impacto vs. esfuerzo)

1. Seguridad y errores (CS-01, CS-02): bajo esfuerzo, impacto crítico.
2. Estructura (CS-03, CS-04, CS-05, CS-06): resuelven la mayoría del costo de cambio.
3. Diseño de dominio (CS-07, CS-08, CS-09, CS-10).
4. Legibilidad y frontend (CS-11 a CS-14).
