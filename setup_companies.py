#!/usr/bin/env python3
"""
Script para configurar empresas do Grupo Kaizen
Agência Kaizen - Sistema de Empresas
"""

import os
import sys
from pathlib import Path

# Adicionar o diretório src ao path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agenciakaizen_cms.settings.dev')
import django
django.setup()

from companies.models import CompanyCategory, Company, CompaniesIndexPage
from home.models import HomePage


def create_categories():
    """Criar categorias de empresas"""
    categories_data = [
        {
            'name': 'CRM e Vendas',
            'slug': 'crm-vendas',
            'description': 'Soluções para gestão de relacionamento e vendas',
            'color': '#8B5CF6'
        },
        {
            'name': 'Lançamentos Digitais',
            'slug': 'lancamentos-digitais',
            'description': 'Especialistas em infoprodutos e lançamentos',
            'color': '#D62042'
        },
        {
            'name': 'Automação',
            'slug': 'automacao',
            'description': 'Automação de processos e integração',
            'color': '#1a1a2e'
        },
        {
            'name': 'Consultoria',
            'slug': 'consultoria',
            'description': 'Mentoria e consultoria estratégica',
            'color': '#2d1b69'
        }
    ]
    
    for cat_data in categories_data:
        category, created = CompanyCategory.objects.get_or_create(
            slug=cat_data['slug'],
            defaults=cat_data
        )
        if created:
            print(f"✅ Categoria criada: {category.name}")
        else:
            print(f"ℹ️  Categoria já existe: {category.name}")
    
    return {cat['slug']: CompanyCategory.objects.get(slug=cat['slug']) for cat in categories_data}


def create_companies(categories):
    """Criar empresas do Grupo Kaizen"""
    companies_data = [
        {
            'name': 'Leadspot',
            'slug': 'leadspot',
            'tagline': 'O CRM que converte mais e melhor',
            'description': '''
            <p>Muitos negócios perdem dinheiro porque não sabem transformar leads em vendas. Por isso, 
            desenvolvemos um CRM para que negócios locais se conectem com seus clientes durante toda a jornada.</p>
            
            <p>Com tecnologia própria e processos otimizados, nossa solução permite gestão inteligente de leads, 
            automação, integração com Hotspot, gravação de chamadas e insights estratégicos para que nenhuma 
            oportunidade seja desperdiçada.</p>
            
            <p>Diferente dos CRMs genéricos, o Leadspot acelera negócios locais, conectando vendas e marketing 
            de forma simples e poderosa.</p>
            ''',
            'category': categories['crm-vendas'],
            'website_url': 'https://www.leadspot.com.br/',
            'contact_email': 'contato@leadspot.com.br',
            'order': 1,
            'founded_date': '2020-01-01'
        },
        {
            'name': 'LauncherX',
            'slug': 'launcherx',
            'tagline': 'Estratégia, escala e resultados reais para infoprodutores',
            'description': '''
            <p>Lançar um infoproduto de sucesso vai muito além de colocar um curso no ar. Requer estratégia, 
            estrutura e escala. A Launcher é uma assessoria de marketing especializada em transformar 
            lançamentos e vendas perpétuas em negócios altamente lucrativos.</p>
            
            <p>Com um time de especialistas e estratégias validadas, aceleramos seu crescimento com tráfego pago 
            agressivo, otimização contínua e um modelo de vendas previsível.</p>
            
            <p>O resultado? Casos como Felipe Dutra, Marcus Reis e Ricardo Piovan, que alcançaram 6 em 7 já no 
            primeiro lançamento com a nossa metodologia.</p>
            ''',
            'category': categories['lancamentos-digitais'],
            'website_url': 'https://www.launcherx.com.br/',
            'contact_email': 'contato@launcherx.com.br',
            'order': 2,
            'founded_date': '2019-01-01'
        },
        {
            'name': 'Fluxo',
            'slug': 'fluxo',
            'tagline': 'Automação, eficiência e escalabilidade para sua operação',
            'description': '''
            <p>Todos os dias, empresas perdem tempo e dinheiro com processos desorganizados e operações travadas. 
            A Fluxo, divisão de automação de processos da Kaizen, resolve esse problema, transformando negócios 
            em máquinas de alta performance.</p>
            
            <p>Com mais de 50 ferramentas de automação, CRMs e integradores homologados globalmente, implantamos 
            soluções inteligentes para otimizar sua operação, acelerar vendas e eliminar gargalos.</p>
            
            <p>Mapeamos e otimizamos seu pipeline, automatizamos interações com leads e clientes, e implementamos 
            o Kommo CRM para otimizar vendas no varejo, B2B e projetos.</p>
            ''',
            'category': categories['automacao'],
            'website_url': 'https://lp.agenciakaizen.com.br/fluxo/',
            'contact_email': 'contato@agenciakaizen.com.br',
            'order': 3,
            'founded_date': '2021-01-01'
        },
        {
            'name': 'Hacker das Vendas',
            'slug': 'hacker-das-vendas',
            'tagline': 'Consultoria e mentoria estratégica para escalar o crescimento',
            'description': '''
            <p>Você gera tráfego, atrai leads, mas sente que as vendas não acompanham o potencial da estratégia? 
            Seus clientes perdem oportunidades porque não sabem como transformar demanda em receita real?</p>
            
            <p>Com o Hacker das Vendas você aprende estratégias definitivas para criar funis de vendas que 
            realmente funcionam. E ainda pode acessar uma ferramenta exclusiva para organizar processos 
            na sua agência ou participar de uma mentoria com nosso time de especialistas.</p>
            ''',
            'category': categories['consultoria'],
            'website_url': 'https://www.hackerdasvendas.com.br/',
            'contact_email': 'contato@hackerdasvendas.com.br',
            'order': 4,
            'founded_date': '2022-01-01'
        }
    ]
    
    for company_data in companies_data:
        company, created = Company.objects.get_or_create(
            slug=company_data['slug'],
            defaults=company_data
        )
        if created:
            print(f"✅ Empresa criada: {company.name}")
        else:
            print(f"ℹ️  Empresa já existe: {company.name}")


