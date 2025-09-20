#!/usr/bin/env python3
"""
Script de debug para investigar problemas na importação
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

def parse_sql_line(line):
    """Parse uma linha SQL específica"""
    try:
        # Encontrar valores entre parênteses
        match = re.search(r'\((.*)\);?$', line.strip())
        if not match:
            return None
        
        values_str = match.group(1)
        
        # Parse manual dos valores
        values = []
        current = ''
        in_quotes = False
        quote_char = None
        i = 0
        
        while i < len(values_str):
            char = values_str[i]
            
            if not in_quotes:
                if char in ['"', "'"]:
                    in_quotes = True
                    quote_char = char
                    current += char
                elif char == ',':
                    values.append(current.strip())
                    current = ''
                else:
                    current += char
            else:
                current += char
                if char == quote_char and (i == 0 or values_str[i-1] != '\\'):
                    in_quotes = False
                    quote_char = None
            
            i += 1
        
        if current.strip():
            values.append(current.strip())
        
        return values
        
    except Exception as e:
        print(f"Erro ao parsear linha: {e}")
        return None

def clean_value(value):
    """Limpa valor SQL"""
    if not value or value.upper() == 'NULL':
        return None
    
    # Remove aspas
    if value.startswith("'") and value.endswith("'"):
        value = value[1:-1]
    elif value.startswith('"') and value.endswith('"'):
        value = value[1:-1]
    
    # Decodifica escapes
    value = value.replace("\\'", "'")
    value = value.replace('\\"', '"')
    value = value.replace('\\\\', '\\')
    
    return value

def main():
    """Função principal de debug"""
    print("🔍 Debug da importação")
    
    sql_file = '/var/www/agenciakaizen/agenci93_wp177.sql'
    
    with open(sql_file, 'r', encoding='utf-8', errors='ignore') as f:
        line_count = 0
        in_insert_section = False
        processed = 0
        
        for line in f:
            line_count += 1
            
            # Verificar se estamos em uma seção de INSERT
            if 'INSERT INTO `wp_posts`' in line:
                in_insert_section = True
                print(f"📝 Encontrada seção de INSERT na linha {line_count}")
                continue
            
            # Se estamos em uma seção de INSERT e encontramos um parêntese
            if in_insert_section and line.strip().startswith('('):
                processed += 1
                
                # Parse da linha
                values = parse_sql_line(line)
                if values and len(values) >= 22:
                    post_data = {
                        'post_title': clean_value(values[5]),
                        'post_content': clean_value(values[4]),
                        'post_name': clean_value(values[11]),
                        'post_status': clean_value(values[7]),
                        'post_type': clean_value(values[20]),
                        'post_date': clean_value(values[2]),
                        'post_excerpt': clean_value(values[6]),
                    }
                    
                    # Verificar se é um post válido
                    if (post_data.get('post_status') == 'publish' and 
                        post_data.get('post_title') and
                        post_data.get('post_content') and
                        post_data.get('post_type') in ['post', 'page']):
                        
                        print(f"✅ Post válido encontrado: {post_data.get('post_title')}")
                        print(f"   Tipo: {post_data.get('post_type')}")
                        print(f"   Status: {post_data.get('post_status')}")
                        print(f"   Slug: {post_data.get('post_name')}")
                        print(f"   Data: {post_data.get('post_date')}")
                        print(f"   Conteúdo: {len(post_data.get('post_content', ''))} caracteres")
                        print("-" * 50)
                        
                        # Processar apenas os primeiros 5 posts para debug
                        if processed >= 5:
                            break
                else:
                    if values:
                        print(f"❌ Post inválido - {len(values)} valores: {values[:5]}...")
                    else:
                        print(f"❌ Erro no parse da linha")
            
            # Se encontramos um ponto e vírgula, saímos da seção
            if in_insert_section and line.strip().endswith(';'):
                in_insert_section = False
    
    print(f"\n📊 Total processado: {processed}")

if __name__ == '__main__':
    main()

