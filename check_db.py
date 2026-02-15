#!/usr/bin/env python3
"""Script para revisar los proyectos en la BD principal"""
from app.core.database import SessionLocal
from app.models.project import Project

db = SessionLocal()
projects = db.query(Project).all()

print(f"\n📊 Total de proyectos en la BD: {len(projects)}\n")
for p in projects:
    print(f"  ID: {p.id} | Título: {p.titulo} | Líder: {p.lider}")

db.close()
print("\n✅ Diagnóstico completado.\n")
