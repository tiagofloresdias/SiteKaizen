from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.blocks import CharBlock, TextBlock, RichTextBlock, StructBlock, ListBlock
from wagtail.images.blocks import ImageChooserBlock


class MidiaProgramaticaPage(Page):
    """
    Página detalhada de Mídia Programática
    """
    # Hero Section
    hero_title = RichTextField(
        blank=True,
        help_text="Título principal da página"
    )
    hero_subtitle = RichTextField(
        blank=True,
        help_text="Subtítulo da página"
    )
    hero_cta_text = models.CharField(
        max_length=100,
        default="Solicitar Consultoria Gratuita",
        help_text="Texto do botão CTA principal"
    )
    
    # Seção Tecnologia Avançada
    tech_title = models.CharField(
        max_length=200,
        default="Tecnologia Avançada",
        help_text="Título da seção de tecnologia"
    )
    tech_description = RichTextField(
        blank=True,
        help_text="Descrição da tecnologia utilizada"
    )
    
    # Seção Canais de Mídia
    channels_title = models.CharField(
        max_length=200,
        default="Canais de Mídia",
        help_text="Título da seção de canais"
    )
    channels_subtitle = models.CharField(
        max_length=300,
        default="Cobertura completa em todos os pontos de contato com seu público",
        help_text="Subtítulo da seção de canais"
    )
    
    # Seção Como Trabalhamos
    process_title = models.CharField(
        max_length=200,
        default="Como Trabalhamos",
        help_text="Título da seção de processo"
    )
    process_subtitle = models.CharField(
        max_length=300,
        default="Processo estruturado para máxima eficiência e resultados",
        help_text="Subtítulo da seção de processo"
    )
    
    # Seção Benefícios
    benefits_title = models.CharField(
        max_length=200,
        default="Por que Escolher Nossa Plataforma?",
        help_text="Título da seção de benefícios"
    )
    
    # CTA Final
    final_cta_title = RichTextField(
        blank=True,
        help_text="Título do CTA final"
    )
    final_cta_subtitle = RichTextField(
        blank=True,
        help_text="Subtítulo do CTA final"
    )
    final_cta_button_text = models.CharField(
        max_length=100,
        default="Solicitar Consultoria Gratuita",
        help_text="Texto do botão CTA final"
    )
    final_cta_secondary_text = models.CharField(
        max_length=100,
        default="Ver Cases de Sucesso",
        help_text="Texto do botão secundário"
    )
    final_cta_secondary_url = models.URLField(
        blank=True,
        help_text="URL do botão secundário"
    )
    
    # SEO
    custom_seo_title = models.CharField(
        max_length=200,
        blank=True,
        help_text="Título SEO customizado (se diferente do título da página)"
    )
    custom_seo_description = models.TextField(
        max_length=300,
        blank=True,
        help_text="Descrição SEO customizada"
    )
    
    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('hero_title'),
            FieldPanel('hero_subtitle'),
            FieldPanel('hero_cta_text'),
        ], heading="Hero Section"),
        
        MultiFieldPanel([
            FieldPanel('tech_title'),
            FieldPanel('tech_description'),
        ], heading="Tecnologia Avançada"),
        
        MultiFieldPanel([
            FieldPanel('channels_title'),
            FieldPanel('channels_subtitle'),
        ], heading="Canais de Mídia"),
        
        MultiFieldPanel([
            FieldPanel('process_title'),
            FieldPanel('process_subtitle'),
        ], heading="Como Trabalhamos"),
        
        MultiFieldPanel([
            FieldPanel('benefits_title'),
        ], heading="Benefícios"),
        
        MultiFieldPanel([
            FieldPanel('final_cta_title'),
            FieldPanel('final_cta_subtitle'),
            FieldPanel('final_cta_button_text'),
            FieldPanel('final_cta_secondary_text'),
            FieldPanel('final_cta_secondary_url'),
        ], heading="CTA Final"),
        
        MultiFieldPanel([
            FieldPanel('custom_seo_title'),
            FieldPanel('custom_seo_description'),
        ], heading="SEO"),
    ]
    
    class Meta:
        verbose_name = "Página de Mídia Programática"
        verbose_name_plural = "Páginas de Mídia Programática"