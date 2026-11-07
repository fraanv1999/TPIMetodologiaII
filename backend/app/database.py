"""Conexion a la base de datos y datos semilla (sinteticos)."""
import os
from typing import Iterator

from sqlmodel import Session, SQLModel, create_engine, select

from app.models import Estudiante, Responsable

DATABASE_PATH = os.environ.get("SGSA_DB", "sgsa.db")
engine = create_engine(f"sqlite:///{DATABASE_PATH}", connect_args={"check_same_thread": False})

ESTUDIANTES_SEMILLA = [
    Estudiante(legajo="10001", nombre="Ana Gomez", email="ana.gomez@example.com", carrera="TUP"),
    Estudiante(legajo="10002", nombre="Bruno Diaz", email="bruno.diaz@example.com", carrera="TUP"),
    Estudiante(legajo="10003", nombre="Carla Ruiz", email="carla.ruiz@example.com", carrera="TUP"),
]
RESPONSABLES_SEMILLA = [
    Responsable(nombre="Laura Perez", area="Alumnado"),
    Responsable(nombre="Martin Sosa", area="Coordinacion"),
    Responsable(nombre="Julia Torres", area="Bedelia"),
]


def inicializar_base() -> None:
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        if session.exec(select(Estudiante)).first() is None:
            session.add_all([e.model_copy() for e in ESTUDIANTES_SEMILLA])
            session.add_all([r.model_copy() for r in RESPONSABLES_SEMILLA])
            session.commit()


def obtener_sesion() -> Iterator[Session]:
    with Session(engine) as session:
        yield session
