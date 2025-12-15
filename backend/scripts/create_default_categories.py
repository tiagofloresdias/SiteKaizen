#!/usr/bin/env python3
"""
Script para criar categorias padrão de empresas
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.orm import Session
from app.db import SessionLocal, engine
from app.models.company import CompanyCategory
from app.db import Base

def create_categories():
    """Cria categorias padrão"""
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        categories_data = [
            {
                'name': 'Marketing Digital',
                'slug': 'marketing-digital',
                'description': 'Empresas de marketing digital e performance',
                'color': '#D62042',
            },
            {
                'name': 'CRM e Vendas',
                'slug': 'crm-vendas',
                'description': 'Soluções de CRM e gestão de vendas',
                'color': '#007bff',
            },
            {
                'name': 'Tecnologia',
                'slug': 'tecnologia',
                'description': 'Desenvolvimento de software e tecnologia',
                'color': '#00d084',
            },
            {
                'name': 'Educação',
                'slug': 'educacao',
                'description': 'Cursos, treinamentos e capacitação',
                'color': '#fcb900',
            },
            {
                'name': 'Consultoria',
                'slug': 'consultoria',
                'description': 'Consultoria e mentoria estratégica',
                'color': '#9b59b6',
            },
        ]
        
        for cat_data in categories_data:
            existing = db.query(CompanyCategory).filter(CompanyCategory.slug == cat_data['slug']).first()
            if not existing:
                category = CompanyCategory(**cat_data)
                db.add(category)
                print(f"✅ Categoria criada: {cat_data['name']}")
            else:
                print(f"⚠️  Categoria já existe: {cat_data['name']}")
        
        db.commit()
        print("\n✅ Categorias criadas com sucesso!")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Erro ao criar categorias: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_categories()