def create_companies_page():
    """Criar página de índice das empresas"""
    try:
        companies_page = CompaniesIndexPage.objects.get(slug='nossas-empresas')
        print("ℹ️  Página 'Nossas Empresas' já existe")
        return companies_page
    except CompaniesIndexPage.DoesNotExist:
        home_page = HomePage.objects.first()
        if not home_page:
            print("❌ Home page não encontrada")
            return None
        
        companies_page = CompaniesIndexPage(
            title="Nossas Empresas",
            slug="nossas-empresas",
            hero_title="Mais que uma agência, um ecossistema de crescimento.",
            hero_subtitle="<p>A Kaizen é mais que uma agência. Somos um grupo de empresas que acelera negócios em diferentes áreas. Cada uma especializada em uma etapa do crescimento: automação, vendas, lançamentos e performance.</p>",
            intro="<p>Conheça cada empresa do Grupo Kaizen e como elas podem impulsionar seu negócio.</p>",
            meta_description="Conheça as empresas do Grupo Kaizen: Leadspot, LauncherX, Fluxo e Hacker das Vendas. Cada uma especializada em acelerar seu crescimento."
        )
        home_page.add_child(instance=companies_page)
        companies_page.save()
        print("✅ Página 'Nossas Empresas' criada")
        return companies_page


def main():
    """Função principal"""
    print("🚀 Configurando sistema de empresas...")
    print("=" * 50)
    
    try:
        # Criar categorias
        categories = create_categories()
        
        # Criar empresas
        create_companies(categories)
        
        # Criar página
        create_companies_page()
        
        print("=" * 50)
        print("✅ Sistema de empresas configurado com sucesso!")
        print("\n📋 Empresas criadas:")
        print("• Leadspot - CRM Inteligente")
        print("• LauncherX - Lançamentos Digitais")
        print("• Fluxo - Automação de Processos")
        print("• Hacker das Vendas - Consultoria Estratégica")
        print("\n🔗 Acesse: http://www.agenciakaizen.com.br/nossas-empresas/")
        print("🔧 Admin: http://www.agenciakaizen.com.br/admin/snippets/companies/company/")
        
    except Exception as e:
        print(f"❌ Erro durante a configuração: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
