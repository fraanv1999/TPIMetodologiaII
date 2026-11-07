"""Punto de armado de la aplicacion: middlewares, routers y manejo central de errores."""
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.database import inicializar_base
from app.domain.errores import DatoInvalido, ErrorDeDominio, RecursoNoEncontrado, ReglaDeNegocioViolada
from app.routers import catalogos_router, reportes_router, solicitudes_router

# Code review CR-04: se reemplaza allow_origins=["*"] por una lista configurable.
ORIGENES_PERMITIDOS = os.environ.get("SGSA_CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173").split(",")

STATUS_POR_ERROR = {
    DatoInvalido: 400,
    RecursoNoEncontrado: 404,
    ReglaDeNegocioViolada: 409,
}


@asynccontextmanager
async def ciclo_de_vida(_: FastAPI):
    inicializar_base()
    yield


def _mensaje_de_validacion(error: dict) -> str:
    if error.get("type") == "missing":
        return f"El campo {error['loc'][-1]} es obligatorio"
    return str(error.get("msg", "Datos invalidos")).removeprefix("Value error, ")


def crear_app() -> FastAPI:
    app = FastAPI(title="SGSA - Sistema de Gestion de Solicitudes Academicas", version="2.0.0", lifespan=ciclo_de_vida)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=ORIGENES_PERMITIDOS,
        allow_methods=["GET", "POST", "PATCH"],
        allow_headers=["Content-Type"],
    )

    @app.exception_handler(ErrorDeDominio)
    async def manejar_error_de_dominio(_: Request, error: ErrorDeDominio):
        return JSONResponse(status_code=STATUS_POR_ERROR.get(type(error), 400), content={"detail": error.mensaje})

    @app.exception_handler(RequestValidationError)
    async def manejar_error_de_validacion(_: Request, error: RequestValidationError):
        # Se mantiene el contrato original: datos invalidos -> 400 con un mensaje legible.
        return JSONResponse(status_code=400, content={"detail": _mensaje_de_validacion(error.errors()[0])})

    app.include_router(catalogos_router)
    app.include_router(solicitudes_router)
    app.include_router(reportes_router)
    return app


app = crear_app()
