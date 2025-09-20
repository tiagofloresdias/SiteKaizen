"""
Modelos para o app de Desenvolvimento de Sites
Inclui galeria de sites desenvolvidos e páginas de detalhes
"""
from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.images.models import Image
from wagtail.documents.models import Document
from wagtail.search import index
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel


class SiteDesenvolvido(ClusterableModel):
    """
    Modelo para sites desenvolvidos pela Kaizen
    """
    nome = models.CharField(max_length=200, verbose_name="Nome do Site/Cliente")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="Slug")
    descricao_curta = models.TextField(max_length=300, verbose_name="Descrição Curta")
    descricao_completa = RichTextField(verbose_name="Descrição Completa")
    
    # Informações do projeto
    tipo_site = models.CharField(
        max_length=100,
        choices=[
            ('ecommerce', 'E-commerce'),
            ('institucional', 'Site Institucional'),
            ('landing_page', 'Landing Page'),
            ('blog', 'Blog/Portal'),
            ('sistema', 'Sistema Web'),
            ('outro', 'Outro'),
        ],
        verbose_name="Tipo de Site"
    )
    
    tecnologias = models.CharField(
        max_length=500,
        verbose_name="Tecnologias Utilizadas",
        help_text="Ex: WordPress, React, Django, etc."
    )
    
    # URLs e links
    url_site = models.URLField(
        blank=True,
        null=True,
        verbose_name="URL do Site",
        help_text="Link para acessar o site no ar"
    )
    
    url_demo = models.URLField(
        blank=True,
        null=True,
        verbose_name="URL de Demo",
        help_text="Link para versão de demonstração"
    )
    
    # Imagens
    imagem_principal = models.ForeignKey(
        Image,
        on_delete=models.CASCADE,
        related_name='+',
        verbose_name="Imagem Principal",
        help_text="Imagem principal do site (desktop)"
    )
    
    imagem_mobile = models.ForeignKey(
        Image,
        on_delete=models.CASCADE,
        related_name='+',
        blank=True,
        null=True,
        verbose_name="Imagem Mobile",
        help_text="Imagem do site em dispositivo móvel"
    )
    
    # Galeria de imagens
    galeria_imagens = models.ManyToManyField(
        Image,
        blank=True,
        related_name='sites_galeria',
        verbose_name="Galeria de Imagens",
        help_text="Imagens adicionais do site"
    )
    
    # Informações do cliente
    nome_cliente = models.CharField(
        max_length=200,
        verbose_name="Nome do Cliente",
        help_text="Nome da empresa ou pessoa"
    )
    
    setor_cliente = models.CharField(
        max_length=100,
        verbose_name="Setor do Cliente",
        help_text="Ex: E-commerce, Saúde, Educação, etc."
    )
    
    # Resultados obtidos
    resultado_principal = models.CharField(
        max_length=200,
        verbose_name="Principal Resultado",
        help_text="Ex: Aumento de 300% nas vendas online"
    )
    
    tempo_desenvolvimento = models.CharField(
        max_length=100,
        verbose_name="Tempo de Desenvolvimento",
        help_text="Ex: 2 meses, 6 semanas, etc."
    )
    
    # SEO e visibilidade
    destaque = models.BooleanField(
        default=False,
        verbose_name="Destaque",
        help_text="Marcar para aparecer em destaque na galeria"
    )
    
    ordem_exibicao = models.PositiveIntegerField(
        default=0,
        verbose_name="Ordem de Exibição",
        help_text="Número para ordenar na galeria (menor = primeiro)"
    )
    
    # Metadados
    data_desenvolvimento = models.DateField(
        verbose_name="Data de Desenvolvimento"
    )
    
    ativo = models.BooleanField(
        default=True,
        verbose_name="Ativo",
        help_text="Se o site deve aparecer na galeria"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Site Desenvolvido"
        verbose_name_plural = "Sites Desenvolvidos"
        ordering = ['ordem_exibicao', '-data_desenvolvimento']
    
    def __str__(self):
        return f"{self.nome} - {self.nome_cliente}"
    
    @property
    def tem_url_ativa(self):
        """Verifica se o site tem URL ativa"""
        return bool(self.url_site)
    
    @property
    def tecnologias_lista(self):
        """Retorna lista das tecnologias"""
        return [t.strip() for t in self.tecnologias.split(',') if t.strip()]


class DesenvolvimentoSitesPage(Page):
    """
    Página principal de Desenvolvimento de Sites
    """
    hero_title = RichTextField(
        verbose_name="Título Principal",
        default="<h1>Desenvolvimento de Sites que <strong>Convertem</strong></h1>"
    )
    
    hero_subtitle = RichTextField(
        verbose_name="Subtítulo Principal",
        default="<p>Criamos sites modernos, responsivos e otimizados para gerar resultados reais para seu negócio.</p>"
    )
    
    hero_image = models.ForeignKey(
        Image,
        on_delete=models.CASCADE,
        related_name='+',
        blank=True,
        null=True,
        verbose_name="Imagem Hero"
    )
    
    # Seção de benefícios
    beneficios_titulo = models.CharField(
        max_length=200,
        default="Por que escolher nossos sites?",
        verbose_name="Título dos Benefícios"
    )
    
    beneficios_conteudo = StreamField([
        ('beneficio', BeneficioBlock()),
    ], blank=True, verbose_name="Benefícios")
    
    # Seção de processo
    processo_titulo = models.CharField(
        max_length=200,
        default="Nosso Processo de Desenvolvimento",
        verbose_name="Título do Processo"
    )
    
    processo_conteudo = StreamField([
        ('etapa', EtapaProcessoBlock()),
    ], blank=True, verbose_name="Etapas do Processo")
    
    # Seção de tecnologias
    tecnologias_titulo = models.CharField(
        max_length=200,
        default="Tecnologias que Dominamos",
        verbose_name="Título das Tecnologias"
    )
    
    tecnologias_conteudo = RichTextField(
        blank=True,
        verbose_name="Conteúdo das Tecnologias"
    )
    
    # SEO
    custom_seo_title = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Título SEO Personalizado"
    )
    
    custom_seo_description = models.TextField(
        max_length=300,
        blank=True,
        verbose_name="Descrição SEO Personalizada"
    )
    
    content_panels = Page.content_panels + [
        FieldPanel('hero_title'),
        FieldPanel('hero_subtitle'),
        FieldPanel('hero_image'),
        FieldPanel('beneficios_titulo'),
        FieldPanel('beneficios_conteudo'),
        FieldPanel('processo_titulo'),
        FieldPanel('processo_conteudo'),
        FieldPanel('tecnologias_titulo'),
        FieldPanel('tecnologias_conteudo'),
        MultiFieldPanel([
            FieldPanel('custom_seo_title'),
            FieldPanel('custom_seo_description'),
        ], heading="SEO"),
    ]
    
    search_fields = Page.search_fields + [
        index.SearchField('hero_title'),
        index.SearchField('hero_subtitle'),
        index.SearchField('beneficios_conteudo'),
        index.SearchField('processo_conteudo'),
    ]
    
    def get_context(self, request):
        context = super().get_context(request)
        context['sites_destaque'] = SiteDesenvolvido.objects.filter(
            ativo=True,
            destaque=True
        ).order_by('ordem_exibicao', '-data_desenvolvimento')[:6]
        
        context['todos_sites'] = SiteDesenvolvido.objects.filter(
            ativo=True
        ).order_by('ordem_exibicao', '-data_desenvolvimento')
        
        return context


