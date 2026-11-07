# 03 - Refactorings aplicados

Cada refactoring es un commit propio. Después de cada uno se ejecutaron las 29 pruebas de
caracterización **sin modificarlas** (ver `04-pruebas.md`). El historial se puede ver con `git log --oneline`.

| # | Técnica (Fowler) | Commit (mensaje) | Smells que resuelve |
|---|---|---|---|
| R0 | Substitute Algorithm (consulta parametrizada) + Remove Dead Code | `fix(seguridad): R0` | CS-01, CS-02, CS-14 |
| R1 | **Extract Method** + Rename Variable | `refactor(R1)` | CS-04, CS-06, CS-11 |
| R2 | **Move Method** / reubicación de responsabilidad | `refactor(R2-R5)` | CS-03, CS-06 |
| R3 | **Introduce Parameter Object** | `refactor(R2-R5)` | CS-09, CS-10 |
| R4 | Replace Conditional with Table + Replace Magic String with Enum | `refactor(R2-R5)` | CS-07, CS-08 |
| R5 | Extract Class (Repository) + Dependency Injection | `refactor(R2-R5)` | CS-05 |
| R6 | Extract Component / Extract Module (frontend) | `refactor(R6)` | CS-12, CS-13 |

## R1 – Extract Method

**Antes** (`estado-inicial`, `crear()`, 36 líneas): la misma función validaba, calculaba la
prioridad con `if/elif`, insertaba y armaba un diccionario de 13 claves (copiado 5 veces en el archivo).

```python
p = ""
if d["tipo"] == "certificado":
    p = "BAJA"
elif d["tipo"] == "equivalencia":
    p = "MEDIA"
...
return {"id": r["id"], "estudiante_id": r["estudiante_id"], "estudiante": r["en"], ...}
```

**Después** (commit `refactor(R1)`): `registrar_solicitud()` queda en 7 líneas que se leen como el caso de uso.

```python
datos = await request.json()
validar_nueva_solicitud(datos)
prioridad = calcular_prioridad(datos["tipo"], datos.get("urgente") is True)
...
return buscar_solicitud_completa(nueva_id)
```

## R2 – Move Method

Las reglas de transición estaban en el endpoint `cambiar_estado()`. Se movieron a la entidad,
que es quien tiene los datos (evita *Feature Envy*):

```python
class Solicitud(SQLModel, table=True):
    def cambiar_estado(self, nuevo: Estado, momento: datetime) -> None:
        actual = self.estado_actual
        if not actual.puede_pasar_a(nuevo):
            raise ReglaDeNegocioViolada(f"No se puede pasar de {actual.value} a {nuevo.value}")
        if nuevo is Estado.EN_PROCESO and self.responsable_id is None:
            raise ReglaDeNegocioViolada("La solicitud debe tener un responsable asignado")
```

## R3 – Introduce Parameter Object

**Antes:** `guardar(estudiante_id, tipo, asunto, descripcion, prioridad, estado, responsable_id, fecha, fecha_act)`
(9 parámetros posicionales; intercambiar dos no da error).

**Después:** `SolicitudCreate` (DTO validado por Pydantic) entra al servicio y `FiltrosSolicitud`
agrupa los 4 filtros de búsqueda: `repositorio.buscar(filtros)`.

## R4 – Replace Conditional with Table / Enum

`PRIORIDAD_BASE_POR_TIPO[tipo]` + `Prioridad.elevada()` reemplazan 16 líneas de `if/elif`.
`Estado.puede_pasar_a()` reemplaza el árbol de condiciones de transiciones.

## R5 – Repository + DIP

`SolicitudService(solicitudes: SolicitudRepository, catalogos: CatalogoRepository, reloj)`.
En producción recibe `SqlSolicitudRepository`; en pruebas, `SolicitudRepositoryEnMemoria`.

## R6 – Frontend

`App.jsx` (211 líneas, 15 `useState`, 7 URLs fijas) → `ResumenCards`, `SolicitudForm`,
`FiltrosSolicitudes`, `TablaSolicitudes`, `useSolicitudes` y `api/solicitudesApi.js`.
