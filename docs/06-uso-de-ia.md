# 06 - Declaración de uso de inteligencia artificial

| Herramienta | Finalidad | Grado de intervención |
|---|---|---|
| NotebookLM | Generar la estructura del trabajo, el prototipo base, el diagnóstico inicial, propuestas de refactoring, pruebas, diagramas y borrador del informe | Alto en la generación inicial. **El equipo debe revisar, comprender, ajustar y poder defender cada decisión.** |

## Forma de trabajo: Spec-Driven Development (SDD)

Todas las consultas a la IA siguieron *Spec-Driven Development*: primero se escribe la
especificación (qué se quiere y cómo se comprueba), después el plan técnico y recién al final el
código. Nunca se pidió código sin una especificación y un plan revisados por el equipo.

| Fase | Qué se le pide a la IA | Qué controla el equipo |
|---|---|---|
| Constitución | Principios fijos para todo el proyecto (una sola vez, al inicio) | Que cada etapa los respete |
| Especificar | Requisitos y criterios de aceptación verificables, sin decisiones técnicas | Que la spec refleje la consigna y que cada criterio se pueda comprobar |
| Planificar | Diseño técnico y lista ordenada de tareas que cumplen la spec | Que el plan no cambie comportamiento que la spec no pide cambiar |
| Implementar y verificar | Ejecutar las tareas y comprobar cada criterio de aceptación | Correr las pruebas y revisar el diff antes de cada commit |

## Registro de prompts

### Tag `estado-inicial`

| # | Fecha | Fase SDD | Prompt (resumen) | Uso del resultado |
|---|---|---|---|---|
| 1 | 05/11/2026 | Constitución | "Antes de escribir código fijemos los principios del proyecto: Sistema de Gestión de Solicitudes Académicas (SGSA) en Python/FastAPI y React, alojado en GitHub con un tag por etapa; cada etapa empieza con una spec con criterios de aceptación, sigue con un plan y termina con el código; los refactorings no cambian el comportamiento observable y se validan con pytest; commits chicos, uno por cambio; al final, informe y presentación en PowerPoint" | Principios aplicados en todas las etapas. Base de la hoja de ruta del TPI, del informe y de la presentación |
| 2 | 05/11/2026 | Especificar | "Especificá la versión inicial del SGSA sin hablar de tecnología: actores, las 6 operaciones (registrar solicitud, listar con filtros, ver detalle, asignar responsable, cambiar estado y reporte), la regla de prioridad por tipo y urgencia, el ciclo de estados permitido y los criterios de aceptación de cada operación. Requisito no funcional a propósito: código básico, sin capas, sin patrones y con nomenclatura básica, porque es el punto de partida que después se analiza" | Spec de la versión inicial. El equipo la revisó contra la consigna |
| 3 | 05/11/2026 | Planificar | "Con esa spec armá el plan técnico y la lista de tareas: backend en un solo `main.py` con FastAPI y sqlite, sin capas; frontend en un solo `App.jsx`; un endpoint por operación y la estructura del repositorio" | Plan y tareas del monolito |
| 4 | 05/11/2026 | Implementar y verificar | "Implementá las tareas del plan y, para cada criterio de aceptación de la spec, decime cómo comprobarlo a mano" | Versión inicial (monolito). El equipo la levantó y comprobó las 6 operaciones contra los criterios antes de commitear |

### Tag `etapa-diagnostico`

| # | Fecha | Fase SDD | Prompt (resumen) | Uso del resultado |
|---|---|---|---|---|
| 5 | 05/11/2026 | Especificar | "Especificá la etapa de diagnóstico: (a) pruebas de caracterización que fijen el comportamiento actual de todos los endpoints, la prioridad por tipo y urgencia y el ciclo de estados; (b) un inventario de al menos 8 code smells con ubicación, evidencia, impacto, riesgo de mantenimiento y prioridad. Criterio de aceptación: las pruebas pasan todas sobre la versión inicial sin tocar el código" | Spec del diagnóstico, alineada con el mínimo de 8 problemas que pide la consigna |
| 6 | 05/11/2026 | Planificar | "Planificá cómo cumplir cada criterio: qué casos de pytest con `TestClient` van en `test_caracterizacion_api.py`, con qué criterios se clasifica cada smell y en qué orden se hace todo" | Plan de pruebas y plantilla de la tabla de code smells |
| 7 | 05/11/2026 | Implementar y verificar | "Ejecutá el plan: escribí las pruebas de caracterización, analizá `main.py` y `App.jsx` para armar el inventario y verificá cada criterio de la spec" | `tests/test_caracterizacion_api.py` (29 pruebas, 29/29 sobre la versión inicial) y base de `01-diagnostico.md` (14 problemas). El equipo revisó los números de línea y reprodujo la inyección SQL |

### Tag `etapa-refactoring`

