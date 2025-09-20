from wagtail import hooks
from django.templatetags.static import static
from django.utils.html import format_html


@hooks.register("insert_global_admin_css", order=100)
def insert_kaizen_admin_css():
    """Inclui o CSS de branding da Kaizen em todas as telas do Wagtail Admin."""
    return format_html('<link rel="stylesheet" href="{}">', static('css/agenciakaizen_cms.css'))


