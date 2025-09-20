from django.db import models
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from wagtail.images.models import Image
from wagtail.snippets.models import register_snippet


@register_setting
class SiteSettings(BaseSiteSetting):
    """Configurações globais do site"""
    
    # Imagem de fundo global
    background_image = models.ForeignKey(
        Image,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text="Imagem de fundo que será usada em todas as páginas internas do site"
    )
    
    # Opacidade da sobreposição
    background_overlay_opacity = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0.4,
        help_text="Opacidade da sobreposição escura sobre a imagem de fundo (0.0 = transparente, 1.0 = opaco)"
    )
    
    # Posicionamento da imagem
    background_position = models.CharField(
        max_length=50,
        default="center",
        choices=[
            ("center", "Centro"),
            ("top", "Topo"),
            ("bottom", "Inferior"),
            ("left", "Esquerda"),
            ("right", "Direita"),
            ("top left", "Topo Esquerda"),
            ("top right", "Topo Direita"),
            ("bottom left", "Inferior Esquerda"),
            ("bottom right", "Inferior Direita"),
        ],
        help_text="Posicionamento da imagem de fundo"
    )
    
    # Tamanho da imagem
    background_size = models.CharField(
        max_length=50,
        default="cover",
        choices=[
            ("cover", "Cobrir (Cover)"),
            ("contain", "Conter (Contain)"),
            ("auto", "Automático"),
            ("100% 100%", "Esticar"),
        ],
        help_text="Como a imagem deve ser redimensionada"
    )
    
    # Repetição da imagem
    background_repeat = models.CharField(
        max_length=50,
        default="no-repeat",
        choices=[
            ("no-repeat", "Não repetir"),
            ("repeat", "Repetir"),
            ("repeat-x", "Repetir horizontalmente"),
            ("repeat-y", "Repetir verticalmente"),
        ],
        help_text="Como a imagem deve ser repetida"
    )
    
    # Anexar imagem (fixed/scroll)
    background_attachment = models.CharField(
        max_length=50,
        default="scroll",
        choices=[
            ("scroll", "Rolar com a página"),
            ("fixed", "Fixo (parallax)"),
        ],
        help_text="Como a imagem se comporta durante o scroll"
    )

    panels = [
        MultiFieldPanel([
            FieldPanel('background_image'),
            FieldPanel('background_overlay_opacity'),
        ], heading="Imagem de Fundo"),
        
        MultiFieldPanel([
            FieldPanel('background_position'),
            FieldPanel('background_size'),
            FieldPanel('background_repeat'),
            FieldPanel('background_attachment'),
        ], heading="Configurações de Exibição"),
    ]

    class Meta:
        verbose_name = "Configurações do Site"
        verbose_name_plural = "Configurações do Site"


@register_snippet
class PartnerLogo(models.Model):
    """Parceiros/Certificações exibidos no rodapé"""
    name = models.CharField(max_length=100, verbose_name="Nome")
    logo = models.ForeignKey(
        Image, null=True, blank=True, on_delete=models.SET_NULL, related_name='+', verbose_name="Logo"
    )
    url = models.URLField(blank=True, verbose_name="URL de destino")
    order = models.PositiveIntegerField(default=0, verbose_name="Ordem")
    is_active = models.BooleanField(default=True, verbose_name="Ativo")

    panels = [
        FieldPanel('name'),
        FieldPanel('logo'),
        FieldPanel('url'),
        FieldPanel('order'),
        FieldPanel('is_active'),
    ]

    class Meta:
        verbose_name = "Logo de Parceiro"
        verbose_name_plural = "Logos de Parceiros"
        ordering = ['order', 'name']

    def __str__(self):
        return self.name