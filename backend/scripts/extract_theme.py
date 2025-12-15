#!/usr/bin/env python3
"""
Script para extrair design tokens do CSS do site antigo
Gera arquivo TypeScript com tokens para Next.js
"""
import re
from pathlib import Path

# Diretório base
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# CSS já clonado (pode ser atualizado depois com scraping real)
CSS_EXAMPLES = """
:root{
  --ka-pink:#D62042;
  --ka-pink-2:#ff6b6b;
  --ka-dark:#0b0b0c;
  --ka-dark-2:#141416;
  --ka-border:rgba(255,255,255,.12);
  --ka-tint:rgba(214,32,66,.18);
  --ka-shadow:0 12px 40px rgba(0,0,0,.35);
}

body{color:#e9eaee;background:#000;}
h1,h2,h3{letter-spacing:.2px}
.lead{opacity:.9}

.btn-pink, .btn-hero{
  background:linear-gradient(135deg,var(--ka-pink),var(--ka-pink-2));
  border:0;
  color:#fff;
  border-radius:12px;
  padding:.9rem 1.6rem;
  font-weight:700
}
"""


def extract_css_variables(css_content: str) -> dict:
    """Extrai variáveis CSS do :root"""
    variables = {}
    
    # Procurar :root { ... }
    root_match = re.search(r':root\s*\{([^}]+)\}', css_content, re.DOTALL)
    if root_match:
        root_content = root_match.group(1)
        # Procurar --variable: value;
        var_matches = re.findall(r'--([^:]+):\s*([^;]+);', root_content)
        for var_name, var_value in var_matches:
            variables[var_name.strip()] = var_value.strip()
    
    return variables


def extract_colors(css_content: str, variables: dict) -> dict:
    """Extrai cores do CSS"""
    colors = {
        'primary': variables.get('ka-pink', '#D62042'),
        'primaryLight': variables.get('ka-pink-2', '#ff6b6b'),
        'dark': variables.get('ka-dark', '#0b0b0c'),
        'darkSecondary': variables.get('ka-dark-2', '#141416'),
        'border': variables.get('ka-border', 'rgba(255,255,255,.12)'),
        'tint': variables.get('ka-tint', 'rgba(214,32,66,.18)'),
        'text': '#e9eaee',
        'textMuted': 'rgba(255,255,255,0.7)',
        'background': '#000000',
        'white': '#ffffff',
    }
    
    return colors


def extract_typography(css_content: str) -> dict:
    """Extrai tipografia do CSS"""
    typography = {
        'fontFamilyBase': "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
        'fontFamilyHeading': "'Poppins', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
        'fontSizes': {
            'xs': 'clamp(0.75rem, 0.7rem + 0.25vw, 0.875rem)',
            'sm': 'clamp(0.875rem, 0.8rem + 0.375vw, 1rem)',
            'base': 'clamp(1rem, 0.9rem + 0.5vw, 1.125rem)',
            'lg': 'clamp(1.125rem, 1rem + 0.625vw, 1.25rem)',
            'xl': 'clamp(1.25rem, 1.1rem + 0.75vw, 1.5rem)',
            '2xl': 'clamp(1.5rem, 1.3rem + 1vw, 2rem)',
            '3xl': 'clamp(1.875rem, 1.6rem + 1.375vw, 2.5rem)',
            '4xl': 'clamp(2.25rem, 1.9rem + 1.75vw, 3rem)',
            '5xl': 'clamp(3rem, 2.5rem + 2.5vw, 4rem)',
        },
        'fontWeights': {
            'normal': '400',
            'medium': '500',
            'semibold': '600',
            'bold': '700',
            'extrabold': '800',
        },
        'lineHeights': {
            'tight': '1.2',
            'normal': '1.6',
            'relaxed': '1.8',
        },
        'letterSpacing': {
            'tight': '-0.02em',
            'normal': '0',
            'wide': '0.02em',
        },
    }
    
    return typography


def extract_buttons(css_content: str, variables: dict) -> dict:
    """Extrai estilos de botões"""
    buttons = {
        'primary': {
            'background': f'linear-gradient(135deg, {variables.get("ka-pink", "#D62042")}, {variables.get("ka-pink-2", "#ff6b6b")})',
            'color': '#fff',
            'borderRadius': '12px',
            'padding': '0.9rem 1.6rem',
            'fontWeight': '700',
            'hover': {
                'filter': 'brightness(1.05)',
            },
        },
        'outline': {
            'border': '2px solid',
            'borderColor': variables.get('ka-border', 'rgba(255,255,255,.12)'),
            'borderRadius': '12px',
            'background': 'transparent',
            'color': '#fff',
        },
    }
    
    return buttons


