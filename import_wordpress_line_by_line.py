#!/usr/bin/env python3
"""
Script EFICIENTE para importar posts do WordPress linha por linha
Evita problemas de memória e travamentos
"""

import os
import sys
import re
import logging
import time
from datetime import datetime

# Adiciona o diretório src ao path
sys.path.append('/var/www/agenciakaizen/src')

# Configura Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agenciakaizen_cms.settings.dev')

import django
django.setup()

from wagtail.models import Page, Site
from blog.models import BlogIndexPage, BlogPage
from home.models import HomePage
from wagtail.rich_text import RichText
from django.utils.text import slugify
from wagtail.contrib.redirects.models import Redirect

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/var/www/agenciakaizen/import_log.txt'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def parse_sql_line(line):
    """Parse uma linha SQL específica"""
    try:
        # Encontrar valores entre parênteses
        match = re.search(r'\((.*)\);?$', line.strip())
        if not match:
            return None
        
        values_str = match.group(1)
        
        # Parse manual dos valores
        values = []
        current = ''
        in_quotes = False
        quote_char = None
        i = 0
        
        while i < len(values_str):
            char = values_str[i]
            
            if not in_quotes:
                if char in ['"', "'"]:
                    in_quotes = True
                    quote_char = char
                    current += char
                elif char == ',':
                    values.append(current.strip())
                    current = ''
                else:
                    current += char
            else:
                current += char
                if char == quote_char and (i == 0 or values_str[i-1] != '\\'):
                    in_quotes = False
                    quote_char = None
            
            i += 1
        
        if current.strip():
            values.append(current.strip())
        
        return values
        
    except Exception as e:
        logger.warning(f"Erro ao parsear linha: {e}")
        return None

def clean_value(value):
    """Limpa valor SQL"""
    if not value or value.upper() == 'NULL':
        return None
    
    # Remove aspas
    if value.startswith("'") and value.endswith("'"):
        value = value[1:-1]
    elif value.startswith('"') and value.endswith('"'):
        value = value[1:-1]
    
    # Decodifica escapes
    value = value.replace("\\'", "'")
    value = value.replace('\\"', '"')
    value = value.replace('\\\\', '\\')
    
    return value

def create_post_from_data(values, blog_index, home_page):
    """Cria post ou página a partir dos dados"""
    try:
        if len(values) < 22:
            return False
        
        post_data = {
            'post_title': clean_value(values[5]),
            'post_content': clean_value(values[4]),
            'post_name': clean_value(values[11]),
            'post_status': clean_value(values[7]),
            'post_type': clean_value(values[20]),
            'post_date': clean_value(values[2]),
            'post_excerpt': clean_value(values[6]),
        }
        
        # Filtrar apenas posts publicados
        if (post_data.get('post_status') != 'publish' or
            not post_data.get('post_title') or
            not post_data.get('post_content') or
            post_data.get('post_type') not in ['post', 'page']):
            return False
        
        title = post_data.get('post_title', '').strip()
        content = post_data.get('post_content', '').strip()
        slug = post_data.get('post_name', '').strip()
        post_type = post_data.get('post_type', '')
        
        # Criar slug se não existir
        if not slug:
            slug = slugify(title)
        
        # Verificar se já existe
        if Page.objects.filter(slug=slug).exists():
            return False
        
        # Converter HTML para RichText
        rich_content = RichText(content)
        
        # Criar data
        post_date = post_data.get('post_date', '').split(' ')[0] if post_data.get('post_date') else None
        
        if post_type == 'post':
            # Criar post do blog
            blog_post = BlogPage(
                title=title,
                slug=slug,
                date=post_date,
                body=rich_content,
                intro=post_data.get('post_excerpt', '')[:200] if post_data.get('post_excerpt') else None,
            )
            
            blog_index.add_child(instance=blog_post)
            blog_post.save_revision().publish()
            
            logger.info(f"✅ Post criado: {title}")
            return True
            
        elif post_type == 'page':
            # Criar página
            page = HomePage(
                title=title,
                slug=slug,
            )
            
            home_page.add_child(instance=page)
            page.save_revision().publish()
            
            logger.info(f"✅ Página criada: {title}")
            return True
        
        return False
        
    except Exception as e:
        logger.error(f"❌ Erro ao criar post: {e}")
        return False

def main():
    """Função principal"""
    logger.info("🚀 Iniciando importação linha por linha")
    
    sql_file = '/var/www/agenciakaizen/agenci93_wp177.sql'
    
    # Encontrar páginas de destino
    blog_index = BlogIndexPage.objects.filter(slug='aprenda-marketing-digital').first()
    home_page = Page.objects.filter(slug='home').first()
    
    if not blog_index or not home_page:
        logger.error("❌ Páginas de destino não encontradas")
        return
    
    stats = {
        'processed': 0,
        'posts_created': 0,
        'pages_created': 0,
        'skipped': 0,
        'errors': 0
    }
    
    start_time = time.time()
    
    try:
        with open(sql_file, 'r', encoding='utf-8', errors='ignore') as f:
            line_count = 0
            in_insert_section = False
            
            for line in f:
                line_count += 1
                
                # Verificar se estamos em uma seção de INSERT
                if 'INSERT INTO `wp_posts`' in line:
                    in_insert_section = True
                    logger.info(f"📝 Encontrada seção de INSERT na linha {line_count}")
                    continue
                
                # Se estamos em uma seção de INSERT e encontramos um parêntese
                if in_insert_section and line.strip().startswith('('):
                    stats['processed'] += 1
                    
                    # Parse da linha
                    values = parse_sql_line(line)
                    if values:
                        # Tentar criar o post
                        if create_post_from_data(values, blog_index, home_page):
                            post_type = clean_value(values[20])
                            if post_type == 'post':
                                stats['posts_created'] += 1
                            elif post_type == 'page':
                                stats['pages_created'] += 1
                        else:
                            stats['skipped'] += 1
                    else:
                        stats['errors'] += 1
                    
                    # Log de progresso a cada 50 posts
                    if stats['processed'] % 50 == 0:
                        elapsed = time.time() - start_time
                        logger.info(f"📊 Progresso: {stats['processed']} processados, {stats['posts_created']} posts, {stats['pages_created']} páginas - {elapsed:.1f}s")
                
                # Se encontramos um ponto e vírgula, saímos da seção
                if in_insert_section and line.strip().endswith(';'):
                    in_insert_section = False
                
                # Log de progresso a cada 100 posts
                if stats['processed'] % 100 == 0:
                    elapsed = time.time() - start_time
                    logger.info(f"📊 Progresso: {stats['processed']} processados, {stats['posts_created']} posts, {stats['pages_created']} páginas - {elapsed:.1f}s")
    
    except Exception as e:
        logger.error(f"💥 Erro fatal: {e}")
    
    # Relatório final
    elapsed = time.time() - start_time
    logger.info("=" * 60)
    logger.info("📊 RELATÓRIO FINAL")
    logger.info("=" * 60)
    logger.info(f"⏱️ Tempo: {elapsed:.2f}s")
    logger.info(f"📝 Linhas processadas: {stats['processed']}")
    logger.info(f"✅ Posts criados: {stats['posts_created']}")
    logger.info(f"✅ Páginas criadas: {stats['pages_created']}")
    logger.info(f"⏭️ Pulados: {stats['skipped']}")
    logger.info(f"❌ Erros: {stats['errors']}")
    logger.info("=" * 60)

if __name__ == '__main__':
    main()
