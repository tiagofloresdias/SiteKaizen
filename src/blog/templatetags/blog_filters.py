from django import template
from django.utils.safestring import mark_safe
import re

register = template.Library()

@register.filter
def fix_newlines(value):
    """
    Converte \n em quebras de linha HTML e remove \n duplicados
    """
    if not value:
        return value
    
    # Converte string para texto se for RichText
    text = str(value)
    
    # Remove \n duplicados (mais de 2 seguidos)
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # Converte \n em <br> tags
    text = text.replace('\n', '<br>')
    
    # Converte <br><br> em </p><p> para criar parágrafos
    text = re.sub(r'<br>\s*<br>', '</p><p>', text)
    
    # Adiciona tags <p> no início e fim se não existirem
    if not text.startswith('<p>'):
        text = '<p>' + text
    if not text.endswith('</p>'):
        text = text + '</p>'
    
    return mark_safe(text)

@register.filter
def clean_content(value):
    """
    Limpa o conteúdo HTML removendo caracteres de escape e formatando corretamente
    """
    if not value:
        return value
    
    text = str(value)
    
    # Remove escapes de aspas
    text = text.replace('\\"', '"').replace("\\'", "'")
    
    # Remove barras invertidas duplas
    text = text.replace('\\\\', '\\')
    
    # Processa quebras de linha
    text = fix_newlines(text)
    
    return text

