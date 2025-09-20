from django.db import models
from django.utils.text import slugify
from django.forms import CheckboxSelectMultiple
from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.search import index
from wagtail.snippets.models import register_snippet
from wagtail.images.blocks import ImageChooserBlock
from wagtail.blocks import (
    CharBlock, TextBlock, RichTextBlock, StructBlock, ListBlock, 
    StreamBlock, PageChooserBlock, URLBlock
)
from taggit.models import Tag as TaggitTag, TaggedItemBase


class BlogIndexPage(Page):
    """Página índice do blog - lista todos os posts"""
    intro = RichTextField(blank=True)
    
    content_panels = Page.content_panels + [
        FieldPanel('intro'),
    ]
    
    def get_context(self, request):
        # Atualizar contexto para incluir apenas posts publicados
        context = super().get_context(request)
        
        # Buscar posts filhos publicados
        blogpages = self.get_children().live().type(BlogPage).order_by('-first_published_at')
        
        # Paginação
        from django.core.paginator import Paginator
        paginator = Paginator(blogpages, 12)  # 12 posts por página
        
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context['blogpages'] = page_obj
        context['categories'] = BlogCategory.objects.all()
        context['popular_tags'] = TaggitTag.objects.all()[:10]
        
        return context


class BlogPageTag(TaggedItemBase):
    """Modelo para tags dos posts do blog"""
    content_object = models.ForeignKey('BlogPage', on_delete=models.CASCADE)


@register_snippet
class BlogCategory(models.Model):
    """Modelo para categorias do blog"""
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=80)
    description = models.TextField(blank=True)
    
    panels = [
        FieldPanel('name'),
        FieldPanel('slug'),
        FieldPanel('description'),
    ]
    
    class Meta:
        verbose_name = "Categoria do Blog"
        verbose_name_plural = "Categorias do Blog"
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class BlogPage(Page):
    """Modelo para posts do blog"""
    date = models.DateField("Data de publicação")
    intro = models.CharField(max_length=250, blank=True)
    body = RichTextField(blank=True)
    categories = models.ManyToManyField(BlogCategory, blank=True)
    is_featured = models.BooleanField(default=False, verbose_name='Post em destaque')
    meta_description = models.TextField(blank=True, help_text='Descrição para SEO (máximo 160 caracteres)', max_length=160)
    meta_keywords = models.CharField(blank=True, help_text='Palavras-chave separadas por vírgula', max_length=255)
    reading_time = models.PositiveIntegerField(default=5, help_text='Tempo estimado de leitura em minutos')
    social_image = models.ForeignKey('wagtailimages.Image', blank=True, null=True, on_delete=models.SET_NULL, related_name='+', verbose_name='Imagem para redes sociais')
    
    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]
    
    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('intro'),
            FieldPanel('categories', widget=CheckboxSelectMultiple),
            FieldPanel('is_featured'),
            FieldPanel('reading_time'),
            FieldPanel('social_image'),
        ], heading="Informações do Post"),
        FieldPanel('body'),
        MultiFieldPanel([
            FieldPanel('meta_description'),
            FieldPanel('meta_keywords'),
        ], heading="SEO"),
    ]
    
    def get_context(self, request):
        context = super().get_context(request)
        context['related_posts'] = BlogPage.objects.live().exclude(id=self.id)[:3]
        return context


# Adicionar tags ao BlogPage
BlogPage.tags = models.ManyToManyField(TaggitTag, through=BlogPageTag, blank=True)


class CategoryIndexPage(Page):
    """Página índice de categorias"""
    intro = RichTextField(blank=True)
    
    content_panels = Page.content_panels + [
        FieldPanel('intro'),
    ]
    
    def get_context(self, request):
        context = super().get_context(request)
        context['categories'] = BlogCategory.objects.all()
        return context


class TagIndexPage(Page):
    """Página índice de tags"""
    intro = RichTextField(blank=True)
    
    content_panels = Page.content_panels + [
        FieldPanel('intro'),
    ]
    
    def get_context(self, request):
        context = super().get_context(request)
        context['tags'] = TaggitTag.objects.all()
        return context