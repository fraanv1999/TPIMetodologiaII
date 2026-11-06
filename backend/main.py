from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import os
from datetime import datetime

app = FastAPI(title="SGSA")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

DB = os.environ.get("SGSA_DB", "solicitudes.db")
conn = sqlite3.connect(DB, check_same_thread=False)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

TIPOS_VALIDOS = ["certificado", "equivalencia", "reclamo_nota", "baja_materia", "otro"]
ESTADOS_VALIDOS = ["PENDIENTE", "EN_PROCESO", "RESUELTA", "RECHAZADA"]
ESTADOS_FINALES = ["RESUELTA", "RECHAZADA"]

CONSULTA_SOLICITUD_COMPLETA = (
    "SELECT s.*, e.nombre AS estudiante_nombre, e.legajo AS estudiante_legajo, r.nombre AS responsable_nombre "
    "FROM solicitudes s JOIN estudiantes e ON s.estudiante_id = e.id "
    "LEFT JOIN responsables r ON s.responsable_id = r.id"
)


def crear_tablas():
    cursor.execute("CREATE TABLE IF NOT EXISTS estudiantes (id INTEGER PRIMARY KEY AUTOINCREMENT, legajo TEXT, nombre TEXT, email TEXT, carrera TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS responsables (id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT, area TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS solicitudes (id INTEGER PRIMARY KEY AUTOINCREMENT, estudiante_id INTEGER, tipo TEXT, asunto TEXT, descripcion TEXT, prioridad TEXT, estado TEXT, responsable_id INTEGER, fecha TEXT, fecha_act TEXT)")


def cargar_datos_semilla():
    cursor.execute("SELECT COUNT(*) FROM estudiantes")
    if cursor.fetchone()[0] > 0:
        return
    estudiantes_semilla = [
        ("10001", "Ana Gomez", "ana.gomez@example.com", "TUP"),
        ("10002", "Bruno Diaz", "bruno.diaz@example.com", "TUP"),
        ("10003", "Carla Ruiz", "carla.ruiz@example.com", "TUP"),
    ]
    responsables_semilla = [("Laura Perez", "Alumnado"), ("Martin Sosa", "Coordinacion"), ("Julia Torres", "Bedelia")]
    cursor.executemany("INSERT INTO estudiantes (legajo, nombre, email, carrera) VALUES (?, ?, ?, ?)", estudiantes_semilla)
    cursor.executemany("INSERT INTO responsables (nombre, area) VALUES (?, ?)", responsables_semilla)
    conn.commit()


crear_tablas()
cargar_datos_semilla()


def ahora():
    return datetime.now().replace(microsecond=0).isoformat()


def fila_a_solicitud(fila):
    return {
        "id": fila["id"],
        "estudiante_id": fila["estudiante_id"],
        "estudiante": fila["estudiante_nombre"],
        "legajo": fila["estudiante_legajo"],
        "tipo": fila["tipo"],
        "asunto": fila["asunto"],
        "descripcion": fila["descripcion"],
        "prioridad": fila["prioridad"],
        "estado": fila["estado"],
        "responsable_id": fila["responsable_id"],
        "responsable": fila["responsable_nombre"],
        "fecha_creacion": fila["fecha"],
        "fecha_actualizacion": fila["fecha_act"],
    }


def buscar_solicitud_completa(solicitud_id):
    cursor.execute(CONSULTA_SOLICITUD_COMPLETA + " WHERE s.id = ?", (solicitud_id,))
    fila = cursor.fetchone()
    if fila is None:
        raise HTTPException(404, "Solicitud no encontrada")
    return fila_a_solicitud(fila)


def buscar_solicitud(solicitud_id):
    cursor.execute("SELECT * FROM solicitudes WHERE id = ?", (solicitud_id,))
    solicitud = cursor.fetchone()
    if solicitud is None:
        raise HTTPException(404, "Solicitud no encontrada")
    return solicitud


def validar_nueva_solicitud(datos):
    if datos.get("estudiante_id") is None:
        raise HTTPException(400, "El estudiante es obligatorio")
    cursor.execute("SELECT id FROM estudiantes WHERE id = ?", (datos["estudiante_id"],))
    if cursor.fetchone() is None:
        raise HTTPException(404, "Estudiante no encontrado")
    if datos.get("tipo") not in TIPOS_VALIDOS:
        raise HTTPException(400, "Tipo de solicitud invalido")
    asunto = datos.get("asunto")
    if not asunto or len(asunto.strip()) < 5:
        raise HTTPException(400, "El asunto debe tener al menos 5 caracteres")
    if len(asunto) > 120:
        raise HTTPException(400, "El asunto no puede superar 120 caracteres")
    if datos.get("descripcion") and len(datos["descripcion"]) > 1000:
        raise HTTPException(400, "La descripcion no puede superar 1000 caracteres")


def calcular_prioridad(tipo, urgente):
    if tipo == "reclamo_nota":
        prioridad = "ALTA"
    elif tipo in ("equivalencia", "baja_materia"):
        prioridad = "MEDIA"
    else:
        prioridad = "BAJA"
    if urgente:
        prioridad = "MEDIA" if prioridad == "BAJA" else "ALTA"
    return prioridad


def guardar(estudiante_id, tipo, asunto, descripcion, prioridad, estado, responsable_id, fecha, fecha_act):
    cursor.execute(
        "INSERT INTO solicitudes (estudiante_id, tipo, asunto, descripcion, prioridad, estado, responsable_id, fecha, fecha_act) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (estudiante_id, tipo, asunto, descripcion, prioridad, estado, responsable_id, fecha, fecha_act),
    )
    conn.commit()
    return cursor.lastrowid


