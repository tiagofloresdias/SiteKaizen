from django.db import models
from django import forms
from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.search import index
from wagtail.snippets.models import register_snippet
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.models import ClusterableModel


class PortfolioIndexPage(Page):
    """
    Página principal do portfolio
    """
    intro = RichTextField(blank=True, help_text="Texto introdutório da página do portfolio")
    
    content_panels = Page.content_panels + [
        FieldPanel('intro'),
    ]
    
    def get_context(self, request):
        context = super().get_context(request)
        portfolio_items = self.get_children().live().order_by('-first_published_at')
        context['portfolio_items'] = portfolio_items
        return context


class PortfolioCategory(models.Model):
    """
    Categoria do portfolio
    """
    name = models.CharField(max_length=255, verbose_name="Nome")
    slug = models.SlugField(unique=True, max_length=80, verbose_name="Slug")
    description = models.TextField(blank=True, verbose_name="Descrição")
    
    panels = [
        FieldPanel('name'),
        FieldPanel('slug'),
        FieldPanel('description'),
    ]
    
    class Meta:
        verbose_name = "Categoria do Portfolio"
        verbose_name_plural = "Categorias do Portfolio"
        ordering = ['name']
    
    def __str__(self):
        return self.name


# Removido o @register_snippet duplicado


class PortfolioItem(Page):
    """
    Item individual do portfolio
    """
    client = models.CharField(max_length=255, verbose_name="Cliente")
    project_date = models.DateField(verbose_name="Data do Projeto")
    project_url = models.URLField(blank=True, verbose_name="URL do Projeto")
    description = RichTextField(verbose_name="Descrição")
    categories = ParentalManyToManyField('portfolio.PortfolioCategory', blank=True, verbose_name="Categorias")
    featured_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="Imagem em destaque"
    )
    
    search_fields = Page.search_fields + [
        index.SearchField('client'),
        index.SearchField('description'),
    ]
    
    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('client'),
            FieldPanel('project_date'),
            FieldPanel('project_url'),
            FieldPanel('categories', widget=forms.CheckboxSelectMultiple),
        ], heading="Informações do Projeto"),
        FieldPanel('description'),
        FieldPanel('featured_image'),
        InlinePanel('gallery_images', label="Galeria de Imagens"),
    ]
    
    def get_context(self, request):
        context = super().get_context(request)
        # Projetos relacionados por categoria
        if self.categories.exists():
            related_projects = PortfolioItem.objects.filter(
                categories__in=self.categories.all()
            ).exclude(id=self.id).distinct()[:3]
            context['related_projects'] = related_projects
        return context


class PortfolioGalleryImage(Orderable):
    """
    Imagens da galeria do portfolio
    """
    page = ParentalKey(PortfolioItem, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.CASCADE,
        related_name='+'
    )
    caption = models.CharField(blank=True, max_length=250)
    
    panels = [
        FieldPanel('image'),
        FieldPanel('caption'),
    ]
