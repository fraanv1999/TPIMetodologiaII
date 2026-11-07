"""Composicion de dependencias (inyeccion via FastAPI Depends)."""
from fastapi import Depends
from sqlmodel import Session

from app.database import obtener_sesion
from app.repositories import SqlCatalogoRepository, SqlSolicitudRepository
from app.services import ReporteService, SolicitudService


def catalogo_repository(session: Session = Depends(obtener_sesion)) -> SqlCatalogoRepository:
    return SqlCatalogoRepository(session)


def solicitud_service(session: Session = Depends(obtener_sesion)) -> SolicitudService:
    return SolicitudService(SqlSolicitudRepository(session), SqlCatalogoRepository(session))


def reporte_service(session: Session = Depends(obtener_sesion)) -> ReporteService:
    return ReporteService(SqlSolicitudRepository(session))
