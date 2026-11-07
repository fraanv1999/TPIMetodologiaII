export default function ResumenCards({ resumen }) {
  if (!resumen) return null;
  const tarjetas = [
    { valor: resumen.total, etiqueta: "Total" },
    { valor: resumen.por_estado.PENDIENTE, etiqueta: "Pendientes" },
    { valor: resumen.sin_responsable, etiqueta: "Sin responsable" },
    { valor: `${resumen.porcentaje_resueltas}%`, etiqueta: "Resueltas" },
  ];
  return (
    <div className="stats">
      {tarjetas.map((tarjeta) => (
        <div className="stat" key={tarjeta.etiqueta}>
          <b>{tarjeta.valor}</b>
          <span>{tarjeta.etiqueta}</span>
        </div>
      ))}
    </div>
  );
}
