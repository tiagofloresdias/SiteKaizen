#!/usr/bin/env python3
"""
Script COMPLETO para clonar TUDO do site agenciakaizen.com.br
- Todas as imagens (backgrounds, logos, icons)
- Todo o CSS inline e externo
- Extração de cores exatas
- Estrutura HTML das páginas principais
"""
import os
import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import json
from pathlib import Path
import re
import hashlib
from datetime import datetime

# Configurações
SITE_URL = "https://agenciakaizen.com.br/"
PAGES_TO_CLONE = [
    "https://agenciakaizen.com.br/",
    "https://agenciakaizen.com.br/nossas-empresas/",
    "https://agenciakaizen.com.br/quem-somos/",
]

BASE_DIR = Path(__file__).resolve().parent.parent.parent
FRONTEND_PUBLIC = BASE_DIR / "frontend" / "public"
CLONE_DATA_DIR = BASE_DIR / "frontend" / "src" / "data" / "cloned"

# Criar diretórios
CLONE_DATA_DIR.mkdir(parents=True, exist_ok=True)
(FRONTEND_PUBLIC / "img" / "backgrounds").mkdir(parents=True, exist_ok=True)
(FRONTEND_PUBLIC / "img" / "logos").mkdir(parents=True, exist_ok=True)
(FRONTEND_PUBLIC / "img" / "icons").mkdir(parents=True, exist_ok=True)
(FRONTEND_PUBLIC / "img" / "content").mkdir(parents=True, exist_ok=True)
(FRONTEND_PUBLIC / "fonts").mkdir(parents=True, exist_ok=True)

downloaded_urls = set()
colors_found = set()
css_content_all = []

def get_file_hash(content):
    """Gera hash MD5 do conteúdo"""
    return hashlib.md5(content).hexdigest()[:12]

def sanitize_filename(filename):
    """Sanitiza nome de arquivo"""
    filename = re.sub(r'[^\w\s.-]', '_', filename)
    filename = re.sub(r'[-\s]+', '-', filename)
    return filename[:200]  # Limitar tamanho

def download_file(url, save_path):
    """Baixa um arquivo"""
    if url in downloaded_urls:
        return False
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        save_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(save_path, 'wb') as f:
            f.write(response.content)
        
        downloaded_urls.add(url)
        print(f"  ✓ {save_path.name}")
        return True
    except Exception as e:
        print(f"  ✗ Erro em {url}: {str(e)[:50]}")
        return False

def extract_colors_from_css(css_text):
    """Extrai todas as cores do CSS"""
    # Padrões de cores
    hex_colors = re.findall(r'#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b', css_text)
    rgb_colors = re.findall(r'rgba?\([^)]+\)', css_text)
    
    for color in hex_colors:
        colors_found.add(f"#{color.lower()}")
    for color in rgb_colors:
        colors_found.add(color)

def extract_images_from_css(css_text, base_url):
    """Extrai URLs de imagens do CSS"""
    urls = []
    patterns = [
        r'url\(["\']?([^"\')]+)["\']?\)',
        r'background-image:\s*url\(["\']?([^"\')]+)["\']?\)',
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, css_text, re.IGNORECASE)
        for match in matches:
            if not match.startswith('data:') and match.strip():
                full_url = urljoin(base_url, match.strip())
                if 'agenciakaizen.com.br' in full_url:
                    urls.append(full_url)
    
    return list(set(urls))

def categorize_image(url, filename):
    """Categoriza uma imagem"""
    url_lower = url.lower()
    filename_lower = filename.lower()
    
    # Logos
    if 'logo' in filename_lower or 'logo' in url_lower:
        return FRONTEND_PUBLIC / "img" / "logos"
    
    # Backgrounds
    if any(k in filename_lower or k in url_lower for k in ['background', 'fundo', 'hero', 'banner', 'asset', 'vector', 'camada', 'layer']):
        return FRONTEND_PUBLIC / "img" / "backgrounds"
    
    # Ícones
    if filename_lower.endswith('.svg') or 'icon' in filename_lower or filename_lower.endswith('.ico'):
        return FRONTEND_PUBLIC / "img" / "icons"
    
    # Default: content
    return FRONTEND_PUBLIC / "img" / "content"

