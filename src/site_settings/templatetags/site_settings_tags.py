from django import template
from django.template import Context
from site_settings.models import SiteSettings, PartnerLogo

register = template.Library()


@register.simple_tag(takes_context=True)
def get_site_settings(context):
    """Retorna as configurações do site para o contexto atual"""
    request = context.get('request')
    if request and hasattr(request, 'site'):
        return SiteSettings.for_site(request.site)
    elif request:
        from wagtail.models import Site
        site = Site.find_for_request(request)
        return SiteSettings.for_site(site)
    return SiteSettings.objects.first()


@register.simple_tag(takes_context=True)
def get_background_style(context):
    """Retorna o CSS inline para a imagem de fundo baseado nas configurações do site"""
    settings = get_site_settings(context)
    
    if not settings or not settings.background_image:
        return ""
    
    # Constrói o CSS para a imagem de fundo
    background_url = settings.background_image.file.url
    
    # Sobreposição com gradiente (mais forte no topo, some para preto embaixo)
    overlay_opacity = float(settings.background_overlay_opacity)
    top_opacity = min(overlay_opacity + 0.30, 0.95)
    mid_opacity = min(overlay_opacity + 0.45, 0.98)
    
    style_parts = [
        (
            "background-image: "
            f"linear-gradient(180deg, rgba(0,0,0,{top_opacity}) 0%, rgba(0,0,0,{mid_opacity}) 40%, rgba(0,0,0,1) 75%, rgba(0,0,0,1) 100%), "
            f"url('{background_url}')"
        ),
        "background-position: top center",
        "background-size: cover",
        "background-repeat: no-repeat",
        "background-attachment: scroll",
    ]
    
    return "; ".join(style_parts)


@register.simple_tag()
def get_partner_logos():
    """Retorna logos de parceiros ativos para o footer"""
    return PartnerLogo.objects.filter(is_active=True).order_by('order', 'name')
