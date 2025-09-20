#!/usr/bin/env python3
"""
Script SIMPLES para importar posts do WordPress
Usa uma abordagem mais direta
"""

import os
import sys
import re
import logging

# Adiciona o diretório src ao path
sys.path.append('/var/www/agenciakaizen/src')

# Configura Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agenciakaizen_cms.settings.dev')

import django
django.setup()

from wagtail.models import Page
from blog.models import BlogIndexPage, BlogPage
from home.models import HomePage
from wagtail.rich_text import RichText
from django.utils.text import slugify

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

def extract_posts_from_sql():
    """Extrai posts usando regex mais simples"""
    sql_file = '/var/www/agenciakaizen/agenci93_wp177.sql'
    
    with open(sql_file, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    logger.info(f"📖 Arquivo lido: {len(content):,} caracteres")
    
    # Regex mais simples para encontrar posts
    # Procura por padrões como: (1, 2, '2015-09-16 05:22:38', '2015-09-16 05:22:38', 'conteudo', 'titulo', '', 'publish', ...
    pattern = r"\((\d+),\s*(\d+),\s*'([^']*)',\s*'([^']*)',\s*'([^']*)',\s*'([^']*)',\s*'([^']*)',\s*'([^']*)',"
    
    posts = []
    for match in re.finditer(pattern, content, re.DOTALL):
        try:
            post_data = {
                'id': match.group(1),
                'author': match.group(2),
                'date': match.group(3),
                'date_gmt': match.group(4),
                'content': match.group(5),
                'title': match.group(6),
                'excerpt': match.group(7),
                'status': match.group(8),
            }
            
            # Verificar se é um post válido
            if (post_data['status'] == 'publish' and 
                post_data['title'] and 
                post_data['content'] and
                len(post_data['content']) > 100):  # Conteúdo mínimo
                
                posts.append(post_data)
                logger.info(f"✅ Post encontrado: {post_data['title']}")
                
        except Exception as e:
            logger.warning(f"Erro ao processar match: {e}")
            continue
    
    logger.info(f"📊 Total de posts válidos encontrados: {len(posts)}")
    return posts

def create_post(post_data):
    """Cria um post no Wagtail"""
    try:
        title = post_data['title']
        content = post_data['content']
        date = post_data['date'].split(' ')[0]  # Apenas a data
        
        # Criar slug
        slug = slugify(title)
        
        # Verificar se já existe
        if Page.objects.filter(slug=slug).exists():
            logger.info(f"⏭️ Post já existe: {title}")
            return False
        
        # Encontrar BlogIndexPage
        blog_index = BlogIndexPage.objects.filter(slug='aprenda-marketing-digital').first()
        if not blog_index:
            logger.error("❌ BlogIndexPage não encontrada")
            return False
        
        # Criar post
        blog_post = BlogPage(
            title=title,
            slug=slug,
            date=date,
            body=RichText(content),
            intro=post_data['excerpt'][:200] if post_data['excerpt'] else title[:200],  # Usar título como intro se excerpt estiver vazio
            is_featured=False,  # Campo obrigatório adicionado
            reading_time=5,  # Campo obrigatório adicionado
        )
        
        blog_index.add_child(instance=blog_post)
        blog_post.save_revision().publish()
        
        logger.info(f"✅ Post criado: {title}")
        return True
        
    except Exception as e:
        logger.error(f"❌ Erro ao criar post '{title}': {e}")
        return False

def main():
    """Função principal"""
    logger.info("🚀 Iniciando importação simples")
    
    # Extrair posts
    posts = extract_posts_from_sql()
    
    if not posts:
        logger.error("❌ Nenhum post encontrado")
        return
    
    # Importar posts
    imported = 0
    for i, post_data in enumerate(posts):  # Processar todos os posts
        logger.info(f"📝 Processando post {i+1}/{len(posts)}: {post_data['title']}")
        
        if create_post(post_data):
            imported += 1
    
    logger.info(f"🎉 Importação concluída! {imported} posts importados")

if __name__ == '__main__':
    main()
