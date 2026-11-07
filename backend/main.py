"""Punto de entrada: `uvicorn main:app --reload` (se mantiene el mismo comando que la version inicial)."""
from app.main import app

__all__ = ["app"]
