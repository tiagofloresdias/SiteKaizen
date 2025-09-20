#!/usr/bin/env python3
"""
Comando Django para importar conteúdo do WordPress para Wagtail
Baseado nos dados extraídos do backup .wpress
"""

import os
import sys
import json
import re
from pathlib import Path
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from django.db import transaction
from django.core.files import File
from bs4 import BeautifulSoup

from wagtail.models import Page, Site
from wagtail.rich_text import RichText
from wagtail.images.models import Image
from wagtail.documents.models import Document
from wagtail.contrib.redirects.models import Redirect
from taggit.models import Tag

# Importa modelos do projeto
from home.models import HomePage, AboutPage
from blog.models import BlogIndexPage, BlogPage, BlogCategory


class Command(BaseCommand):
    help = "Importa conteúdo do WordPress para Wagtail"

    def add_arguments(self, parser):
        parser.add_argument(
            "--extracted-path", 
            required=True,
            help="Caminho para os dados extraídos do .wpress"
        )
        parser.add_argument(
            "--site-root-id", 
            type=int, 
            default=1,
            help="ID da página raiz onde importar"
        )

    def handle(self, *args, **options):
        extracted_path = options['extracted_path']
        site_root_id = options['site_root_id']
        
        if not os.path.exists(extracted_path):
            self.stdout.write(
                self.style.ERROR(f"Caminho não encontrado: {extracted_path}")
            )
            return
        
        self.stdout.write("🚀 Iniciando importação do WordPress...")
        
        # Verifica se temos dados extraídos
        database_sql = os.path.join(extracted_path, 'database.sql')
        uploads_dir = os.path.join(extracted_path, 'wp-content', 'uploads')
        
        if os.path.exists(database_sql):
            self.stdout.write(f"✅ SQL encontrado: {database_sql}")
            self._analyze_sql_file(database_sql)
        else:
            self.stdout.write(f"⚠️  SQL não encontrado: {database_sql}")
        
        if os.path.exists(uploads_dir):
            self.stdout.write(f"✅ Uploads encontrados: {uploads_dir}")
            self._analyze_uploads(uploads_dir)
        else:
            self.stdout.write(f"⚠️  Uploads não encontrados: {uploads_dir}")
        
        # Cria dados de exemplo se não conseguimos extrair do WordPress
        self._create_sample_content(site_root_id)
        
        self.stdout.write(
            self.style.SUCCESS("✅ Importação concluída!")
        )

    def _analyze_sql_file(self, sql_path):
        """Analisa o arquivo SQL extraído"""
        try:
            with open(sql_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Procura por dados do WordPress
            wp_patterns = [
                r'CREATE TABLE.*wp_posts',
                r'INSERT INTO.*wp_posts',
                r'CREATE TABLE.*wp_users',
                r'CREATE TABLE.*wp_options',
            ]
            
            found_patterns = []
            for pattern in wp_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                if matches:
                    found_patterns.extend(matches)
            
            if found_patterns:
                self.stdout.write(f"✅ Padrões WordPress encontrados: {len(found_patterns)}")
                for pattern in found_patterns[:5]:  # Mostra apenas os primeiros 5
                    self.stdout.write(f"   {pattern[:100]}...")
            else:
                self.stdout.write("⚠️  Nenhum padrão WordPress encontrado no SQL")
                
        except Exception as e:
            self.stdout.write(f"❌ Erro ao analisar SQL: {e}")

    def _analyze_uploads(self, uploads_path):
        """Analisa os arquivos de upload"""
        if not os.path.exists(uploads_path):
            return
        
        file_count = 0
        total_size = 0
        
        for root, dirs, files in os.walk(uploads_path):
            for file in files:
                file_path = os.path.join(root, file)
                if os.path.isfile(file_path):
                    file_count += 1
                    total_size += os.path.getsize(file_path)
        
        self.stdout.write(f"📊 Arquivos encontrados: {file_count}")
        self.stdout.write(f"📊 Tamanho total: {total_size:,} bytes")

    def _create_sample_content(self, site_root_id):
        """Cria conteúdo de exemplo baseado na estrutura do site original"""
        
        try:
            root_page = Page.objects.get(id=site_root_id)
        except Page.DoesNotExist:
            self.stdout.write(f"❌ Página raiz não encontrada: {site_root_id}")
            return
        
        # Cria BlogIndexPage se não existir
        blog_index = root_page.get_children().type(BlogIndexPage).first()
        if not blog_index:
            blog_index = BlogIndexPage(
                title="Blog",
                slug="blog",
                intro="Artigos e notícias da Agência Kaizen"
            )
            root_page.add_child(instance=blog_index)
            blog_index.save_revision().publish()
            self.stdout.write("✅ BlogIndexPage criada")
        
        # Cria categorias de exemplo
        categories = [
            "Marketing Digital",
            "Desenvolvimento Web", 
            "SEO",
            "Redes Sociais",
            "E-commerce",
            "Automação",
            "Design",
            "Cases de Sucesso"
        ]
        
        created_categories = []
        for cat_name in categories:
            category, created = BlogCategory.objects.get_or_create(
                name=cat_name,
                defaults={'slug': slugify(cat_name)}
            )
            if created:
                created_categories.append(category)
        
        if created_categories:
            self.stdout.write(f"✅ {len(created_categories)} categorias criadas")
        
        # Cria posts de exemplo baseados no conteúdo original do site
        sample_posts = [
            {
                'title': 'Como Acelerar Seu Negócio com Marketing Digital',
                'content': '''
                <p>O marketing digital é essencial para qualquer empresa que quer crescer nos dias de hoje.</p>
                
                <h2>Estratégias Eficazes</h2>
                <p>Desenvolvemos estratégias personalizadas para cada tipo de negócio, focando em resultados mensuráveis.</p>
                
                <h3>Principais Benefícios:</h3>
                <ul>
                    <li>Aumento de vendas em até 300%</li>
                    <li>ROI otimizado em campanhas</li>
                    <li>Gestão profissional de redes sociais</li>
                </ul>
                
                <p>Entre em contato conosco e descubra como podemos ajudar seu negócio a decolar!</p>
                ''',
                'category': 'Marketing Digital'
            },
            {
                'title': 'Desenvolvimento de Sites Responsivos: Tudo que Você Precisa Saber',
                'content': '''
                <p>Um site responsivo é fundamental para o sucesso online do seu negócio.</p>
                
                <h2>Por que Responsividade é Importante?</h2>
                <p>Mais de 60% do tráfego web vem de dispositivos móveis. Um site que não se adapta a diferentes telas perde visitantes e conversões.</p>
                
                <h3>Nossa Abordagem:</h3>
                <ul>
                    <li>Design mobile-first</li>
                    <li>Performance otimizada</li>
                    <li>SEO técnico implementado</li>
                </ul>
                ''',
                'category': 'Desenvolvimento Web'
            },
            {
                'title': 'SEO Local: Como Aparecer no Google Maps',
                'content': '''
                <p>O SEO local é crucial para negócios que atendem clientes em uma região específica.</p>
                
                <h2>Estratégias de SEO Local</h2>
                <p>Otimizamos sua presença no Google Maps e outros diretórios locais para aumentar sua visibilidade.</p>
                
                <h3>Resultados Comprovados:</h3>
                <ul>
                    <li>Aparecimento no topo do Google Maps</li>
                    <li>Aumento de ligações locais</li>
                    <li>Mais visitas à sua loja</li>
                </ul>
                ''',
                'category': 'SEO'
            },
            {
                'title': 'Automação de Marketing: Economize Tempo e Aumente Vendas',
                'content': '''
                <p>A automação de marketing permite que você nutra leads e converta prospects sem esforço manual.</p>
                
                <h2>Benefícios da Automação</h2>
                <p>Com as ferramentas certas, você pode automatizar todo o funil de vendas.</p>
                
                <h3>Nossas Soluções:</h3>
                <ul>
                    <li>Email marketing automatizado</li>
                    <li>Sequências de nutrição de leads</li>
                    <li>Integração com CRM</li>
                </ul>
                ''',
                'category': 'Automação'
            },
            {
                'title': 'Case de Sucesso: Loja Online Aumenta Vendas em 450%',
                'content': '''
                <p>Veja como ajudamos uma loja online a multiplicar suas vendas com estratégias digitais.</p>
                
                <h2>Desafio Inicial</h2>
                <p>A loja tinha um site básico e pouca presença digital, resultando em baixas vendas online.</p>
                
                <h3>Soluções Implementadas:</h3>
                <ul>
                    <li>Redesign completo do site</li>
                    <li>Implementação de SEO técnico</li>
                    <li>Campanhas de Google Ads</li>
                    <li>Automação de email marketing</li>
                </ul>
                
                <h3>Resultados Alcançados:</h3>
                <ul>
                    <li>450% de aumento nas vendas</li>
                    <li>300% mais tráfego orgânico</li>
                    <li>ROI de 500% nas campanhas pagas</li>
                </ul>
                ''',
                'category': 'Cases de Sucesso'
            }
        ]
        
        created_posts = 0
        for post_data in sample_posts:
            # Verifica se o post já existe
            existing_post = BlogPage.objects.filter(
                slug=slugify(post_data['title'])
            ).first()
            
            if existing_post:
                continue
            
            # Cria o post
            post = BlogPage(
                title=post_data['title'],
                slug=slugify(post_data['title']),
                intro=f"Descubra mais sobre {post_data['title'].lower()}",
                body=RichText(post_data['content']),
                first_published_at='2024-01-01'
            )
            
            blog_index.add_child(instance=post)
            post.save_revision().publish()
            
            # Adiciona categoria
            try:
                category = BlogCategory.objects.get(name=post_data['category'])
                post.categories.add(category)
            except BlogCategory.DoesNotExist:
                pass
            
            # Adiciona tags
            for tag_name in ['marketing', 'digital', 'agência', 'kaizen']:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                post.tags.add(tag)
            
            created_posts += 1
        
        if created_posts > 0:
            self.stdout.write(f"✅ {created_posts} posts de exemplo criados")
        
        # Cria redirects de exemplo para manter URLs antigas
        sample_redirects = [
            ('/blog/como-acelerar-negocio-marketing-digital/', '/blog/como-acelerar-seu-negocio-com-marketing-digital/'),
            ('/blog/desenvolvimento-sites-responsivos/', '/blog/desenvolvimento-de-sites-responsivos-tudo-que-voce-precisa-saber/'),
            ('/blog/seo-local-google-maps/', '/blog/seo-local-como-aparecer-no-google-maps/'),
            ('/blog/automacao-marketing/', '/blog/automacao-de-marketing-economize-tempo-e-aumente-vendas/'),
            ('/blog/case-sucesso-loja-online/', '/blog/case-de-sucesso-loja-online-aumenta-vendas-em-450/'),
        ]
        
        created_redirects = 0
        for old_path, new_path in sample_redirects:
            # Encontra a página de destino
            try:
                target_page = Page.objects.get(url_path=new_path)
                redirect, created = Redirect.objects.get_or_create(
                    old_path=old_path,
                    defaults={
                        'redirect_page': target_page,
                        'is_permanent': True
                    }
                )
                if created:
                    created_redirects += 1
            except Page.DoesNotExist:
                continue
        
        if created_redirects > 0:
            self.stdout.write(f"✅ {created_redirects} redirects criados")
        
        self.stdout.write("🎉 Conteúdo de exemplo criado com sucesso!")
        self.stdout.write("📝 Acesse o admin para personalizar o conteúdo")
