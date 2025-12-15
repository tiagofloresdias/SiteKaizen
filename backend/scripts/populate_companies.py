#!/usr/bin/env python3
"""
Script para popular empresas do Grupo Kaizen
Baseado no site original agenciakaizen.com.br/nossas-empresas
"""
import sys
import os
from pathlib import Path

# Adicionar o diretório backend ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Configurar variáveis de ambiente
os.environ.setdefault('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/agenciakaizen')

from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.company import Company, CompanyCategory

def create_categories(db: Session):
    """Cria categorias de empresas"""
    categories_data = [
        {
            "name": "Marketing Digital",
            "slug": "marketing-digital",
            "description": "Empresas especializadas em marketing digital e performance"
        },
        {
            "name": "Tecnologia",
            "slug": "tecnologia",
            "description": "Empresas de desenvolvimento e tecnologia"
        },
        {
            "name": "Inside Sales",
            "slug": "inside-sales",
            "description": "Empresas especializadas em vendas internas"
        }
    ]
    
    categories = {}
    for cat_data in categories_data:
        # Verificar se já existe
        existing = db.query(CompanyCategory).filter(CompanyCategory.slug == cat_data['slug']).first()
        if existing:
            categories[cat_data['slug']] = existing
        else:
            category = CompanyCategory(**cat_data)
            db.add(category)
            db.flush()
            categories[cat_data['slug']] = category
    
    db.commit()
    return categories

