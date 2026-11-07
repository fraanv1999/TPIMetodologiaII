"""Pruebas unitarias de servicios con repositorios en memoria.

Gracias a la inversion de dependencias (DIP), el servicio se prueba sin
SQLite ni FastAPI. En la version inicial esto no era posible.
"""
from datetime import datetime

import pytest

from app.domain.errores import DatoInvalido, RecursoNoEncontrado, ReglaDeNegocioViolada
from app.models import Estudiante, Responsable
from app.schemas import FiltrosSolicitud, SolicitudCreate
from app.services import ReporteService, SolicitudService

MOMENTO = datetime(2026, 11, 5, 12, 0, 0)


class SolicitudRepositoryEnMemoria:
    def __init__(self):
        self.datos = {}

    def agregar(self, solicitud):
        solicitud.id = len(self.datos) + 1
        return self.guardar(solicitud)

    def guardar(self, solicitud):
        self.datos[solicitud.id] = solicitud
        return solicitud

    def obtener(self, solicitud_id):
        return self.datos.get(solicitud_id)

    def buscar(self, filtros: FiltrosSolicitud):
        return [s for s in self.datos.values() if not filtros.estado or s.estado == filtros.estado]

    def listar_todas(self):
        return list(self.datos.values())


class CatalogoEnMemoria:
    estudiantes = {1: Estudiante(id=1, legajo="1", nombre="Ana", email="a@example.com", carrera="TUP")}
    responsables = {7: Responsable(id=7, nombre="Laura", area="Alumnado")}

    def listar_estudiantes(self):
        return list(self.estudiantes.values())

    def listar_responsables(self):
        return list(self.responsables.values())

    def obtener_estudiante(self, estudiante_id):
        return self.estudiantes.get(estudiante_id)

    def obtener_responsable(self, responsable_id):
        return self.responsables.get(responsable_id)


@pytest.fixture
def repo():
    return SolicitudRepositoryEnMemoria()


@pytest.fixture
def servicio(repo):
    return SolicitudService(repo, CatalogoEnMemoria(), reloj=lambda: MOMENTO)


def _datos(**cambios):
    base = {"estudiante_id": 1, "tipo": "equivalencia", "asunto": "Equivalencia Programacion I", "urgente": True}
    base.update(cambios)
    return SolicitudCreate(**base)


def test_registrar_calcula_prioridad_estado_y_fechas(servicio):
    solicitud = servicio.registrar(_datos())
    assert (solicitud.prioridad, solicitud.estado) == ("ALTA", "PENDIENTE")
    assert solicitud.fecha_creacion == solicitud.fecha_actualizacion == MOMENTO


def test_registrar_con_estudiante_inexistente(servicio):
    with pytest.raises(RecursoNoEncontrado, match="Estudiante"):
        servicio.registrar(_datos(estudiante_id=99))


def test_flujo_asignar_tomar_resolver(servicio):
    sid = servicio.registrar(_datos()).id
    servicio.asignar_responsable(sid, 7)
    servicio.cambiar_estado(sid, "EN_PROCESO")
    assert servicio.cambiar_estado(sid, "RESUELTA").estado == "RESUELTA"


def test_orden_de_validacion_en_cambio_de_estado(servicio):
    # Igual que la version inicial: primero 404, despues 400, despues 409.
    with pytest.raises(RecursoNoEncontrado):
        servicio.cambiar_estado(999, "CUALQUIERA")
    sid = servicio.registrar(_datos()).id
    with pytest.raises(DatoInvalido):
        servicio.cambiar_estado(sid, "CUALQUIERA")
    with pytest.raises(ReglaDeNegocioViolada):
        servicio.cambiar_estado(sid, "RESUELTA")


def test_asignar_responsable_inexistente(servicio):
    sid = servicio.registrar(_datos()).id
    with pytest.raises(RecursoNoEncontrado, match="Responsable"):
        servicio.asignar_responsable(sid, 123)


def test_reporte_resumen(repo, servicio):
    servicio.registrar(_datos())
    sid = servicio.registrar(_datos(tipo="certificado", urgente=False)).id
    servicio.cambiar_estado(sid, "RECHAZADA")
    resumen = ReporteService(repo).resumen()
    assert resumen.total == 2
    assert resumen.por_estado == {"PENDIENTE": 1, "EN_PROCESO": 0, "RESUELTA": 0, "RECHAZADA": 1}
    assert resumen.por_tipo == {"equivalencia": 1, "certificado": 1}
    assert resumen.sin_responsable == 1
    assert resumen.porcentaje_resueltas == 0


def test_reporte_vacio(repo):
    assert ReporteService(repo).resumen().porcentaje_resueltas == 0


@pytest.mark.parametrize(
    "cambios, mensaje",
    [
        ({"tipo": "x"}, "Tipo de solicitud invalido"),
        ({"asunto": "   abc   "}, "al menos 5"),
        ({"asunto": "a" * 121}, "120"),
        ({"descripcion": "a" * 1001}, "1000"),
        ({"estudiante_id": None}, "obligatorio"),
    ],
)
def test_dto_valida_entrada(cambios, mensaje):
    with pytest.raises(ValueError, match=mensaje):
        _datos(**cambios)


def test_dto_normaliza_asunto_y_descripcion():
    datos = _datos(asunto="  Equivalencia Fisica  ", descripcion=None)
    assert datos.asunto == "Equivalencia Fisica"
    assert datos.descripcion == ""
