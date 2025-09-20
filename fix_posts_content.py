#!/usr/bin/env python3
"""
Script para corrigir o conteúdo dos posts existentes removendo \n duplicados
"""

import os
import sys
import re

# Adiciona o diretório src ao path
sys.path.append('/var/www/agenciakaizen/src')

# Configura Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agenciakaizen_cms.settings.dev')
import django
django.setup()

from blog.models import BlogPage

def fix_post_content(content):
    """
    Corrige o conteúdo do post removendo \n duplicados e escapando corretamente
    """
    if not content:
        return content
    
    # Remove escapes de aspas
    content = content.replace('\\"', '"').replace("\\'", "'")
    
    # Remove barras invertidas duplas
    content = content.replace('\\\\', '\\')
    
    # Remove \n duplicados (mais de 2 seguidos)
    content = re.sub(r'\\n{3,}', '\\n\\n', content)
    
    return content

def main():
    print("🔧 Iniciando correção do conteúdo dos posts...")
    
    posts = BlogPage.objects.all()
    total_posts = posts.count()
    fixed_count = 0
    
    print(f"📊 Total de posts encontrados: {total_posts}")
    
    for i, post in enumerate(posts, 1):
        print(f"📝 Processando post {i}/{total_posts}: {post.title}")
        
        # Corrige o body
        if post.body:
            original_body = post.body
            fixed_body = fix_post_content(original_body)
            
            if original_body != fixed_body:
                post.body = fixed_body
                post.save()
                fixed_count += 1
                print(f"  ✅ Corrigido: {post.title}")
            else:
                print(f"  ⏭️  Sem alterações: {post.title}")
        
        # Corrige o intro
        if post.intro:
            original_intro = post.intro
            fixed_intro = fix_post_content(original_intro)
            
            if original_intro != fixed_intro:
                post.intro = fixed_intro
                post.save()
                print(f"  ✅ Intro corrigido: {post.title}")
    
    print(f"🎉 Correção concluída! {fixed_count} posts foram corrigidos.")

if __name__ == "__main__":
    main()

