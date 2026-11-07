import FiltrosSolicitudes from "./components/FiltrosSolicitudes";
import ResumenCards from "./components/ResumenCards";
import SolicitudForm from "./components/SolicitudForm";
import TablaSolicitudes from "./components/TablaSolicitudes";
import { useSolicitudes } from "./hooks/useSolicitudes";

export default function App() {
  const {
    solicitudes, resumen, estudiantes, responsables, filtros, setFiltros, error,
    registrar, cambiarEstado, asignarResponsable,
  } = useSolicitudes();

  return (
    <div className="app">
      <h1>Gestión de Solicitudes Académicas</h1>
      <p className="sub">Registrar, clasificar, asignar y seguir solicitudes de estudiantes</p>
      <ResumenCards resumen={resumen} />
      <div className="grid" style={{ marginTop: 16 }}>
        <SolicitudForm estudiantes={estudiantes} onRegistrar={registrar} error={error} />
        <section className="card">
          <h2>Solicitudes</h2>
          <FiltrosSolicitudes filtros={filtros} onCambiar={setFiltros} />
          <TablaSolicitudes
            solicitudes={solicitudes}
            responsables={responsables}
            onAsignar={asignarResponsable}
            onCambiarEstado={cambiarEstado}
          />
        </section>
      </div>
    </div>
  );
}
