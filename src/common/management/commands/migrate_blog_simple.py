"""
Comando simples para migrar posts do blog
"""
import sqlite3
from django.core.management.base import BaseCommand
from django.db import transaction
from blog.models import BlogIndexPage, BlogPage
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Migra posts do blog de forma simples'

    def handle(self, *args, **options):
        try:
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
                
                # Conectar ao SQLite
                sqlite_conn = sqlite3.connect('/var/www/agenciakaizen/src/db.sqlite3')
                sqlite_cursor = sqlite_conn.cursor()
                
                # Migrar posts do blog
                self.stdout.write('Migrando posts do blog...')
                sqlite_cursor.execute("""
                    SELECT p.id, p.title, p.slug, p.live, p.url_path, p.first_published_at, p.last_published_at,
                           COALESCE(b.intro, '') as intro, COALESCE(b.body, '') as body, COALESCE(b.date, p.first_published_at) as date
                    FROM wagtailcore_page p
                    LEFT JOIN blog_blogpage b ON p.id = b.page_ptr_id
                    WHERE p.content_type_id IN (SELECT id FROM django_content_type WHERE model = 'blogpage')
                    AND p.live = 1
                    ORDER BY p.first_published_at DESC
                    LIMIT 50
                """)
                posts_data = sqlite_cursor.fetchall()
                
                migrated_count = 0
                for post_data in posts_data:
                    try:
                        # Verificar se o post já existe
                        existing_post = BlogPage.objects.filter(id=post_data[0]).first()
                        if existing_post:
                            continue
                        
                        # Criar novo post
                        post = BlogPage(
                            id=post_data[0],
                            title=post_data[1],
                            slug=post_data[2],
                            live=bool(post_data[3]),
                            url_path=post_data[4],
                            first_published_at=post_data[5],
                            last_published_at=post_data[6],
                            owner=admin_user,
                            intro=post_data[7],
                            body=post_data[8],
                            date=post_data[9]
                        )
                        
                        # Definir como filha da página do blog
                        post = blog_index.add_child(instance=post)
                        
                        migrated_count += 1
                        if migrated_count % 10 == 0:
                            self.stdout.write(f'Migrados {migrated_count} posts...')
                        
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f'Erro ao migrar post {post_data[1]}: {e}'))
                
                sqlite_conn.close()
                self.stdout.write(self.style.SUCCESS(f'{migrated_count} posts do blog migrados com sucesso!'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erro durante migração: {e}'))
