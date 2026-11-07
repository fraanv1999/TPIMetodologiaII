"""Reglas de negocio puras (sin base de datos ni HTTP): faciles de probar."""
from app.domain.enums import Prioridad, TipoSolicitud

PRIORIDAD_BASE_POR_TIPO: dict[TipoSolicitud, Prioridad] = {
    TipoSolicitud.CERTIFICADO: Prioridad.BAJA,
    TipoSolicitud.EQUIVALENCIA: Prioridad.MEDIA,
    TipoSolicitud.RECLAMO_NOTA: Prioridad.ALTA,
    TipoSolicitud.BAJA_MATERIA: Prioridad.MEDIA,
    TipoSolicitud.OTRO: Prioridad.BAJA,
}


def calcular_prioridad(tipo: TipoSolicitud, urgente: bool) -> Prioridad:
    """Prioridad base segun el tipo; si es urgente sube un nivel."""
    prioridad = PRIORIDAD_BASE_POR_TIPO[tipo]
    return prioridad.elevada() if urgente else prioridad
