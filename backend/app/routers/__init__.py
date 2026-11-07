"""Endpoints HTTP: reciben el request, delegan en servicios y devuelven response models."""
from typing import Optional

from fastapi import APIRouter, Depends

from app.dependencies import catalogo_repository, reporte_service, solicitud_service
from app.repositories import CatalogoRepository
from app.schemas import (
    AsignacionResponsableRequest,
    CambioEstadoRequest,
    EstudianteResponse,
    FiltrosSolicitud,
    ResponsableResponse,
    ResumenResponse,
    SolicitudCreate,
    SolicitudResponse,
)
from app.services import ReporteService, SolicitudService

catalogos_router = APIRouter(prefix="/api", tags=["catalogos"])
solicitudes_router = APIRouter(prefix="/api/solicitudes", tags=["solicitudes"])
reportes_router = APIRouter(prefix="/api/reportes", tags=["reportes"])


@catalogos_router.get("/estudiantes", response_model=list[EstudianteResponse])
def listar_estudiantes(catalogos: CatalogoRepository = Depends(catalogo_repository)):
    return catalogos.listar_estudiantes()


@catalogos_router.get("/responsables", response_model=list[ResponsableResponse])
def listar_responsables(catalogos: CatalogoRepository = Depends(catalogo_repository)):
    return catalogos.listar_responsables()


@solicitudes_router.post("", status_code=201, response_model=SolicitudResponse)
def registrar_solicitud(datos: SolicitudCreate, servicio: SolicitudService = Depends(solicitud_service)):
    return SolicitudResponse.desde_entidad(servicio.registrar(datos))


@solicitudes_router.get("", response_model=list[SolicitudResponse])
def buscar_solicitudes(
    estado: Optional[str] = None,
    tipo: Optional[str] = None,
    prioridad: Optional[str] = None,
    texto: Optional[str] = None,
    servicio: SolicitudService = Depends(solicitud_service),
):
    filtros = FiltrosSolicitud(estado=estado, tipo=tipo, prioridad=prioridad, texto=texto)
    return [SolicitudResponse.desde_entidad(s) for s in servicio.buscar(filtros)]


@solicitudes_router.get("/{solicitud_id}", response_model=SolicitudResponse)
def obtener_solicitud(solicitud_id: int, servicio: SolicitudService = Depends(solicitud_service)):
    return SolicitudResponse.desde_entidad(servicio.obtener(solicitud_id))


@solicitudes_router.patch("/{solicitud_id}/estado", response_model=SolicitudResponse)
def cambiar_estado(
    solicitud_id: int, cambio: CambioEstadoRequest, servicio: SolicitudService = Depends(solicitud_service)
):
    return SolicitudResponse.desde_entidad(servicio.cambiar_estado(solicitud_id, cambio.estado))


@solicitudes_router.patch("/{solicitud_id}/responsable", response_model=SolicitudResponse)
def asignar_responsable(
    solicitud_id: int,
    asignacion: AsignacionResponsableRequest,
    servicio: SolicitudService = Depends(solicitud_service),
):
    return SolicitudResponse.desde_entidad(servicio.asignar_responsable(solicitud_id, asignacion.responsable_id))


@reportes_router.get("/resumen", response_model=ResumenResponse)
def generar_resumen(servicio: ReporteService = Depends(reporte_service)):
    return servicio.resumen()
