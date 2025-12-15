#!/usr/bin/env python3
"""
Script para clonar assets do site antigo agenciakaizen.com.br
Baixa imagens, ícones, logos e fontes para o frontend Next.js
"""
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import json
from pathlib import Path
import hashlib
import re

# Configurações
SITE_URL = "https://agenciakaizen.com.br/"
PAGES_TO_SCRAPE = [
    "https://agenciakaizen.com.br/",
    "https://agenciakaizen.com.br/nossas-empresas/",
]

# Diretório base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent.parent
FRONTEND_PUBLIC = BASE_DIR / "frontend" / "public"

# Estrutura de pastas
BACKGROUNDS_DIR = FRONTEND_PUBLIC / "img" / "backgrounds"
ICONS_DIR = FRONTEND_PUBLIC / "img" / "icons"
LOGOS_DIR = FRONTEND_PUBLIC / "img" / "logos"
FONTS_DIR = FRONTEND_PUBLIC / "fonts"

# Criar diretórios
for dir_path in [BACKGROUNDS_DIR, ICONS_DIR, LOGOS_DIR, FONTS_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)

# Tipos de assets
ASSET_EXTENSIONS = {
    'image': ['.webp', '.jpg', '.jpeg', '.png', '.svg', '.gif'],
    'font': ['.woff', '.woff2', '.ttf', '.eot', '.otf'],
}

# Cache de URLs já baixadas (para evitar duplicados)
downloaded_urls = set()


def get_file_hash(content: bytes) -> str:
    """Gera hash MD5 do conteúdo do arquivo"""
    return hashlib.md5(content).hexdigest()


def download_file(url: str, save_path: Path) -> bool:
    """Baixa um arquivo e salva no caminho especificado"""
    if url in downloaded_urls:
        return False
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        # Verificar se é imagem válida ou arquivo
        content_type = response.headers.get('Content-Type', '')
        if 'image' not in content_type and 'font' not in content_type and 'octet-stream' not in content_type:
            # Tentar detectar tipo pelo conteúdo
            if not any(response.content.startswith(prefix) for prefix in [b'\x89PNG', b'\xff\xd8', b'GIF', b'<?xml', b'<svg']):
                return False
        
        # Criar diretório se não existir
        save_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Salvar arquivo
        with open(save_path, 'wb') as f:
            f.write(response.content)
        
        downloaded_urls.add(url)
        print(f"✓ Baixado: {save_path.relative_to(BASE_DIR)}")
        return True
    except Exception as e:
        print(f"✗ Erro ao baixar {url}: {e}")
        return False


def get_css_images(css_content: str, base_url: str) -> list:
    """Extrai URLs de imagens do CSS"""
    urls = []
    
    # Padrões para url() e background-image
    patterns = [
        r'url\(["\']?([^"\')]+)["\']?\)',
        r'background-image:\s*url\(["\']?([^"\')]+)["\']?\)',
        r'background:\s*url\(["\']?([^"\')]+)["\']?\)',
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, css_content, re.IGNORECASE)
        for match in matches:
            # Remover data: URLs e fragmentos
            if not match.startswith('data:') and not match.startswith('#') and match.strip():
                full_url = urljoin(base_url, match.strip())
                # Filtrar apenas do mesmo domínio
                parsed = urlparse(full_url)
                if parsed.netloc and 'agenciakaizen.com.br' in parsed.netloc:
                    urls.append(full_url)
    
    return list(set(urls))


def categorize_asset(url: str, filename: str) -> tuple:
    """
    Categoriza um asset e retorna (tipo, diretório de destino)
    tipos: background, icon, logo, font
    """
    url_lower = url.lower()
    filename_lower = filename.lower()
    
    # Fontes
    if any(ext in filename_lower for ext in ASSET_EXTENSIONS['font']):
        return ('font', FONTS_DIR)
    
    # Logos
    if 'logo' in filename_lower or 'logo' in url_lower:
        return ('logo', LOGOS_DIR)
    
    # Backgrounds
    if any(keyword in filename_lower or keyword in url_lower 
           for keyword in ['background', 'fundo', 'hero', 'banner']):
        return ('background', BACKGROUNDS_DIR)
    
    # Ícones (SVG pequenos ou ícones)
    if filename_lower.endswith('.svg') or 'icon' in filename_lower or 'icon' in url_lower:
        return ('icon', ICONS_DIR)
    
    # Default: background se for imagem grande, icon se for SVG
    if filename_lower.endswith('.svg'):
        return ('icon', ICONS_DIR)
    
    return ('background', BACKGROUNDS_DIR)


