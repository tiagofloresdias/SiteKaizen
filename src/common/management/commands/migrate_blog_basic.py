"""
Comando básico para migrar posts do blog sem JOIN
"""
import sqlite3
from django.core.management.base import BaseCommand
from django.db import transaction
from blog.models import BlogIndexPage, BlogPage
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Migra posts do blog de forma básica'

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
                    SELECT id, title, slug, live, url_path, first_published_at, last_published_at
                    FROM wagtailcore_page 
                    WHERE content_type_id IN (SELECT id FROM django_content_type WHERE model = 'blogpage')
                    AND live = 1
                    ORDER BY first_published_at DESC
                    LIMIT 20
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
                        from datetime import date
                        post = BlogPage(
                            id=post_data[0],
                            title=post_data[1],
                            slug=post_data[2],
                            live=bool(post_data[3]),
                            url_path=post_data[4],
                            first_published_at=post_data[5],
                            last_published_at=post_data[6],
                            owner=admin_user,
                            intro='',
                            body='<p>Conteúdo migrado do WordPress</p>',
                            date=post_data[5].date() if post_data[5] else date.today()
                        )
                        
                        # Definir como filha da página do blog
                        post = blog_index.add_child(instance=post)
                        
                        migrated_count += 1
                        self.stdout.write(f'Post migrado: {post.title}')
                        
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f'Erro ao migrar post {post_data[1]}: {e}'))
                
                sqlite_conn.close()
                self.stdout.write(self.style.SUCCESS(f'{migrated_count} posts do blog migrados com sucesso!'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erro durante migração: {e}'))
