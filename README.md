# SGSA – Sistema de Gestión de Solicitudes Académicas

Trabajo Práctico Integrador – **Metodología de Sistemas II** (TUP a distancia, UTN).

## Integrantes

Vazquez Franco

## Descripción

Sistema simple para registrar solicitudes de estudiantes, clasificarlas por tipo, prioridad y estado,
asignar responsables, consultarlas y obtener un reporte. El foco del trabajo **no** es la cantidad de
funcionalidades sino la mejora de la **calidad interna** mediante diagnóstico, refactoring seguro,
pruebas y code review.

## Funcionalidades

- Registrar solicitud (prioridad automática según tipo + urgencia)
- Buscar / filtrar por estado, tipo, prioridad y texto (asunto, nombre o legajo)
- Ver detalle de una solicitud
- Asignar responsable
- Cambiar estado: `PENDIENTE → EN_PROCESO → RESUELTA`, o `RECHAZADA`
- Reporte resumen (totales por estado, tipo, prioridad, sin responsable, % resueltas)

## Tecnologías

| Capa | Tecnología |
|---|---|
| Backend | Python 3.11+, FastAPI, SQLModel, SQLite |
| Frontend | React 18 + Vite |
| Pruebas | pytest, pytest-cov, TestClient de FastAPI |

## Instalación y uso

```bash
# Backend (http://127.0.0.1:8000, documentación en /docs)
cd backend
python -m venv .venv && .venv\Scripts\activate      # Linux/Mac: source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend (http://localhost:5173) – en otra terminal
cd frontend
npm install
npm run dev

# Pruebas
cd backend
pytest -v --cov=app
```

Variables opcionales: `SGSA_DB` (ruta de la base, por defecto `sgsa.db`),
`SGSA_CORS_ORIGINS` (orígenes permitidos separados por coma), `VITE_API_URL` (URL del backend si no se usa el proxy de Vite).

> La versión inicial usaba `solicitudes.db` con otro esquema; la refactorizada crea `sgsa.db` (ver CR-03).

## Estructura

```
backend/
  main.py                 punto de entrada (uvicorn main:app)
  app/
    routers/              endpoints HTTP (Request → Response Model)
    schemas/              DTOs de entrada y salida (validación)
    services/             casos de uso (SolicitudService, ReporteService)
    repositories/         acceso a datos (Protocol + SQLModel)
    models/               tablas y reglas de la entidad Solicitud
    domain/               enums, reglas puras y errores de dominio
  tests/                  caracterización, dominio, servicios, seguridad
frontend/src/
  api/ hooks/ components/ constants/
docs/                     diagnóstico, SOLID, refactorings, pruebas, code review, IA, diagramas, evidencias
```

## Versiones (tags)

| Tag | Contenido |
|---|---|
| `estado-inicial` | Sistema base con problemas de diseño (1 archivo backend, 1 componente frontend) |
| `etapa-diagnostico` | Pruebas de caracterización + `docs/01-diagnostico.md` |
| `etapa-refactoring` | Refactorings R0–R6 aplicados |
| `etapa-pruebas` | Pruebas unitarias y de seguridad (65 pruebas, 99% cobertura) |
| `etapa-docs` | Documentación, checklist y code review |
| `estado-refactorizado` | Estado final |

Ver la versión inicial: `git checkout estado-inicial` (volver con `git checkout main`).

## Documentación

1. [Diagnóstico y code smells](docs/01-diagnostico.md)
2. [SOLID y Clean Code](docs/02-solid-clean-code.md)
3. [Refactorings](docs/03-refactorings.md)
4. [Pruebas y verificación](docs/04-pruebas.md)
5. [Code review y checklist](docs/05-code-review.md)
6. [Uso de IA](docs/06-uso-de-ia.md)