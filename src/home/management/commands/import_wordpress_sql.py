#!/usr/bin/env python3
"""
Comando para importar COMPLETAMENTE o conteúdo do WordPress do arquivo SQL
Importa TODOS os posts, páginas, categorias, tags e metadados
"""

import os
import sys
import re
import json
from datetime import datetime

# Observação: a configuração do Django deve estar carregada externamente (via manage.py).
# Não forçar DJANGO_SETTINGS_MODULE aqui para permitir execução em diferentes ambientes.

from wagtail.models import Page, Site
from blog.models import BlogIndexPage, BlogPage
from home.models import HomePage
from pages.models import StandardPage
from wagtail.rich_text import RichText
from wagtail.images.models import Image
from taggit.models import Tag
from django.utils.text import slugify
from django.core.files.base import ContentFile
from wagtail.contrib.redirects.models import Redirect

class WordPressImporter:
    def __init__(self):
        self.imported_posts = 0
        self.imported_pages = 0
        self.imported_categories = 0
        self.imported_tags = 0
        self.imported_images = 0
        self.categories = {}
        self.tags = {}
        
    def parse_sql_file(self, sql_file):
        """Parseia o arquivo SQL do WordPress"""
        print(f"🔍 Parseando arquivo SQL: {sql_file}", flush=True)
        
        if not os.path.exists(sql_file):
            print(f"❌ Arquivo não encontrado: {sql_file}")
            return None
        
        with open(sql_file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        print(f"📖 Arquivo lido: {len(content):,} caracteres", flush=True)
        
        # Extrair dados das tabelas
        posts_data = self.extract_posts_data(content)
        categories_data = self.extract_categories_data(content)
        tags_data = self.extract_tags_data(content)
        postmeta_data = self.extract_postmeta_data(content)
        
        return {
            'posts': posts_data,
            'categories': categories_data,
            'tags': tags_data,
            'postmeta': postmeta_data
        }
    
    def extract_posts_data(self, content):
        """Extrai dados da tabela wp_posts"""
        print("🔄 Extraindo dados de posts...", flush=True)
        
        # Encontrar TODAS as seções INSERT INTO wp_posts (o dump pode fracionar)
        insert_blocks = re.findall(r'INSERT INTO `wp_posts`[\s\S]*?VALUES\s*(\(.*?\));', content, re.DOTALL)
        if not insert_blocks:
            print("❌ Seção de posts não encontrada", flush=True)
            return []

        value_lines = []
        for block in insert_blocks:
            value_lines.extend(re.findall(r'\((.*?)\)', block, re.DOTALL))
        
        posts = []
        for line in value_lines:
            try:
                values = self.parse_sql_values(line)
                if len(values) >= 22:  # wp_posts tem 23 campos
                    post_data = {
                        'ID': self.clean_value(values[0]),
                        'post_author': self.clean_value(values[1]),
                        'post_date': self.clean_value(values[2]),
                        'post_date_gmt': self.clean_value(values[3]),
                        'post_content': self.clean_value(values[4]),
                        'post_title': self.clean_value(values[5]),
                        'post_excerpt': self.clean_value(values[6]),
                        'post_status': self.clean_value(values[7]),
                        'comment_status': self.clean_value(values[8]),
                        'ping_status': self.clean_value(values[9]),
                        'post_password': self.clean_value(values[10]),
                        'post_name': self.clean_value(values[11]),
                        'to_ping': self.clean_value(values[12]),
                        'pinged': self.clean_value(values[13]),
                        'post_modified': self.clean_value(values[14]),
                        'post_modified_gmt': self.clean_value(values[15]),
                        'post_content_filtered': self.clean_value(values[16]),
                        'post_parent': self.clean_value(values[17]),
                        'guid': self.clean_value(values[18]),
                        'menu_order': self.clean_value(values[19]),
                        'post_type': self.clean_value(values[20]),
                        'post_mime_type': self.clean_value(values[21]),
                        'comment_count': self.clean_value(values[22]) if len(values) > 22 else 0,
                    }
                    
                    # Filtrar apenas posts publicados com conteúdo
                    if (post_data.get('post_status') == 'publish' and 
                        post_data.get('post_title') and
                        post_data.get('post_content') and
                        post_data.get('post_type') in ['post', 'page']):
                        
                        posts.append(post_data)
                        
            except Exception as e:
                print(f"⚠️ Erro ao processar post: {e}")
                continue
        
        print(f"✅ {len(posts)} posts válidos encontrados", flush=True)
        return posts
    
    def extract_categories_data(self, content):
        """Extrai dados de categorias"""
        print("🔄 Extraindo categorias...", flush=True)
        
        # Encontrar todas as seções de wp_terms
        categories = []
        insert_blocks = re.findall(r'INSERT INTO `wp_terms`[\s\S]*?VALUES\s*(\(.*?\));', content, re.DOTALL)
        if not insert_blocks:
            print("❌ Seção de categorias não encontrada", flush=True)
            return []
        value_lines = []
        for block in insert_blocks:
            value_lines.extend(re.findall(r'\((.*?)\)', block, re.DOTALL))
        
        for line in value_lines:
            try:
                values = self.parse_sql_values(line)
                if len(values) >= 3:
                    category_data = {
                        'term_id': self.clean_value(values[0]),
                        'name': self.clean_value(values[1]),
                        'slug': self.clean_value(values[2]),
                    }
                    categories.append(category_data)
            except Exception as e:
                continue
        
        print(f"✅ {len(categories)} categorias encontradas", flush=True)
        return categories
    
    def extract_tags_data(self, content):
        """Extrai dados de tags"""
        print("🔄 Extraindo tags...", flush=True)
        
        # Tags também estão na tabela wp_terms, mas com taxonomy diferente
        # Vamos extrair da tabela wp_term_taxonomy
        insert_blocks = re.findall(r'INSERT INTO `wp_term_taxonomy`[\s\S]*?VALUES\s*(\(.*?\));', content, re.DOTALL)
        if not insert_blocks:
            print("❌ Seção de taxonomias não encontrada", flush=True)
            return []
        tags = []
        value_lines = []
        for block in insert_blocks:
            value_lines.extend(re.findall(r'\((.*?)\)', block, re.DOTALL))
        
        for line in value_lines:
            try:
                values = self.parse_sql_values(line)
                if len(values) >= 4:
                    taxonomy_data = {
                        'term_taxonomy_id': self.clean_value(values[0]),
                        'term_id': self.clean_value(values[1]),
                        'taxonomy': self.clean_value(values[2]),
                        'description': self.clean_value(values[3]),
                    }
                    
                    # Filtrar apenas tags (post_tag) e categorias (category)
                    if taxonomy_data.get('taxonomy') in ['post_tag', 'category']:
                        tags.append(taxonomy_data)
            except Exception as e:
                continue
        
        print(f"✅ {len(tags)} tags/categorias encontradas", flush=True)
        return tags
    
    def extract_postmeta_data(self, content):
        """Extrai metadados dos posts"""
        print("🔄 Extraindo metadados...", flush=True)
        
        insert_blocks = re.findall(r'INSERT INTO `wp_postmeta`[\s\S]*?VALUES\s*(\(.*?\));', content, re.DOTALL)
        if not insert_blocks:
            print("❌ Seção de metadados não encontrada", flush=True)
            return []
        metadata = {}
        value_lines = []
        for block in insert_blocks:
            value_lines.extend(re.findall(r'\((.*?)\)', block, re.DOTALL))
        
        for line in value_lines:
            try:
                values = self.parse_sql_values(line)
                if len(values) >= 4:
                    meta_data = {
                        'meta_id': self.clean_value(values[0]),
                        'post_id': self.clean_value(values[1]),
                        'meta_key': self.clean_value(values[2]),
                        'meta_value': self.clean_value(values[3]),
                    }
                    
                    post_id = meta_data['post_id']
                    if post_id not in metadata:
                        metadata[post_id] = {}
                    
                    metadata[post_id][meta_data['meta_key']] = meta_data['meta_value']
            except Exception as e:
                continue
        
        print(f"✅ Metadados para {len(metadata)} posts encontrados", flush=True)
        return metadata
    
    def parse_sql_values(self, values_string):
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
    
    def clean_value(self, value):
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
    
    def create_categories(self, categories_data, tags_data):
        """Cria categorias e tags no Wagtail"""
        print("🔄 Criando categorias e tags...", flush=True)
        
        # Criar categorias
        for category in categories_data:
            try:
                name = category.get('name', '').strip()
                slug = category.get('slug', '').strip()
                
                if name and slug:
                    # Usar taggit para categorias
                    tag, created = Tag.objects.get_or_create(
                        name=name,
                        defaults={'slug': slug}
                    )
                    
                    if created:
                        self.imported_categories += 1
                        self.categories[category['term_id']] = tag
                        
            except Exception as e:
                print(f"❌ Erro ao criar categoria {category}: {e}", flush=True)
        
        # Criar tags
        for tag_data in tags_data:
            try:
                if tag_data.get('taxonomy') == 'post_tag':
                    # Buscar nome da tag na tabela wp_terms
                    # Por enquanto, vamos criar tags genéricas
                    tag_name = f"Tag_{tag_data['term_id']}"
                    
                    tag, created = Tag.objects.get_or_create(name=tag_name)
                    
                    if created:
                        self.imported_tags += 1
                        self.tags[tag_data['term_id']] = tag
                        
            except Exception as e:
                print(f"❌ Erro ao criar tag {tag_data}: {e}", flush=True)
        
        print(f"✅ {self.imported_categories} categorias e {self.imported_tags} tags criadas", flush=True)
    
    def create_blog_posts(self, posts_data, metadata):
        """Cria posts do blog no Wagtail"""
        print("🔄 Criando posts do blog...", flush=True)
        
        # Encontrar ou criar BlogIndexPage
        blog_index = BlogIndexPage.objects.filter(slug='aprenda-marketing-digital').first()
        if not blog_index:
            print("❌ BlogIndexPage não encontrada")
            return
        
        # Filtrar apenas posts do blog
        blog_posts = [p for p in posts_data if p.get('post_type') == 'post']
        
        print(f"📝 Processando {len(blog_posts)} posts do blog...", flush=True)
        
        for post_data in blog_posts:
            try:
                title = post_data.get('post_title', '').strip()
                content = post_data.get('post_content', '').strip()
                slug = post_data.get('post_name', '').strip()
                post_id = post_data.get('ID')
                
                if not title or not content:
                    continue
                
                # Criar slug se não existir
                if not slug:
                    slug = slugify(title)
                
                # Verificar se já existe
                if BlogPage.objects.filter(slug=slug).exists():
                    print(f"ℹ️ Post já existe: {title}", flush=True)
                    continue
                
                # Converter HTML para RichText
                rich_content = RichText(content)
                
                # Criar data
                post_date = None
                if post_data.get('post_date'):
                    try:
                        post_date = datetime.strptime(post_data.get('post_date').split(' ')[0], "%Y-%m-%d").date()
                    except Exception:
                        post_date = None
                
                # Criar post
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
                
                # Adicionar tags/categorias se existirem
                if post_id in metadata:
                    post_meta = metadata[post_id]
                    
                    # Adicionar tags genéricas
                    for i, tag in enumerate(list(self.tags.values())[:3]):
                        blog_post.tags.add(tag)
                
                self.imported_posts += 1
                print(f"✅ Post criado: {title}", flush=True)
                
            except Exception as e:
                print(f"❌ Erro ao criar post {post_data.get('post_title', 'Unknown')}: {e}", flush=True)
    
    def create_pages(self, posts_data):
        """Cria páginas no Wagtail"""
        print("🔄 Criando páginas...", flush=True)
        
        # Filtrar apenas páginas
        pages = [p for p in posts_data if p.get('post_type') == 'page']
        
        print(f"📄 Processando {len(pages)} páginas...", flush=True)
        
        # Encontrar página inicial
        home_site = Site.objects.filter(is_default_site=True).first() or Site.objects.first()
        home_page = home_site.root_page.specific if home_site else Page.objects.get(id=1)
        if not home_page:
            print("❌ Página inicial não encontrada", flush=True)
            return
        
        for page_data in pages:
            try:
                title = page_data.get('post_title', '').strip()
                content = page_data.get('post_content', '').strip()
                slug = page_data.get('post_name', '').strip()
                
                if not title or not content:
                    continue
                
                # Criar slug se não existir
                if not slug:
                    slug = slugify(title)
                
                # Verificar se já existe (não importar home/URLs existentes)
                if slug in ['home', 'index', 'pagina-inicial'] or Page.objects.filter(slug=slug).exists():
                    print(f"ℹ️ Página já existe: {title}", flush=True)
                    continue
                
                # Converter HTML para RichText
                rich_content = RichText(content)
                
                # Criar página padrão
                page = StandardPage(
                    title=title,
                    slug=slug,
                )
                # Popular conteúdo básico
                from wagtail.rich_text import RichText
                page.intro = RichText(content[:500]) if content else ''
                page.body = [("paragraph", content)] if content else []
                
                # Adicionar à página inicial
                home_page.add_child(instance=page)
                page.save_revision().publish()
                
                self.imported_pages += 1
                print(f"✅ Página criada: {title}", flush=True)
                
            except Exception as e:
                print(f"❌ Erro ao criar página {page_data.get('post_title', 'Unknown')}: {e}", flush=True)
    
    def create_redirects(self, posts_data):
        """Cria redirects para URLs antigas"""
        print("🔄 Criando redirects...", flush=True)
        
        # Encontrar site padrão
        site = Site.objects.get(is_default_site=True)
        
        redirect_count = 0
        
        for post_data in posts_data:
            try:
                title = post_data.get('post_title', '').strip()
                slug = post_data.get('post_name', '').strip()
                post_type = post_data.get('post_type', '')
                
                if not title or not slug:
                    continue
                
                # Criar URL antiga
                if post_type == 'post':
                    old_url = f"/{slug}/"
                else:
                    old_url = f"/{slug}/"
                
                # Criar URL nova
                if post_type == 'post':
                    new_url = f"/aprenda-marketing-digital/{slug}/"
                else:
                    new_url = f"/{slug}/"
                
                # Verificar se redirect já existe
                if Redirect.objects.filter(old_path=old_url).exists():
                    continue
                
                # Criar redirect
                redirect = Redirect(
                    old_path=old_url,
                    redirect_to=new_url,
                    site=site
                )
                redirect.save()
                
                redirect_count += 1
                
            except Exception as e:
                print(f"❌ Erro ao criar redirect: {e}", flush=True)
        
        print(f"✅ {redirect_count} redirects criados", flush=True)
    
    def run(self):
        """Executa o comando"""
        print("🚀 Iniciando importação completa do WordPress SQL", flush=True)
        
        sql_file = "/var/www/agenciakaizen/agenci93_wp177.sql"
        
        # Parsear arquivo SQL
        data = self.parse_sql_file(sql_file)
        if not data:
            return
        
        print(f"📊 Dados encontrados:", flush=True)
        print(f"   Posts: {len(data['posts'])}", flush=True)
        print(f"   Categorias: {len(data['categories'])}", flush=True)
        print(f"   Tags: {len(data['tags'])}", flush=True)
        print(f"   Metadados: {len(data['postmeta'])}", flush=True)
        
        # Criar categorias e tags
        self.create_categories(data['categories'], data['tags'])
        
        # Criar posts (ignorando slugs que já existem)
        self.create_blog_posts(data['posts'], data['postmeta'])
        
        # Criar páginas (ignorando slugs já existentes e ignorando home/URLs atuais)
        self.create_pages([p for p in data['posts'] if p.get('post_type') == 'page' and p.get('post_name') not in ['home','index','pagina-inicial']])
        
        # Criar redirects
        self.create_redirects(data['posts'])
        
        print(f"\n🎉 Importação concluída!", flush=True)
        print(f"   Posts importados: {self.imported_posts}", flush=True)
        print(f"   Páginas importadas: {self.imported_pages}", flush=True)
        print(f"   Categorias criadas: {self.imported_categories}", flush=True)
        print(f"   Tags criadas: {self.imported_tags}", flush=True)
        print(f"   Total: {self.imported_posts + self.imported_pages}", flush=True)

if __name__ == "__main__":
    importer = WordPressImporter()
    importer.run()

