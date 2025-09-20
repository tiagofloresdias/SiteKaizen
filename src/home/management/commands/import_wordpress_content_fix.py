#!/usr/bin/env python3
"""
Comando para importar conteúdo completo do WordPress
Corrige o problema dos posts com conteúdo incompleto
"""

import os
import sys
import django
import re
import gzip
import tempfile
from pathlib import Path

# Configura Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agenciakaizen_cms.settings.dev')
django.setup()

from wagtail.models import Page, Site
from blog.models import BlogIndexPage, BlogPage
from wagtail.rich_text import RichText
from wagtail.images.models import Image
from taggit.models import Tag
from django.utils.text import slugify
from django.core.files.base import ContentFile
import mysql.connector
from mysql.connector import Error

class Command:
    def __init__(self):
        self.connection = None
        
    def connect_to_mysql(self):
        """Conecta ao MySQL temporário"""
        try:
            self.connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='680143',
                database='wp_legacy'
            )
            print("✅ Conectado ao MySQL")
            return True
        except Error as e:
            print(f"❌ Erro ao conectar MySQL: {e}")
            return False
    
    def extract_wpress_content(self, wpress_file):
        """Extrai conteúdo do arquivo .wpress"""
        print(f"🔄 Extraindo conteúdo de {wpress_file}")
        
        try:
            with open(wpress_file, 'rb') as f:
                content = f.read()
            
            # Procurar por dados SQL no arquivo
            sql_pattern = b'CREATE TABLE'
            sql_start = content.find(sql_pattern)
            
            if sql_start == -1:
                print("❌ Não foi possível encontrar dados SQL")
                return None
            
            # Extrair dados SQL
            sql_data = content[sql_start:]
            
            # Salvar em arquivo temporário
            with tempfile.NamedTemporaryFile(mode='w', suffix='.sql', delete=False) as temp_file:
                temp_file.write(sql_data.decode('utf-8', errors='ignore'))
                temp_file_path = temp_file.name
            
            print(f"✅ Dados SQL extraídos para {temp_file_path}")
            return temp_file_path
            
        except Exception as e:
            print(f"❌ Erro ao extrair conteúdo: {e}")
            return None
    
    def import_mysql_dump(self, sql_file):
        """Importa dump SQL para MySQL"""
        print(f"🔄 Importando {sql_file} para MySQL")
        
        try:
            # Criar database se não existir
            cursor = self.connection.cursor()
            cursor.execute("CREATE DATABASE IF NOT EXISTS wp_legacy")
            cursor.execute("USE wp_legacy")
            
            # Ler e executar SQL
            with open(sql_file, 'r', encoding='utf-8', errors='ignore') as f:
                sql_content = f.read()
            
            # Dividir em comandos individuais
            commands = sql_content.split(';')
            
            for command in commands:
                command = command.strip()
                if command and not command.startswith('--'):
                    try:
                        cursor.execute(command)
                    except Error as e:
                        if "already exists" not in str(e).lower():
                            print(f"⚠️ Erro ao executar comando: {e}")
            
            self.connection.commit()
            print("✅ Dados importados para MySQL")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao importar para MySQL: {e}")
            return False
    
    def get_wordpress_posts(self):
        """Obtém posts do WordPress"""
        print("🔄 Buscando posts do WordPress")
        
        try:
            cursor = self.connection.cursor(dictionary=True)
            
            # Buscar posts publicados
            query = """
            SELECT 
                ID, post_title, post_content, post_excerpt, post_date, 
                post_name, post_status, post_type
            FROM wp_posts 
            WHERE post_type = 'post' 
            AND post_status = 'publish'
            ORDER BY post_date DESC
            """
            
            cursor.execute(query)
            posts = cursor.fetchall()
            
            print(f"✅ Encontrados {len(posts)} posts")
            return posts
            
        except Error as e:
            print(f"❌ Erro ao buscar posts: {e}")
            return []
    
    def create_blog_posts(self, wp_posts):
        """Cria posts no Wagtail"""
        print("🔄 Criando posts no Wagtail")
        
        # Encontrar ou criar BlogIndexPage
        blog_index = BlogIndexPage.objects.filter(slug='aprenda-marketing-digital').first()
        if not blog_index:
            print("❌ BlogIndexPage não encontrada")
            return
        
        # Mapeamento de posts existentes
        existing_posts = {}
        for post in BlogPage.objects.all():
            existing_posts[post.slug] = post
        
        for wp_post in wp_posts:
            try:
                # Limpar título e conteúdo
                title = wp_post['post_title'].strip()
                content = wp_post['post_content'].strip()
                
                if not title or not content:
                    continue
                
                # Criar slug
                slug = slugify(title)
                
                # Verificar se já existe
                if slug in existing_posts:
                    existing_post = existing_posts[slug]
                    
                    # Atualizar conteúdo se estiver vazio ou muito pequeno
                    if len(existing_post.body) < 1000:
                        print(f"📝 Atualizando conteúdo de: {title}")
                        
                        # Converter HTML para RichText
                        rich_content = RichText(content)
                        
                        existing_post.body = rich_content
                        existing_post.save()
                        existing_post.save_revision().publish()
                        
                        print(f"✅ Conteúdo atualizado: {title} ({len(content)} chars)")
                    else:
                        print(f"ℹ️ Post já tem conteúdo completo: {title}")
                else:
                    print(f"📄 Criando novo post: {title}")
                    
                    # Converter HTML para RichText
                    rich_content = RichText(content)
                    
                    # Criar post
                    blog_post = BlogPage(
                        title=title,
                        slug=slug,
                        date=wp_post['post_date'].date() if wp_post['post_date'] else None,
                        body=rich_content,
                        intro=wp_post['post_excerpt'][:200] if wp_post['post_excerpt'] else None,
                    )
                    
                    # Adicionar ao blog index
                    blog_index.add_child(instance=blog_post)
                    blog_post.save_revision().publish()
                    
                    print(f"✅ Post criado: {title}")
                
            except Exception as e:
                print(f"❌ Erro ao processar post {wp_post.get('post_title', 'Unknown')}: {e}")
    
    def run(self):
        """Executa o comando"""
        print("🚀 Iniciando importação de conteúdo WordPress")
        
        # Arquivo .wpress
        wpress_file = "/home/ubuntu/novosite-agenciakaizen-com-br-20250918-173213-xqm3zy7ohdo1.wpress"
        
        if not os.path.exists(wpress_file):
            print(f"❌ Arquivo não encontrado: {wpress_file}")
            return
        
        # Conectar ao MySQL
        if not self.connect_to_mysql():
            return
        
        try:
            # Extrair conteúdo
            sql_file = self.extract_wpress_content(wpress_file)
            if not sql_file:
                return
            
            # Importar para MySQL
            if not self.import_mysql_dump(sql_file):
                return
            
            # Obter posts
            wp_posts = self.get_wordpress_posts()
            if not wp_posts:
                return
            
            # Criar posts no Wagtail
            self.create_blog_posts(wp_posts)
            
            print("🎉 Importação concluída!")
            
        finally:
            if self.connection:
                self.connection.close()
            
            # Limpar arquivo temporário
            if 'sql_file' in locals():
                os.unlink(sql_file)

if __name__ == "__main__":
    command = Command()
    command.run()
