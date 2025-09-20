#!/usr/bin/env python3
"""
Comando Django para aplicar imagens extraídas aos posts do blog
Usa apenas as imagens, sem nenhum código do WordPress original
"""

import os
import sys
from django.core.management.base import BaseCommand
from django.db import transaction

from wagtail.images.models import Image
from blog.models import BlogPage


class Command(BaseCommand):
    help = "Aplica imagens extraídas aos posts do blog"

    def add_arguments(self, parser):
        parser.add_argument(
            "--force", 
            action="store_true",
            help="Força a aplicação mesmo se o post já tiver imagem"
        )

    def handle(self, *args, **options):
        force = options.get('force', False)
        
        self.stdout.write("🖼️  Aplicando imagens aos posts do blog...")
        
        # Busca todas as imagens disponíveis
        images = Image.objects.all()
        
        if not images:
            self.stdout.write("⚠️  Nenhuma imagem encontrada no sistema")
            return
        
        self.stdout.write(f"📸 Imagens disponíveis: {images.count()}")
        for img in images:
            self.stdout.write(f"   - {img.title} ({img.width}x{img.height})")
        
        # Busca todos os posts do blog
        posts = BlogPage.objects.all()
        
        if not posts:
            self.stdout.write("⚠️  Nenhum post encontrado")
            return
        
        self.stdout.write(f"📝 Posts encontrados: {posts.count()}")
        
        applied_count = 0
        
        with transaction.atomic():
            for i, post in enumerate(posts):
                # Verifica se o post já tem imagem
                if post.featured_image and not force:
                    self.stdout.write(f"   ⏭️  {post.title} (já tem imagem)")
                    continue
                
                # Seleciona uma imagem baseada no índice do post
                image_index = i % images.count()
                selected_image = images[image_index]
                
                # Aplica a imagem ao post
                post.featured_image = selected_image
                post.save()
                
                # Publica a alteração
                post.save_revision().publish()
                
                self.stdout.write(f"   ✅ {post.title} -> {selected_image.title}")
                applied_count += 1
        
        self.stdout.write(f"\n🎉 Aplicação concluída!")
        self.stdout.write(f"📊 {applied_count} posts atualizados")
        
        if applied_count > 0:
            self.stdout.write("\n📝 Próximos passos:")
            self.stdout.write("   1. Verifique os posts no admin: /admin/pages/")
            self.stdout.write("   2. Ajuste as imagens conforme necessário")
            self.stdout.write("   3. Teste o frontend para ver as imagens")
        
        # Mostra estatísticas finais
        self.stdout.write(f"\n📊 Estatísticas finais:")
        posts_with_images = BlogPage.objects.filter(featured_image__isnull=False).count()
        total_posts = BlogPage.objects.count()
        self.stdout.write(f"   Posts com imagens: {posts_with_images}/{total_posts}")
        
        # Lista posts com imagens
        self.stdout.write(f"\n🖼️  Posts com imagens:")
        for post in BlogPage.objects.filter(featured_image__isnull=False):
            self.stdout.write(f"   - {post.title} -> {post.featured_image.title}")


def main():
    import django
    from django.conf import settings
    
    if not settings.configured:
        settings.configure(
            DEBUG=True,
            DATABASES={
                'default': {
                    'ENGINE': 'django.db.backends.sqlite3',
                    'NAME': 'db.sqlite3',
                }
            },
            INSTALLED_APPS=[
                'django.contrib.contenttypes',
                'django.contrib.auth',
                'wagtail.core',
                'wagtail.images',
                'blog',
            ]
        )
        django.setup()
    
    command = Command()
    command.handle()

if __name__ == "__main__":
    main()
