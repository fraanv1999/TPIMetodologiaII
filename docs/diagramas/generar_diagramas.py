import sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

OUT = sys.argv[1]
AZUL = "#1F4E79"; AZUL_C = "#DCE8F5"; GRIS = "#5B6577"; ROJO_C = "#FBE3E1"; ROJO = "#A11D1D"
VERDE_C = "#E3F4E8"; VERDE = "#1C6B37"; AMAR_C = "#FFF3D6"; AMAR = "#8A5A00"
plt.rcParams["font.family"] = "DejaVu Sans"


def caja(ax, x, y, w, h, texto, fc=AZUL_C, ec=AZUL, tc="#1D2433", fs=9, bold=False, r=0.02):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0.005,rounding_size={r}", fc=fc, ec=ec, lw=1.4))
    ax.text(x + w / 2, y + h / 2, texto, ha="center", va="center", fontsize=fs, color=tc,
            fontweight="bold" if bold else "normal", wrap=True)


def flecha(ax, x1, y1, x2, y2, color=GRIS, texto=None, fs=8, curva=0.0):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=12, color=color, lw=1.3,
                                 connectionstyle=f"arc3,rad={curva}"))
    if texto:
        ax.text((x1 + x2) / 2, (y1 + y2) / 2 + 0.012, texto, ha="center", va="bottom", fontsize=fs, color=color)


def lienzo(w, h):
    fig, ax = plt.subplots(figsize=(w, h), dpi=170)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    return fig, ax


# 1) Plan / hoja de ruta del TPI
fig, ax = lienzo(16.5, 7.2)
ax.text(0.5, 0.965, "Hoja de ruta del TPI: diagnóstico → mejora → verificación → comunicación", ha="center",
        fontsize=14, fontweight="bold", color=AZUL)
etapas = [
    ("1. Sistema base", "Dominio, actores,\nalcance, tecnología\nversión inicial", "estado-inicial"),
    ("2. Calidad externa\ne interna", "Qué ve el usuario vs\nqué ve el equipo", "etapa-diagnostico"),
    ("3. Deuda técnica\ny code smells", "≥ 8 problemas con\nevidencia, impacto,\nriesgo, prioridad", "etapa-diagnostico"),
    ("4. SOLID y\nClean Code", "SRP, OCP, DIP\nnombres, funciones,\nerrores, cohesión", "etapa-refactoring"),
    ("5. Refactoring\nseguro", "≥ 4 técnicas:\nExtract / Move Method\nParameter Object", "etapa-refactoring"),
    ("6. Pruebas y\nverificación", "Caracterización\nantes = después\n+ unitarias", "etapa-pruebas"),
    ("7. Code review", "Checklist, hallazgos,\ncorrecciones,\naceptación", "etapa-docs"),
    ("8. Conclusiones", "Aprendizajes,\nlímites, mejoras\nfuturas", "estado-refactorizado"),
]
fases = [("CONTEXTO", 0, 2, "#EEF2F8"), ("ANÁLISIS", 1, 3, "#FDF1F0"), ("MEJORA", 3, 5, "#EEF7F1"), ("VERIFICACIÓN Y CIERRE", 5, 8, "#FFF8E8")]
w, gap, x0, y = 0.105, 0.017, 0.03, 0.47
for i, (titulo, desc, tag) in enumerate(etapas):
    x = x0 + i * (w + gap)
    caja(ax, x, y + 0.17, w, 0.12, titulo, fc=AZUL, ec=AZUL, tc="white", fs=9, bold=True)
    caja(ax, x, y, w, 0.15, desc, fc="white", ec="#B9C6D8", fs=8)
    caja(ax, x + 0.003, y - 0.085, w - 0.006, 0.055, tag, fc=VERDE_C, ec=VERDE, tc=VERDE, fs=7.5)
    if i < len(etapas) - 1:
        flecha(ax, x + w, y + 0.23, x + w + gap, y + 0.23, color=AZUL)