def clone_page(url):
    """Clona uma página completa"""
    print(f"\n{'='*60}")
    print(f"📄 Clonando: {url}")
    print(f"{'='*60}")
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        page_data = {
            'url': url,
            'title': soup.title.string if soup.title else '',
            'images': [],
            'css_files': [],
            'inline_styles': []
        }
        
        # 1. Baixar todas as imagens <img>
        print("\n📸 Baixando imagens <img>...")
        img_count = 0
        for img in soup.find_all('img'):
            src = img.get('src') or img.get('data-src') or img.get('data-lazy-src')
            if src and not src.startswith('data:'):
                full_url = urljoin(url, src)
                parsed = urlparse(full_url)
                filename = os.path.basename(parsed.path) or f"img_{get_file_hash(src.encode())}.webp"
                filename = sanitize_filename(filename)
                
                target_dir = categorize_image(full_url, filename)
                save_path = target_dir / filename
                
                if download_file(full_url, save_path):
                    img_count += 1
                    page_data['images'].append({
                        'original_url': full_url,
                        'local_path': str(save_path.relative_to(FRONTEND_PUBLIC))
                    })
        
        print(f"  Total: {img_count} imagens")
        
        # 2. Processar CSS externo
        print("\n🎨 Processando CSS externo...")
        css_count = 0
        for link in soup.find_all('link', rel='stylesheet'):
            href = link.get('href', '')
            if href:
                full_url = urljoin(url, href)
                try:
                    css_response = requests.get(full_url, headers=headers, timeout=30)
                    css_response.raise_for_status()
                    css_text = css_response.text
                    
                    css_content_all.append(css_text)
                    extract_colors_from_css(css_text)
                    
                    # Extrair imagens do CSS
                    css_images = extract_images_from_css(css_text, full_url)
                    for img_url in css_images:
                        parsed = urlparse(img_url)
                        filename = os.path.basename(parsed.path)
                        if filename:
                            filename = sanitize_filename(filename)
                            target_dir = categorize_image(img_url, filename)
                            save_path = target_dir / filename
                            if download_file(img_url, save_path):
                                css_count += 1
                    
                    page_data['css_files'].append(full_url)
                except Exception as e:
                    print(f"  ✗ Erro CSS {href}: {str(e)[:40]}")
        
        print(f"  Total: {css_count} imagens de CSS")
        
        # 3. Processar CSS inline
        print("\n📝 Processando CSS inline...")
        for style in soup.find_all('style'):
            if style.string:
                css_content_all.append(style.string)
                extract_colors_from_css(style.string)
                page_data['inline_styles'].append(style.string)
        
        # 4. Baixar imagens de background inline
        print("\n🖼️  Processando backgrounds inline...")
        bg_count = 0
        for elem in soup.find_all(style=True):
            style_attr = elem.get('style', '')
            bg_urls = re.findall(r'url\(["\']?([^"\')]+)["\']?\)', style_attr)
            for bg_url in bg_urls:
                if not bg_url.startswith('data:'):
                    full_url = urljoin(url, bg_url)
                    parsed = urlparse(full_url)
                    filename = os.path.basename(parsed.path)
                    if filename:
                        filename = sanitize_filename(filename)
                        save_path = FRONTEND_PUBLIC / "img" / "backgrounds" / filename
                        if download_file(full_url, save_path):
                            bg_count += 1
        
        print(f"  Total: {bg_count} backgrounds inline")
        
        # 5. Baixar favicons e ícones
        print("\n🔖 Baixando favicons...")
        for link in soup.find_all('link'):
            rel = link.get('rel', [])
            href = link.get('href', '')
            
            if isinstance(rel, list):
                rel = ' '.join(rel)
            
            if 'icon' in rel.lower() and href:
                full_url = urljoin(url, href)
                parsed = urlparse(full_url)
                filename = os.path.basename(parsed.path) or 'favicon.ico'
                save_path = FRONTEND_PUBLIC / "img" / "icons" / filename
                download_file(full_url, save_path)
        
        return page_data
        
    except Exception as e:
        print(f"❌ Erro ao clonar {url}: {e}")
        return None

