# 02 - Aplicación de SOLID y Clean Code

| Principio | Antes (estado-inicial) | Después (estado-refactorizado) | Archivo |
|---|---|---|---|
| **SRP** – Responsabilidad única | `main.py` hacía HTTP, validación, reglas, SQL y reportes | Cada capa tiene un motivo de cambio: routers (HTTP), schemas (contratos), services (casos de uso), repositories (persistencia), domain (reglas) | `backend/app/*` |
| **OCP** – Abierto/cerrado | `if/elif` para prioridad y transiciones | Tablas `PRIORIDAD_BASE_POR_TIPO` y `_TRANSICIONES_PERMITIDAS`: agregar un tipo/estado = agregar una entrada | `domain/reglas.py`, `domain/enums.py` |
| **LSP** – Sustitución de Liskov | No aplicaba (sin abstracciones) | Cualquier implementación de `SolicitudRepository` (SQL o en memoria) es intercambiable; las pruebas lo demuestran | `repositories`, `tests/test_servicios.py` |
| **ISP** – Segregación de interfaces | — | Dos interfaces chicas (`SolicitudRepository`, `CatalogoRepository`) en lugar de un "DAO" gigante; `ReporteService` sólo depende de la que usa | `repositories/__init__.py` |
| **DIP** – Inversión de dependencias | Endpoints dependen de `sqlite3` y de una conexión global | Servicios dependen de `Protocol`; la implementación concreta se inyecta con `Depends` | `dependencies.py` |

## Clean Code

| Criterio | Mejora aplicada |
|---|---|
| Nombres | `d → datos`, `p → prioridad`, `x → nueva_id`, `data2 → resumen`, `f1..f4 → filtros.estado/tipo/...` |
| Funciones pequeñas | Largo promedio de función 17,1 → 4,1 líneas; la más larga 43 → 17 |
| Manejo de errores | Jerarquía `ErrorDeDominio` → traducción HTTP centralizada; sin `except:` vacío |
| Cohesión | La entidad `Solicitud` conoce sus propias reglas (`cambiar_estado`, `asignar_responsable`) |
| Acoplamiento | El frontend sólo habla con `api/solicitudesApi.js`; el backend sólo con repositorios |
| Límites entre componentes | DTO de entrada (`SolicitudCreate`) y de salida (`SolicitudResponse`) separados, como pide el apunte CRUD Persistente |
| Comentarios | Se eliminó código comentado; los docstrings explican el *por qué* |

## Métricas antes / después (backend)

| Métrica | Inicial | Refactorizada |
|---|---|---|
| Archivos Python | 1 | 13 (7 paquetes) |
| Función más larga | `crear()` 43 líneas | `buscar()` 17 líneas |
| Complejidad ciclomática máx. (aprox.) | 18 | 9 |
| Largo promedio de función | 17,1 | 4,1 |
| Copias del SELECT / dict de respuesta | 5 / 5 | 0 (un único `desde_entidad`) |
| Consultas SQL concatenadas | 4 | 0 |
| Pruebas automatizadas | 29 | 65 (cobertura 99%) |
| Frontend: componentes / URL hardcodeada | 1 / 7 | 5 + hook + módulo API / 0 |
