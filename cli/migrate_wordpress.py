#!/usr/bin/env python3
"""
Utilitário CLI para migração de conteúdo do WordPress para Wagtail CMS
Agência Kaizen - Sistema de Migração Inteligente
"""

import os
import sys
import json
import requests
import argparse
import hashlib
import mimetypes
import time
from datetime import datetime
from pathlib import Path
from urllib.parse import urljoin, urlparse, unquote
import re
import logging
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

# Adicionar o diretório src ao path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agenciakaizen_cms.settings.dev')
import django
django.setup()

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.files.images import ImageFile
from wagtail.models import Page, Site
from wagtail.images.models import Image
from home.models import HomePage
from blog.models import BlogPage, BlogIndexPage, BlogCategory
from portfolio.models import PortfolioItem, PortfolioIndexPage, PortfolioCategory
from services.models import ServicePage, ServicesIndexPage
from contact.models import ContactPage


@dataclass
class MigrationStats:
    """Estatísticas da migração"""
    posts_migrated: int = 0
    pages_migrated: int = 0
    images_downloaded: int = 0
    categories_created: int = 0
    errors: int = 0
    url_mappings: Dict[str, str] = None
    
    def __post_init__(self):
        if self.url_mappings is None:
            self.url_mappings = {}


@dataclass
class ImageInfo:
    """Informações sobre uma imagem"""
    url: str
    filename: str
    content_type: str
    size: int
    wagtail_image: Optional[Image] = None


class ImageDownloader:
    """Classe para download seguro de imagens"""
    
    ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg'}
    ALLOWED_MIME_TYPES = {
        'image/jpeg', 'image/jpg', 'image/png', 'image/gif', 
        'image/webp', 'image/svg+xml'
    }
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    MIN_FILE_SIZE = 1024  # 1KB
    
    def __init__(self, session: requests.Session):
        self.session = session
        self.downloaded_images: Dict[str, ImageInfo] = {}
        
    def is_valid_image_url(self, url: str) -> bool:
        """Verifica se a URL é uma imagem válida"""
        try:
            parsed = urlparse(url)
            if not parsed.scheme or not parsed.netloc:
                return False
                
            # Verificar extensão
            path = unquote(parsed.path).lower()
            if not any(path.endswith(ext) for ext in self.ALLOWED_EXTENSIONS):
                return False
                
            return True
        except Exception:
            return False
    
    def get_image_info(self, url: str) -> Optional[ImageInfo]:
        """Obtém informações da imagem sem baixar o conteúdo completo"""
        try:
            response = self.session.head(url, timeout=10, allow_redirects=True)
            response.raise_for_status()
            
            content_type = response.headers.get('content-type', '').lower()
            content_length = int(response.headers.get('content-length', 0))
            
            if content_type not in self.ALLOWED_MIME_TYPES:
                return None
                
            if content_length > self.MAX_FILE_SIZE or content_length < self.MIN_FILE_SIZE:
                return None
                
            # Gerar nome de arquivo único
            url_hash = hashlib.md5(url.encode()).hexdigest()[:8]
            parsed_url = urlparse(url)
            original_filename = os.path.basename(unquote(parsed_url.path))
            
            if not original_filename or '.' not in original_filename:
                original_filename = f"image_{url_hash}.jpg"
                
            filename = f"wp_{url_hash}_{original_filename}"
            
            return ImageInfo(
                url=url,
                filename=filename,
                content_type=content_type,
                size=content_length
            )
            
        except Exception as e:
            logging.warning(f"Erro ao obter informações da imagem {url}: {e}")
            return None
    
    def download_image(self, image_info: ImageInfo) -> Optional[Image]:
        """Baixa a imagem e cria objeto Image do Wagtail"""
        try:
            # Verificar se já foi baixada
            if image_info.url in self.downloaded_images:
                return self.downloaded_images[image_info.url].wagtail_image
            
            response = self.session.get(image_info.url, timeout=30, stream=True)
            response.raise_for_status()
            
            # Verificar tamanho real
            content = response.content
            if len(content) > self.MAX_FILE_SIZE or len(content) < self.MIN_FILE_SIZE:
                logging.warning(f"Imagem {image_info.url} fora do tamanho permitido")
                return None
            
            # Verificar tipo MIME real
            import magic
            mime_type = magic.from_buffer(content, mime=True)
            if mime_type not in self.ALLOWED_MIME_TYPES:
                logging.warning(f"Tipo MIME inválido para {image_info.url}: {mime_type}")
                return None
            
            # Criar arquivo temporário
            file_content = ContentFile(content)
            file_path = f"migrated_images/{image_info.filename}"
            
            # Salvar no storage do Django
            saved_path = default_storage.save(file_path, file_content)
            
            # Criar objeto Image do Wagtail
            wagtail_image = Image.objects.create(
                title=image_info.filename,
                file=saved_path
            )
            
            # Atualizar informações
            image_info.wagtail_image = wagtail_image
            self.downloaded_images[image_info.url] = image_info
            
            logging.info(f"Imagem baixada: {image_info.url} -> {saved_path}")
            return wagtail_image
            
        except Exception as e:
            logging.error(f"Erro ao baixar imagem {image_info.url}: {e}")
            return None


