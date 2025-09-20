#!/usr/bin/env python3
"""
Script simples para importar posts e páginas do WordPress do arquivo SQL
"""

import os
import sys
import django
import re
from datetime import datetime

# Configura Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agenciakaizen_cms.settings.dev')
django.setup()

from wagtail.models import Page, Site
from blog.models import BlogIndexPage, BlogPage
from home.models import HomePage
from wagtail.rich_text import RichText
from taggit.models import Tag
from django.utils.text import slugify
from wagtail.contrib.redirects.models import Redirect

def parse_sql_values(values_string):
    """Parseia valores de um INSERT INTO"""
    values = []
    current_value = ""
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
                current_value = ""
            else:
                current_value += char
        else:
            current_value += char
            if char == quote_char:
                # Verificar se não é escape
                if i > 0 and values_string[i-1] == '\\':
                    continue
                in_quotes = False
                quote_char = None
        
        i += 1
    
    # Adicionar último valor
    if current_value.strip():
        values.append(current_value.strip())
    
    return values

def clean_value(value):
    """Limpa valores SQL"""
    if not value or value.upper() == 'NULL':
        return None
    
    # Remover aspas
    if value.startswith("'") and value.endswith("'"):
        value = value[1:-1]
    elif value.startswith('"') and value.endswith('"'):
        value = value[1:-1]
    
    # Decodificar escapes
    value = value.replace("\\'", "'")
    value = value.replace('\\"', '"')
    value = value.replace('\\\\', '\\')
    
    return value

def main():
    print("🚀 Iniciando importação do WordPress")
    
    sql_file = "/var/www/agenciakaizen/agenci93_wp177.sql"
    
    if not os.path.exists(sql_file):
        print(f"❌ Arquivo não encontrado: {sql_file}")
        return
    
    # Ler arquivo SQL
    with open(sql_file, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    print(f"📖 Arquivo lido: {len(content):,} caracteres")
    
    # Encontrar seção de posts
    posts_section = re.search(r'INSERT INTO `wp_posts`.*?VALUES\s*\((.*?)\);', content, re.DOTALL)
    
    if not posts_section:
        print("❌ Seção de posts não encontrada")
        return
    
    values_section = posts_section.group(1)
    value_lines = re.findall(r'\((.*?)\)', values_section, re.DOTALL)
    
    print(f"✅ {len(value_lines)} posts encontrados no SQL")
    
    # Encontrar ou criar BlogIndexPage
    blog_index = BlogIndexPage.objects.filter(slug='aprenda-marketing-digital').first()
    if not blog_index:
        print("❌ BlogIndexPage não encontrada")
        return
    
    # Encontrar página inicial
    home_page = Page.objects.filter(slug='home').first()
    if not home_page:
        print("❌ Página inicial não encontrada")
        return
    
    imported_posts = 0
    imported_pages = 0
    
    # Processar posts
    for i, line in enumerate(value_lines):
        try:
            values = parse_sql_values(line)
            
            if len(values) >= 22:  # wp_posts tem 23 campos
                post_data = {
                    'ID': clean_value(values[0]),
                    'post_author': clean_value(values[1]),
                    'post_date': clean_value(values[2]),
                    'post_date_gmt': clean_value(values[3]),
                    'post_content': clean_value(values[4]),
                    'post_title': clean_value(values[5]),
                    'post_excerpt': clean_value(values[6]),
                    'post_status': clean_value(values[7]),
                    'comment_status': clean_value(values[8]),
                    'ping_status': clean_value(values[9]),
                    'post_password': clean_value(values[10]),
                    'post_name': clean_value(values[11]),
                    'to_ping': clean_value(values[12]),
                    'pinged': clean_value(values[13]),
                    'post_modified': clean_value(values[14]),
                    'post_modified_gmt': clean_value(values[15]),
                    'post_content_filtered': clean_value(values[16]),
                    'post_parent': clean_value(values[17]),
                    'guid': clean_value(values[18]),
                    'menu_order': clean_value(values[19]),
                    'post_type': clean_value(values[20]),
                    'post_mime_type': clean_value(values[21]),
                    'comment_count': clean_value(values[22]) if len(values) > 22 else 0,
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
                        print(f"ℹ️ Já existe: {title}")
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
                        print(f"✅ Post criado: {title}")
                        
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
                        print(f"✅ Página criada: {title}")
                    
                    # Criar redirect para URL antiga
                    try:
                        site = Site.objects.get(is_default_site=True)
                        
                        if post_type == 'post':
                            old_url = f"/{slug}/"
                            new_url = f"/aprenda-marketing-digital/{slug}/"
                        else:
                            old_url = f"/{slug}/"
                            new_url = f"/{slug}/"
                        
                        # Verificar se redirect já existe
                        if not Redirect.objects.filter(old_path=old_url).exists():
                            redirect = Redirect(
                                old_path=old_url,
                                redirect_to=new_url,
                                site=site
                            )
                            redirect.save()
                            
                    except Exception as e:
                        print(f"⚠️ Erro ao criar redirect: {e}")
                        
        except Exception as e:
            print(f"❌ Erro ao processar post {i+1}: {e}")
            continue
    
    print(f"\n🎉 Importação concluída!")
    print(f"   Posts importados: {imported_posts}")
    print(f"   Páginas importadas: {imported_pages}")
    print(f"   Total: {imported_posts + imported_pages}")

if __name__ == "__main__":
    main()

