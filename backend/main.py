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
c = conn.cursor()

c.execute("CREATE TABLE IF NOT EXISTS estudiantes (id INTEGER PRIMARY KEY AUTOINCREMENT, legajo TEXT, nombre TEXT, email TEXT, carrera TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS responsables (id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT, area TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS solicitudes (id INTEGER PRIMARY KEY AUTOINCREMENT, estudiante_id INTEGER, tipo TEXT, asunto TEXT, descripcion TEXT, prioridad TEXT, estado TEXT, responsable_id INTEGER, fecha TEXT, fecha_act TEXT)")
c.execute("SELECT COUNT(*) FROM estudiantes")
if c.fetchone()[0] == 0:
    c.execute("INSERT INTO estudiantes (legajo, nombre, email, carrera) VALUES ('10001', 'Ana Gomez', 'ana.gomez@example.com', 'TUP')")
    c.execute("INSERT INTO estudiantes (legajo, nombre, email, carrera) VALUES ('10002', 'Bruno Diaz', 'bruno.diaz@example.com', 'TUP')")
    c.execute("INSERT INTO estudiantes (legajo, nombre, email, carrera) VALUES ('10003', 'Carla Ruiz', 'carla.ruiz@example.com', 'TUP')")
    c.execute("INSERT INTO responsables (nombre, area) VALUES ('Laura Perez', 'Alumnado')")
    c.execute("INSERT INTO responsables (nombre, area) VALUES ('Martin Sosa', 'Coordinacion')")
    c.execute("INSERT INTO responsables (nombre, area) VALUES ('Julia Torres', 'Bedelia')")
    conn.commit()


@app.get("/api/estudiantes")
def estudiantes():
    c.execute("SELECT * FROM estudiantes")
    x = []
    for r in c.fetchall():
        x.append({"id": r["id"], "legajo": r["legajo"], "nombre": r["nombre"], "email": r["email"], "carrera": r["carrera"]})
    return x


@app.get("/api/responsables")
def responsables():
    c.execute("SELECT * FROM responsables")
    x = []
    for r in c.fetchall():
        x.append({"id": r["id"], "nombre": r["nombre"], "area": r["area"]})
    return x


def guardar(estudiante_id, tipo, asunto, descripcion, prioridad, estado, responsable_id, fecha, fecha_act):
    c.execute(
        "INSERT INTO solicitudes (estudiante_id, tipo, asunto, descripcion, prioridad, estado, responsable_id, fecha, fecha_act) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (estudiante_id, tipo, asunto, descripcion, prioridad, estado, responsable_id, fecha, fecha_act),
    )
    conn.commit()
    return c.lastrowid


@app.post("/api/solicitudes", status_code=201)
async def crear(request: Request):
    d = await request.json()
    if d.get("estudiante_id") is None:
        raise HTTPException(400, "El estudiante es obligatorio")
    c.execute("SELECT * FROM estudiantes WHERE id = ?", (d["estudiante_id"],))
    if c.fetchone() is None:
        raise HTTPException(404, "Estudiante no encontrado")
    if d.get("tipo") not in ["certificado", "equivalencia", "reclamo_nota", "baja_materia", "otro"]:
        raise HTTPException(400, "Tipo de solicitud invalido")
    if not d.get("asunto") or len(d["asunto"].strip()) < 5:
        raise HTTPException(400, "El asunto debe tener al menos 5 caracteres")
    if len(d["asunto"]) > 120:
        raise HTTPException(400, "El asunto no puede superar 120 caracteres")
    if d.get("descripcion") and len(d["descripcion"]) > 1000:
        raise HTTPException(400, "La descripcion no puede superar 1000 caracteres")
    p = ""
    if d["tipo"] == "certificado":
        p = "BAJA"
    elif d["tipo"] == "equivalencia":
        p = "MEDIA"
    elif d["tipo"] == "reclamo_nota":
        p = "ALTA"
    elif d["tipo"] == "baja_materia":
        p = "MEDIA"
    else:
        p = "BAJA"
    if d.get("urgente") == True:
        if p == "BAJA":
            p = "MEDIA"
        elif p == "MEDIA":
            p = "ALTA"
    ahora = datetime.now().replace(microsecond=0).isoformat()
    nuevo = guardar(d["estudiante_id"], d["tipo"], d["asunto"].strip(), d.get("descripcion") or "", p, "PENDIENTE", None, ahora, ahora)
    c.execute("SELECT s.*, e.nombre AS en, e.legajo AS el, r.nombre AS rn FROM solicitudes s JOIN estudiantes e ON s.estudiante_id = e.id LEFT JOIN responsables r ON s.responsable_id = r.id WHERE s.id = ?", (nuevo,))
    r = c.fetchone()
    return {"id": r["id"], "estudiante_id": r["estudiante_id"], "estudiante": r["en"], "legajo": r["el"], "tipo": r["tipo"], "asunto": r["asunto"], "descripcion": r["descripcion"], "prioridad": r["prioridad"], "estado": r["estado"], "responsable_id": r["responsable_id"], "responsable": r["rn"], "fecha_creacion": r["fecha"], "fecha_actualizacion": r["fecha_act"]}


