"""Vocabulario del dominio: reemplaza los strings magicos de la version inicial (CS-08)."""
from enum import Enum

from app.domain.errores import DatoInvalido


class TipoSolicitud(str, Enum):
    CERTIFICADO = "certificado"
    EQUIVALENCIA = "equivalencia"
    RECLAMO_NOTA = "reclamo_nota"
    BAJA_MATERIA = "baja_materia"
    OTRO = "otro"


class Prioridad(str, Enum):
    BAJA = "BAJA"
    MEDIA = "MEDIA"
    ALTA = "ALTA"

    def elevada(self) -> "Prioridad":
        """Devuelve la prioridad inmediata superior (ALTA es el tope)."""
        orden = list(Prioridad)
        return orden[min(orden.index(self) + 1, len(orden) - 1)]


class Estado(str, Enum):
    PENDIENTE = "PENDIENTE"
    EN_PROCESO = "EN_PROCESO"
    RESUELTA = "RESUELTA"
    RECHAZADA = "RECHAZADA"

    @classmethod
    def desde_texto(cls, valor: str | None) -> "Estado":
        try:
            return cls(valor)
        except ValueError:
            raise DatoInvalido("Estado invalido") from None

    @property
    def es_final(self) -> bool:
        return not _TRANSICIONES_PERMITIDAS[self]

    def puede_pasar_a(self, destino: "Estado") -> bool:
        return destino in _TRANSICIONES_PERMITIDAS[self]


# Tabla de transiciones: agregar un estado nuevo no requiere tocar if/elif (OCP).
_TRANSICIONES_PERMITIDAS: dict[Estado, frozenset[Estado]] = {
    Estado.PENDIENTE: frozenset({Estado.EN_PROCESO, Estado.RECHAZADA}),
    Estado.EN_PROCESO: frozenset({Estado.RESUELTA, Estado.RECHAZADA}),
    Estado.RESUELTA: frozenset(),
    Estado.RECHAZADA: frozenset(),
}
