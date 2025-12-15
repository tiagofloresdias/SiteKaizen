"""
Sistema de Templates Jinja2 para renderização de páginas
"""
from jinja2 import Environment, FileSystemLoader, select_autoescape
from pathlib import Path
from app.config import get_settings

settings = get_settings()

# Configurar diretório de templates
templates_dir = Path(settings.templates_dir)
if not templates_dir.exists():
    # Fallback para templates dentro do backend
    templates_dir = Path(__file__).parent.parent.parent / "templates"
    templates_dir.mkdir(exist_ok=True)

# Criar ambiente Jinja2
jinja_env = Environment(
    loader=FileSystemLoader(str(templates_dir)),
    autoescape=select_autoescape(['html', 'xml']),
    trim_blocks=True,
    lstrip_blocks=True,
)


def get_template(name: str):
    """Obtém um template Jinja2"""
    return jinja_env.get_template(name)


def render_template(name: str, **context):
    """Renderiza um template com contexto"""
    template = get_template(name)
    return template.render(**context)

