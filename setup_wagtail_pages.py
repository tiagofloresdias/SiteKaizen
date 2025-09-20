#!/usr/bin/env python3
"""
Script para configurar páginas básicas no Wagtail CMS
Agência Kaizen - Configuração de Páginas
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

from django.contrib.auth import get_user_model
from wagtail.models import Page, Site
from home.models import HomePage
from blog.models import BlogIndexPage, BlogCategory
from portfolio.models import PortfolioIndexPage, PortfolioCategory
from services.models import ServicesIndexPage
from contact.models import ContactPage

def create_home_page():
    """Criar ou atualizar home page"""
    try:
        home_page = HomePage.objects.get(slug='home')
        print("✅ Home page já existe")
        return home_page
    except HomePage.DoesNotExist:
        # Criar home page
        home_page = HomePage(
            title="Agência Kaizen",
            slug="home",
            hero_title="Transformamos Ideias em Soluções Digitais",
            hero_subtitle="<p class='lead'>Somos uma agência digital especializada em criar experiências únicas que conectam marcas e pessoas através da tecnologia.</p>",
            about_title="Sobre a Agência Kaizen",
            about_text="<p class='lead'>Somos uma equipe apaixonada por tecnologia e inovação, dedicada a transformar ideias em soluções digitais que fazem a diferença.</p><p>Com anos de experiência no mercado, oferecemos serviços completos de desenvolvimento web, marketing digital e design, sempre focados em resultados excepcionais para nossos clientes.</p>",
            services_title="Nossos Serviços",
            services_text="<p class='lead'>Oferecemos soluções completas para impulsionar seu negócio no mundo digital.</p>",
            portfolio_title="Nosso Portfolio",
            portfolio_text="<p class='lead'>Conheça alguns dos projetos que desenvolvemos para nossos clientes.</p>",
            contact_title="Pronto para Começar?",
            contact_text="<p class='lead'>Entre em contato conosco e vamos transformar sua ideia em realidade.</p>"
        )
        
        # Adicionar como filha da root page
        root = Page.get_first_root_node()
        root.add_child(instance=home_page)
        home_page.save()
        print("✅ Home page criada")
        return home_page

def create_portfolio_page():
    """Criar página do portfolio"""
    try:
        portfolio_index = PortfolioIndexPage.objects.get(slug='portfolio')
        print("✅ Página do portfolio já existe")
        return portfolio_index
    except PortfolioIndexPage.DoesNotExist:
        home_page = HomePage.objects.first()
        if not home_page:
            print("❌ Home page não encontrada")
            return None
        
        portfolio_index = PortfolioIndexPage(
            title="Portfolio",
            slug="portfolio",
            intro="<p>Conheça alguns dos projetos que desenvolvemos para nossos clientes.</p>"
        )
        home_page.add_child(instance=portfolio_index)
        portfolio_index.save()
        print("✅ Página do portfolio criada")
        return portfolio_index

def create_services_page():
    """Criar página de serviços"""
    try:
        services_index = ServicesIndexPage.objects.get(slug='servicos')
        print("✅ Página de serviços já existe")
        return services_index
    except ServicesIndexPage.DoesNotExist:
        home_page = HomePage.objects.first()
        if not home_page:
            print("❌ Home page não encontrada")
            return None
        
        services_index = ServicesIndexPage(
            title="Serviços",
            slug="servicos",
            intro="<p>Oferecemos soluções completas para impulsionar seu negócio no mundo digital.</p>"
        )
        home_page.add_child(instance=services_index)
        services_index.save()
        print("✅ Página de serviços criada")
        return services_index

def create_contact_page():
    """Criar ou atualizar página de contato"""
    try:
        contact_page = ContactPage.objects.get(slug='contato')
        # Atualizar campos existentes
        contact_page.intro = "<p>Entre em contato conosco e vamos transformar sua ideia em realidade.</p>"
        contact_page.address = "<p>São Paulo, SP - Brasil</p>"
        contact_page.phone = "+55 11 99999-9999"
        contact_page.phone_0800 = "0800-550-8000"
        contact_page.whatsapp = "0800-550-8000"
        contact_page.email = "contato@www.agenciakaizen.com.br"
        contact_page.highlight_title = "Fale Conosco"
        contact_page.highlight_subtitle = "Estamos prontos para atender você!"
        contact_page.save()
        print("✅ Página de contato atualizada")
        return contact_page
    except ContactPage.DoesNotExist:
        home_page = HomePage.objects.first()
        if not home_page:
            print("❌ Home page não encontrada")
            return None
        
        contact_page = ContactPage(
            title="Contato",
            slug="contato",
            intro="<p>Entre em contato conosco e vamos transformar sua ideia em realidade.</p>",
            address="<p>São Paulo, SP - Brasil</p>",
            phone="+55 11 99999-9999",
            phone_0800="0800-550-8000",
            whatsapp="0800-550-8000",
            email="contato@www.agenciakaizen.com.br",
            highlight_title="Fale Conosco",
            highlight_subtitle="Estamos prontos para atender você!"
        )
        home_page.add_child(instance=contact_page)
        contact_page.save()
        print("✅ Página de contato criada")
        return contact_page

def create_blog_page():
    """Criar página do blog"""
    try:
        blog_index = BlogIndexPage.objects.get(slug='blog')
        print("✅ Página do blog já existe")
        return blog_index
    except BlogIndexPage.DoesNotExist:
        home_page = HomePage.objects.first()
        if not home_page:
            print("❌ Home page não encontrada")
            return None
        
        blog_index = BlogIndexPage(
            title="Blog",
            slug="blog",
            intro="<p>Artigos, dicas e insights sobre desenvolvimento web, marketing digital e tecnologia.</p>"
        )
        home_page.add_child(instance=blog_index)
        blog_index.save()
        print("✅ Página do blog criada")
        return blog_index

def create_about_page():
    """Criar página sobre"""
    try:
        about_page = Page.objects.get(slug='sobre')
        print("✅ Página sobre já existe")
        return about_page
    except Page.DoesNotExist:
        home_page = HomePage.objects.first()
        if not home_page:
            print("❌ Home page não encontrada")
            return None
        
        about_page = Page(
            title="Sobre a Agência Kaizen",
            slug="sobre",
            live=True,
            show_in_menus=True
        )
        home_page.add_child(instance=about_page)
        about_page.save()
        print("✅ Página sobre criada")
        return about_page

def create_solutions_page():
    """Criar página de soluções"""
    try:
        solutions_page = Page.objects.get(slug='solucoes')
        print("✅ Página de soluções já existe")
        return solutions_page
    except Page.DoesNotExist:
        home_page = HomePage.objects.first()
        if not home_page:
            print("❌ Home page não encontrada")
            return None
        
        solutions_page = Page(
            title="Soluções",
            slug="solucoes",
            live=True,
            show_in_menus=True
        )
        home_page.add_child(instance=solutions_page)
        solutions_page.save()
        print("✅ Página de soluções criada")
        return solutions_page

def configure_site():
    """Configurar site principal"""
    site = Site.objects.first()
    if site:
        home_page = HomePage.objects.first()
        if home_page:
            site.root_page = home_page
            site.hostname = 'www.agenciakaizen.com.br'
            site.port = 80
            site.is_default_site = True
            site.save()
            print("✅ Site configurado")
    else:
        home_page = HomePage.objects.first()
        if home_page:
            site = Site.objects.create(
                hostname='www.agenciakaizen.com.br',
                port=80,
                root_page=home_page,
                is_default_site=True
            )
            print("✅ Site criado e configurado")

def main():
    """Função principal"""
    print("🚀 Configurando páginas do Wagtail CMS...")
    print("=" * 50)
    
    try:
        # Criar páginas
        create_home_page()
        create_portfolio_page()
        create_services_page()
        create_contact_page()
        create_blog_page()
        create_about_page()
        create_solutions_page()
        
        # Configurar site
        configure_site()
        
        print("=" * 50)
        print("✅ Configuração concluída com sucesso!")
        print("\n📋 Páginas criadas:")
        print("• Home: /")
        print("• Portfolio: /portfolio/")
        print("• Serviços: /servicos/")
        print("• Contato: /contato/")
        print("• Blog: /blog/")
        print("• Sobre: /sobre/")
        print("• Soluções: /solucoes/")
        print("\n🔗 Acesse: http://www.agenciakaizen.com.br")
        
    except Exception as e:
        print(f"❌ Erro durante a configuração: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
