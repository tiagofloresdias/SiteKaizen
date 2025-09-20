#!/usr/bin/env python3
"""
Script para importar todos os posts e páginas do WordPress SQL para Wagtail
"""

import os
import sys
import re
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

def parse_sql_values(values_string):
    """Parse valores SQL complexos com aspas e escapes"""
    values = []
    current_value = ''
    in_quotes = False
    quote_char = None
    i = 0
    
    while i < len(values_string):
        char = values_string[i]
        
        if not in_quotes:
            if char in ['"', "'"]:
                in_quotes = True
                quote_char = char
                current_value += char
            elif char == ',':
                values.append(current_value.strip())
                current_value = ''
            else:
                current_value += char
        else:
            current_value += char
            if char == quote_char:
                if i > 0 and values_string[i-1] == '\\':
                    continue
                in_quotes = False
                quote_char = None
        
        i += 1
    
    if current_value.strip():
        values.append(current_value.strip())
    
    return values

def clean_value(value):
    """Limpa valores SQL"""
    if not value or value.upper() == 'NULL':
        return None
    
    if value.startswith("'") and value.endswith("'"):
        value = value[1:-1]
    elif value.startswith('"') and value.endswith('"'):
        value = value[1:-1]
    
    value = value.replace("\\'", "'")
    value = value.replace('\\"', '"')
    value = value.replace('\\\\', '\\')
    
    return value

def main():
    print('🚀 Iniciando importação completa do WordPress')
    
    sql_file = '/var/www/agenciakaizen/agenci93_wp177.sql'
    
    # Ler arquivo SQL
    with open(sql_file, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    print(f'📖 Arquivo lido: {len(content):,} caracteres')
    
    # Encontrar todas as seções de posts
    posts_sections = re.findall(r'INSERT INTO `wp_posts`.*?VALUES\s*\((.*?)\);', content, re.DOTALL)
    
    if posts_sections:
        all_value_lines = []
        for section in posts_sections:
            value_lines = re.findall(r'\((.*?)\)', section, re.DOTALL)
            all_value_lines.extend(value_lines)
        
        print(f'✅ {len(all_value_lines)} posts encontrados no SQL')
        
        # Encontrar BlogIndexPage
        blog_index = BlogIndexPage.objects.filter(slug='aprenda-marketing-digital').first()
        home_page = Page.objects.filter(slug='home').first()
        
        if blog_index and home_page:
            print('✅ Páginas encontradas')
            
            imported_posts = 0
            imported_pages = 0
            skipped = 0
            
            # Processar todos os posts
            for i, line in enumerate(all_value_lines):
                try:
                    values = parse_sql_values(line)
                    
                    if len(values) >= 22:
                        post_data = {
                            'post_title': clean_value(values[5]),
                            'post_content': clean_value(values[4]),
                            'post_name': clean_value(values[11]),
                            'post_status': clean_value(values[7]),
                            'post_type': clean_value(values[20]),
                            'post_date': clean_value(values[2]),
                            'post_excerpt': clean_value(values[6]),
                        }
                        
                        # Filtrar apenas posts publicados com conteúdo
                        if (post_data.get('post_status') == 'publish' and 
                            post_data.get('post_title') and
                            post_data.get('post_content') and
                            post_data.get('post_type') in ['post', 'page']):
                            
                            title = post_data.get('post_title', '').strip()
                            content = post_data.get('post_content', '').strip()
                            slug = post_data.get('post_name', '').strip()
                            post_type = post_data.get('post_type', '')
                            
                            # Criar slug se não existir
                            if not slug:
                                slug = slugify(title)
                            
                            # Verificar se já existe
                            if Page.objects.filter(slug=slug).exists():
                                skipped += 1
                                continue
                            
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
                                
                                # Adicionar ao blog index
                                blog_index.add_child(instance=blog_post)
                                blog_post.save_revision().publish()
                                
                                imported_posts += 1
                                print(f'✅ Post criado: {title}')
                                
                            elif post_type == 'page':
                                # Criar página
                                page = HomePage(
                                    title=title,
                                    slug=slug,
                                )
                                
                                # Adicionar à página inicial
                                home_page.add_child(instance=page)
                                page.save_revision().publish()
                                
                                imported_pages += 1
                                print(f'✅ Página criada: {title}')
                            
                except Exception as e:
                    print(f'❌ Erro ao processar post {i+1}: {e}')
                    continue
            
            print(f'\n🎉 Importação concluída!')
            print(f'   Posts importados: {imported_posts}')
            print(f'   Páginas importadas: {imported_pages}')
            print(f'   Total: {imported_posts + imported_pages}')
            print(f'   Pulados (já existem): {skipped}')
            
        else:
            print('❌ Páginas não encontradas')
    else:
        print('❌ Seção de posts não encontrada')

if __name__ == '__main__':
    main()