@app.get("/api/solicitudes")
def listar(estado: str = None, tipo: str = None, prioridad: str = None, texto: str = None):
    q = "SELECT s.*, e.nombre AS en, e.legajo AS el, r.nombre AS rn FROM solicitudes s JOIN estudiantes e ON s.estudiante_id = e.id LEFT JOIN responsables r ON s.responsable_id = r.id WHERE 1=1"
    params = []
    if estado:
        q += " AND s.estado = ?"
        params.append(estado)
    if tipo:
        q += " AND s.tipo = ?"
        params.append(tipo)
    if prioridad:
        q += " AND s.prioridad = ?"
        params.append(prioridad)
    if texto:
        q += " AND (s.asunto LIKE ? OR e.nombre LIKE ? OR e.legajo LIKE ?)"
        params += ["%" + texto + "%"] * 3
    q += " ORDER BY s.id DESC"
    c.execute(q, params)
    data2 = []
    for r in c.fetchall():
        data2.append({"id": r["id"], "estudiante_id": r["estudiante_id"], "estudiante": r["en"], "legajo": r["el"], "tipo": r["tipo"], "asunto": r["asunto"], "descripcion": r["descripcion"], "prioridad": r["prioridad"], "estado": r["estado"], "responsable_id": r["responsable_id"], "responsable": r["rn"], "fecha_creacion": r["fecha"], "fecha_actualizacion": r["fecha_act"]})
    return data2


@app.get("/api/solicitudes/{id}")
def obtener(id: int):
    c.execute("SELECT s.*, e.nombre AS en, e.legajo AS el, r.nombre AS rn FROM solicitudes s JOIN estudiantes e ON s.estudiante_id = e.id LEFT JOIN responsables r ON s.responsable_id = r.id WHERE s.id = ?", (id,))
    r = c.fetchone()
    if r is None:
        raise HTTPException(404, "Solicitud no encontrada")
    return {"id": r["id"], "estudiante_id": r["estudiante_id"], "estudiante": r["en"], "legajo": r["el"], "tipo": r["tipo"], "asunto": r["asunto"], "descripcion": r["descripcion"], "prioridad": r["prioridad"], "estado": r["estado"], "responsable_id": r["responsable_id"], "responsable": r["rn"], "fecha_creacion": r["fecha"], "fecha_actualizacion": r["fecha_act"]}