| # | Fecha | Fase SDD | Prompt (resumen) | Uso del resultado |
|---|---|---|---|---|
| 8 | 05/11/2026 | Especificar | "Especificá R0: eliminar la inyección SQL (CS-01), el `except:` vacío (CS-02) y el código muerto (CS-14). Criterios de aceptación: un filtro con payload de inyección no altera la consulta, los errores no se silencian y las 29 pruebas de caracterización pasan sin modificarlas. Tiene que ser un commit chico y aparte" | Spec de R0 |
| 9 | 05/11/2026 | Planificar | "Planificá R0 como lista de tareas: qué consultas pasan a parametrizadas, qué excepción concreta reemplaza al `except:` vacío y qué líneas se eliminan" | Plan de R0 |
| 10 | 05/11/2026 | Implementar y verificar | "Implementá las tareas de R0 y verificá cada criterio de la spec" | R0: consultas parametrizadas, sin `except:` vacío ni código muerto. Caracterización 29/29 |
| 11 | 05/11/2026 | Especificar | "Especificá R1 sobre el Long Method `crear()` (CS-06) y el SELECT y el diccionario de respuesta duplicados (CS-04): funciones cortas, sin código repetido y con nombres que expliquen la intención. Criterio de aceptación: la API responde igual y las pruebas pasan 29/29 sin modificarlas" | Spec de R1 |
| 12 | 05/11/2026 | Planificar | "Planificá R1 con Extract Method y Rename Variable: qué funciones se extraen, con qué nombres y en qué orden, para que las pruebas sigan en verde después de cada paso" | Plan de R1 |
| 13 | 05/11/2026 | Implementar y verificar | "Implementá R1 tarea por tarea, corriendo las pruebas de caracterización después de cada una" | R1: `registrar_solicitud()` pasa a 7 líneas. 29/29 sin modificar las pruebas |
| 14 | 05/11/2026 | Especificar | "Especificá la separación en capas (R2-R5): qué responsabilidad tiene cada capa, estado y prioridad como tipos y no como strings sueltos, contratos de entrada y salida explícitos y servicios que no dependan de sqlite. Criterios de aceptación: cada capa cumple SRP y DIP, y la API se comporta igual (29/29)" | Spec de R2-R5 |
| 15 | 05/11/2026 | Planificar | "Proponé el plan técnico y las tareas: carpetas de `app/` (routers, servicios, repositorios y dominio), enums para estado y prioridad, DTOs con Pydantic y el repositorio inyectado con `Depends`" | Plan de R2-R5. El equipo lo contrastó con SOLID antes de implementar |
| 16 | 05/11/2026 | Implementar y verificar | "Implementá el plan de R2-R5 y verificá cada criterio de la spec, incluido el chequeo de SOLID capa por capa" | R2-R5 aplicados en un commit; el equipo revisó cada capa contra SOLID. 29/29 |
| 17 | 05/11/2026 | Especificar | "Especificá R6 para el frontend: separar `App.jsx` por responsabilidad (presentación, estado y acceso a la API). Criterios de aceptación: la pantalla se ve y funciona igual y el build no tiene errores" | Spec de R6 |
| 18 | 05/11/2026 | Planificar | "Planificá qué componentes salen de `App.jsx`, qué estado pasa a un hook y qué `fetch` pasan a un módulo de API, como lista de tareas" | Plan de R6 |
| 19 | 05/11/2026 | Implementar y verificar | "Implementá las tareas de R6 y verificá los criterios de la spec" | R6: componentes + hook `useSolicitudes` + `api/solicitudesApi.js`. Verificado con `npm run build` y prueba manual de la pantalla |

### Tag `etapa-pruebas`

| # | Fecha | Fase SDD | Prompt (resumen) | Uso del resultado |
|---|---|---|---|---|
| 20 | 05/11/2026 | Especificar | "Especificá la estrategia de pruebas: unitarias de dominio, de servicios aislados de la base y de regresión de seguridad para la inyección SQL. Criterios de aceptación: todas pasan sobre el código refactorizado, la cobertura de `app/` es de al menos 90% y las pruebas de seguridad fallan sobre la versión inicial" | Spec de la etapa de pruebas |
| 21 | 05/11/2026 | Planificar | "Planificá los casos: qué reglas de dominio cubrir, repositorios en memoria como dobles de prueba para los servicios, qué payloads de inyección usar y cómo medir y guardar la cobertura" | Plan de pruebas por nivel |
| 22 | 05/11/2026 | Implementar y verificar | "Implementá las pruebas del plan, medí la cobertura, corré las de seguridad sobre la versión inicial y guardá las salidas como evidencia" | 65 pruebas, 99% de cobertura (`pytest --cov=app`); las de seguridad dan 1/5 sobre la versión inicial. Evidencias en `docs/evidencias/` |
