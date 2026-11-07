import { useCallback, useEffect, useState } from "react";
import { solicitudesApi } from "../api/solicitudesApi";

export const FILTROS_VACIOS = { estado: "", tipo: "", prioridad: "", texto: "" };

// Estado y efectos de la pantalla separados de la presentacion (CS-12).
export function useSolicitudes() {
  const [solicitudes, setSolicitudes] = useState([]);
  const [resumen, setResumen] = useState(null);
  const [estudiantes, setEstudiantes] = useState([]);
  const [responsables, setResponsables] = useState([]);
  const [filtros, setFiltros] = useState(FILTROS_VACIOS);
  const [error, setError] = useState("");

  const recargar = useCallback(async () => {
    try {
      const [lista, nuevoResumen] = await Promise.all([solicitudesApi.buscar(filtros), solicitudesApi.resumen()]);
      setSolicitudes(lista);
      setResumen(nuevoResumen);
    } catch (e) {
      setError(e.message);
    }
  }, [filtros]);

  useEffect(() => {
    Promise.all([solicitudesApi.listarEstudiantes(), solicitudesApi.listarResponsables()])
      .then(([listaEstudiantes, listaResponsables]) => {
        setEstudiantes(listaEstudiantes);
        setResponsables(listaResponsables);
      })
      .catch((e) => setError(e.message));
  }, []);

  useEffect(() => {
    recargar();
  }, [recargar]);

  const ejecutar = useCallback(
    async (operacion) => {
      setError("");
      try {
        await operacion();
        await recargar();
        return true;
      } catch (e) {
        setError(e.message);
        return false;
      }
    },
    [recargar]
  );

  return {
    solicitudes,
    resumen,
    estudiantes,
    responsables,
    filtros,
    setFiltros,
    error,
    registrar: (datos) => ejecutar(() => solicitudesApi.registrar(datos)),
    cambiarEstado: (id, estado) => ejecutar(() => solicitudesApi.cambiarEstado(id, estado)),
    asignarResponsable: (id, responsableId) => ejecutar(() => solicitudesApi.asignarResponsable(id, responsableId)),
  };
}
