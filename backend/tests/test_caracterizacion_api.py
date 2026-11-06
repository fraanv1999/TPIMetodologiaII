"""Pruebas de caracterizacion (caja negra) de la API.

Se escribieron sobre la VERSION INICIAL (tag estado-inicial) y se ejecutan sin
cambios sobre la VERSION REFACTORIZADA. Si todas pasan en ambas versiones, el
comportamiento externo se conservo.
"""
import pytest

CAMPOS_SOLICITUD = {
    "id", "estudiante_id", "estudiante", "legajo", "tipo", "asunto", "descripcion",
    "prioridad", "estado", "responsable_id", "responsable",
    "fecha_creacion", "fecha_actualizacion",
}


# ---------- CP-01 / CP-02: catalogos ----------

def test_cp01_lista_estudiantes_semilla(client):
    response = client.get("/api/estudiantes")
    assert response.status_code == 200
    estudiantes = response.json()
    assert len(estudiantes) >= 3
    assert set(estudiantes[0]) == {"id", "legajo", "nombre", "email", "carrera"}


def test_cp02_lista_responsables_semilla(client):
    response = client.get("/api/responsables")
    assert response.status_code == 200
    assert {r["area"] for r in response.json()} >= {"Alumnado", "Coordinacion", "Bedelia"}


# ---------- CP-03 a CP-05: registrar solicitud ----------

def test_cp03_registrar_solicitud_valida(nueva_solicitud):
    solicitud = nueva_solicitud()
    assert set(solicitud) == CAMPOS_SOLICITUD
    assert solicitud["estado"] == "PENDIENTE"
    assert solicitud["prioridad"] == "BAJA"
    assert solicitud["responsable_id"] is None
    assert solicitud["estudiante"] == "Ana Gomez"
    assert solicitud["legajo"] == "10001"


@pytest.mark.parametrize(
    "tipo, urgente, prioridad_esperada",
    [
        ("certificado", False, "BAJA"),
        ("certificado", True, "MEDIA"),
        ("equivalencia", False, "MEDIA"),
        ("equivalencia", True, "ALTA"),
        ("reclamo_nota", False, "ALTA"),
        ("reclamo_nota", True, "ALTA"),
        ("baja_materia", False, "MEDIA"),
        ("otro", False, "BAJA"),
        ("otro", True, "MEDIA"),
    ],
)
def test_cp04_prioridad_segun_tipo_y_urgencia(nueva_solicitud, tipo, urgente, prioridad_esperada):
    assert nueva_solicitud(tipo=tipo, urgente=urgente)["prioridad"] == prioridad_esperada


@pytest.mark.parametrize(
    "cambios, status",
    [
        ({"tipo": "inexistente"}, 400),
        ({"asunto": "abc"}, 400),
        ({"asunto": "x" * 121}, 400),
        ({"descripcion": "x" * 1001}, 400),
        ({"estudiante_id": None}, 400),
        ({"estudiante_id": 9999}, 404),
    ],
)
def test_cp05_rechaza_datos_invalidos(client, cambios, status):
    payload = {"estudiante_id": 1, "tipo": "certificado", "asunto": "Asunto valido"}
    payload.update(cambios)
    assert client.post("/api/solicitudes", json=payload).status_code == status


# ---------- CP-06 / CP-07: consultar y filtrar ----------

def test_cp06_obtener_por_id_y_404(client, nueva_solicitud):
    creada = nueva_solicitud()
    assert client.get(f"/api/solicitudes/{creada['id']}").json() == creada
    assert client.get("/api/solicitudes/999999").status_code == 404


