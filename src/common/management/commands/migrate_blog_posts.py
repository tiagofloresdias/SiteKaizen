"""
Comando para migrar posts do blog do SQLite para PostgreSQL
"""
import sqlite3
from django.core.management.base import BaseCommand
from django.db import transaction
from blog.models import BlogIndexPage, BlogPage
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Migra posts do blog do SQLite para PostgreSQL'

    def add_arguments(self, parser):
        parser.add_argument('--sqlite-db', type=str, default='/var/www/agenciakaizen/src/db.sqlite3',
                            help='Path to the SQLite database file.')

    def handle(self, *args, **options):
        sqlite_db_path = options['sqlite_db']
        
        try:
            # Conectar ao SQLite
            sqlite_conn = sqlite3.connect(sqlite_db_path)
            sqlite_cursor = sqlite_conn.cursor()
            
            with transaction.atomic():
                # Buscar usuário admin
                admin_user = User.objects.filter(is_superuser=True).first()
                if not admin_user:
                    self.stdout.write(self.style.ERROR('Usuário admin não encontrado'))
                    return
                
                # Buscar página do blog
                try:
                    blog_index = BlogIndexPage.objects.get(slug='aprenda-marketing-digital')
                except BlogIndexPage.DoesNotExist:
                    self.stdout.write(self.style.ERROR('Página do blog não encontrada'))
                    return
                
                # Migrar posts do blog
                self.stdout.write('Migrando posts do blog...')
                sqlite_cursor.execute("""
                    SELECT p.id, p.title, p.slug, p.live, p.url_path, p.content_type_id, p.path, p.depth, p.numchild, 
                           p.seo_title, p.show_in_menus, p.locked, p.locked_at, p.locked_by_id,
                           p.has_unpublished_changes, p.live_revision_id, p.first_published_at, p.last_published_at,
                           p.latest_revision_id, p.owner_id, b.intro, b.body, b.date
                    FROM wagtailcore_page p
                    LEFT JOIN blog_blogpage b ON p.id = b.page_ptr_id
                    WHERE p.content_type_id IN (SELECT id FROM django_content_type WHERE model = 'blogpage')
                    ORDER BY p.first_published_at DESC
                """)
                posts_data = sqlite_cursor.fetchall()
                
                migrated_count = 0
                for post_data in posts_data:
                    try:
                        # Verificar se o post já existe
                        existing_post = BlogPage.objects.filter(id=post_data[0]).first()
                        if existing_post:
                            self.stdout.write(f'Post {post_data[1]} já existe, pulando...')
                            continue
                        
                        # Criar novo post
                        post = BlogPage(
                            id=post_data[0],
                            title=post_data[1],
                            slug=post_data[2],
                            live=bool(post_data[3]),
                            url_path=post_data[4],
                            content_type_id=post_data[5],
                            path=post_data[6],
                            depth=post_data[7],
                            numchild=post_data[8],
                            seo_title=post_data[9] or '',
                            show_in_menus=bool(post_data[10]),
                            locked=bool(post_data[11]),
                            locked_at=post_data[12],
                            locked_by_id=post_data[13],
                            has_unpublished_changes=bool(post_data[14]),
                            live_revision_id=post_data[15],
                            first_published_at=post_data[16],
                            last_published_at=post_data[17],
                            latest_revision_id=post_data[18],
                            owner=admin_user,
                            intro=post_data[20] or '',
                            body=post_data[21] or '',
                            date=post_data[22]
                        )
                        
                        # Definir como filha da página do blog
                        post = blog_index.add_child(instance=post)
                        
                        migrated_count += 1
                        if migrated_count % 50 == 0:
                            self.stdout.write(f'Migrados {migrated_count} posts...')
                        
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f'Erro ao migrar post {post_data[1]}: {e}'))
                
                self.stdout.write(self.style.SUCCESS(f'{migrated_count} posts do blog migrados com sucesso!'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erro durante migração: {e}'))
        finally:
            sqlite_conn.close()
