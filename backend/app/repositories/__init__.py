"""Acceso a datos.

Los servicios dependen de las abstracciones (Protocol) y no de SQLModel/SQLite
(DIP, CS-05). Toda consulta es parametrizada por el ORM (CS-01).
"""
from typing import Optional, Protocol, Sequence

from sqlmodel import Session, or_, select

from app.models import Estudiante, Responsable, Solicitud
from app.schemas import FiltrosSolicitud


class SolicitudRepository(Protocol):
    def agregar(self, solicitud: Solicitud) -> Solicitud: ...
    def guardar(self, solicitud: Solicitud) -> Solicitud: ...
    def obtener(self, solicitud_id: int) -> Optional[Solicitud]: ...
    def buscar(self, filtros: FiltrosSolicitud) -> Sequence[Solicitud]: ...
    def listar_todas(self) -> Sequence[Solicitud]: ...


class CatalogoRepository(Protocol):
    def listar_estudiantes(self) -> Sequence[Estudiante]: ...
    def listar_responsables(self) -> Sequence[Responsable]: ...
    def obtener_estudiante(self, estudiante_id: int) -> Optional[Estudiante]: ...
    def obtener_responsable(self, responsable_id: Optional[int]) -> Optional[Responsable]: ...


class SqlSolicitudRepository:
    def __init__(self, session: Session):
        self._session = session

    def agregar(self, solicitud: Solicitud) -> Solicitud:
        return self.guardar(solicitud)

    def guardar(self, solicitud: Solicitud) -> Solicitud:
        self._session.add(solicitud)
        self._session.commit()
        self._session.refresh(solicitud)
        return solicitud

    def obtener(self, solicitud_id: int) -> Optional[Solicitud]:
        return self._session.get(Solicitud, solicitud_id)

    def buscar(self, filtros: FiltrosSolicitud) -> Sequence[Solicitud]:
        consulta = select(Solicitud).join(Estudiante)
        if filtros.estado:
            consulta = consulta.where(Solicitud.estado == filtros.estado)
        if filtros.tipo:
            consulta = consulta.where(Solicitud.tipo == filtros.tipo)
        if filtros.prioridad:
            consulta = consulta.where(Solicitud.prioridad == filtros.prioridad)
        if filtros.texto:
            consulta = consulta.where(
                or_(
                    Solicitud.asunto.contains(filtros.texto),
                    Estudiante.nombre.contains(filtros.texto),
                    Estudiante.legajo.contains(filtros.texto),
                )
            )
        return self._session.exec(consulta.order_by(Solicitud.id.desc())).all()

    def listar_todas(self) -> Sequence[Solicitud]:
        return self._session.exec(select(Solicitud)).all()


class SqlCatalogoRepository:
    def __init__(self, session: Session):
        self._session = session

    def listar_estudiantes(self) -> Sequence[Estudiante]:
        return self._session.exec(select(Estudiante)).all()

    def listar_responsables(self) -> Sequence[Responsable]:
        return self._session.exec(select(Responsable)).all()

    def obtener_estudiante(self, estudiante_id: int) -> Optional[Estudiante]:
        return self._session.get(Estudiante, estudiante_id)

    def obtener_responsable(self, responsable_id: Optional[int]) -> Optional[Responsable]:
        if responsable_id is None:
            return None
        return self._session.get(Responsable, responsable_id)
