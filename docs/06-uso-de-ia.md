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