def scrape_page(url: str):
    """Faz scraping de uma página"""
    print(f"\n📄 Analisando: {url}")
    
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # 1. Baixar todas as imagens <img>
        for img in soup.find_all('img'):
            src = img.get('src') or img.get('data-src') or img.get('data-lazy-src')
            if src and not src.startswith('data:'):
                full_url = urljoin(url, src)
                parsed = urlparse(full_url)
                filename = os.path.basename(parsed.path) or f"image_{get_file_hash(src.encode())}.webp"
                
                # Categorizar
                asset_type, target_dir = categorize_asset(full_url, filename)
                save_path = target_dir / filename
                
                download_file(full_url, save_path)
        
        # 2. Baixar CSS e extrair imagens
        for link in soup.find_all('link', rel='stylesheet'):
            href = link.get('href', '')
            if href:
                full_url = urljoin(url, href)
                
                try:
                    css_response = requests.get(full_url, timeout=30)
                    css_response.raise_for_status()
                    css_content = css_response.text
                    
                    # Extrair imagens do CSS
                    css_images = get_css_images(css_content, full_url)
                    for img_url in css_images:
                        parsed = urlparse(img_url)
                        filename = os.path.basename(parsed.path)
                        if filename and any(filename.lower().endswith(ext) for ext in ASSET_EXTENSIONS['image']):
                            asset_type, target_dir = categorize_asset(img_url, filename)
                            save_path = target_dir / filename
                            download_file(img_url, save_path)
                except Exception as e:
                    print(f"  Aviso: Erro ao processar CSS {href}: {e}")
        
        # 3. Baixar fontes de @font-face no CSS inline
        for style in soup.find_all('style'):
            if style.string:
                # Procurar @font-face
                font_matches = re.findall(r"url\(['\"]?([^'\"]+\.(?:woff2?|ttf|eot|otf))['\"]?\)", style.string, re.IGNORECASE)
                for font_url in font_matches:
                    if not font_url.startswith('data:'):
                        full_url = urljoin(url, font_url)
                        parsed = urlparse(full_url)
                        filename = os.path.basename(parsed.path) or "font.woff2"
                        save_path = FONTS_DIR / filename
                        download_file(full_url, save_path)
        
        # 4. Baixar favicons e ícones
        for link in soup.find_all('link'):
            rel = link.get('rel', [])
            href = link.get('href', '')
            
            if isinstance(rel, list):
                rel = ' '.join(rel)
            
            if 'icon' in rel.lower() or 'shortcut' in rel.lower() or 'apple-touch-icon' in rel.lower():
                if href:
                    full_url = urljoin(url, href)
                    parsed = urlparse(full_url)
                    filename = os.path.basename(parsed.path) or 'favicon.ico'
                    save_path = ICONS_DIR / filename
                    download_file(full_url, save_path)
    
    except Exception as e:
        print(f"✗ Erro ao fazer scraping de {url}: {e}")


def main():
    print("🚀 Iniciando clone de assets do site agenciakaizen.com.br\n")
    
    results = {
        'backgrounds': [],
        'icons': [],
        'logos': [],
        'fonts': [],
    }
    
    # Scraping das páginas
    for page_url in PAGES_TO_SCRAPE:
        scrape_page(page_url)
    
    # Contar arquivos baixados
    for dir_path, key in [
        (BACKGROUNDS_DIR, 'backgrounds'),
        (ICONS_DIR, 'icons'),
        (LOGOS_DIR, 'logos'),
        (FONTS_DIR, 'fonts'),
    ]:
        files = list(dir_path.glob('*'))
        results[key] = [str(f.relative_to(FRONTEND_PUBLIC)) for f in files if f.is_file()]
    
    # Salvar metadata
    metadata_path = FRONTEND_PUBLIC / "assets_metadata.json"
    with open(metadata_path, 'w', encoding='utf-8') as f:
        json.dump({
            'site_url': SITE_URL,
            'pages_scraped': PAGES_TO_SCRAPE,
            'assets': results,
            'total_backgrounds': len(results['backgrounds']),
            'total_icons': len(results['icons']),
            'total_logos': len(results['logos']),
            'total_fonts': len(results['fonts']),
        }, f, indent=2, ensure_ascii=False)
    
    print("\n✅ Clone concluído!")
    print(f"  📸 Backgrounds: {len(results['backgrounds'])}")
    print(f"  🎨 Ícones: {len(results['icons'])}")
    print(f"  🏢 Logos: {len(results['logos'])}")
    print(f"  📝 Fontes: {len(results['fonts'])}")
    print(f"\n📁 Arquivos salvos em: {FRONTEND_PUBLIC.relative_to(BASE_DIR)}")
    print(f"📄 Metadata: {metadata_path.relative_to(BASE_DIR)}")


if __name__ == "__main__":
    main()