@app.get("/api/estudiantes")
def listar_estudiantes():
    cursor.execute("SELECT id, legajo, nombre, email, carrera FROM estudiantes")
    return [dict(fila) for fila in cursor.fetchall()]


@app.get("/api/responsables")
def listar_responsables():
    cursor.execute("SELECT id, nombre, area FROM responsables")
    return [dict(fila) for fila in cursor.fetchall()]


@app.post("/api/solicitudes", status_code=201)
async def registrar_solicitud(request: Request):
    datos = await request.json()
    validar_nueva_solicitud(datos)
    prioridad = calcular_prioridad(datos["tipo"], datos.get("urgente") is True)
    momento = ahora()
    descripcion = datos.get("descripcion") or ""
    nueva_id = guardar(datos["estudiante_id"], datos["tipo"], datos["asunto"].strip(), descripcion, prioridad, "PENDIENTE", None, momento, momento)
    return buscar_solicitud_completa(nueva_id)


@app.get("/api/solicitudes")
def buscar_solicitudes(estado: str = None, tipo: str = None, prioridad: str = None, texto: str = None):
    consulta = CONSULTA_SOLICITUD_COMPLETA + " WHERE 1=1"
    parametros = []
    for columna, valor in (("s.estado", estado), ("s.tipo", tipo), ("s.prioridad", prioridad)):
        if valor:
            consulta += f" AND {columna} = ?"
            parametros.append(valor)
    if texto:
        consulta += " AND (s.asunto LIKE ? OR e.nombre LIKE ? OR e.legajo LIKE ?)"
        parametros += [f"%{texto}%"] * 3
    cursor.execute(consulta + " ORDER BY s.id DESC", parametros)
    return [fila_a_solicitud(fila) for fila in cursor.fetchall()]


@app.get("/api/solicitudes/{solicitud_id}")
def obtener_solicitud(solicitud_id: int):
    return buscar_solicitud_completa(solicitud_id)


@app.patch("/api/solicitudes/{solicitud_id}/estado")
async def cambiar_estado(solicitud_id: int, request: Request):
    datos = await request.json()
    solicitud = buscar_solicitud(solicitud_id)
    nuevo_estado = datos.get("estado")
    if nuevo_estado not in ESTADOS_VALIDOS:
        raise HTTPException(400, "Estado invalido")
    estado_actual = solicitud["estado"]
    if estado_actual == "PENDIENTE":
        if nuevo_estado not in ("EN_PROCESO", "RECHAZADA"):
            raise HTTPException(409, f"No se puede pasar de {estado_actual} a {nuevo_estado}")
        if nuevo_estado == "EN_PROCESO" and solicitud["responsable_id"] is None:
            raise HTTPException(409, "La solicitud debe tener un responsable asignado")
    elif estado_actual == "EN_PROCESO":
        if nuevo_estado not in ("RESUELTA", "RECHAZADA"):
            raise HTTPException(409, f"No se puede pasar de {estado_actual} a {nuevo_estado}")
    else:
        raise HTTPException(409, f"No se puede pasar de {estado_actual} a {nuevo_estado}")
    cursor.execute("UPDATE solicitudes SET estado = ?, fecha_act = ? WHERE id = ?", (nuevo_estado, ahora(), solicitud_id))
    conn.commit()
    return buscar_solicitud_completa(solicitud_id)


@app.patch("/api/solicitudes/{solicitud_id}/responsable")
async def asignar_responsable(solicitud_id: int, request: Request):
    datos = await request.json()
    solicitud = buscar_solicitud(solicitud_id)
    if solicitud["estado"] in ESTADOS_FINALES:
        raise HTTPException(409, "No se puede asignar responsable a una solicitud cerrada")
    responsable_id = datos.get("responsable_id")
    cursor.execute("SELECT id FROM responsables WHERE id = ?", (responsable_id,))
    if cursor.fetchone() is None:
        raise HTTPException(404, "Responsable no encontrado")
    cursor.execute("UPDATE solicitudes SET responsable_id = ?, fecha_act = ? WHERE id = ?", (responsable_id, ahora(), solicitud_id))
    conn.commit()
    return buscar_solicitud_completa(solicitud_id)


@app.get("/api/reportes/resumen")
def generar_resumen():
    cursor.execute("SELECT * FROM solicitudes")
    solicitudes = cursor.fetchall()
    total = len(solicitudes)
    por_estado = {estado: 0 for estado in ESTADOS_VALIDOS}
    por_tipo = {}
    por_prioridad = {"BAJA": 0, "MEDIA": 0, "ALTA": 0}
    sin_responsable = 0
    for solicitud in solicitudes:
        por_estado[solicitud["estado"]] += 1
        por_tipo[solicitud["tipo"]] = por_tipo.get(solicitud["tipo"], 0) + 1
        por_prioridad[solicitud["prioridad"]] += 1
        if solicitud["responsable_id"] is None and solicitud["estado"] not in ESTADOS_FINALES:
            sin_responsable += 1
    porcentaje_resueltas = round(por_estado["RESUELTA"] * 100 / total, 2) if total else 0
    return {
        "total": total,
        "por_estado": por_estado,
        "por_tipo": por_tipo,
        "por_prioridad": por_prioridad,
        "sin_responsable": sin_responsable,
        "porcentaje_resueltas": porcentaje_resueltas,
    }
