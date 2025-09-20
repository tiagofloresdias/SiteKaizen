#!/usr/bin/env python3
"""
Comando Django para importar imagens extraídas do backup WordPress
Importa apenas as imagens, sem nenhum código do WordPress original
"""

import os
import sys
from pathlib import Path
from django.core.management.base import BaseCommand
from django.core.files import File
from django.core.files.base import ContentFile

from wagtail.images.models import Image
from wagtail.documents.models import Document


class Command(BaseCommand):
    help = "Importa imagens extraídas do backup WordPress para o sistema de mídia do Wagtail"

    def add_arguments(self, parser):
        parser.add_argument(
            "--images-path", 
            default="media/original_images",
            help="Caminho para as imagens extraídas"
        )

    def handle(self, *args, **options):
        images_path = options['images_path']
        
        if not os.path.exists(images_path):
            self.stdout.write(
                self.style.ERROR(f"Caminho não encontrado: {images_path}")
            )
            return
        
        self.stdout.write("🖼️  Iniciando importação de imagens...")
        
        # Lista arquivos de imagem
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
        image_files = []
        
        for file_path in Path(images_path).iterdir():
            if file_path.is_file() and file_path.suffix.lower() in image_extensions:
                image_files.append(file_path)
        
        if not image_files:
            self.stdout.write("⚠️  Nenhuma imagem encontrada")
            return
        
        self.stdout.write(f"📸 Encontradas {len(image_files)} imagens:")
        
        imported_count = 0
        for image_file in image_files:
            try:
                # Verifica se a imagem já existe
                existing_image = Image.objects.filter(
                    file__icontains=image_file.name
                ).first()
                
                if existing_image:
                    self.stdout.write(f"   ⏭️  {image_file.name} (já existe)")
                    continue
                
                # Lê o arquivo
                with open(image_file, 'rb') as f:
                    image_content = ContentFile(f.read(), name=image_file.name)
                
                # Cria o nome do arquivo
                file_name = image_file.name
                
                # Determina o título baseado no nome do arquivo
                title = file_name.replace('_', ' ').replace('-', ' ').replace('.', ' ')
                title = ' '.join(word.capitalize() for word in title.split())
                
                # Cria a imagem no Wagtail
                wagtail_image = Image(
                    title=title,
                    file=image_content
                )
                wagtail_image.save()
                
                self.stdout.write(f"   ✅ {file_name} -> {title}")
                imported_count += 1
                
            except Exception as e:
                self.stdout.write(f"   ❌ {image_file.name}: {e}")
        
        self.stdout.write(f"\n🎉 Importação concluída!")
        self.stdout.write(f"📊 {imported_count} imagens importadas")
        
        if imported_count > 0:
            self.stdout.write("\n📝 Próximos passos:")
            self.stdout.write("   1. Acesse o admin: /admin/images/image/")
            self.stdout.write("   2. Edite as imagens para adicionar títulos descritivos")
            self.stdout.write("   3. Use as imagens nos posts e páginas")
        
        # Lista as imagens disponíveis
        self.stdout.write(f"\n🖼️  Imagens disponíveis no sistema:")
        for img in Image.objects.all():
            self.stdout.write(f"   - {img.title} ({img.file.name})")


def main():
    if len(sys.argv) != 3:
        print("Uso: python import_images.py --images-path <caminho>")
        sys.exit(1)
    
    images_path = sys.argv[2]
    
    # Simula a execução do comando Django
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
                'wagtail.documents',
            ]
        )
        django.setup()
    
    command = Command()
    command.handle(images_path=images_path)

if __name__ == "__main__":
    main()
