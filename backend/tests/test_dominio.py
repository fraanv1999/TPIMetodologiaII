"""Pruebas unitarias de reglas de dominio (sin base de datos ni HTTP)."""
from datetime import datetime

import pytest

from app.domain.enums import Estado, Prioridad, TipoSolicitud
from app.domain.errores import DatoInvalido, ReglaDeNegocioViolada
from app.domain.reglas import calcular_prioridad
from app.models import Responsable, Solicitud

MOMENTO = datetime(2026, 11, 5, 10, 0, 0)


def _solicitud(estado=Estado.PENDIENTE, responsable_id=None):
    return Solicitud(
        id=1, estudiante_id=1, responsable_id=responsable_id, tipo="certificado", asunto="Asunto de prueba",
        prioridad="BAJA", estado=estado.value, fecha_creacion=MOMENTO, fecha_actualizacion=MOMENTO,
    )


@pytest.mark.parametrize("tipo", list(TipoSolicitud))
def test_toda_solicitud_tiene_prioridad_base(tipo):
    assert calcular_prioridad(tipo, urgente=False) in Prioridad


def test_urgencia_eleva_un_nivel_y_alta_es_tope():
    assert Prioridad.BAJA.elevada() is Prioridad.MEDIA
    assert Prioridad.MEDIA.elevada() is Prioridad.ALTA
    assert Prioridad.ALTA.elevada() is Prioridad.ALTA


@pytest.mark.parametrize(
    "origen, destino, permitido",
    [
        (Estado.PENDIENTE, Estado.EN_PROCESO, True),
        (Estado.PENDIENTE, Estado.RECHAZADA, True),
        (Estado.PENDIENTE, Estado.RESUELTA, False),
        (Estado.EN_PROCESO, Estado.RESUELTA, True),
        (Estado.EN_PROCESO, Estado.PENDIENTE, False),
        (Estado.RESUELTA, Estado.PENDIENTE, False),
        (Estado.RECHAZADA, Estado.EN_PROCESO, False),
    ],
)
def test_tabla_de_transiciones(origen, destino, permitido):
    assert origen.puede_pasar_a(destino) is permitido


def test_estados_finales():
    assert {e for e in Estado if e.es_final} == {Estado.RESUELTA, Estado.RECHAZADA}


def test_estado_desde_texto_invalido_lanza_dato_invalido():
    with pytest.raises(DatoInvalido, match="Estado invalido"):
        Estado.desde_texto("CUALQUIERA")


def test_no_pasa_a_en_proceso_sin_responsable():
    with pytest.raises(ReglaDeNegocioViolada, match="responsable"):
        _solicitud().cambiar_estado(Estado.EN_PROCESO, MOMENTO)


def test_cambiar_estado_actualiza_fecha():
    solicitud = _solicitud(responsable_id=1)
    nuevo_momento = datetime(2026, 11, 6, 9, 30, 0)
    solicitud.cambiar_estado(Estado.EN_PROCESO, nuevo_momento)
    assert solicitud.estado == "EN_PROCESO"
    assert solicitud.fecha_actualizacion == nuevo_momento


def test_no_se_asigna_responsable_a_solicitud_cerrada():
    with pytest.raises(ReglaDeNegocioViolada, match="cerrada"):
        _solicitud(estado=Estado.RESUELTA).asignar_responsable(Responsable(id=1, nombre="X", area="Y"), MOMENTO)
