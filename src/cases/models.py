from django.db import models
from django.utils import timezone
from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, TabbedInterface, ObjectList
from wagtail.search import index
from wagtail.blocks import (
    CharBlock, TextBlock, RichTextBlock, 
    StructBlock, ListBlock, URLBlock, IntegerBlock
)
from wagtail.images.blocks import ImageChooserBlock
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel


class CaseMetrics(StructBlock):
    """Bloco para métricas do case"""
    metric_name = CharBlock(max_length=100, label="Nome da Métrica")
    metric_value = CharBlock(max_length=50, label="Valor")
    metric_description = TextBlock(label="Descrição", required=False)
    
    class Meta:
        label = "Métrica"
        icon = "chart-line"


class CaseGallery(StructBlock):
    """Bloco para galeria de imagens do case"""
    image = ImageChooserBlock(label="Imagem")
    caption = CharBlock(max_length=200, label="Legenda", required=False)
    
    class Meta:
        label = "Imagem da Galeria"
        icon = "image"


class Case(ClusterableModel):
    """
    Modelo para cases de sucesso da Kaizen
    """
    # Informações básicas
    title = models.CharField(max_length=200, verbose_name="Título do Case")
    slug = models.SlugField(unique=True, max_length=100, verbose_name="Slug")
    client_name = models.CharField(max_length=100, verbose_name="Nome do Cliente")
    client_logo = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="Logo do Cliente"
    )
    
    # Categorização
    CATEGORY_CHOICES = [
        ('ecommerce', 'E-commerce'),
        ('saas', 'SaaS/Software'),
        ('servicos', 'Serviços'),
        ('varejo', 'Varejo'),
        ('industria', 'Indústria'),
        ('saude', 'Saúde'),
        ('educacao', 'Educação'),
        ('imobiliaria', 'Imobiliária'),
        ('automotivo', 'Automotivo'),
        ('outros', 'Outros'),
    ]
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        verbose_name="Categoria"
    )
    
    # Conteúdo principal
    hero_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="Imagem Principal"
    )
    short_description = models.TextField(
        max_length=300,
        verbose_name="Descrição Curta",
        help_text="Descrição resumida para cards e previews"
    )
    challenge = RichTextField(
        verbose_name="Desafio",
        help_text="Qual era o desafio do cliente?"
    )
    solution = RichTextField(
        verbose_name="Solução",
        help_text="Como a Kaizen resolveu o problema?"
    )
    results = RichTextField(
        verbose_name="Resultados",
        help_text="Quais foram os resultados alcançados?"
    )
    
    # Métricas em destaque
    main_metric_value = models.CharField(
        max_length=50,
        verbose_name="Métrica Principal",
        help_text="Ex: +300% de vendas"
    )
    main_metric_description = models.CharField(
        max_length=200,
        verbose_name="Descrição da Métrica",
        help_text="Ex: Aumento nas vendas em 6 meses"
    )
    
    # Conteúdo avançado
    content = StreamField([
        ('metrics', CaseMetrics()),
        ('gallery', CaseGallery()),
        ('paragraph', RichTextBlock()),
        ('heading', CharBlock()),
    ], blank=True, use_json_field=True, verbose_name="Conteúdo Adicional")
    
    # SEO
    meta_description = models.TextField(
        max_length=160,
        blank=True,
        verbose_name="Meta Description",
        help_text="Descrição para SEO (máximo 160 caracteres)"
    )
    
    # Status e datas
    is_featured = models.BooleanField(
        default=False,
        verbose_name="Case em Destaque"
    )
    is_published = models.BooleanField(
        default=True,
        verbose_name="Publicado"
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name="Ordem de Exibição"
    )
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")
    
    panels = [
        MultiFieldPanel([
            FieldPanel('title'),
            FieldPanel('slug'),
            FieldPanel('client_name'),
            FieldPanel('client_logo'),
            FieldPanel('category'),
        ], heading="Informações Básicas"),
        
        MultiFieldPanel([
            FieldPanel('hero_image'),
            FieldPanel('short_description'),
        ], heading="Visual e Descrição"),
        
        MultiFieldPanel([
            FieldPanel('challenge'),
            FieldPanel('solution'),
            FieldPanel('results'),
        ], heading="Storytelling"),
        
        MultiFieldPanel([
            FieldPanel('main_metric_value'),
            FieldPanel('main_metric_description'),
        ], heading="Métricas em Destaque"),
        
        FieldPanel('content'),
        
        MultiFieldPanel([
            FieldPanel('is_featured'),
            FieldPanel('is_published'),
            FieldPanel('order'),
        ], heading="Configurações"),
        
        FieldPanel('meta_description'),
    ]
    
    search_fields = [
        index.SearchField('title'),
        index.SearchField('client_name'),
        index.SearchField('short_description'),
        index.SearchField('challenge'),
        index.SearchField('solution'),
        index.SearchField('results'),
    ]
    
    class Meta:
        verbose_name = "Case de Sucesso"
        verbose_name_plural = "Cases de Sucesso"
        ordering = ['order', '-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.client_name}"
    
    def get_absolute_url(self):
        return f"/cases/{self.slug}/"


class CaseIndexPage(Page):
    """
    Página índice de cases (Cases)
    """
    # Hero Section
    hero_title = models.CharField(
        max_length=200,
        default="Cases de Sucesso",
        verbose_name="Título Principal"
    )
    hero_subtitle = RichTextField(
        default="<p>Resultados reais que transformaram negócios e geraram crescimento exponencial</p>",
        verbose_name="Subtítulo Principal"
    )
    hero_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="Imagem do Hero"
    )
    
    # Seção de filtros
    show_category_filters = models.BooleanField(
        default=True,
        verbose_name="Mostrar Filtros por Categoria"
    )
    show_featured_section = models.BooleanField(
        default=True,
        verbose_name="Mostrar Seção de Cases em Destaque"
    )
    
    # SEO
    meta_description = models.TextField(
        max_length=160,
        default="Cases de sucesso da Agência Kaizen. Veja como transformamos negócios e geramos resultados reais para nossos clientes.",
        verbose_name="Meta Description"
    )
    
    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('hero_title'),
            FieldPanel('hero_subtitle'),
            FieldPanel('hero_image'),
        ], heading="Hero Section"),
        
        MultiFieldPanel([
            FieldPanel('show_category_filters'),
            FieldPanel('show_featured_section'),
        ], heading="Configurações da Página"),
    ]
    
    promote_panels = [
        MultiFieldPanel([
            FieldPanel('meta_description'),
        ], heading="SEO"),
    ]
    
    def get_context(self, request):
        context = super().get_context(request)
        
        # Cases publicados ordenados
        cases = Case.objects.filter(is_published=True).order_by('order', '-created_at')
        
        # Cases em destaque
        featured_cases = cases.filter(is_featured=True)[:3]
        
        # Todas as categorias disponíveis
        categories = Case.CATEGORY_CHOICES
        
        # Filtro por categoria se especificado
        category_filter = request.GET.get('category')
        if category_filter:
            cases = cases.filter(category=category_filter)
        
        context.update({
            'cases': cases,
            'featured_cases': featured_cases,
            'categories': categories,
            'current_category': category_filter,
        })
        
        return context


