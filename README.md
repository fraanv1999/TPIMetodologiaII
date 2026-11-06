# SGSA – Sistema de Gestión de Solicitudes Académicas

Trabajo Práctico Integrador – **Metodología de Sistemas II** (TUP a distancia, UTN).

Sistema simple para registrar solicitudes de estudiantes, clasificarlas por tipo, prioridad y estado,
asignar responsables, consultarlas y obtener un reporte.

> Esta es la **versión inicial** (tag `estado-inicial`): funciona, pero tiene problemas de diseño
> que se analizan y corrigen en las etapas siguientes del trabajo.

## Uso

```bash
# Backend (http://127.0.0.1:8000, documentación en /docs)
cd backend
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend (http://localhost:5173) – en otra terminal
cd frontend
npm install
npm run dev
```
