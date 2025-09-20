from django.db import models
from django import forms
from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel, TabbedInterface, ObjectList
from wagtail.search import index
from wagtail.snippets.models import register_snippet
from wagtail import blocks
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.models import ClusterableModel
from wagtail.images.models import Image


class ServiceIcon(models.Model):
    """
    Ícones para os serviços
    """
    name = models.CharField(max_length=100, verbose_name="Nome do ícone")
    icon_class = models.CharField(max_length=100, verbose_name="Classe do ícone (FontAwesome)")
    description = models.TextField(blank=True, verbose_name="Descrição")
    
    class Meta:
        verbose_name = "Ícone de Serviço"
        verbose_name_plural = "Ícones de Serviços"
        ordering = ['name']
    
    def __str__(self):
        return self.name


@register_snippet
class Service(ClusterableModel):
    """
    Serviço individual dentro de uma seção
    """
    title = models.CharField(max_length=200, verbose_name="Título")
    description = models.TextField(verbose_name="Descrição")
    icon = models.ForeignKey(
        ServiceIcon,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Ícone"
    )
    custom_icon_class = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Classe de ícone personalizada",
        help_text="Se preenchido, será usado em vez do ícone selecionado"
    )
    is_featured = models.BooleanField(default=False, verbose_name="Destaque")
    order = models.PositiveIntegerField(default=0, verbose_name="Ordem")
    
    # SEO
    meta_description = models.TextField(
        max_length=160,
        blank=True,
        help_text="Descrição para SEO"
    )
    
    panels = [
        FieldPanel('title'),
        FieldPanel('description'),
        FieldPanel('icon'),
        FieldPanel('custom_icon_class'),
        FieldPanel('is_featured'),
        FieldPanel('order'),
        FieldPanel('meta_description'),
    ]
    
    class Meta:
        verbose_name = "Serviço"
        verbose_name_plural = "Serviços"
        ordering = ['order', 'title']
    
    def __str__(self):
        return self.title
    
    @property
    def icon_class(self):
        """Retorna a classe do ícone a ser usada"""
        if self.custom_icon_class:
            return self.custom_icon_class
        elif self.icon:
            return self.icon.icon_class
        return "fas fa-cog"  # ícone padrão


class SolutionSection(ClusterableModel):
    """
    Seção de soluções (ex: Geração de Oportunidades, Mídia Paga, etc.)
    """
    title = models.CharField(max_length=200, verbose_name="Título da Seção")
    subtitle = models.TextField(verbose_name="Subtítulo/Descrição")
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="Imagem da seção"
    )
    background_color = models.CharField(
        max_length=20,
        choices=[
            ('bg-dark', 'Escuro'),
            ('bg-black', 'Preto'),
            ('bg-primary', 'Primário'),
        ],
        default='bg-dark',
        verbose_name="Cor de Fundo"
    )
    services = ParentalManyToManyField(
        Service,
        blank=True,
        verbose_name="Serviços",
        help_text="Selecione os serviços desta seção"
    )
    order = models.PositiveIntegerField(default=0, verbose_name="Ordem")
    is_active = models.BooleanField(default=True, verbose_name="Ativo")
    
    # CTA da seção
    cta_text = models.CharField(
        max_length=100,
        default="Converse com um especialista",
        verbose_name="Texto do CTA"
    )
    cta_url = models.URLField(
        default="/contato/",
        verbose_name="URL do CTA"
    )
    
    panels = [
        FieldPanel('title'),
        FieldPanel('subtitle'),
        FieldPanel('image'),
        FieldPanel('background_color'),
        FieldPanel('services', widget=forms.CheckboxSelectMultiple),
        FieldPanel('order'),
        FieldPanel('is_active'),
        MultiFieldPanel([
            FieldPanel('cta_text'),
            FieldPanel('cta_url'),
        ], heading="Call to Action"),
    ]
    
    class Meta:
        verbose_name = "Seção de Soluções"
        verbose_name_plural = "Seções de Soluções"
        ordering = ['order', 'title']
    
    def __str__(self):
        return self.title


class SolutionsPage(Page):
    """
    Página principal de soluções
    """
    hero_title = models.CharField(
        max_length=200,
        default="Estratégias de impacto para resultados reais",
        verbose_name="Título Principal"
    )
    hero_subtitle = RichTextField(
        blank=True,
        verbose_name="Subtítulo Principal",
        help_text="Texto introdutório da página"
    )
    hero_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="Imagem de Fundo do Hero"
    )
    
    # CTA Final
    final_cta_title = models.CharField(
        max_length=200,
        default="Está pronto para transformar suas oportunidades em vendas reais?",
        verbose_name="Título do CTA Final"
    )
    final_cta_subtitle = models.TextField(
        default="Nossa equipe de especialistas está pronta para analisar seu negócio e desenvolver a estratégia perfeita para acelerar seu crescimento.",
        verbose_name="Subtítulo do CTA Final"
    )
    final_cta_button_text = models.CharField(
        max_length=100,
        default="Converse com um especialista",
        verbose_name="Texto do Botão CTA Final"
    )
    
    # SEO
    meta_description = models.TextField(
        max_length=160,
        blank=True,
        help_text="Descrição para SEO (máximo 160 caracteres)"
    )
    meta_keywords = models.CharField(
        max_length=255,
        blank=True,
        help_text="Palavras-chave separadas por vírgula"
    )
    
    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('hero_title'),
            FieldPanel('hero_subtitle'),
            FieldPanel('hero_image'),
        ], heading="Hero Section"),
        MultiFieldPanel([
            FieldPanel('final_cta_title'),
            FieldPanel('final_cta_subtitle'),
            FieldPanel('final_cta_button_text'),
        ], heading="CTA Final"),
    ]
    
    promote_panels = [
        MultiFieldPanel([
            FieldPanel('meta_description'),
            FieldPanel('meta_keywords'),
        ], heading="SEO"),
    ]
    
    def get_template(self, request):
        return "solutions/solutions_page.html"
    
    def get_context(self, request):
        context = super().get_context(request)
        
        # Buscar seções ativas ordenadas
        context['sections'] = SolutionSection.objects.filter(is_active=True).order_by('order')
        
        return context
    
    class Meta:
        verbose_name = "Página de Soluções"
        verbose_name_plural = "Páginas de Soluções"


# StreamField blocks para conteúdo mais flexível
class ServiceCardBlock(blocks.StructBlock):
    """
    Bloco para card de serviço
    """
    service = blocks.PageChooserBlock(
        target_model=Service,
        required=True,
        help_text="Selecione o serviço"
    )
    
    class Meta:
        icon = 'fa-cog'
        label = 'Card de Serviço'


class SolutionSectionBlock(blocks.StructBlock):
    """
    Bloco para seção de soluções
    """
    section = blocks.PageChooserBlock(
        target_model=SolutionSection,
        required=True,
        help_text="Selecione a seção"
    )
    
    class Meta:
        icon = 'fa-th-large'
        label = 'Seção de Soluções'