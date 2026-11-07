"""Contratos de entrada (validacion) y salida (response models).

Introduce Parameter Object: `SolicitudCreate` reemplaza los 9 parametros
posicionales de `guardar()` y `FiltrosSolicitud` agrupa los 4 filtros de busqueda.
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, field_validator

from app.domain.enums import TipoSolicitud
from app.models import Solicitud

ASUNTO_MIN = 5
ASUNTO_MAX = 120
DESCRIPCION_MAX = 1000


# ---------- entrada ----------

class SolicitudCreate(BaseModel):
    estudiante_id: int
    tipo: TipoSolicitud
    asunto: str
    descripcion: Optional[str] = ""
    urgente: bool = False

    @field_validator("estudiante_id", mode="before")
    @classmethod
    def _estudiante_obligatorio(cls, valor):
        if valor is None:
            raise ValueError("El estudiante es obligatorio")
        return valor

    @field_validator("tipo", mode="before")
    @classmethod
    def _tipo_valido(cls, valor):
        if valor not in {tipo.value for tipo in TipoSolicitud}:
            raise ValueError("Tipo de solicitud invalido")
        return valor

    @field_validator("asunto", mode="before")
    @classmethod
    def _asunto_valido(cls, valor):
        if not isinstance(valor, str) or len(valor.strip()) < ASUNTO_MIN:
            raise ValueError(f"El asunto debe tener al menos {ASUNTO_MIN} caracteres")
        if len(valor) > ASUNTO_MAX:
            raise ValueError(f"El asunto no puede superar {ASUNTO_MAX} caracteres")
        return valor.strip()

    @field_validator("descripcion", mode="before")
    @classmethod
    def _descripcion_valida(cls, valor):
        valor = valor or ""
        if len(valor) > DESCRIPCION_MAX:
            raise ValueError(f"La descripcion no puede superar {DESCRIPCION_MAX} caracteres")
        return valor


class CambioEstadoRequest(BaseModel):
    estado: Optional[str] = None


class AsignacionResponsableRequest(BaseModel):
    responsable_id: Optional[int] = None


@dataclass(frozen=True)
class FiltrosSolicitud:
    estado: Optional[str] = None
    tipo: Optional[str] = None
    prioridad: Optional[str] = None
    texto: Optional[str] = None


# ---------- salida ----------

class EstudianteResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    legajo: str
    nombre: str
    email: str
    carrera: str


class ResponsableResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    nombre: str
    area: str


class SolicitudResponse(BaseModel):
    id: int
    estudiante_id: int
    estudiante: str
    legajo: str
    tipo: str
    asunto: str
    descripcion: str
    prioridad: str
    estado: str
    responsable_id: Optional[int]
    responsable: Optional[str]
    fecha_creacion: datetime
    fecha_actualizacion: datetime

    @classmethod
    def desde_entidad(cls, solicitud: Solicitud) -> "SolicitudResponse":
        return cls(
            id=solicitud.id,
            estudiante_id=solicitud.estudiante_id,
            estudiante=solicitud.estudiante.nombre,
            legajo=solicitud.estudiante.legajo,
            tipo=solicitud.tipo,
            asunto=solicitud.asunto,
            descripcion=solicitud.descripcion,
            prioridad=solicitud.prioridad,
            estado=solicitud.estado,
            responsable_id=solicitud.responsable_id,
            responsable=solicitud.responsable.nombre if solicitud.responsable else None,
            fecha_creacion=solicitud.fecha_creacion,
            fecha_actualizacion=solicitud.fecha_actualizacion,
        )


class ResumenResponse(BaseModel):
    total: int
    por_estado: dict[str, int]
    por_tipo: dict[str, int]
    por_prioridad: dict[str, int]
    sin_responsable: int
    porcentaje_resueltas: float
