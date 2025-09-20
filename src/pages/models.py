"""
Modelos para páginas evergreen e padrão
"""
from django.db import models
from django.utils.text import slugify
from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.search import index
from wagtail.blocks import (
    CharBlock, TextBlock, RichTextBlock, StructBlock, ListBlock, 
    StreamBlock, PageChooserBlock, URLBlock
)
from wagtail.images.blocks import ImageChooserBlock


class StandardPage(Page):
    """
    Modelo para páginas evergreen com template padrão
    """
    intro = RichTextField(
        blank=True,
        help_text="Introdução da página"
    )
    
    body = StreamField([
        ('paragraph', RichTextBlock()),
        ('heading', CharBlock(classname="title")),
        ('image', ImageChooserBlock()),
        ('quote', StructBlock([
            ('quote', TextBlock()),
            ('attribution', CharBlock()),
        ])),
        ('raw_html', TextBlock(label='Raw HTML')),
    ], blank=True, use_json_field=True)
    
    meta_description = models.TextField(
        blank=True,
        help_text='Descrição para SEO (máximo 160 caracteres)',
        max_length=160
    )
    
    meta_keywords = models.CharField(
        blank=True,
        help_text='Palavras-chave separadas por vírgula',
        max_length=255
    )
    
    reading_time = models.PositiveIntegerField(
        default=5,
        help_text='Tempo estimado de leitura em minutos'
    )
    
    social_image = models.ForeignKey(
        'wagtailimages.Image',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Imagem para redes sociais'
    )

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('intro'),
            FieldPanel('body'),
            FieldPanel('reading_time'),
            FieldPanel('social_image'),
        ], heading="Conteúdo"),
        MultiFieldPanel([
            FieldPanel('meta_description'),
            FieldPanel('meta_keywords'),
        ], heading="SEO"),
    ]

    class Meta:
        verbose_name = "Página Padrão"
        verbose_name_plural = "Páginas Padrão"

