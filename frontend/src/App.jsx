import { useEffect, useState } from "react";

export default function App() {
  const [solicitudes, setSolicitudes] = useState([]);
  const [resumen, setResumen] = useState(null);
  const [estudiantes, setEstudiantes] = useState([]);
  const [responsables, setResponsables] = useState([]);
  const [f1, setF1] = useState("");
  const [f2, setF2] = useState("");
  const [f3, setF3] = useState("");
  const [f4, setF4] = useState("");
  const [estudianteId, setEstudianteId] = useState("");
  const [tipo, setTipo] = useState("certificado");
  const [asunto, setAsunto] = useState("");
  const [descripcion, setDescripcion] = useState("");
  const [urgente, setUrgente] = useState(false);
  const [error, setError] = useState("");
  const [ok, setOk] = useState("");

  useEffect(() => {
    fetch("http://127.0.0.1:8000/api/estudiantes").then((r) => r.json()).then((d) => setEstudiantes(d));
    fetch("http://127.0.0.1:8000/api/responsables").then((r) => r.json()).then((d) => setResponsables(d));
  }, []);

  function cargar() {
    let url = "http://127.0.0.1:8000/api/solicitudes?";
    if (f1) url += "estado=" + f1 + "&";
    if (f2) url += "tipo=" + f2 + "&";
    if (f3) url += "prioridad=" + f3 + "&";
    if (f4) url += "texto=" + f4;
    fetch(url).then((r) => r.json()).then((d) => setSolicitudes(d));
    fetch("http://127.0.0.1:8000/api/reportes/resumen").then((r) => r.json()).then((d) => setResumen(d));
  }

  useEffect(() => {
    cargar();
  }, [f1, f2, f3, f4]);

  function registrar(e) {
    e.preventDefault();
    setError("");
    setOk("");
    fetch("http://127.0.0.1:8000/api/solicitudes", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        estudiante_id: estudianteId ? Number(estudianteId) : null,
        tipo: tipo,
        asunto: asunto,
        descripcion: descripcion,
        urgente: urgente,
      }),
    }).then((r) => {
      if (r.status !== 201) {
        r.json().then((d) => setError(d.detail));
      } else {
        setOk("Solicitud registrada");
        setTipo("certificado");
        setAsunto("");
        setDescripcion("");
        setUrgente(false);
        cargar();
      }
    });
  }

  function cambiarEstado(id, estado) {
    setError("");
    fetch("http://127.0.0.1:8000/api/solicitudes/" + id + "/estado", {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ estado: estado }),
    }).then((r) => {
      if (r.status !== 200) {
        r.json().then((d) => setError(d.detail));
      } else {
        cargar();
      }
    });
  }

  function asignar(id, responsableId) {
    setError("");
    fetch("http://127.0.0.1:8000/api/solicitudes/" + id + "/responsable", {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ responsable_id: Number(responsableId) }),
    }).then((r) => {
      if (r.status !== 200) {
        r.json().then((d) => setError(d.detail));
      } else {
        cargar();
      }
    });
  }

  return (
    <div className="app">
      <h1>Gestión de Solicitudes Académicas</h1>
      <p className="sub">Registrar, clasificar, asignar y seguir solicitudes de estudiantes</p>
      {resumen && (
        <div className="stats">
          <div className="stat"><b>{resumen.total}</b><span>Total</span></div>
          <div className="stat"><b>{resumen.por_estado.PENDIENTE}</b><span>Pendientes</span></div>
          <div className="stat"><b>{resumen.sin_responsable}</b><span>Sin responsable</span></div>
          <div className="stat"><b>{resumen.porcentaje_resueltas}%</b><span>Resueltas</span></div>
        </div>
      )}
      <div className="grid" style={{ marginTop: 16 }}>
        <form className="card" onSubmit={registrar}>
          <h2>Nueva solicitud</h2>
          <label>Estudiante</label>
          <select value={estudianteId} onChange={(e) => setEstudianteId(e.target.value)}>
            <option value="">Seleccionar...</option>
            {estudiantes.map((x) => (
              <option key={x.id} value={x.id}>{x.legajo} - {x.nombre}</option>
            ))}
          </select>
          <label>Tipo</label>
          <select value={tipo} onChange={(e) => setTipo(e.target.value)}>
            <option value="certificado">Certificado</option>
            <option value="equivalencia">Equivalencia</option>
            <option value="reclamo_nota">Reclamo de nota</option>
            <option value="baja_materia">Baja de materia</option>
            <option value="otro">Otro</option>
          </select>
          <label>Asunto</label>
          <input value={asunto} onChange={(e) => setAsunto(e.target.value)} />
          <label>Descripción</label>
          <textarea value={descripcion} onChange={(e) => setDescripcion(e.target.value)} />
          <label className="check">
            <input type="checkbox" checked={urgente} onChange={(e) => setUrgente(e.target.checked)} />
            <span>Urgente</span>
          </label>
          <div style={{ marginTop: 12 }}>
            <button type="submit">Registrar</button>
          </div>
          {error && <p className="error">{error}</p>}
          {ok && <p>{ok}</p>}
        </form>
        <section className="card">
          <h2>Solicitudes</h2>
          <div className="filters">
            <select value={f1} onChange={(e) => setF1(e.target.value)}>
              <option value="">Estado (todos)</option>
              <option value="PENDIENTE">PENDIENTE</option>
              <option value="EN_PROCESO">EN_PROCESO</option>
              <option value="RESUELTA">RESUELTA</option>
              <option value="RECHAZADA">RECHAZADA</option>
            </select>
            <select value={f2} onChange={(e) => setF2(e.target.value)}>
              <option value="">Tipo (todos)</option>
              <option value="certificado">Certificado</option>
              <option value="equivalencia">Equivalencia</option>
              <option value="reclamo_nota">Reclamo de nota</option>
              <option value="baja_materia">Baja de materia</option>
              <option value="otro">Otro</option>
            </select>
            <select value={f3} onChange={(e) => setF3(e.target.value)}>
              <option value="">Prioridad (todas)</option>
              <option value="ALTA">ALTA</option>
              <option value="MEDIA">MEDIA</option>
              <option value="BAJA">BAJA</option>
            </select>
            <input placeholder="Buscar..." value={f4} onChange={(e) => setF4(e.target.value)} />
          </div>
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>#</th><th>Estudiante</th><th>Tipo</th><th>Asunto</th>
                  <th>Prioridad</th><th>Estado</th><th>Responsable</th><th>Acciones</th>
                </tr>
              </thead>
              <tbody>
                {solicitudes.map((s) => (
                  <tr key={s.id}>
                    <td>{s.id}</td>
                    <td>{s.legajo} - {s.estudiante}</td>
                    <td>{s.tipo}</td>
                    <td>{s.asunto}</td>
                    <td><span className={"badge " + s.prioridad}>{s.prioridad}</span></td>
                    <td><span className="badge estado">{s.estado}</span></td>
                    <td>{s.responsable ? s.responsable : "-"}</td>
                    <td>
                      <div className="actions">
                        {s.estado !== "RESUELTA" && s.estado !== "RECHAZADA" && (
                          <select value={s.responsable_id ? s.responsable_id : ""} onChange={(e) => asignar(s.id, e.target.value)}>
                            <option value="" disabled>Asignar...</option>
                            {responsables.map((x) => (
                              <option key={x.id} value={x.id}>{x.nombre} ({x.area})</option>
                            ))}
                          </select>
                        )}
                        {s.estado === "PENDIENTE" && <button onClick={() => cambiarEstado(s.id, "EN_PROCESO")}>Tomar</button>}
                        {s.estado === "EN_PROCESO" && <button onClick={() => cambiarEstado(s.id, "RESUELTA")}>Resolver</button>}
                        {(s.estado === "PENDIENTE" || s.estado === "EN_PROCESO") && (
                          <button className="secondary" onClick={() => cambiarEstado(s.id, "RECHAZADA")}>Rechazar</button>
                        )}
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>
      </div>
    </div>
  );
}
