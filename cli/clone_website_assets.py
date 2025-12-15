#!/usr/bin/env python3
"""
Script para clonar todas as imagens e assets do site agenciakaizen.com.br
Mantém a estrutura de pastas e baixa todos os recursos visuais
"""
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import json
from pathlib import Path

# Configurações
SITE_URL = "https://agenciakaizen.com.br/"
BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "src" / "static" / "images" / "cloned"
STATIC_DIR.mkdir(parents=True, exist_ok=True)

# Tipos de assets para baixar
ASSET_EXTENSIONS = ['.webp', '.jpg', '.jpeg', '.png', '.svg', '.gif', '.ico', '.woff', '.woff2', '.ttf', '.eot']

def download_file(url, save_path):
    """Baixa um arquivo e salva no caminho especificado"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        # Criar diretório se não existir
        save_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Salvar arquivo
        with open(save_path, 'wb') as f:
            f.write(response.content)
        
        print(f"✓ Baixado: {save_path.relative_to(BASE_DIR)}")
        return True
    except Exception as e:
        print(f"✗ Erro ao baixar {url}: {e}")
        return False

def get_css_images(css_content, base_url):
    """Extrai URLs de imagens do CSS"""
    import re
    urls = []
    
    # Buscar url() e url("") e url('')
    patterns = [
        r'url\(["\']?([^"\')]+)["\']?\)',
        r'url\(([^)]+)\)',
        r'background-image:\s*url\(["\']?([^"\')]+)["\']?\)',
        r'background:\s*url\(["\']?([^"\')]+)["\']?\)',
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, css_content)
        for match in matches:
            # Remover data: URLs
            if not match.startswith('data:'):
                full_url = urljoin(base_url, match.strip())
                urls.append(full_url)
    
    return list(set(urls))

def extract_font_info():
    """Extrai informações sobre fontes do site"""
    try:
        response = requests.get(SITE_URL, timeout=30)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        fonts = set()
        
        # Buscar Google Fonts
        for link in soup.find_all('link', href=True):
            href = link.get('href', '')
            if 'fonts.googleapis.com' in href:
                fonts.add(href)
        
        # Buscar @import em style tags
        for style in soup.find_all('style'):
            if style.string:
                import re
                matches = re.findall(r"@import\s+url\(['\"]?([^'\"]+)['\"]?\)", style.string)
                for match in matches:
                    if 'fonts.googleapis.com' in match:
                        fonts.add(match)
        
        return list(fonts)
    except Exception as e:
        print(f"Erro ao extrair fontes: {e}")
        return []

def main():
    print("🚀 Iniciando clone de assets do site agenciakaizen.com.br\n")
    
    downloaded = {
        'images': [],
        'css': [],
        'fonts': [],
        'icons': []
    }
    
    try:
        # 1. Baixar HTML principal
        print("1. Baixando HTML principal...")
        response = requests.get(SITE_URL, timeout=30)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # 2. Baixar todas as imagens
        print("\n2. Baixando imagens...")
        images_dir = STATIC_DIR / "images"
        images_dir.mkdir(parents=True, exist_ok=True)
        
        for img in soup.find_all('img'):
            src = img.get('src') or img.get('data-src') or img.get('data-lazy-src')
            if src and not src.startswith('data:'):
                full_url = urljoin(SITE_URL, src)
                parsed = urlparse(full_url)
                filename = os.path.basename(parsed.path)
                
                # Manter estrutura de pastas
                if '/uploads/' in parsed.path:
                    path_parts = parsed.path.split('/uploads/')[-1]
                    save_path = images_dir / path_parts
                else:
                    save_path = images_dir / filename
                
                if download_file(full_url, save_path):
                    downloaded['images'].append({
                        'url': full_url,
                        'path': str(save_path.relative_to(BASE_DIR)),
                        'filename': filename
                    })
        
        # 3. Baixar CSS e extrair imagens
        print("\n3. Baixando CSS...")
        css_dir = STATIC_DIR / "css"
        css_dir.mkdir(parents=True, exist_ok=True)
        
        for link in soup.find_all('link', rel='stylesheet'):
            href = link.get('href', '')
            if href:
                full_url = urljoin(SITE_URL, href)
                parsed = urlparse(full_url)
                filename = os.path.basename(parsed.path) or 'style.css'
                save_path = css_dir / filename
                
                if download_file(full_url, save_path):
                    downloaded['css'].append({
                        'url': full_url,
                        'path': str(save_path.relative_to(BASE_DIR))
                    })
                    
                    # Extrair imagens do CSS
                    try:
                        with open(save_path, 'r', encoding='utf-8') as f:
                            css_content = f.read()
                            css_images = get_css_images(css_content, full_url)
                            
                            for img_url in css_images:
                                parsed_img = urlparse(img_url)
                                img_filename = os.path.basename(parsed_img.path)
                                if any(img_filename.lower().endswith(ext) for ext in ASSET_EXTENSIONS):
                                    img_save_path = images_dir / img_filename
                                    if download_file(img_url, img_save_path):
                                        downloaded['images'].append({
                                            'url': img_url,
                                            'path': str(img_save_path.relative_to(BASE_DIR)),
                                            'source': 'css'
                                        })
                    except Exception as e:
                        print(f"  Aviso: Erro ao processar CSS {filename}: {e}")
        
        # 4. Extrair informações de fontes
        print("\n4. Extraindo informações de fontes...")
        fonts = extract_font_info()
        downloaded['fonts'] = fonts
        for font_url in fonts:
            print(f"  📝 Fonte encontrada: {font_url}")
        
        # 5. Baixar favicon e ícones
        print("\n5. Baixando favicons e ícones...")
        for link in soup.find_all('link'):
            rel = link.get('rel', [])
            href = link.get('href', '')
            
            if 'icon' in rel or 'shortcut' in rel or 'apple-touch-icon' in rel:
                full_url = urljoin(SITE_URL, href)
                filename = os.path.basename(urlparse(full_url).path) or 'favicon.ico'
                save_path = STATIC_DIR / filename
                
                if download_file(full_url, save_path):
                    downloaded['icons'].append({
                        'url': full_url,
                        'path': str(save_path.relative_to(BASE_DIR)),
                        'rel': rel
                    })
        
        # 6. Salvar metadata
        print("\n6. Salvando metadata...")
        metadata_path = STATIC_DIR / "metadata.json"
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump({
                'site_url': SITE_URL,
                'downloaded': downloaded,
                'total_images': len(downloaded['images']),
                'total_css': len(downloaded['css']),
                'total_fonts': len(downloaded['fonts']),
                'total_icons': len(downloaded['icons'])
            }, f, indent=2, ensure_ascii=False)
        
        print("\n✅ Clone concluído!")
        print(f"  📸 Imagens: {len(downloaded['images'])}")
        print(f"  🎨 CSS: {len(downloaded['css'])}")
        print(f"  📝 Fontes: {len(downloaded['fonts'])}")
        print(f"  🔖 Ícones: {len(downloaded['icons'])}")
        print(f"\n📁 Arquivos salvos em: {STATIC_DIR.relative_to(BASE_DIR)}")
        print(f"📄 Metadata: {metadata_path.relative_to(BASE_DIR)}")
        
    except Exception as e:
        print(f"\n❌ Erro durante o clone: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()


