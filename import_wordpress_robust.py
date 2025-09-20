#!/usr/bin/env python3
"""
Script ROBUSTO para importar todos os posts e páginas do WordPress SQL para Wagtail
Com controle completo, logs e monitoramento de integridade
"""

import os
import sys
import re
import logging
import time
from datetime import datetime
from typing import Dict, List, Any

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

class WordPressImporter:
    def __init__(self, sql_file_path: str):
        self.sql_file_path = sql_file_path
        self.stats = {
            'total_found': 0,
            'posts_imported': 0,
            'pages_imported': 0,
            'skipped_duplicates': 0,
            'errors': 0,
            'start_time': time.time()
        }
        self.error_log = []
        
    def parse_sql_values(self, values_string: str) -> List[str]:
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

    def clean_value(self, value: str) -> str:
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

    def extract_posts_from_sql(self) -> List[Dict[str, Any]]:
        """Extrai todos os posts do arquivo SQL"""
        logger.info("🔍 Extraindo posts do arquivo SQL...")
        
        with open(self.sql_file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        logger.info(f"📖 Arquivo lido: {len(content):,} caracteres")
        
        # Encontrar todas as seções de posts
        posts_sections = re.findall(r'INSERT INTO `wp_posts`.*?VALUES\s*\((.*?)\);', content, re.DOTALL)
        
        if not posts_sections:
            logger.error("❌ Nenhuma seção de posts encontrada no SQL")
            return []
        
        all_posts = []
        
        for section_idx, section in enumerate(posts_sections):
            logger.info(f"📝 Processando seção {section_idx + 1}/{len(posts_sections)}")
            
            value_lines = re.findall(r'\((.*?)\)', section, re.DOTALL)
            
            for line_idx, line in enumerate(value_lines):
                try:
                    values = self.parse_sql_values(line)
                    
                    if len(values) >= 22:
                        post_data = {
                            'post_title': self.clean_value(values[5]),
                            'post_content': self.clean_value(values[4]),
                            'post_name': self.clean_value(values[11]),
                            'post_status': self.clean_value(values[7]),
                            'post_type': self.clean_value(values[20]),
                            'post_date': self.clean_value(values[2]),
                            'post_excerpt': self.clean_value(values[6]),
                        }
                        
                        # Filtrar apenas posts publicados com conteúdo
                        if (post_data.get('post_status') == 'publish' and 
                            post_data.get('post_title') and
                            post_data.get('post_content') and
                            post_data.get('post_type') in ['post', 'page']):
                            
                            all_posts.append(post_data)
                            
                except Exception as e:
                    logger.warning(f"⚠️ Erro ao processar linha {line_idx + 1} da seção {section_idx + 1}: {e}")
                    self.stats['errors'] += 1
                    continue
        
        self.stats['total_found'] = len(all_posts)
        logger.info(f"✅ {len(all_posts)} posts válidos encontrados")
        
        return all_posts

    def create_blog_post(self, post_data: Dict[str, Any], blog_index: BlogIndexPage) -> bool:
        """Cria um post do blog"""
        try:
            title = post_data.get('post_title', '').strip()
            content = post_data.get('post_content', '').strip()
            slug = post_data.get('post_name', '').strip()
            
            if not slug:
                slug = slugify(title)
            
            # Verificar se já existe
            if Page.objects.filter(slug=slug).exists():
                logger.debug(f"⏭️ Post já existe: {title}")
                self.stats['skipped_duplicates'] += 1
                return False
            
            # Converter HTML para RichText
            rich_content = RichText(content)
            
            # Criar data
            post_date = post_data.get('post_date', '').split(' ')[0] if post_data.get('post_date') else None
            
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
            
            self.stats['posts_imported'] += 1
            logger.info(f"✅ Post criado: {title}")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro ao criar post '{title}': {e}")
            self.stats['errors'] += 1
            self.error_log.append(f"Post '{title}': {e}")
            return False

    def create_page(self, post_data: Dict[str, Any], home_page: Page) -> bool:
        """Cria uma página"""
        try:
            title = post_data.get('post_title', '').strip()
            content = post_data.get('post_content', '').strip()
            slug = post_data.get('post_name', '').strip()
            
            if not slug:
                slug = slugify(title)
            
            # Verificar se já existe
            if Page.objects.filter(slug=slug).exists():
                logger.debug(f"⏭️ Página já existe: {title}")
                self.stats['skipped_duplicates'] += 1
                return False
            
            # Criar página
            page = HomePage(
                title=title,
                slug=slug,
            )
            
            # Adicionar à página inicial
            home_page.add_child(instance=page)
            page.save_revision().publish()
            
            self.stats['pages_imported'] += 1
            logger.info(f"✅ Página criada: {title}")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro ao criar página '{title}': {e}")
            self.stats['errors'] += 1
            self.error_log.append(f"Página '{title}': {e}")
            return False

    def import_posts(self, posts: List[Dict[str, Any]]) -> None:
        """Importa todos os posts"""
        logger.info("🚀 Iniciando importação dos posts...")
        
        # Encontrar páginas de destino
        blog_index = BlogIndexPage.objects.filter(slug='aprenda-marketing-digital').first()
        home_page = Page.objects.filter(slug='home').first()
        
        if not blog_index:
            logger.error("❌ BlogIndexPage 'aprenda-marketing-digital' não encontrada")
            return
        
        if not home_page:
            logger.error("❌ Página 'home' não encontrada")
            return
        
        logger.info("✅ Páginas de destino encontradas")
        
        # Processar posts em lotes para controle
        batch_size = 10
        total_batches = (len(posts) + batch_size - 1) // batch_size
        
        for batch_idx in range(total_batches):
            start_idx = batch_idx * batch_size
            end_idx = min(start_idx + batch_size, len(posts))
            batch_posts = posts[start_idx:end_idx]
            
            logger.info(f"📦 Processando lote {batch_idx + 1}/{total_batches} (posts {start_idx + 1}-{end_idx})")
            
            for post_data in batch_posts:
                post_type = post_data.get('post_type', '')
                
                if post_type == 'post':
                    self.create_blog_post(post_data, blog_index)
                elif post_type == 'page':
                    self.create_page(post_data, home_page)
                else:
                    logger.warning(f"⚠️ Tipo de post não suportado: {post_type}")
            
            # Log de progresso
            progress = ((batch_idx + 1) / total_batches) * 100
            logger.info(f"📊 Progresso: {progress:.1f}% - Posts: {self.stats['posts_imported']}, Páginas: {self.stats['pages_imported']}")

    def generate_report(self) -> None:
        """Gera relatório final da importação"""
        end_time = time.time()
        duration = end_time - self.stats['start_time']
        
        logger.info("=" * 60)
        logger.info("📊 RELATÓRIO FINAL DA IMPORTAÇÃO")
        logger.info("=" * 60)
        logger.info(f"⏱️ Tempo total: {duration:.2f} segundos")
        logger.info(f"📝 Posts encontrados no SQL: {self.stats['total_found']}")
        logger.info(f"✅ Posts importados: {self.stats['posts_imported']}")
        logger.info(f"✅ Páginas importadas: {self.stats['pages_imported']}")
        logger.info(f"⏭️ Pulados (duplicatas): {self.stats['skipped_duplicates']}")
        logger.info(f"❌ Erros: {self.stats['errors']}")
        logger.info(f"📈 Taxa de sucesso: {((self.stats['posts_imported'] + self.stats['pages_imported']) / max(1, self.stats['total_found'])) * 100:.1f}%")
        
        if self.error_log:
            logger.info("\n❌ ERROS ENCONTRADOS:")
            for error in self.error_log[:10]:  # Mostrar apenas os primeiros 10 erros
                logger.info(f"  - {error}")
            if len(self.error_log) > 10:
                logger.info(f"  ... e mais {len(self.error_log) - 10} erros")
        
        logger.info("=" * 60)

    def run(self) -> None:
        """Executa a importação completa"""
        logger.info("🚀 Iniciando importação robusta do WordPress")
        
        try:
            # 1. Extrair posts do SQL
            posts = self.extract_posts_from_sql()
            
            if not posts:
                logger.error("❌ Nenhum post válido encontrado")
                return
            
            # 2. Importar posts
            self.import_posts(posts)
            
            # 3. Gerar relatório
            self.generate_report()
            
            logger.info("🎉 Importação concluída com sucesso!")
            
        except Exception as e:
            logger.error(f"💥 Erro fatal na importação: {e}")
            self.generate_report()

def main():
    """Função principal"""
    sql_file = '/var/www/agenciakaizen/agenci93_wp177.sql'
    
    if not os.path.exists(sql_file):
        logger.error(f"❌ Arquivo SQL não encontrado: {sql_file}")
        return
    
    importer = WordPressImporter(sql_file)
    importer.run()

if __name__ == '__main__':
    main()