@app.patch("/api/solicitudes/{id}/estado")
async def cambiar_estado(id: int, request: Request):
    d = await request.json()
    c.execute("SELECT * FROM solicitudes WHERE id = ?", (id,))
    x = c.fetchone()
    if x is None:
        raise HTTPException(404, "Solicitud no encontrada")
    e = d.get("estado")
    if e not in ["PENDIENTE", "EN_PROCESO", "RESUELTA", "RECHAZADA"]:
        raise HTTPException(400, "Estado invalido")
    if x["estado"] == "PENDIENTE":
        if e != "EN_PROCESO" and e != "RECHAZADA":
            raise HTTPException(409, "No se puede pasar de PENDIENTE a " + e)
        if e == "EN_PROCESO" and x["responsable_id"] is None:
            raise HTTPException(409, "La solicitud debe tener un responsable asignado")
    elif x["estado"] == "EN_PROCESO":
        if e != "RESUELTA" and e != "RECHAZADA":
            raise HTTPException(409, "No se puede pasar de EN_PROCESO a " + e)
    else:
        raise HTTPException(409, "No se puede pasar de " + x["estado"] + " a " + e)
    ahora = datetime.now().replace(microsecond=0).isoformat()
    c.execute("UPDATE solicitudes SET estado = ?, fecha_act = ? WHERE id = ?", (e, ahora, id))
    conn.commit()
    c.execute("SELECT s.*, e.nombre AS en, e.legajo AS el, r.nombre AS rn FROM solicitudes s JOIN estudiantes e ON s.estudiante_id = e.id LEFT JOIN responsables r ON s.responsable_id = r.id WHERE s.id = ?", (id,))
    r = c.fetchone()
    return {"id": r["id"], "estudiante_id": r["estudiante_id"], "estudiante": r["en"], "legajo": r["el"], "tipo": r["tipo"], "asunto": r["asunto"], "descripcion": r["descripcion"], "prioridad": r["prioridad"], "estado": r["estado"], "responsable_id": r["responsable_id"], "responsable": r["rn"], "fecha_creacion": r["fecha"], "fecha_actualizacion": r["fecha_act"]}


@app.patch("/api/solicitudes/{id}/responsable")
async def asignar(id: int, request: Request):
    d = await request.json()
    c.execute("SELECT * FROM solicitudes WHERE id = ?", (id,))
    x = c.fetchone()
    if x is None:
        raise HTTPException(404, "Solicitud no encontrada")
    if x["estado"] == "RESUELTA" or x["estado"] == "RECHAZADA":
        raise HTTPException(409, "No se puede asignar responsable a una solicitud cerrada")
    c.execute("SELECT * FROM responsables WHERE id = ?", (d.get("responsable_id"),))
    if c.fetchone() is None:
        raise HTTPException(404, "Responsable no encontrado")
    ahora = datetime.now().replace(microsecond=0).isoformat()
    c.execute("UPDATE solicitudes SET responsable_id = ?, fecha_act = ? WHERE id = ?", (d["responsable_id"], ahora, id))
    conn.commit()
    c.execute("SELECT s.*, e.nombre AS en, e.legajo AS el, r.nombre AS rn FROM solicitudes s JOIN estudiantes e ON s.estudiante_id = e.id LEFT JOIN responsables r ON s.responsable_id = r.id WHERE s.id = ?", (id,))
    r = c.fetchone()
    return {"id": r["id"], "estudiante_id": r["estudiante_id"], "estudiante": r["en"], "legajo": r["el"], "tipo": r["tipo"], "asunto": r["asunto"], "descripcion": r["descripcion"], "prioridad": r["prioridad"], "estado": r["estado"], "responsable_id": r["responsable_id"], "responsable": r["rn"], "fecha_creacion": r["fecha"], "fecha_actualizacion": r["fecha_act"]}


@app.get("/api/reportes/resumen")
def resumen():
    c.execute("SELECT * FROM solicitudes")
    todas = c.fetchall()
    t = len(todas)
    pe = {"PENDIENTE": 0, "EN_PROCESO": 0, "RESUELTA": 0, "RECHAZADA": 0}
    pt = {}
    pp = {"BAJA": 0, "MEDIA": 0, "ALTA": 0}
    sr = 0
    for s in todas:
        pe[s["estado"]] += 1
        pt[s["tipo"]] = pt.get(s["tipo"], 0) + 1
        pp[s["prioridad"]] += 1
        if s["responsable_id"] is None and s["estado"] != "RESUELTA" and s["estado"] != "RECHAZADA":
            sr += 1
    porc = 0
    if t > 0:
        porc = round(pe["RESUELTA"] * 100 / t, 2)
    return {"total": t, "por_estado": pe, "por_tipo": pt, "por_prioridad": pp, "sin_responsable": sr, "porcentaje_resueltas": porc}

