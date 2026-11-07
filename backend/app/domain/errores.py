"""Errores de dominio.

Los servicios y entidades no conocen HTTP: lanzan estas excepciones y
`app.main` las traduce a codigos de estado en un unico lugar (CS-02).
"""


class ErrorDeDominio(Exception):
    """Base de todos los errores esperables del negocio."""

    def __init__(self, mensaje: str):
        super().__init__(mensaje)
        self.mensaje = mensaje


class DatoInvalido(ErrorDeDominio):
    """El dato recibido no cumple el formato esperado (HTTP 400)."""


class RecursoNoEncontrado(ErrorDeDominio):
    """La entidad referenciada no existe (HTTP 404)."""


class ReglaDeNegocioViolada(ErrorDeDominio):
    """La operacion es valida en formato pero no en el estado actual (HTTP 409)."""