def populate_companies(db: Session):
    """Popula empresas do Grupo Kaizen"""
    
    # Criar categorias primeiro
    categories = create_categories(db)
    
    companies_data = [
        {
            "name": "Agência Kaizen",
            "slug": "agencia-kaizen",
            "tagline": "Marketing Digital de Alta Performance",
            "description": "<p>A <strong>Agência Kaizen</strong> é a principal empresa do grupo, especializada em marketing digital de performance. Google Partner Premier, ajudamos empresas a escalar suas vendas com estratégias afiadas, dados precisos e um time de elite.</p><p>Desde 2015, já ajudamos mais de 1.000 empresas a crescerem exponencialmente.</p>",
            "logo_url": "/img/logos/logo@3x.webp",
            "featured_image_url": "/img/backgrounds/PRINCIPAL-COM-SOBRA_3x.webp",
            "category_id": categories['marketing-digital'].id,
            "website_url": "https://agenciakaizen.com.br",
            "contact_email": "contato@agenciakaizen.com.br",
            "phone": "0800-550-8000",
            "is_active": True,
            "order": 1,
            "meta_description": "Agência Kaizen - Marketing Digital de Alta Performance. Google Partner Premier desde 2015.",
            "founded_date": "2015-01-01"
        },
        {
            "name": "Leadspot",
            "slug": "leadspot",
            "tagline": "Geração de Leads Qualificados",
            "description": "<p><strong>Leadspot</strong> é a empresa do grupo especializada em geração de leads qualificados B2B. Utilizamos tecnologia de ponta e estratégias data-driven para conectar empresas aos seus clientes ideais.</p><p>Nossa plataforma proprietária identifica, qualifica e nutre leads até que estejam prontos para a conversão.</p>",
            "logo_url": "/img/logos/logo2_3x.webp",
            "featured_image_url": "/img/content/grafico_3x-scaled.webp",
            "category_id": categories['marketing-digital'].id,
            "website_url": "https://leadspot.com.br",
            "contact_email": "contato@leadspot.com.br",
            "is_active": True,
            "order": 2,
            "meta_description": "Leadspot - Geração de leads qualificados B2B com tecnologia de ponta.",
        },
        {
            "name": "Unimed Leads",
            "slug": "unimed-leads",
            "tagline": "Leads Exclusivos para Unimed",
            "description": "<p><strong>Unimed Leads</strong> é nossa empresa especializada em geração de leads para o setor de saúde, focada em cooperativas Unimed em todo o Brasil.</p><p>Desenvolvemos estratégias customizadas que geram leads qualificados para planos de saúde, aumentando a base de beneficiários das cooperativas parceiras.</p>",
            "logo_url": "/img/logos/2Logo_unimed1_3x.webp",
            "featured_image_url": "/img/content/1Black-White-1_3x.webp",
            "category_id": categories['marketing-digital'].id,
            "website_url": "https://unimedleads.com.br",
            "contact_email": "contato@unimedleads.com.br",
            "is_active": True,
            "order": 3,
            "meta_description": "Unimed Leads - Geração de leads exclusivos para cooperativas Unimed.",
        },
        {
            "name": "Kaizen Academy",
            "slug": "kaizen-academy",
            "tagline": "Educação e Capacitação em Marketing Digital",
            "description": "<p>A <strong>Kaizen Academy</strong> é nossa escola de marketing digital, oferecendo cursos, workshops e treinamentos para profissionais e empresas que desejam dominar as melhores práticas do mercado.</p><p>Formamos centenas de profissionais certificados em marketing digital, inside sales e growth hacking.</p>",
            "logo_url": "/img/logos/3Copia-de-_Logotipo-03-copia_3x.webp",
            "featured_image_url": "/img/backgrounds/group-young-professionals-working-computers-modern-office_3x-scaled.webp",
            "category_id": categories['marketing-digital'].id,
            "website_url": "https://academy.agenciakaizen.com.br",
            "contact_email": "academy@agenciakaizen.com.br",
            "is_active": True,
            "order": 4,
            "meta_description": "Kaizen Academy - Educação e capacitação em marketing digital de performance.",
        },
        {
            "name": "Kaizen Tech",
            "slug": "kaizen-tech",
            "tagline": "Desenvolvimento de Software e Automação",
            "description": "<p><strong>Kaizen Tech</strong> é o braço de tecnologia do grupo, especializado em desenvolvimento de software customizado, automação de marketing e integrações complexas.</p><p>Criamos plataformas proprietárias que potencializam os resultados de marketing e vendas das empresas parceiras.</p>",
            "logo_url": "/img/logos/monday.com-white-logo-300x87_3x.webp",
            "featured_image_url": "/img/backgrounds/view-futuristic-space-rocket_3x-scaled.webp",
            "category_id": categories['tecnologia'].id,
            "website_url": "https://tech.agenciakaizen.com.br",
            "contact_email": "tech@agenciakaizen.com.br",
            "is_active": True,
            "order": 5,
            "meta_description": "Kaizen Tech - Desenvolvimento de software e automação de marketing.",
        },
        {
            "name": "Kaizen Inside Sales",
            "slug": "kaizen-inside-sales",
            "tagline": "Terceirização de SDRs e Closers",
            "description": "<p><strong>Kaizen Inside Sales</strong> oferece times completos de SDRs (Sales Development Representatives) e closers para empresas que desejam escalar suas vendas sem aumentar custos fixos.</p><p>Nossos profissionais são treinados pela Kaizen Academy e utilizam as melhores ferramentas e processos do mercado.</p>",
            "logo_url": "/img/logos/logo@3x.webp",
            "featured_image_url": "/img/backgrounds/businessmen-handshake_3x-scaled.webp",
            "category_id": categories['inside-sales'].id,
            "website_url": "https://insidesales.agenciakaizen.com.br",
            "contact_email": "sales@agenciakaizen.com.br",
            "is_active": True,
            "order": 6,
            "meta_description": "Kaizen Inside Sales - Terceirização de SDRs e Closers para empresas B2B.",
        }
    ]
    
    print("🚀 Populando empresas do Grupo Kaizen...\n")
    
    for company_data in companies_data:
        # Verificar se já existe
        existing = db.query(Company).filter(Company.slug == company_data['slug']).first()
        
        if existing:
            print(f"⚠️  {company_data['name']} já existe, atualizando...")
            for key, value in company_data.items():
                setattr(existing, key, value)
        else:
            print(f"✅ Criando {company_data['name']}...")
            company = Company(**company_data)
            db.add(company)
    
    db.commit()
    print(f"\n✅ {len(companies_data)} empresas criadas/atualizadas com sucesso!")

def main():
    db = SessionLocal()
    try:
        populate_companies(db)
    finally:
        db.close()

if __name__ == "__main__":
    main()

