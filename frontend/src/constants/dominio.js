// Vocabulario del dominio compartido por los componentes (CS-08).
export const TIPOS = [
  { valor: "certificado", etiqueta: "Certificado" },
  { valor: "equivalencia", etiqueta: "Equivalencia" },
  { valor: "reclamo_nota", etiqueta: "Reclamo de nota" },
  { valor: "baja_materia", etiqueta: "Baja de materia" },
  { valor: "otro", etiqueta: "Otro" },
];

export const ESTADOS = {
  PENDIENTE: "PENDIENTE",
  EN_PROCESO: "EN_PROCESO",
  RESUELTA: "RESUELTA",
  RECHAZADA: "RECHAZADA",
};

export const PRIORIDADES = ["ALTA", "MEDIA", "BAJA"];

export const ESTADOS_FINALES = [ESTADOS.RESUELTA, ESTADOS.RECHAZADA];

// Acciones disponibles en la interfaz segun el estado actual.
export const ACCIONES_POR_ESTADO = {
  [ESTADOS.PENDIENTE]: [
    { destino: ESTADOS.EN_PROCESO, etiqueta: "Tomar" },
    { destino: ESTADOS.RECHAZADA, etiqueta: "Rechazar", secundaria: true },
  ],
  [ESTADOS.EN_PROCESO]: [
    { destino: ESTADOS.RESUELTA, etiqueta: "Resolver" },
    { destino: ESTADOS.RECHAZADA, etiqueta: "Rechazar", secundaria: true },
  ],
  [ESTADOS.RESUELTA]: [],
  [ESTADOS.RECHAZADA]: [],
};

export const etiquetaDeTipo = (valor) => TIPOS.find((t) => t.valor === valor)?.etiqueta ?? valor;