class SiteDetalhePage(Page):
    """
    Página de detalhes de um site específico
    """
    site = models.ForeignKey(
        SiteDesenvolvido,
        on_delete=models.CASCADE,
        related_name='pagina_detalhe',
        verbose_name="Site"
    )
    
    conteudo_adicional = StreamField([
        ('paragrafo', RichTextBlock()),
        ('imagem', ImageBlock()),
        ('galeria', ImageGalleryBlock()),
    ], blank=True, verbose_name="Conteúdo Adicional")
    
    content_panels = Page.content_panels + [
        FieldPanel('site'),
        FieldPanel('conteudo_adicional'),
    ]
    
    def get_context(self, request):
        context = super().get_context(request)
        context['site'] = self.site
        
        # Sites relacionados (mesmo tipo ou setor)
        context['sites_relacionados'] = SiteDesenvolvido.objects.filter(
            ativo=True,
            tipo_site=self.site.tipo_site
        ).exclude(id=self.site.id)[:3]
        
        return context


# Blocks para StreamField
from wagtail.blocks import RichTextBlock, StructBlock, CharBlock, TextBlock, URLBlock, ImageBlock, ListBlock
from wagtail.images.blocks import ImageChooserBlock


class BeneficioBlock(StructBlock):
    """Block para benefícios dos sites"""
    icone = CharBlock(max_length=50, help_text="Classe do ícone FontAwesome")
    titulo = CharBlock(max_length=100)
    descricao = TextBlock()
    
    class Meta:
        icon = 'tick'
        label = 'Benefício'


class EtapaProcessoBlock(StructBlock):
    """Block para etapas do processo"""
    numero = CharBlock(max_length=10)
    titulo = CharBlock(max_length=100)
    descricao = TextBlock()
    icone = CharBlock(max_length=50, help_text="Classe do ícone FontAwesome")
    
    class Meta:
        icon = 'list-ol'
        label = 'Etapa do Processo'


class ImageGalleryBlock(StructBlock):
    """Block para galeria de imagens"""
    titulo = CharBlock(max_length=100, required=False)
    imagens = ListBlock(ImageChooserBlock())
    
    class Meta:
        icon = 'image'
        label = 'Galeria de Imagens'