// Unico punto de acceso HTTP (CS-13). La URL base se configura por entorno.
const API_BASE = import.meta.env.VITE_API_URL ?? "";

async function request(path, { method = "GET", body } = {}) {
  const response = await fetch(`${API_BASE}${path}`, {
    method,
    headers: body ? { "Content-Type": "application/json" } : undefined,
    body: body ? JSON.stringify(body) : undefined,
  });
  const data = await response.json().catch(() => null);
  if (!response.ok) {
    throw new Error(data?.detail ?? `Error ${response.status}`);
  }
  return data;
}

function aQueryString(filtros) {
  const params = new URLSearchParams();
  Object.entries(filtros).forEach(([clave, valor]) => {
    if (valor) params.append(clave, valor);
  });
  const query = params.toString();
  return query ? `?${query}` : "";
}

export const solicitudesApi = {
  listarEstudiantes: () => request("/api/estudiantes"),
  listarResponsables: () => request("/api/responsables"),
  buscar: (filtros) => request(`/api/solicitudes${aQueryString(filtros)}`),
  registrar: (solicitud) => request("/api/solicitudes", { method: "POST", body: solicitud }),
  cambiarEstado: (id, estado) => request(`/api/solicitudes/${id}/estado`, { method: "PATCH", body: { estado } }),
  asignarResponsable: (id, responsableId) =>
    request(`/api/solicitudes/${id}/responsable`, { method: "PATCH", body: { responsable_id: responsableId } }),
  resumen: () => request("/api/reportes/resumen"),
};