class HTMLProcessor:
    """Classe para processamento inteligente de HTML"""
    
    def __init__(self, image_downloader: ImageDownloader):
        self.image_downloader = image_downloader
        self.url_mappings: Dict[str, str] = {}
    
    def clean_wordpress_html(self, html_content: str) -> str:
        """Limpa HTML do WordPress mantendo estrutura"""
        if not html_content:
            return ""
        
        # Remover scripts e estilos inline perigosos
        html_content = re.sub(r'<script[^>]*>.*?</script>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
        html_content = re.sub(r'<style[^>]*>.*?</style>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
        
        # Converter shortcodes do WordPress
        html_content = self._convert_wordpress_shortcodes(html_content)
        
        # Limpar classes CSS específicas do WordPress
        html_content = re.sub(r'class="[^"]*wp-[^"]*"', '', html_content)
        html_content = re.sub(r'id="[^"]*wp-[^"]*"', '', html_content)
        
        # Processar imagens
        html_content = self._process_images(html_content)
        
        # Limpar elementos vazios
        html_content = re.sub(r'<p>\s*</p>', '', html_content)
        html_content = re.sub(r'<div>\s*</div>', '', html_content)
        
        return html_content.strip()
    
    def _convert_wordpress_shortcodes(self, html: str) -> str:
        """Converte shortcodes do WordPress"""
        # Gallery
        html = re.sub(r'\[gallery[^\]]*\]', '', html)
        
        # Caption
        html = re.sub(r'\[caption[^\]]*\](.*?)\[/caption\]', r'\1', html, flags=re.DOTALL)
        
        # Embed
        html = re.sub(r'\[embed[^\]]*\](.*?)\[/embed\]', r'\1', html, flags=re.DOTALL)
        
        # Video
        html = re.sub(r'\[video[^\]]*\](.*?)\[/video\]', r'<video controls>\1</video>', html, flags=re.DOTALL)
        
        # Audio
        html = re.sub(r'\[audio[^\]]*\](.*?)\[/audio\]', r'<audio controls>\1</audio>', html, flags=re.DOTALL)
        
        return html
    
    def _process_images(self, html: str) -> str:
        """Processa imagens no HTML"""
        def replace_image(match):
            img_tag = match.group(0)
            src_match = re.search(r'src="([^"]*)"', img_tag)
            
            if not src_match:
                return img_tag
                
            img_url = src_match.group(1)
            
            # Verificar se é uma URL válida
            if not self.image_downloader.is_valid_image_url(img_url):
                return img_tag
            
            # Obter informações da imagem
            image_info = self.image_downloader.get_image_info(img_url)
            if not image_info:
                return img_tag
            
            # Baixar imagem
            wagtail_image = self.image_downloader.download_image(image_info)
            if not wagtail_image:
                return img_tag
            
            # Substituir src pela URL do Wagtail
            new_src = wagtail_image.file.url
            new_img_tag = img_tag.replace(f'src="{img_url}"', f'src="{new_src}"')
            
            # Adicionar atributos de acessibilidade se não existirem
            if 'alt=' not in new_img_tag:
                new_img_tag = new_img_tag.replace('>', f' alt="{wagtail_image.title}">')
            
            return new_img_tag
        
        # Processar todas as tags img
        html = re.sub(r'<img[^>]*>', replace_image, html)
        
        return html
    
    def extract_excerpt(self, html_content: str, max_length: int = 250) -> str:
        """Extrai excerpt limpo do HTML"""
        if not html_content:
            return ""
        
        # Remover HTML tags
        text = re.sub(r'<[^>]+>', '', html_content)
        
        # Limpar espaços extras
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Truncar se necessário
        if len(text) > max_length:
            text = text[:max_length].rsplit(' ', 1)[0] + '...'
        
        return text


class URLMapper:
    """Classe para mapeamento de URLs"""
    
    def __init__(self):
        self.mappings: Dict[str, str] = {}
        self.reverse_mappings: Dict[str, str] = {}
    
    def add_mapping(self, old_url: str, new_url: str):
        """Adiciona mapeamento de URL"""
        self.mappings[old_url] = new_url
        self.reverse_mappings[new_url] = old_url
    
    def get_new_url(self, old_url: str) -> Optional[str]:
        """Obtém nova URL baseada na antiga"""
        return self.mappings.get(old_url)
    
    def get_old_url(self, new_url: str) -> Optional[str]:
        """Obtém URL antiga baseada na nova"""
        return self.reverse_mappings.get(new_url)
    
    def save_mappings(self, filepath: str):
        """Salva mapeamentos em arquivo JSON"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump({
                'mappings': self.mappings,
                'reverse_mappings': self.reverse_mappings,
                'created_at': datetime.now().isoformat()
            }, f, indent=2, ensure_ascii=False)
    
    def load_mappings(self, filepath: str):
        """Carrega mapeamentos de arquivo JSON"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.mappings = data.get('mappings', {})
                self.reverse_mappings = data.get('reverse_mappings', {})
        except FileNotFoundError:
            pass


class WordPressMigrator:
    """
    Classe principal para migração de conteúdo do WordPress
    """
    
    def __init__(self, wp_url, wp_user=None, wp_password=None, dry_run=False):
        self.wp_url = wp_url.rstrip('/')
        self.wp_user = wp_user
        self.wp_password = wp_password
        self.dry_run = dry_run
        self.session = requests.Session()
        self.stats = MigrationStats()
        self.url_mapper = URLMapper()
        
        # Configurar logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('migration.log'),
                logging.StreamHandler()
            ]
        )
        
        # Configurar sessão
        self.session.headers.update({
            'User-Agent': 'Agência Kaizen Migration Tool/1.0'
        })
        
        if wp_user and wp_password:
            self.session.auth = (wp_user, wp_password)
        
        # Inicializar processadores
        self.image_downloader = ImageDownloader(self.session)
        self.html_processor = HTMLProcessor(self.image_downloader)
        
        # Carregar mapeamentos existentes
        self.url_mapper.load_mappings('url_mappings.json')
    
    def get_wp_posts(self, post_type='posts', per_page=100, page=1):
        """
        Buscar posts do WordPress via API REST com paginação
        """
        url = f"{self.wp_url}/wp-json/wp/v2/{post_type}"
        params = {
            'per_page': per_page,
            'page': page,
            'status': 'publish',
            '_embed': True
        }
        
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logging.error(f"Erro ao buscar posts: {e}")
            return []
    
    def get_all_wp_posts(self, post_type='posts', per_page=100):
        """
        Buscar todos os posts com paginação automática
        """
        all_posts = []
        page = 1
        
        while True:
            posts = self.get_wp_posts(post_type, per_page, page)
            if not posts:
                break
                
            all_posts.extend(posts)
            page += 1
            
            # Rate limiting
            time.sleep(0.5)
        
        return all_posts
    
    def get_wp_categories(self):
        """
        Buscar categorias do WordPress
        """
        url = f"{self.wp_url}/wp-json/wp/v2/categories"
        
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Erro ao buscar categorias: {e}")
            return []
    
    def download_image(self, image_url, filename):
        """
        Baixar imagem do WordPress e salvar no Wagtail
        """
        try:
            response = self.session.get(image_url, stream=True)
            response.raise_for_status()
            
            # Criar arquivo temporário
            file_content = ContentFile(response.content)
            file_path = f"migrated_images/{filename}"
            
            # Salvar no storage do Django
            saved_path = default_storage.save(file_path, file_content)
            return saved_path
        except Exception as e:
            print(f"Erro ao baixar imagem {image_url}: {e}")
            return None
    
    def clean_html(self, html_content):
        """
        Limpar HTML do WordPress para formato compatível com Wagtail
        """
        if not html_content:
            return ""
        
        # Remover scripts e estilos inline
        html_content = re.sub(r'<script[^>]*>.*?</script>', '', html_content, flags=re.DOTALL)
        html_content = re.sub(r'<style[^>]*>.*?</style>', '', html_content, flags=re.DOTALL)
        
        # Converter shortcodes do WordPress (exemplo básico)
        html_content = re.sub(r'\[gallery[^\]]*\]', '', html_content)
        html_content = re.sub(r'\[caption[^\]]*\](.*?)\[/caption\]', r'\1', html_content, flags=re.DOTALL)
        
        # Limpar classes CSS específicas do WordPress
        html_content = re.sub(r'class="[^"]*wp-[^"]*"', '', html_content)
        
        return html_content.strip()
    
    def migrate_categories(self):
        """
        Migrar categorias do WordPress para o Wagtail
        """
        print("Migrando categorias...")
        wp_categories = self.get_wp_categories()
        
        for wp_cat in wp_categories:
            category, created = BlogCategory.objects.get_or_create(
                slug=wp_cat['slug'],
                defaults={
                    'name': wp_cat['name']
                }
            )
            
            if created:
                print(f"Criada categoria: {category.name}")
            else:
                print(f"Categoria já existe: {category.name}")
    
    def migrate_blog_posts(self):
        """
        Migrar posts do blog do WordPress para o Wagtail
        """
        logging.info("Iniciando migração de posts do blog...")
        
        # Criar página de índice do blog se não existir
        try:
            blog_index = BlogIndexPage.objects.get(slug='blog')
        except BlogIndexPage.DoesNotExist:
            if not self.dry_run:
                home_page = HomePage.objects.first()
                if not home_page:
                    logging.error("Home page não encontrada")
                    return
                
                blog_index = BlogIndexPage(
                    title="Blog",
                    slug="blog",
                    intro="<p>Artigos, dicas e insights sobre desenvolvimento web, marketing digital e tecnologia.</p>"
                )
                home_page.add_child(instance=blog_index)
                blog_index.save()
                logging.info("Página de índice do blog criada")
            else:
                logging.info("DRY RUN: Página de índice do blog seria criada")
                return
        
        # Buscar todos os posts do WordPress
        wp_posts = self.get_all_wp_posts('posts')
        logging.info(f"Encontrados {len(wp_posts)} posts para migrar")
        
        for wp_post in wp_posts:
            try:
                # Verificar se o post já existe
                if BlogPage.objects.filter(slug=wp_post['slug']).exists():
                    logging.info(f"Post já existe: {wp_post['title']['rendered']}")
                    continue
                
                # Processar HTML do conteúdo
                clean_content = self.html_processor.clean_wordpress_html(wp_post['content']['rendered'])
                clean_excerpt = self.html_processor.extract_excerpt(clean_content)
                
                if self.dry_run:
                    logging.info(f"DRY RUN: Post seria migrado: {wp_post['title']['rendered']}")
                    self.stats.posts_migrated += 1
                    continue
                
                # Criar post do blog
                blog_post = BlogPage(
                    title=wp_post['title']['rendered'],
                    slug=wp_post['slug'],
                    intro=clean_excerpt,
                    body=clean_content,
                    date=datetime.fromisoformat(wp_post['date'].replace('Z', '+00:00')).date(),
                    live=True,
                    show_in_menus=False
                )
                
                # Adicionar à página de índice do blog
                blog_index.add_child(instance=blog_post)
                blog_post.save()
                
                # Mapear URL
                old_url = f"{self.wp_url}/{wp_post['slug']}/"
                new_url = f"/blog/{wp_post['slug']}/"
                self.url_mapper.add_mapping(old_url, new_url)
                
                # Migrar imagem destacada se existir
                if wp_post.get('_embedded') and 'wp:featuredmedia' in wp_post['_embedded']:
                    featured_media = wp_post['_embedded']['wp:featuredmedia'][0]
                    if featured_media.get('source_url'):
                        image_url = featured_media['source_url']
                        if self.image_downloader.is_valid_image_url(image_url):
                            image_info = self.image_downloader.get_image_info(image_url)
                            if image_info:
                                wagtail_image = self.image_downloader.download_image(image_info)
                                if wagtail_image:
                                    blog_post.featured_image = wagtail_image
                                    blog_post.save()
                                    self.stats.images_downloaded += 1
                
                # Migrar categorias
                if wp_post.get('categories'):
                    wp_categories = self.get_wp_categories()
                    category_map = {cat['id']: cat['slug'] for cat in wp_categories}
                    
                    for cat_id in wp_post['categories']:
                        if cat_id in category_map:
                            try:
                                category = BlogCategory.objects.get(slug=category_map[cat_id])
                                blog_post.categories.add(category)
                            except BlogCategory.DoesNotExist:
                                pass
                
                self.stats.posts_migrated += 1
                logging.info(f"Post migrado: {blog_post.title}")
                
                # Rate limiting
                time.sleep(0.2)
                
            except Exception as e:
                logging.error(f"Erro ao migrar post {wp_post.get('title', {}).get('rendered', 'Unknown')}: {e}")
                self.stats.errors += 1
    
    def migrate_pages(self):
        """
        Migrar páginas do WordPress para o Wagtail
        """
        print("Migrando páginas...")
        wp_pages = self.get_wp_posts('pages')
        
        for wp_page in wp_pages:
            # Pular páginas especiais
            if wp_page['slug'] in ['home', 'blog', 'contact']:
                continue
            
            # Verificar se a página já existe
            if Page.objects.filter(slug=wp_page['slug']).exists():
                print(f"Página já existe: {wp_page['title']['rendered']}")
                continue
            
            # Criar página genérica
            page = Page(
                title=wp_page['title']['rendered'],
                slug=wp_page['slug'],
                live=True,
                show_in_menus=True
            )
            
            # Adicionar à home page
            home_page = HomePage.objects.first()
            if home_page:
                home_page.add_child(instance=page)
                page.save()
                print(f"Migrada página: {page.title}")
    
    def migrate_media(self):
        """
        Migrar mídia do WordPress
        """
        print("Migrando mídia...")
        # Implementar migração de mídia se necessário
        pass
    
    def run_migration(self):
        """
        Executar migração completa
        """
        logging.info("Iniciando migração do WordPress para Wagtail...")
        logging.info(f"URL do WordPress: {self.wp_url}")
        logging.info(f"Modo dry-run: {self.dry_run}")
        
        try:
            # Testar conexão
            response = self.session.get(f"{self.wp_url}/wp-json/wp/v2/")
            response.raise_for_status()
            logging.info("Conexão com WordPress estabelecida com sucesso!")
        except requests.RequestException as e:
            logging.error(f"Erro ao conectar com WordPress: {e}")
            return False
        
        start_time = time.time()
        
        try:
            # Executar migrações
            self.migrate_categories()
            self.migrate_blog_posts()
            self.migrate_pages()
            self.migrate_media()
            
            # Salvar mapeamentos de URL
            self.url_mapper.save_mappings('url_mappings.json')
            
            # Gerar relatório
            self.generate_report()
            
            end_time = time.time()
            duration = end_time - start_time
            
            logging.info(f"Migração concluída em {duration:.2f} segundos!")
            logging.info(f"Estatísticas: {self.stats}")
            
            return True
            
        except Exception as e:
            logging.error(f"Erro durante a migração: {e}")
            return False
    
    def generate_report(self):
        """
        Gerar relatório de migração
        """
        report = {
            'migration_date': datetime.now().isoformat(),
            'wordpress_url': self.wp_url,
            'dry_run': self.dry_run,
            'stats': {
                'posts_migrated': self.stats.posts_migrated,
                'pages_migrated': self.stats.pages_migrated,
                'images_downloaded': self.stats.images_downloaded,
                'categories_created': self.stats.categories_created,
                'errors': self.stats.errors
            },
            'url_mappings_count': len(self.url_mapper.mappings),
            'downloaded_images': len(self.image_downloader.downloaded_images)
        }
        
        with open('migration_report.json', 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        logging.info(f"Relatório salvo em: migration_report.json")
    
    def create_redirects_file(self, output_file='redirects.txt'):
        """
        Criar arquivo de redirecionamentos para Nginx/Apache
        """
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("# Redirecionamentos do WordPress para Wagtail\n")
            f.write("# Gerado automaticamente pelo sistema de migração\n\n")
            
            for old_url, new_url in self.url_mapper.mappings.items():
                # Remover domínio da URL antiga
                old_path = old_url.replace(self.wp_url, '')
                f.write(f"rewrite ^{old_path}$ {new_url} permanent;\n")
        
        logging.info(f"Arquivo de redirecionamentos criado: {output_file}")


def main():
    """
    Função principal do CLI
    """
    parser = argparse.ArgumentParser(
        description='Migrar conteúdo do WordPress para Wagtail CMS - Agência Kaizen',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  python migrate_wordpress.py --wp-url https://www.agenciakaizen.com.br
  python migrate_wordpress.py --wp-url https://www.agenciakaizen.com.br --dry-run
  python migrate_wordpress.py --wp-url https://www.agenciakaizen.com.br --posts-only --wp-user admin --wp-password senha
  python migrate_wordpress.py --wp-url https://www.agenciakaizen.com.br --create-redirects
        """
    )
    
    parser.add_argument('--wp-url', required=True, help='URL do site WordPress (ex: https://www.agenciakaizen.com.br)')
    parser.add_argument('--wp-user', help='Usuário do WordPress (opcional)')
    parser.add_argument('--wp-password', help='Senha do WordPress (opcional)')
    parser.add_argument('--dry-run', action='store_true', help='Simular migração sem fazer alterações')
    parser.add_argument('--posts-only', action='store_true', help='Migrar apenas posts do blog')
    parser.add_argument('--pages-only', action='store_true', help='Migrar apenas páginas')
    parser.add_argument('--media-only', action='store_true', help='Migrar apenas mídia')
    parser.add_argument('--create-redirects', action='store_true', help='Criar arquivo de redirecionamentos')
    parser.add_argument('--per-page', type=int, default=100, help='Posts por página na API (padrão: 100)')
    parser.add_argument('--max-posts', type=int, help='Número máximo de posts para migrar')
    parser.add_argument('--log-level', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'], 
                       default='INFO', help='Nível de log (padrão: INFO)')
    
    args = parser.parse_args()
    
    # Configurar nível de log
    logging.getLogger().setLevel(getattr(logging, args.log_level))
    
    # Criar migrador
    migrator = WordPressMigrator(
        wp_url=args.wp_url, 
        wp_user=args.wp_user, 
        wp_password=args.wp_password,
        dry_run=args.dry_run
    )
    
    # Configurar limite de posts se especificado
    if args.max_posts:
        migrator.max_posts = args.max_posts
    
    try:
        if args.posts_only:
            logging.info("Migrando apenas posts do blog...")
            migrator.migrate_categories()
            migrator.migrate_blog_posts()
        elif args.pages_only:
            logging.info("Migrando apenas páginas...")
            migrator.migrate_pages()
        elif args.media_only:
            logging.info("Migrando apenas mídia...")
            migrator.migrate_media()
        else:
            logging.info("Executando migração completa...")
            migrator.run_migration()
        
        # Criar arquivo de redirecionamentos se solicitado
        if args.create_redirects:
            migrator.create_redirects_file()
        
        logging.info("Processo concluído com sucesso!")
        
    except KeyboardInterrupt:
        logging.info("Migração interrompida pelo usuário")
    except Exception as e:
        logging.error(f"Erro fatal: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
