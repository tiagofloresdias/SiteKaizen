#!/usr/bin/env python3
"""
Script para debugar e encontrar páginas no SQL
"""

import re

def debug_pages():
    print("🔍 Procurando páginas no SQL...")
    
    with open('agenci93_wp177.sql', 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    page_count = 0
    
    for i, line in enumerate(lines):
        if 'INSERT INTO `wp_posts`' in line and "'page'" in line:
            page_count += 1
            print(f"📄 Linha {i}: Encontrada página")
            # Extrair título se possível
            title_match = re.search(r"','([^']+)','([^']*)','([^']+)'", line)
            if title_match:
                title = title_match.group(1)
                print(f"   Título: {title}")
            
            if page_count >= 10:  # Limitar para não sobrecarregar
                break
    
    print(f"\n✅ Total de páginas encontradas: {page_count}")

if __name__ == "__main__":
    debug_pages()

