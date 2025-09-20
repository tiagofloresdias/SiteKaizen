"""
Comando para migrar dados do SQLite para PostgreSQL
"""
import sqlite3
from django.core.management.base import BaseCommand
from django.db import transaction
from wagtail.models import Page, Site
from django.conf import settings


class Command(BaseCommand):
    help = 'Migra dados do SQLite para PostgreSQL'

    def add_arguments(self, parser):
        parser.add_argument(
            '--sqlite-path',
            type=str,
            default='db.sqlite3',
            help='Caminho para o arquivo SQLite'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Executa sem fazer alterações no banco'
        )

    def handle(self, *args, **options):
        sqlite_path = options['sqlite_path']
        dry_run = options['dry_run']
        
        if dry_run:
            self.stdout.write(self.style.WARNING('MODO DRY-RUN: Nenhuma alteração será feita'))
        
        try:
            # Conectar ao SQLite
            sqlite_conn = sqlite3.connect(sqlite_path)
            sqlite_cursor = sqlite_conn.cursor()
            
            # Verificar se há dados no SQLite
            sqlite_cursor.execute("SELECT COUNT(*) FROM wagtailcore_page")
            sqlite_count = sqlite_cursor.fetchone()[0]
            
            self.stdout.write(f'Páginas no SQLite: {sqlite_count}')
            
            if sqlite_count == 0:
                self.stdout.write(self.style.WARNING('Nenhuma página encontrada no SQLite'))
                return
            
            # Verificar páginas no PostgreSQL
            postgres_count = Page.objects.count()
            self.stdout.write(f'Páginas no PostgreSQL: {postgres_count}')
            
            if not dry_run:
                # Migrar páginas
                self.migrate_pages(sqlite_cursor)
                
                # Migrar sites
                self.migrate_sites(sqlite_cursor)
                
                # Atualizar configuração do site
                self.update_site_config()
                
                self.stdout.write(self.style.SUCCESS('Migração concluída com sucesso!'))
            else:
                self.stdout.write('DRY-RUN: Migração seria executada aqui')
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erro durante migração: {e}'))
        finally:
            if 'sqlite_conn' in locals():
                sqlite_conn.close()

    def migrate_pages(self, sqlite_cursor):
        """Migra páginas do SQLite para PostgreSQL"""
        self.stdout.write('Migrando páginas...')
        
        # Buscar todas as páginas do SQLite
        sqlite_cursor.execute("""
            SELECT id, title, slug, live, url_path, content_type_id, path, depth, numchild, 
                   seo_title, show_in_menus, locked, locked_at, locked_by_id,
                   has_unpublished_changes, live_revision_id, first_published_at, last_published_at,
                   latest_revision_id, owner_id
            FROM wagtailcore_page 
            ORDER BY path
        """)
        
        pages_data = sqlite_cursor.fetchall()
        
        with transaction.atomic():
            for page_data in pages_data:
                try:
                    # Verificar se a página já existe
                    existing_page = Page.objects.filter(id=page_data[0]).first()
                    if existing_page:
                        self.stdout.write(f'Página {page_data[1]} já existe, pulando...')
                        continue
                    
                    # Criar nova página
                    page = Page(
                        id=page_data[0],
                        title=page_data[1],
                        slug=page_data[2],
                        live=bool(page_data[3]),
                        url_path=page_data[4],
                        content_type_id=page_data[5],
                        path=page_data[6],
                        depth=page_data[7],
                        numchild=page_data[8],
                        seo_title=page_data[9] or '',
                        show_in_menus=bool(page_data[10]),
                        locked=bool(page_data[11]),
                        locked_at=page_data[12],
                        locked_by_id=page_data[13],
                        has_unpublished_changes=bool(page_data[14]),
                        live_revision_id=page_data[15],
                        first_published_at=page_data[16],
                        last_published_at=page_data[17],
                        latest_revision_id=page_data[18],
                        owner_id=page_data[19]
                    )
                    
                    page.save()
                    self.stdout.write(f'Página migrada: {page.title}')
                    
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Erro ao migrar página {page_data[1]}: {e}'))

    def migrate_sites(self, sqlite_cursor):
        """Migra sites do SQLite para PostgreSQL"""
        self.stdout.write('Migrando sites...')
        
        sqlite_cursor.execute("""
            SELECT id, hostname, port, is_default_site, root_page_id, site_name
            FROM wagtailcore_site
        """)
        
        sites_data = sqlite_cursor.fetchall()
        
        with transaction.atomic():
            for site_data in sites_data:
                try:
                    # Verificar se o site já existe
                    existing_site = Site.objects.filter(id=site_data[0]).first()
                    if existing_site:
                        self.stdout.write(f'Site {site_data[1]} já existe, pulando...')
                        continue
                    
                    # Buscar a página raiz
                    root_page = Page.objects.filter(id=site_data[4]).first()
                    if not root_page:
                        self.stdout.write(self.style.WARNING(f'Página raiz {site_data[4]} não encontrada'))
                        continue
                    
                    # Criar novo site
                    site = Site(
                        id=site_data[0],
                        hostname=site_data[1],
                        port=site_data[2],
                        is_default_site=bool(site_data[3]),
                        root_page=root_page,
                        site_name=site_data[5] or ''
                    )
                    
                    site.save()
                    self.stdout.write(f'Site migrado: {site.hostname}')
                    
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Erro ao migrar site {site_data[1]}: {e}'))

    def update_site_config(self):
        """Atualiza configuração do site para agenciakaizen.com.br"""
        try:
            site = Site.objects.first()
            if site:
                site.hostname = 'agenciakaizen.com.br'
                site.port = 80
                site.is_default_site = True
                site.save()
                self.stdout.write('Configuração do site atualizada para agenciakaizen.com.br')
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erro ao atualizar configuração do site: {e}'))
