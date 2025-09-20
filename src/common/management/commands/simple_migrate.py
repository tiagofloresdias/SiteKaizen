"""
Comando simples para migrar páginas principais do SQLite para PostgreSQL
"""
import sqlite3
from django.core.management.base import BaseCommand
from django.db import transaction
from wagtail.models import Page, Site
from django.conf import settings


class Command(BaseCommand):
    help = 'Migra páginas principais do SQLite para PostgreSQL'

    def handle(self, *args, **options):
        try:
            # Conectar ao SQLite
            sqlite_conn = sqlite3.connect('db.sqlite3')
            sqlite_cursor = sqlite_conn.cursor()
            
            # Buscar páginas principais (não blog posts)
            sqlite_cursor.execute("""
                SELECT id, title, slug, live, url_path, content_type_id, path, depth, numchild
                FROM wagtailcore_page 
                WHERE live = 1 
                AND url_path NOT LIKE '/home/aprenda-marketing-digital/%'
                AND url_path != '/home/'
                ORDER BY path
            """)
            
            pages_data = sqlite_cursor.fetchall()
            self.stdout.write(f'Encontradas {len(pages_data)} páginas principais para migrar')
            
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
                            seo_title='',
                            show_in_menus=False,
                            locked=False,
                            has_unpublished_changes=False,
                            owner_id=1
                        )
                        
                        page.save()
                        self.stdout.write(f'Página migrada: {page.title}')
                        
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f'Erro ao migrar página {page_data[1]}: {e}'))
            
            # Atualizar configuração do site
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
            
            self.stdout.write(self.style.SUCCESS('Migração concluída!'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erro durante migração: {e}'))
        finally:
            if 'sqlite_conn' in locals():
                sqlite_conn.close()