class CaseDetailPage(Page):
    """
    Página de detalhes de um case específico
    """
    case = models.ForeignKey(
        Case,
        on_delete=models.PROTECT,
        verbose_name="Case"
    )
    
    # Conteúdo adicional específico da página
    additional_content = RichTextField(
        blank=True,
        verbose_name="Conteúdo Adicional"
    )
    
    # Call to action
    cta_title = models.CharField(
        max_length=100,
        default="Quer resultados similares?",
        verbose_name="Título do CTA"
    )
    cta_text = models.TextField(
        default="Entre em contato e descubra como podemos ajudar seu negócio a crescer.",
        verbose_name="Texto do CTA"
    )
    cta_button_text = models.CharField(
        max_length=50,
        default="Fale Conosco",
        verbose_name="Texto do Botão"
    )
    
    content_panels = Page.content_panels + [
        FieldPanel('case'),
        FieldPanel('additional_content'),
        MultiFieldPanel([
            FieldPanel('cta_title'),
            FieldPanel('cta_text'),
            FieldPanel('cta_button_text'),
        ], heading="Call to Action"),
    ]
    
    def get_context(self, request):
        context = super().get_context(request)
        context['case'] = self.case
        
        # Cases relacionados (mesma categoria)
        related_cases = Case.objects.filter(
            category=self.case.category,
            is_published=True
        ).exclude(id=self.case.id)[:3]
        
        context['related_cases'] = related_cases
        return context
    
    def save(self, *args, **kwargs):
        # Auto-generate slug and title from case
        if not self.slug and self.case:
            self.slug = self.case.slug
        if not self.title and self.case:
            self.title = f"{self.case.title} - Case de Sucesso"
        super().save(*args, **kwargs)