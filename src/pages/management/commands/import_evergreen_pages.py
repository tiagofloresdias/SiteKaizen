#!/usr/bin/env python3
"""
Comando para importar páginas evergreen do WordPress para o Wagtail
Importa páginas com tipo 'page' do WordPress como StandardPage no Wagtail
"""

import os
import sys
import re
import html
from datetime import datetime
import logging

import django
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from django.db import transaction

# Adiciona o diretório src ao path
sys.path.append('/var/www/agenciakaizen/src')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agenciakaizen_cms.settings.dev')
django.setup()

from wagtail.models import Page, Site
from pages.models import StandardPage
from home.models import HomePage
from wagtail.rich_text import RichText
from wagtail.contrib.redirects.models import Redirect

# Configurar logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(levelname)s %(asctime)s %(name)s %(message)s')

class Command(BaseCommand):
    help = 'Importa páginas evergreen do WordPress SQL para Wagtail StandardPage.'

    def add_arguments(self, parser):
        parser.add_argument('sql_file', type=str, help='Caminho para o arquivo SQL do WordPress.')
        parser.add_argument('--pages', nargs='+', help='Slugs específicos de páginas para importar (ex: leads rd-station marketing-digital)')

    def handle(self, *args, **options):
        sql_file_path = options['sql_file']
        specific_pages = options.get('pages', [])
        
        self.stdout.write(self.style.SUCCESS(f'🚀 Iniciando importação de páginas evergreen de {sql_file_path}'))
        
        if specific_pages:
            self.stdout.write(self.style.WARNING(f'📋 Importando apenas páginas específicas: {", ".join(specific_pages)}'))

        try:
            with open(sql_file_path, 'r', encoding='utf-8') as f:
                sql_content = f.read()
        except FileNotFoundError:
            self.stderr.write(self.style.ERROR(f'❌ Erro: Arquivo SQL não encontrado em {sql_file_path}'))
            return

        self.stdout.write(f'📖 Arquivo lido: {len(sql_content)} caracteres')

        # 1. Extrair páginas do WordPress
        pages_data = self._extract_pages(sql_content, specific_pages)
        self.stdout.write(self.style.SUCCESS(f'✅ {len(pages_data)} páginas encontradas no SQL'))

        if not pages_data:
            self.stdout.write(self.style.WARNING('⚠️ Nenhuma página encontrada para importar'))
            return

        # 2. Garantir que a HomePage existe como parent
        home_page = self._get_or_create_home_page()
        if not home_page:
            self.stderr.write(self.style.ERROR('❌ Não foi possível encontrar ou criar a HomePage.'))
            return
        self.stdout.write(self.style.SUCCESS('✅ HomePage encontrada'))

        # 3. Importar páginas
        imported_count = self._import_pages(pages_data, home_page)
        
        self.stdout.write(self.style.SUCCESS(f'🎉 Importação concluída! {imported_count} páginas importadas com sucesso!'))

    def _extract_pages(self, sql_content, specific_pages=None):
        """Extrai páginas do SQL do WordPress"""
        pages = []
        
        # Procurar por linhas INSERT INTO wp_posts que contenham 'page'
        lines = sql_content.split('\n')
        
        for line in lines:
            if 'INSERT INTO `wp_posts`' in line and "'page'" in line:
                # Extrair dados da linha usando regex mais simples
                match = re.search(
                    r"\((\d+),(\d+),'([^']+)','([^']+)','([^']*)','([^']+)','([^']*)','([^']+)','[^']*','[^']*','[^']*','([^']*)','[^']*','[^']*','[^']*','[^']*','[^']*',(\d+),'([^']*)',\d+,'([^']*)'",
                    line
                )
                
                if match:
                    post_data = {
                        'ID': match.group(1),
                        'post_author': match.group(2),
                        'post_date': match.group(3),
                        'post_date_gmt': match.group(4),
                        'post_content': match.group(5),
                        'post_title': match.group(6),
                        'post_excerpt': match.group(7),
                        'post_status': match.group(8),
                        'post_name': match.group(9),
                        'post_parent': match.group(10),
                        'guid': match.group(11),
                        'post_type': match.group(12)
                    }
                    
                    # Filtra apenas páginas (post_type = 'page') e publicadas
                    if post_data['post_type'] != 'page' or post_data['post_status'] != 'publish':
                        continue
                    
                    # Se especificou páginas específicas, filtra por slug
                    if specific_pages:
                        post_name = post_data['post_name']
                        if post_name not in specific_pages:
                            continue
                    
                    # Limpa aspas escapadas e outros caracteres
                    for key in ['post_content', 'post_title', 'post_excerpt', 'post_name', 'guid']:
                        if post_data[key]:
                            post_data[key] = post_data[key].replace('\\\'', "'").replace('\\"', '"').replace('\\\\', '\\')
                            post_data[key] = html.unescape(post_data[key])
                    
                    pages.append(post_data)
        
        return pages

    def _get_or_create_home_page(self):
        """Encontra ou cria a HomePage"""
        try:
            home_page = HomePage.objects.first()
            if home_page:
                return home_page
        except:
            pass
        
        # Se não encontrar, tenta pegar a página raiz
        try:
            root_page = Page.objects.filter(slug='home').first()
            if not root_page:
                root_page = Page.objects.first()
            
            if root_page:
                return root_page
        except:
            pass
        
        self.stderr.write(self.style.ERROR('❌ Não foi possível encontrar uma página pai para as páginas evergreen'))
        return None

    def _import_pages(self, pages_data, parent_page):
        """Importa as páginas para o Wagtail"""
        imported_count = 0
        
        for i, page_data in enumerate(pages_data, 1):
            try:
                self.stdout.write(f'📄 Processando página {i}/{len(pages_data)}: {page_data["post_title"]}')
                
                title = page_data['post_title']
                slug = page_data['post_name'] if page_data['post_name'] else slugify(title)
                content = page_data['post_content']
                excerpt = page_data['post_excerpt']
                
                # Verifica se a página já existe
                existing_page = StandardPage.objects.filter(slug=slug).first()
                if existing_page:
                    self.stdout.write(f'  ⚠️ Página "{title}" já existe. Atualizando...')
                    page = existing_page
                    page.title = title
                    page.intro = excerpt
                    page.body = [('paragraph', RichText(content))]
                    page.meta_description = excerpt[:160] if excerpt else title[:160]
                    page.meta_keywords = self._extract_keywords_from_content(content)
                    page.reading_time = self._calculate_reading_time(content)
                    page.save_revision().publish()
                else:
                    self.stdout.write(f'  ✅ Criando página: {title}')
                    page = StandardPage(
                        title=title,
                        slug=slug,
                        intro=excerpt,
                        body=[('paragraph', RichText(content))],
                        meta_description=excerpt[:160] if excerpt else title[:160],
                        meta_keywords=self._extract_keywords_from_content(content),
                        reading_time=self._calculate_reading_time(content),
                        live=True,
                    )
                    parent_page.add_child(instance=page)
                    page.save_revision().publish()

                # Cria redirect se necessário
                old_url = f"/{slug}/"
                try:
                    Redirect.objects.get_or_create(
                        old_path=old_url,
                        site=page.get_site(),
                        defaults={'redirect_link': page.url, 'is_permanent': True}
                    )
                    self.stdout.write(f'  🔄 Redirect criado: {old_url} → {page.url}')
                except Exception as e:
                    self.stdout.write(f'  ⚠️ Erro ao criar redirect: {e}')

                imported_count += 1
                
            except Exception as e:
                self.stderr.write(self.style.ERROR(f'❌ Erro ao processar página "{title}": {e}'))
                continue
        
        return imported_count

    def _extract_keywords_from_content(self, content):
        """Extrai palavras-chave do conteúdo"""
        if not content:
            return ""
        
        # Remove tags HTML
        clean_content = re.sub(r'<[^>]+>', ' ', content)
        # Pega palavras com mais de 3 caracteres
        words = [word.lower() for word in re.findall(r'\b\w{4,}\b', clean_content)]
        # Remove palavras muito comuns
        common_words = {'para', 'com', 'que', 'uma', 'dos', 'das', 'este', 'esta', 'isso', 'aqui', 'muito', 'mais', 'pode', 'será', 'são', 'foi', 'tem', 'ter', 'pela', 'pelo'}
        keywords = [word for word in words if word not in common_words]
        # Retorna as 10 palavras mais frequentes
        from collections import Counter
        most_common = Counter(keywords).most_common(10)
        return ', '.join([word for word, count in most_common])

    def _calculate_reading_time(self, content):
        """Calcula tempo estimado de leitura"""
        if not content:
            return 5
        
        # Remove tags HTML
        clean_content = re.sub(r'<[^>]+>', ' ', content)
        # Conta palavras
        word_count = len(clean_content.split())
        # Assume 200 palavras por minuto
        reading_time = max(1, word_count // 200)
        return min(reading_time, 60)  # Máximo 60 minutos