for nombre, a, b, color in [("CONTEXTO", 0, 1, "#EEF2F8"), ("ANÁLISIS", 1, 3, "#FDF1F0"), ("MEJORA", 3, 5, "#EEF7F1"), ("VERIFICACIÓN Y CIERRE", 5, 8, "#FFF8E8")]:
    xa = x0 + a * (w + gap) - 0.005; xb = x0 + b * (w + gap) - gap + 0.005
    ax.add_patch(FancyBboxPatch((xa, 0.79), xb - xa, 0.07, boxstyle="round,pad=0.003,rounding_size=0.01", fc=color, ec="#C9D2DE"))
    ax.text((xa + xb) / 2, 0.825, nombre, ha="center", va="center", fontsize=10, fontweight="bold", color=GRIS)
ax.text(0.03, 0.335, "Tag Git que marca el hito de cada etapa", fontsize=8, color=VERDE, style="italic")
ent = [("Informe PDF único", "Portada, resumen 5-7 líneas,\netapas, evidencias, IA, enlaces"),
       ("Repositorio GitHub", "Versión inicial y refactorizada,\ntags, README, /docs, commits"),
       ("Anexo ZIP", "Capturas, diagramas, reportes\nde pruebas, prompts de IA"),
       ("Video 10-15 min", "Cámara y voz propias, demo,\ndiagnóstico, refactor, pruebas")]
ax.text(0.5, 0.27, "Entregables (se considera entregado sólo con los 4 cargados)", ha="center", fontsize=11,
        fontweight="bold", color=AZUL)
for i, (t, d) in enumerate(ent):
    x = 0.04 + i * 0.235
    caja(ax, x, 0.05, 0.215, 0.18, f"{t}\n\n{d}", fc=AMAR_C, ec=AMAR, fs=8.5)
fig.savefig(f"{OUT}/01_hoja_de_ruta_tpi.png", bbox_inches="tight", facecolor="white"); plt.close(fig)

# 2) Arquitectura antes / despues
fig, ax = lienzo(13, 6.6)
ax.text(0.22, 0.95, "ANTES (estado-inicial)", ha="center", fontsize=13, fontweight="bold", color=ROJO)
ax.text(0.71, 0.95, "DESPUÉS (estado-refactorizado)", ha="center", fontsize=13, fontweight="bold", color=VERDE)
caja(ax, 0.06, 0.78, 0.32, 0.09, "React: App.jsx (1 componente,\n15 useState, URL fija x7)", fc=ROJO_C, ec=ROJO, fs=9)
flecha(ax, 0.22, 0.78, 0.22, 0.71, color=ROJO)
ax.text(0.235, 0.745, "fetch directo", fontsize=8, color=ROJO, va="center")
caja(ax, 0.06, 0.2, 0.32, 0.5, "", fc=ROJO_C, ec=ROJO)
ax.text(0.22, 0.665, "main.py  (200 líneas)", ha="center", fontsize=10, fontweight="bold", color=ROJO)
for i, t in enumerate(["Endpoints HTTP", "Validación manual (Request crudo)", "Cálculo de prioridad (if/elif)",
                       "Reglas de estados (if/elif)", "SQL concatenado + conn global", "Armado de respuesta x5", "Reporte"]):
    caja(ax, 0.08, 0.6 - i * 0.055, 0.28, 0.045, t, fc="white", ec="#E0B4B0", fs=8)
caja(ax, 0.12, 0.06, 0.2, 0.08, "SQLite\n(sqlite3 directo)", fc="#F1F1F1", ec=GRIS, fs=8.5)
flecha(ax, 0.22, 0.2, 0.22, 0.14, color=ROJO)
ax.plot([0.455, 0.455], [0.05, 0.92], color="#C9D2DE", lw=1.5, ls="--")
capas = [
    ("React: App + 4 componentes + useSolicitudes + api/solicitudesApi.js", 0.81),
    ("routers/   → recibe Request, delega, devuelve Response Model", 0.67),
    ("schemas/   → DTOs: SolicitudCreate, FiltrosSolicitud, SolicitudResponse", 0.55),
    ("services/  → casos de uso: SolicitudService, ReporteService", 0.43),
    ("repositories/ → Protocol + implementación SQLModel (DIP)", 0.31),
]
for t, y0 in capas:
    caja(ax, 0.5, y0, 0.42, 0.075, t, fc=VERDE_C, ec=VERDE, fs=8.5)
