"""Configuracion comun de pruebas.

Se usa una base SQLite temporal para no tocar datos reales. La variable
SGSA_DB se define ANTES de importar la aplicacion.
"""
import os
import sys
import tempfile

import pytest
from fastapi.testclient import TestClient

_TMP_DIR = tempfile.mkdtemp(prefix="sgsa_test_")
os.environ["SGSA_DB"] = os.path.join(_TMP_DIR, "test.db")
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app  # noqa: E402


@pytest.fixture(scope="session")
def client():
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def nueva_solicitud(client):
    """Crea una solicitud valida y devuelve el JSON de respuesta."""

    def _crear(**overrides):
        payload = {
            "estudiante_id": 1,
            "tipo": "certificado",
            "asunto": "Certificado de alumno regular",
            "descripcion": "Lo necesito para presentar en el trabajo",
            "urgente": False,
        }
        payload.update(overrides)
        response = client.post("/api/solicitudes", json=payload)
        assert response.status_code == 201, response.text
        return response.json()

    return _crear
