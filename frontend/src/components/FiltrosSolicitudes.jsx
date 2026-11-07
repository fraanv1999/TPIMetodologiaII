import { ESTADOS, PRIORIDADES, TIPOS } from "../constants/dominio";

export default function FiltrosSolicitudes({ filtros, onCambiar }) {
  const actualizar = (campo) => (evento) => onCambiar({ ...filtros, [campo]: evento.target.value });

  return (
    <div className="filters">
      <select aria-label="Filtrar por estado" value={filtros.estado} onChange={actualizar("estado")}>
        <option value="">Estado (todos)</option>
        {Object.values(ESTADOS).map((estado) => (
          <option key={estado} value={estado}>{estado}</option>
        ))}
      </select>
      <select aria-label="Filtrar por tipo" value={filtros.tipo} onChange={actualizar("tipo")}>
        <option value="">Tipo (todos)</option>
        {TIPOS.map((tipo) => (
          <option key={tipo.valor} value={tipo.valor}>{tipo.etiqueta}</option>
        ))}
      </select>
      <select aria-label="Filtrar por prioridad" value={filtros.prioridad} onChange={actualizar("prioridad")}>
        <option value="">Prioridad (todas)</option>
        {PRIORIDADES.map((prioridad) => (
          <option key={prioridad} value={prioridad}>{prioridad}</option>
        ))}
      </select>
      <input aria-label="Buscar" placeholder="Buscar..." value={filtros.texto} onChange={actualizar("texto")} />
    </div>
  );
}