for (_, ya), (_, yb) in zip(capas, capas[1:]):
    flecha(ax, 0.71, ya, 0.71, yb + 0.075, color=VERDE)
caja(ax, 0.935, 0.31, 0.06, 0.435, "domain/\nEnums\nReglas\nErrores\n\nmodels/\nSolicitud\n(reglas\nde la\nentidad)",
     fc=AZUL_C, ec=AZUL, fs=7.5)
caja(ax, 0.61, 0.15, 0.2, 0.08, "SQLite (SQLModel,\nconsultas parametrizadas)", fc="#F1F1F1", ec=GRIS, fs=8.5)
flecha(ax, 0.71, 0.31, 0.71, 0.23, color=VERDE)
ax.text(0.71, 0.065, "Manejo central de errores: DatoInvalido→400 · RecursoNoEncontrado→404 · ReglaDeNegocioViolada→409",
        ha="center", fontsize=8, color=GRIS)
fig.savefig(f"{OUT}/02_arquitectura_antes_despues.png", bbox_inches="tight", facecolor="white"); plt.close(fig)

# 3) Diagrama de clases
fig, ax = lienzo(12, 6.6)
ax.text(0.5, 0.96, "Modelo de dominio (versión refactorizada)", ha="center", fontsize=13, fontweight="bold", color=AZUL)


def clase(x, y, w, nombre, attrs, metodos=(), alto_linea=0.04, stereo=None):
    n = len(attrs) + len(metodos)
    h = 0.07 + n * alto_linea + (0.02 if metodos else 0)
    ax.add_patch(FancyBboxPatch((x, y - h), w, h, boxstyle="square,pad=0", fc="white", ec=AZUL, lw=1.4))
    ax.add_patch(FancyBboxPatch((x, y - 0.065), w, 0.065, boxstyle="square,pad=0", fc=AZUL, ec=AZUL))
    titulo = (f"«{stereo}»\n" if stereo else "") + nombre
    ax.text(x + w / 2, y - 0.0325, titulo, ha="center", va="center", color="white", fontsize=8.5 if stereo else 10, fontweight="bold")
    yy = y - 0.065 - alto_linea * 0.75
    for a in attrs:
        ax.text(x + 0.008, yy, a, fontsize=8, va="center", family="DejaVu Sans Mono"); yy -= alto_linea
    if metodos:
        ax.plot([x, x + w], [yy + alto_linea * 0.45, yy + alto_linea * 0.45], color=AZUL, lw=0.8); yy -= 0.01
        for m in metodos:
            ax.text(x + 0.008, yy, m, fontsize=8, va="center", family="DejaVu Sans Mono", color=VERDE); yy -= alto_linea
    return h


clase(0.03, 0.88, 0.22, "Estudiante", ["id: int", "legajo: str", "nombre: str", "email: str", "carrera: str"])
clase(0.03, 0.42, 0.22, "Responsable", ["id: int", "nombre: str", "area: str"])
clase(0.36, 0.88, 0.32, "Solicitud", ["id: int", "estudiante_id: int", "responsable_id: int?", "tipo / prioridad / estado",
                                      "asunto, descripcion: str", "fecha_creacion: datetime", "fecha_actualizacion: datetime"],
      ["estado_actual -> Estado", "cambiar_estado(nuevo, momento)", "validar_admite_asignacion()", "asignar_responsable(resp, momento)"])