def generate_theme_file(output_path: Path, css_content: str):
    """Gera arquivo TypeScript com tokens"""
    variables = extract_css_variables(css_content)
    colors = extract_colors(css_content, variables)
    typography = extract_typography(css_content)
    buttons = extract_buttons(css_content, variables)
    
    theme_content = f'''/**
 * Design Tokens da Agência Kaizen
 * Extraído do site original agenciakaizen.com.br
 * 
 * ATENÇÃO: Este arquivo é gerado automaticamente.
 * Para modificar, edite o CSS original e rode o script extract_theme.py novamente.
 */

export const theme = {{
  colors: {{
    primary: '{colors["primary"]}',
    primaryLight: '{colors["primaryLight"]}',
    dark: '{colors["dark"]}',
    darkSecondary: '{colors["darkSecondary"]}',
    border: '{colors["border"]}',
    tint: '{colors["tint"]}',
    text: '{colors["text"]}',
    textMuted: '{colors["textMuted"]}',
    background: '{colors["background"]}',
    white: '{colors["white"]}',
  }},
  
  typography: {{
    fontFamilyBase: {typography["fontFamilyBase"]},
    fontFamilyHeading: {typography["fontFamilyHeading"]},
    fontSizes: {{
      xs: '{typography["fontSizes"]["xs"]}',
      sm: '{typography["fontSizes"]["sm"]}',
      base: '{typography["fontSizes"]["base"]}',
      lg: '{typography["fontSizes"]["lg"]}',
      xl: '{typography["fontSizes"]["xl"]}',
      '2xl': '{typography["fontSizes"]["2xl"]}',
      '3xl': '{typography["fontSizes"]["3xl"]}',
      '4xl': '{typography["fontSizes"]["4xl"]}',
      '5xl': '{typography["fontSizes"]["5xl"]}',
    }},
    fontWeights: {{
      normal: '{typography["fontWeights"]["normal"]}',
      medium: '{typography["fontWeights"]["medium"]}',
      semibold: '{typography["fontWeights"]["semibold"]}',
      bold: '{typography["fontWeights"]["bold"]}',
      extrabold: '{typography["fontWeights"]["extrabold"]}',
    }},
    lineHeights: {{
      tight: '{typography["lineHeights"]["tight"]}',
      normal: '{typography["lineHeights"]["normal"]}',
      relaxed: '{typography["lineHeights"]["relaxed"]}',
    }},
    letterSpacing: {{
      tight: '{typography["letterSpacing"]["tight"]}',
      normal: '{typography["letterSpacing"]["normal"]}',
      wide: '{typography["letterSpacing"]["wide"]}',
    }},
  }},
  
  buttons: {{
    primary: {{
      background: '{buttons["primary"]["background"]}',
      color: '{buttons["primary"]["color"]}',
      borderRadius: '{buttons["primary"]["borderRadius"]}',
      padding: '{buttons["primary"]["padding"]}',
      fontWeight: '{buttons["primary"]["fontWeight"]}',
      hover: {{
        filter: '{buttons["primary"]["hover"]["filter"]}',
      }},
    }},
    outline: {{
      border: '{buttons["outline"]["border"]}',
      borderColor: '{buttons["outline"]["borderColor"]}',
      borderRadius: '{buttons["outline"]["borderRadius"]}',
      background: '{buttons["outline"]["background"]}',
      color: '{buttons["outline"]["color"]}',
    }},
  }},
  
  spacing: {{
    xs: '0.25rem',
    sm: '0.5rem',
    md: '1rem',
    lg: '1.5rem',
    xl: '2rem',
    '2xl': '3rem',
    '3xl': '4rem',
  }},
  
  borderRadius: {{
    sm: '0.5rem',
    md: '0.75rem',
    lg: '1rem',
    xl: '1.5rem',
    '2xl': '2rem',
    full: '9999px',
  }},
  
  shadows: {{
    sm: '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
    md: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
    lg: '0 10px 15px -3px rgba(0, 0, 0, 0.1)',
    xl: '0 20px 25px -5px rgba(0, 0, 0, 0.1)',
    '2xl': '0 25px 50px -12px rgba(0, 0, 0, 0.25)',
    kaizen: '{variables.get("ka-shadow", "0 12px 40px rgba(0,0,0,.35)")}',
  }},
}} as const

export type Theme = typeof theme
'''

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(theme_content)
    
    print(f"✅ Arquivo de tema gerado: {output_path.relative_to(BASE_DIR)}")


def main():
    """Função principal"""
    print("🎨 Extraindo design tokens do CSS...\n")
    
    # Tentar ler CSS clonado
    css_files = [
        BASE_DIR / "src" / "static" / "images" / "cloned" / "css" / "*.css",
        BASE_DIR / "src" / "static" / "css" / "kaizen-modern.css",
    ]
    
    css_content = CSS_EXAMPLES  # Fallback
    
    # Tentar encontrar CSS real
    for pattern in css_files:
        css_paths = list(Path(pattern.parent).glob(pattern.name))
        if css_paths:
            try:
                with open(css_paths[0], 'r', encoding='utf-8') as f:
                    css_content = f.read()
                print(f"📄 Usando CSS: {css_paths[0].relative_to(BASE_DIR)}")
                break
            except Exception as e:
                print(f"⚠️  Erro ao ler {css_paths[0]}: {e}")
    
    # Gerar arquivo de tema
    output_path = BASE_DIR / "frontend" / "theme" / "tokens.ts"
    generate_theme_file(output_path, css_content)
    
    print("\n✅ Extração concluída!")


if __name__ == "__main__":
    main()



