"""Pruebas de regresion de seguridad (CS-01 / CS-02).

Estas pruebas FALLAN en el tag estado-inicial (la inyeccion devuelve todas las
filas) y PASAN desde el commit fix(seguridad). Ver docs/evidencias.
"""
import pytest

INYECCIONES = [
    {"estado": "x' OR 1=1 --"},
    {"tipo": "x' OR '1'='1"},
    {"prioridad": "x' OR 1=1 --"},
    {"texto": "zzz%' OR 1=1 OR s.asunto LIKE '%"},
]


@pytest.mark.parametrize("filtro", INYECCIONES)
def test_filtros_no_permiten_inyeccion_sql(client, nueva_solicitud, filtro):
    nueva_solicitud()
    response = client.get("/api/solicitudes", params=filtro)
    assert response.status_code == 200
    assert response.json() == []


def test_texto_con_comodines_se_trata_como_dato(client, nueva_solicitud):
    creada = nueva_solicitud(asunto="Pedido 100% urgente de certificado")
    ids = [s["id"] for s in client.get("/api/solicitudes", params={"texto": "100%"}).json()]
    assert creada["id"] in ids
