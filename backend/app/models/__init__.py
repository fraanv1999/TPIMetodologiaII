"""Modelos persistentes (tablas). Contienen el comportamiento propio de la entidad."""
from datetime import datetime
from typing import Optional

from pydantic import NaiveDatetime
from sqlmodel import Field, Relationship, SQLModel

from app.domain.enums import Estado
from app.domain.errores import ReglaDeNegocioViolada


class Estudiante(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    legajo: str
    nombre: str
    email: str
    carrera: str


class Responsable(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    area: str


class Solicitud(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    estudiante_id: int = Field(foreign_key="estudiante.id")
    responsable_id: Optional[int] = Field(default=None, foreign_key="responsable.id")
    # Se persisten los valores de los enums (TipoSolicitud, Prioridad, Estado).
    tipo: str
    asunto: str
    descripcion: str = ""
    prioridad: str
    estado: str = Estado.PENDIENTE.value
    # Hora local sin zona horaria, igual que la version inicial.
    fecha_creacion: NaiveDatetime
    fecha_actualizacion: NaiveDatetime

    estudiante: Optional[Estudiante] = Relationship()
    responsable: Optional[Responsable] = Relationship()

    # --- Move Method: estas reglas antes vivian en los endpoints de main.py ---

    @property
    def estado_actual(self) -> Estado:
        return Estado(self.estado)

    def validar_admite_asignacion(self) -> None:
        if self.estado_actual.es_final:
            raise ReglaDeNegocioViolada("No se puede asignar responsable a una solicitud cerrada")

    def asignar_responsable(self, responsable: Responsable, momento: datetime) -> None:
        self.validar_admite_asignacion()
        self.responsable_id = responsable.id
        self.responsable = responsable
        self.fecha_actualizacion = momento

    def cambiar_estado(self, nuevo: Estado, momento: datetime) -> None:
        actual = self.estado_actual
        if not actual.puede_pasar_a(nuevo):
            raise ReglaDeNegocioViolada(f"No se puede pasar de {actual.value} a {nuevo.value}")
        if nuevo is Estado.EN_PROCESO and self.responsable_id is None:
            raise ReglaDeNegocioViolada("La solicitud debe tener un responsable asignado")
        self.estado = nuevo.value
        self.fecha_actualizacion = momento
