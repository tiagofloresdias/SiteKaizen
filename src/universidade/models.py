from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel

class Expert(ClusterableModel):
    """
    Modelo para experts da Universidade Kaizen
    """
    name = models.CharField(max_length=200, help_text="Nome do expert")
    title = models.CharField(max_length=300, help_text="Título/cargo do expert")
    bio = RichTextField(help_text="Biografia do expert")
    photo = models.ImageField(upload_to='experts/', help_text="Foto do expert")
    specialties = models.CharField(max_length=500, help_text="Especialidades (separadas por vírgula)")
    social_linkedin = models.URLField(blank=True, help_text="LinkedIn do expert")
    social_instagram = models.URLField(blank=True, help_text="Instagram do expert")
    social_twitter = models.URLField(blank=True, help_text="Twitter do expert")
    
    panels = [
        FieldPanel('name'),
        FieldPanel('title'),
        FieldPanel('bio'),
        FieldPanel('photo'),
        FieldPanel('specialties'),
        MultiFieldPanel([
            FieldPanel('social_linkedin'),
            FieldPanel('social_instagram'),
            FieldPanel('social_twitter'),
        ], heading="Redes Sociais"),
    ]
    
    class Meta:
        verbose_name = "Expert"
        verbose_name_plural = "Experts"
    
    def __str__(self):
        return self.name

class Curso(ClusterableModel):
    """
    Modelo para cursos da Universidade Kaizen
    """
    title = models.CharField(max_length=200, help_text="Título do curso")
    description = RichTextField(help_text="Descrição do curso")
    duration = models.CharField(max_length=100, help_text="Duração do curso")
    level = models.CharField(max_length=50, choices=[
        ('iniciante', 'Iniciante'),
        ('intermediario', 'Intermediário'),
        ('avancado', 'Avançado'),
    ], help_text="Nível do curso")
    thumbnail = models.ImageField(upload_to='cursos/', help_text="Thumbnail do curso")
    is_free = models.BooleanField(default=True, help_text="Curso gratuito")
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Preço do curso")
    
    panels = [
        FieldPanel('title'),
        FieldPanel('description'),
        FieldPanel('duration'),
        FieldPanel('level'),
        FieldPanel('thumbnail'),
        FieldPanel('is_free'),
        FieldPanel('price'),
    ]
    
    class Meta:
        verbose_name = "Curso"
        verbose_name_plural = "Cursos"
    
    def __str__(self):
        return self.title

class UniversidadeKaizenPage(Page):
    """
    Página principal da Universidade Kaizen
    """
    template = 'universidade/universidade_kaizen_page.html'
    
    # Hero Section
    hero_title = RichTextField(
        default="<span class='text-pink'>Universidade Kaizen</span>",
        help_text="Título principal da seção Hero"
    )
    hero_subtitle = RichTextField(
        default="Evolução contínua para performance máxima",
        help_text="Subtítulo da seção Hero"
    )
    hero_description = RichTextField(
        default="O conhecimento certo pode transformar qualquer negócio. Na Universidade Kaizen, você tem acesso ao que há de mais avançado em marketing digital, vendas e estratégias de crescimento.",
        help_text="Descrição da seção Hero"
    )
    hero_cta_text = models.CharField(
        max_length=100,
        default="QUERO PARTICIPAR",
        help_text="Texto do botão CTA na seção Hero"
    )
    hero_image = models.ImageField(
        upload_to='universidade/',
        blank=True,
        null=True,
        help_text="Imagem principal da seção Hero"
    )
    
    # Sobre a Universidade
    about_title = models.CharField(
        max_length=200,
        default="Por que a Universidade Kaizen?",
        help_text="Título da seção sobre"
    )
    about_description = RichTextField(
        default="Aqui, você encontra cursos gratuitos e trilhas completas ministradas pelos maiores especialistas do mercado. Conteúdo prático, atualizado e focado em resultados reais.",
        help_text="Descrição da seção sobre"
    )
    
    # Vantagens
    advantages_title = models.CharField(
        max_length=200,
        default="O que você vai encontrar",
        help_text="Título da seção de vantagens"
    )
    
    # Experts Section
    experts_title = models.CharField(
        max_length=200,
        default="Conheça nossos especialistas",
        help_text="Título da seção de experts"
    )
    experts_subtitle = models.CharField(
        max_length=300,
        default="Aprenda com os melhores profissionais do mercado",
        help_text="Subtítulo da seção de experts"
    )
    
    # Cursos Section
    cursos_title = models.CharField(
        max_length=200,
        default="Cursos Disponíveis",
        help_text="Título da seção de cursos"
    )
    cursos_subtitle = models.CharField(
        max_length=300,
        default="Conteúdo prático e atualizado para acelerar seu crescimento",
        help_text="Subtítulo da seção de cursos"
    )
    
    # CTA Final
    final_cta_title = RichTextField(
        default="Pronto para <span class='text-pink'>Evoluir</span> seu Conhecimento?",
        help_text="Título do CTA final"
    )
    final_cta_subtitle = RichTextField(
        default="Junte-se a milhares de profissionais que já transformaram seus negócios com a Universidade Kaizen.",
        help_text="Subtítulo do CTA final"
    )
    final_cta_button_text = models.CharField(
        max_length=100,
        default="COMEÇAR AGORA",
        help_text="Texto do botão principal do CTA final"
    )
    
    # SEO
    custom_seo_title = models.CharField(
        max_length=200,
        blank=True,
        help_text="Título SEO personalizado"
    )
    custom_seo_description = models.TextField(
        max_length=300,
        blank=True,
        help_text="Descrição SEO personalizada"
    )
    
    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('hero_title'),
            FieldPanel('hero_subtitle'),
            FieldPanel('hero_description'),
            FieldPanel('hero_cta_text'),
            FieldPanel('hero_image'),
        ], heading="Hero Section"),
        
        MultiFieldPanel([
            FieldPanel('about_title'),
            FieldPanel('about_description'),
        ], heading="Sobre a Universidade"),
        
        MultiFieldPanel([
            FieldPanel('advantages_title'),
        ], heading="Vantagens"),
        
        MultiFieldPanel([
            FieldPanel('experts_title'),
            FieldPanel('experts_subtitle'),
        ], heading="Seção de Experts"),
        
        MultiFieldPanel([
            FieldPanel('cursos_title'),
            FieldPanel('cursos_subtitle'),
        ], heading="Seção de Cursos"),
        
        MultiFieldPanel([
            FieldPanel('final_cta_title'),
            FieldPanel('final_cta_subtitle'),
            FieldPanel('final_cta_button_text'),
        ], heading="CTA Final"),
        
        MultiFieldPanel([
            FieldPanel('custom_seo_title'),
            FieldPanel('custom_seo_description'),
        ], heading="SEO"),
    ]
    
    class Meta:
        verbose_name = "Página da Universidade Kaizen"
        verbose_name_plural = "Páginas da Universidade Kaizen"
