"""Casos de uso. Orquestan entidades y repositorios; no conocen HTTP ni SQL."""
from collections import Counter
from datetime import datetime
from typing import Callable, Sequence

from app.domain.enums import Estado, Prioridad
from app.domain.errores import RecursoNoEncontrado
from app.domain.reglas import calcular_prioridad
from app.models import Solicitud
from app.repositories import CatalogoRepository, SolicitudRepository
from app.schemas import FiltrosSolicitud, ResumenResponse, SolicitudCreate

Reloj = Callable[[], datetime]


def reloj_sistema() -> datetime:
    return datetime.now().replace(microsecond=0)


class SolicitudService:
    def __init__(self, solicitudes: SolicitudRepository, catalogos: CatalogoRepository, reloj: Reloj = reloj_sistema):
        self._solicitudes = solicitudes
        self._catalogos = catalogos
        self._reloj = reloj

    def registrar(self, datos: SolicitudCreate) -> Solicitud:
        estudiante = self._catalogos.obtener_estudiante(datos.estudiante_id)
        if estudiante is None:
            raise RecursoNoEncontrado("Estudiante no encontrado")
        momento = self._reloj()
        solicitud = Solicitud(
            estudiante_id=estudiante.id,
            tipo=datos.tipo.value,
            asunto=datos.asunto,
            descripcion=datos.descripcion,
            prioridad=calcular_prioridad(datos.tipo, datos.urgente).value,
            estado=Estado.PENDIENTE.value,
            fecha_creacion=momento,
            fecha_actualizacion=momento,
        )
        solicitud.estudiante = estudiante
        return self._solicitudes.agregar(solicitud)

    def obtener(self, solicitud_id: int) -> Solicitud:
        solicitud = self._solicitudes.obtener(solicitud_id)
        if solicitud is None:
            raise RecursoNoEncontrado("Solicitud no encontrada")
        return solicitud

    def buscar(self, filtros: FiltrosSolicitud) -> Sequence[Solicitud]:
        return self._solicitudes.buscar(filtros)

    def cambiar_estado(self, solicitud_id: int, estado: str | None) -> Solicitud:
        solicitud = self.obtener(solicitud_id)
        solicitud.cambiar_estado(Estado.desde_texto(estado), self._reloj())
        return self._solicitudes.guardar(solicitud)

    def asignar_responsable(self, solicitud_id: int, responsable_id: int | None) -> Solicitud:
        solicitud = self.obtener(solicitud_id)
        solicitud.validar_admite_asignacion()
        responsable = self._catalogos.obtener_responsable(responsable_id)
        if responsable is None:
            raise RecursoNoEncontrado("Responsable no encontrado")
        solicitud.asignar_responsable(responsable, self._reloj())
        return self._solicitudes.guardar(solicitud)


class ReporteService:
    def __init__(self, solicitudes: SolicitudRepository):
        self._solicitudes = solicitudes

    def resumen(self) -> ResumenResponse:
        solicitudes = self._solicitudes.listar_todas()
        por_estado = Counter(s.estado for s in solicitudes)
        por_prioridad = Counter(s.prioridad for s in solicitudes)
        total = len(solicitudes)
        return ResumenResponse(
            total=total,
            por_estado={estado.value: por_estado[estado.value] for estado in Estado},
            por_tipo=dict(Counter(s.tipo for s in solicitudes)),
            por_prioridad={prioridad.value: por_prioridad[prioridad.value] for prioridad in Prioridad},
            sin_responsable=sum(1 for s in solicitudes if s.responsable_id is None and not s.estado_actual.es_final),
            porcentaje_resueltas=round(por_estado[Estado.RESUELTA.value] * 100 / total, 2) if total else 0,
        )