def test_cp07_filtrar_por_estado_tipo_prioridad_y_texto(client, nueva_solicitud):
    creada = nueva_solicitud(tipo="reclamo_nota", asunto="Reclamo nota final Algebra", estudiante_id=2)
    filtros = {"estado": "PENDIENTE", "tipo": "reclamo_nota", "prioridad": "ALTA", "texto": "Algebra"}
    resultado = client.get("/api/solicitudes", params=filtros).json()
    assert creada["id"] in [s["id"] for s in resultado]
    assert all(s["tipo"] == "reclamo_nota" and s["estado"] == "PENDIENTE" for s in resultado)
    por_legajo = client.get("/api/solicitudes", params={"texto": "10002"}).json()
    assert creada["id"] in [s["id"] for s in por_legajo]


def test_cp07b_listado_ordenado_descendente(client, nueva_solicitud):
    nueva_solicitud()
    ids = [s["id"] for s in client.get("/api/solicitudes").json()]
    assert ids == sorted(ids, reverse=True)


def test_cp07c_texto_con_comilla_no_rompe(client):
    response = client.get("/api/solicitudes", params={"texto": "O'Brien"})
    assert response.status_code == 200


# ---------- CP-08 a CP-10: asignar responsable y cambiar estado ----------

def test_cp08_asignar_responsable(client, nueva_solicitud):
    creada = nueva_solicitud()
    response = client.patch(f"/api/solicitudes/{creada['id']}/responsable", json={"responsable_id": 2})
    assert response.status_code == 200
    assert response.json()["responsable"] == "Martin Sosa"
    assert client.patch(f"/api/solicitudes/{creada['id']}/responsable", json={"responsable_id": 999}).status_code == 404
    assert client.patch("/api/solicitudes/999999/responsable", json={"responsable_id": 1}).status_code == 404


def test_cp09_flujo_completo_de_estados(client, nueva_solicitud):
    sid = nueva_solicitud()["id"]
    # sin responsable no puede pasar a EN_PROCESO
    assert client.patch(f"/api/solicitudes/{sid}/estado", json={"estado": "EN_PROCESO"}).status_code == 409
    client.patch(f"/api/solicitudes/{sid}/responsable", json={"responsable_id": 1})
    assert client.patch(f"/api/solicitudes/{sid}/estado", json={"estado": "EN_PROCESO"}).json()["estado"] == "EN_PROCESO"
    assert client.patch(f"/api/solicitudes/{sid}/estado", json={"estado": "RESUELTA"}).json()["estado"] == "RESUELTA"
    # estado final: no admite cambios ni reasignacion
    assert client.patch(f"/api/solicitudes/{sid}/estado", json={"estado": "PENDIENTE"}).status_code == 409
    assert client.patch(f"/api/solicitudes/{sid}/responsable", json={"responsable_id": 2}).status_code == 409


@pytest.mark.parametrize(
    "estado, status",
    [("RESUELTA", 409), ("PENDIENTE", 409), ("CUALQUIERA", 400), ("RECHAZADA", 200)],
)
def test_cp10_transiciones_desde_pendiente(client, nueva_solicitud, estado, status):
    sid = nueva_solicitud()["id"]
    assert client.patch(f"/api/solicitudes/{sid}/estado", json={"estado": estado}).status_code == status


# ---------- CP-11: reporte ----------

def test_cp11_reporte_resumen_se_actualiza(client, nueva_solicitud):
    antes = client.get("/api/reportes/resumen").json()
    assert set(antes) == {"total", "por_estado", "por_tipo", "por_prioridad", "sin_responsable", "porcentaje_resueltas"}
    nueva_solicitud(tipo="equivalencia")
    despues = client.get("/api/reportes/resumen").json()
    assert despues["total"] == antes["total"] + 1
    assert despues["por_estado"]["PENDIENTE"] == antes["por_estado"]["PENDIENTE"] + 1
    assert despues["por_tipo"]["equivalencia"] == antes["por_tipo"].get("equivalencia", 0) + 1
    assert despues["por_prioridad"]["MEDIA"] == antes["por_prioridad"]["MEDIA"] + 1
    assert despues["sin_responsable"] == antes["sin_responsable"] + 1
    esperado = round(despues["por_estado"]["RESUELTA"] * 100 / despues["total"], 2)
    assert despues["porcentaje_resueltas"] == esperado