def extract_design_tokens():
    """Extrai design tokens do CSS coletado"""
    print("\n🎨 Extraindo Design Tokens...")
    
    all_css = '\n'.join(css_content_all)
    
    tokens = {
        'colors': {},
        'fonts': [],
        'spacing': [],
        'shadows': [],
        'borders': []
    }
    
    # Cores organizadas
    sorted_colors = sorted(list(colors_found))
    for i, color in enumerate(sorted_colors):
        tokens['colors'][f'color-{i+1}'] = color
    
    # Fontes
    font_families = re.findall(r'font-family:\s*([^;]+)', all_css, re.IGNORECASE)
    tokens['fonts'] = list(set([f.strip().strip('"\'') for f in font_families if f.strip()]))
    
    # Shadows
    shadows = re.findall(r'box-shadow:\s*([^;]+)', all_css, re.IGNORECASE)
    tokens['shadows'] = list(set([s.strip() for s in shadows if s.strip() and 'none' not in s.lower()]))[:10]
    
    # Border radius
    radius = re.findall(r'border-radius:\s*([^;]+)', all_css, re.IGNORECASE)
    tokens['borders'] = list(set([r.strip() for r in radius if r.strip() and 'none' not in r.lower()]))[:10]
    
    return tokens

def save_results(pages_data, tokens):
    """Salva resultados da clonagem"""
    print("\n💾 Salvando resultados...")
    
    # Salvar metadata das páginas
    metadata_path = FRONTEND_PUBLIC / "cloned_metadata.json"
    with open(metadata_path, 'w', encoding='utf-8') as f:
        json.dump({
            'cloned_at': datetime.now().isoformat(),
            'source_url': SITE_URL,
            'pages': pages_data,
            'total_images': len(downloaded_urls),
            'total_colors': len(colors_found)
        }, f, indent=2, ensure_ascii=False)
    
    # Salvar design tokens
    tokens_path = CLONE_DATA_DIR / "design_tokens.json"
    with open(tokens_path, 'w', encoding='utf-8') as f:
        json.dump(tokens, f, indent=2, ensure_ascii=False)
    
    # Gerar arquivo TypeScript com tokens
    ts_path = BASE_DIR / "frontend" / "src" / "theme" / "cloned_tokens.ts"
    ts_path.parent.mkdir(parents=True, exist_ok=True)
    
    ts_content = f"""/**
 * Design Tokens clonados de agenciakaizen.com.br
 * Gerado automaticamente em {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
 */

export const clonedColors = {{
"""
    
    for key, value in tokens['colors'].items():
        ts_content += f"  '{key}': '{value}',\n"
    
    ts_content += """}

export const clonedFonts = [
"""
    
    for font in tokens['fonts'][:5]:
        ts_content += f"  '{font}',\n"
    
    ts_content += """]

export const clonedShadows = [
"""
    
    for shadow in tokens['shadows'][:5]:
        ts_content += f"  '{shadow}',\n"
    
    ts_content += """]
"""
    
    with open(ts_path, 'w', encoding='utf-8') as f:
        f.write(ts_content)
    
    print(f"\n✅ Metadata salva: {metadata_path}")
    print(f"✅ Tokens salvos: {tokens_path}")
    print(f"✅ TypeScript gerado: {ts_path}")

def main():
    print("""
╔════════════════════════════════════════════════════════════════╗
║   🚀 CLONE COMPLETO DO SITE AGÊNCIA KAIZEN                     ║
║   Clonando TODAS as imagens, CSS e design tokens              ║
╚════════════════════════════════════════════════════════════════╝
""")
    
    pages_data = []
    
    # Clonar cada página
    for page_url in PAGES_TO_CLONE:
        page_data = clone_page(page_url)
        if page_data:
            pages_data.append(page_data)
    
    # Extrair design tokens
    tokens = extract_design_tokens()
    
    # Salvar resultados
    save_results(pages_data, tokens)
    
    # Estatísticas finais
    print(f"""
╔════════════════════════════════════════════════════════════════╗
║   ✅ CLONE CONCLUÍDO COM SUCESSO!                              ║
╠════════════════════════════════════════════════════════════════╣
║   📸 Total de imagens: {len(downloaded_urls):<40} ║
║   🎨 Cores encontradas: {len(colors_found):<39} ║
║   📄 Páginas clonadas: {len(pages_data):<40} ║
║   📁 Salvos em: frontend/public/img/                          ║
╚════════════════════════════════════════════════════════════════╝
""")
    
    # Listar arquivos por tipo
    print("\n📊 Arquivos por categoria:")
    for dirname in ['backgrounds', 'logos', 'icons', 'content']:
        dir_path = FRONTEND_PUBLIC / "img" / dirname
        if dir_path.exists():
            count = len(list(dir_path.glob('*')))
            print(f"  • {dirname.capitalize()}: {count} arquivos")

if __name__ == "__main__":
    main()

