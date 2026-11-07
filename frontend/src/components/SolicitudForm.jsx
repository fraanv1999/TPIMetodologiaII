import { useState } from "react";
import { TIPOS } from "../constants/dominio";

const FORMULARIO_INICIAL = { estudianteId: "", tipo: "certificado", asunto: "", descripcion: "", urgente: false };

export default function SolicitudForm({ estudiantes, onRegistrar, error }) {
  const [formulario, setFormulario] = useState(FORMULARIO_INICIAL);

  const actualizar = (campo) => (evento) => {
    const valor = evento.target.type === "checkbox" ? evento.target.checked : evento.target.value;
    setFormulario((anterior) => ({ ...anterior, [campo]: valor }));
  };

  async function enviar(evento) {
    evento.preventDefault();
    const registrada = await onRegistrar({
      estudiante_id: formulario.estudianteId ? Number(formulario.estudianteId) : null,
      tipo: formulario.tipo,
      asunto: formulario.asunto,
      descripcion: formulario.descripcion,
      urgente: formulario.urgente,
    });
    if (registrada) {
      setFormulario((anterior) => ({ ...FORMULARIO_INICIAL, estudianteId: anterior.estudianteId }));
    }
  }

  return (
    <form className="card" onSubmit={enviar}>
      <h2>Nueva solicitud</h2>
      <label htmlFor="estudiante">Estudiante</label>
      <select id="estudiante" value={formulario.estudianteId} onChange={actualizar("estudianteId")}>
        <option value="">Seleccionar...</option>
        {estudiantes.map((estudiante) => (
          <option key={estudiante.id} value={estudiante.id}>
            {estudiante.legajo} - {estudiante.nombre}
          </option>
        ))}
      </select>
      <label htmlFor="tipo">Tipo</label>
      <select id="tipo" value={formulario.tipo} onChange={actualizar("tipo")}>
        {TIPOS.map((tipo) => (
          <option key={tipo.valor} value={tipo.valor}>{tipo.etiqueta}</option>
        ))}
      </select>
      <label htmlFor="asunto">Asunto</label>
      <input id="asunto" value={formulario.asunto} onChange={actualizar("asunto")} />
      <label htmlFor="descripcion">Descripción</label>
      <textarea id="descripcion" value={formulario.descripcion} onChange={actualizar("descripcion")} />
      <label className="check" htmlFor="urgente">
        <input id="urgente" type="checkbox" checked={formulario.urgente} onChange={actualizar("urgente")} />
        <span>Urgente</span>
      </label>
      <div style={{ marginTop: 12 }}>
        <button type="submit">Registrar</button>
      </div>
      {error && <p className="error" role="alert">{error}</p>}
    </form>
  );
}