clase(0.77, 0.88, 0.2, "Estado", ["PENDIENTE", "EN_PROCESO", "RESUELTA", "RECHAZADA"], ["puede_pasar_a(d)", "es_final", "desde_texto(v)"], stereo="enum")
clase(0.77, 0.4, 0.2, "Prioridad", ["BAJA, MEDIA, ALTA"], ["elevada()"], stereo="enum")
clase(0.47, 0.3, 0.22, "TipoSolicitud", ["certificado, equivalencia,", "reclamo_nota, baja_materia,", "otro"], stereo="enum")
flecha(ax, 0.36, 0.78, 0.25, 0.78, color=AZUL, texto="1   *")
flecha(ax, 0.36, 0.5, 0.25, 0.37, color=AZUL, texto="0..1   *")
flecha(ax, 0.68, 0.75, 0.77, 0.75, color=GRIS)
flecha(ax, 0.68, 0.45, 0.77, 0.33, color=GRIS)
flecha(ax, 0.58, 0.35, 0.58, 0.3, color=GRIS)
ax.text(0.03, 0.05, "Reglas puras: calcular_prioridad(tipo, urgente) en domain/reglas.py  ·  "
        "Servicios dependen de SolicitudRepository / CatalogoRepository (Protocol)", fontsize=8.5, color=GRIS)
fig.savefig(f"{OUT}/03_diagrama_de_clases.png", bbox_inches="tight", facecolor="white"); plt.close(fig)

# 4) Diagrama de estados
fig, ax = lienzo(10, 4.4)
ax.text(0.5, 0.94, "Ciclo de vida de una Solicitud", ha="center", fontsize=13, fontweight="bold", color=AZUL)
ax.add_patch(plt.Circle((0.05, 0.55), 0.02, color="#1D2433"))
caja(ax, 0.12, 0.47, 0.18, 0.16, "PENDIENTE", fs=10, bold=True)
caja(ax, 0.45, 0.47, 0.18, 0.16, "EN_PROCESO", fs=10, bold=True)
caja(ax, 0.78, 0.62, 0.18, 0.15, "RESUELTA", fc=VERDE_C, ec=VERDE, fs=10, bold=True)
caja(ax, 0.78, 0.2, 0.18, 0.15, "RECHAZADA", fc=ROJO_C, ec=ROJO, fs=10, bold=True)
flecha(ax, 0.07, 0.55, 0.12, 0.55, color="#1D2433")
ax.text(0.07, 0.42, "registrar\n(prioridad\nautomática)", fontsize=7.5, color=GRIS, ha="center")
flecha(ax, 0.30, 0.55, 0.45, 0.55, color=AZUL)
ax.text(0.375, 0.65, "Tomar\n[requiere responsable]", ha="center", va="bottom", fontsize=8, color=AZUL)
flecha(ax, 0.63, 0.58, 0.78, 0.69, color=VERDE, texto="Resolver")
flecha(ax, 0.63, 0.52, 0.78, 0.29, color=ROJO, texto="Rechazar")
flecha(ax, 0.21, 0.47, 0.78, 0.25, color=ROJO, curva=0.25)
ax.text(0.42, 0.12, "Rechazar", fontsize=8, color=ROJO)
ax.text(0.5, 0.03, "Estados finales (RESUELTA, RECHAZADA): no admiten cambios ni reasignación → HTTP 409",
        ha="center", fontsize=8.5, color=GRIS)
fig.savefig(f"{OUT}/04_diagrama_de_estados.png", bbox_inches="tight", facecolor="white"); plt.close(fig)

# 5) Flujo de un request (apunte CRUD persistente)
fig, ax = lienzo(12, 2.6)
pasos = [("Request\nPOST /api/solicitudes", AZUL_C, AZUL), ("Validación\nSolicitudCreate (DTO)\n400 si falla", AMAR_C, AMAR),
         ("Service\nreglas + prioridad\n404 / 409", AZUL_C, AZUL), ("Commit\nRepository\nadd/commit/refresh", VERDE_C, VERDE),
         ("Response Model\nSolicitudResponse\n201", AZUL_C, AZUL)]
for i, (t, fc, ec) in enumerate(pasos):
    x = 0.02 + i * 0.198
    caja(ax, x, 0.2, 0.165, 0.6, t, fc=fc, ec=ec, fs=9)
    if i < len(pasos) - 1:
        flecha(ax, x + 0.165, 0.5, x + 0.198, 0.5, color=AZUL)
fig.savefig(f"{OUT}/05_flujo_request.png", bbox_inches="tight", facecolor="white"); plt.close(fig)
print("ok")
