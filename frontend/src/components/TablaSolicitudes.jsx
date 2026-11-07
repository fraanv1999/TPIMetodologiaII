import { ACCIONES_POR_ESTADO, ESTADOS_FINALES, etiquetaDeTipo } from "../constants/dominio";

function AccionesSolicitud({ solicitud, responsables, onAsignar, onCambiarEstado }) {
  const cerrada = ESTADOS_FINALES.includes(solicitud.estado);
  return (
    <div className="actions">
      {!cerrada && (
        <select
          aria-label={`Asignar responsable a la solicitud ${solicitud.id}`}
          value={solicitud.responsable_id ?? ""}
          onChange={(evento) => onAsignar(solicitud.id, Number(evento.target.value))}
        >
          <option value="" disabled>Asignar...</option>
          {responsables.map((responsable) => (
            <option key={responsable.id} value={responsable.id}>
              {responsable.nombre} ({responsable.area})
            </option>
          ))}
        </select>
      )}
      {ACCIONES_POR_ESTADO[solicitud.estado].map((accion) => (
        <button
          key={accion.destino}
          className={accion.secundaria ? "secondary" : undefined}
          onClick={() => onCambiarEstado(solicitud.id, accion.destino)}
        >
          {accion.etiqueta}
        </button>
      ))}
    </div>
  );
}

export default function TablaSolicitudes({ solicitudes, responsables, onAsignar, onCambiarEstado }) {
  return (
    <div className="table-wrap">
      <table>
        <thead>
          <tr>
            <th>#</th><th>Estudiante</th><th>Tipo</th><th>Asunto</th>
            <th>Prioridad</th><th>Estado</th><th>Responsable</th><th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          {solicitudes.map((solicitud) => (
            <tr key={solicitud.id}>
              <td>{solicitud.id}</td>
              <td>{solicitud.legajo} - {solicitud.estudiante}</td>
              <td>{etiquetaDeTipo(solicitud.tipo)}</td>
              <td>{solicitud.asunto}</td>
              <td><span className={`badge ${solicitud.prioridad}`}>{solicitud.prioridad}</span></td>
              <td><span className="badge estado">{solicitud.estado}</span></td>
              <td>{solicitud.responsable ?? "-"}</td>
              <td>
                <AccionesSolicitud
                  solicitud={solicitud}
                  responsables={responsables}
                  onAsignar={onAsignar}
                  onCambiarEstado={onCambiarEstado}
                />
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
