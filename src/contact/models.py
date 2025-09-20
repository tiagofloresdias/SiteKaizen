from django.db import models
from django.utils import timezone
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel


class Newsletter(models.Model):
    """
    Modelo para newsletter
    """
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255, blank=True)
    source = models.CharField(max_length=100, default='blog_sidebar')
    page_url = models.URLField(blank=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True)
    
    # UTM Parameters
    utm_source = models.CharField(max_length=100, blank=True)
    utm_medium = models.CharField(max_length=100, blank=True)
    utm_campaign = models.CharField(max_length=100, blank=True)
    utm_term = models.CharField(max_length=100, blank=True)
    utm_content = models.CharField(max_length=100, blank=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    subscribed_at = models.DateTimeField(default=timezone.now)
    unsubscribed_at = models.DateTimeField(null=True, blank=True)
    
    def unsubscribe(self):
        """Marca como descadastrado"""
        self.is_active = False
        self.unsubscribed_at = timezone.now()
        self.save()
    
    def __str__(self):
        return f"{self.email} ({'Ativo' if self.is_active else 'Inativo'})"
    
    class Meta:
        verbose_name = "Newsletter"
        verbose_name_plural = "Newsletters"


class ContactMessage(models.Model):
    """
    Modelo para mensagens de contato
    """
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    company = models.CharField(max_length=255, blank=True)
    message = models.TextField()
    
    # Tracking
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True)
    page_url = models.URLField(blank=True)
    
    # UTM Parameters
    utm_source = models.CharField(max_length=100, blank=True)
    utm_medium = models.CharField(max_length=100, blank=True)
    utm_campaign = models.CharField(max_length=100, blank=True)
    utm_term = models.CharField(max_length=100, blank=True)
    utm_content = models.CharField(max_length=100, blank=True)
    
    # Status
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.name} - {self.email}"
    
    class Meta:
        verbose_name = "Mensagem de Contato"
        verbose_name_plural = "Mensagens de Contato"
        ordering = ['-created_at']


class ConnectPage(Page):
    """
    Página Conecte-se com widgets de redes sociais
    """
    hero_title = models.CharField(
        max_length=255,
        default="Conecte-se com a Kaizen",
        verbose_name="Título Principal"
    )
    hero_subtitle = RichTextField(
        default="Siga nossa jornada nas redes sociais e fique por dentro de tudo que acontece na nossa aceleradora de vendas.",
        verbose_name="Subtítulo Principal"
    )
    
    # Instagram Section
    instagram_title = models.CharField(
        max_length=255,
        default="Nosso Instagram",
        verbose_name="Título da Seção Instagram"
    )
    instagram_subtitle = models.TextField(
        default="Acompanhe nosso dia a dia, cases de sucesso e dicas de marketing digital.",
        verbose_name="Subtítulo da Seção Instagram"
    )
    instagram_username = models.CharField(
        max_length=100,
        default="digitakaizen",
        verbose_name="Username do Instagram"
    )
    instagram_url = models.URLField(
        default="https://www.instagram.com/digitakaizen/",
        verbose_name="URL do Instagram"
    )
    
    # LinkedIn Section
    linkedin_title = models.CharField(
        max_length=255,
        default="Nosso LinkedIn",
        verbose_name="Título da Seção LinkedIn"
    )
    linkedin_subtitle = models.TextField(
        default="Conteúdo profissional, insights de mercado e networking de qualidade.",
        verbose_name="Subtítulo da Seção LinkedIn"
    )
    linkedin_url = models.URLField(
        default="https://www.linkedin.com/company/kaizenmarketingdigital/",
        verbose_name="URL do LinkedIn"
    )
    
    # CTA Section
    cta_title = models.CharField(
        max_length=255,
        default="Vamos Conectar?",
        verbose_name="Título do CTA"
    )
    cta_subtitle = RichTextField(
        default="Escolha sua rede social preferida e vamos conversar sobre como acelerar seu negócio!",
        verbose_name="Subtítulo do CTA"
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
        ], heading="Hero Section"),
        
        MultiFieldPanel([
            FieldPanel('instagram_title'),
            FieldPanel('instagram_subtitle'),
            FieldPanel('instagram_username'),
            FieldPanel('instagram_url'),
        ], heading="Instagram"),
        
        MultiFieldPanel([
            FieldPanel('linkedin_title'),
            FieldPanel('linkedin_subtitle'),
            FieldPanel('linkedin_url'),
        ], heading="LinkedIn"),
        
        MultiFieldPanel([
            FieldPanel('cta_title'),
            FieldPanel('cta_subtitle'),
        ], heading="Call to Action"),
        
        MultiFieldPanel([
            FieldPanel('meta_description'),
            FieldPanel('meta_keywords'),
        ], heading="SEO"),
    ]
    
    class Meta:
        verbose_name = "Página Conecte-se"
        verbose_name_plural = "Páginas Conecte-se"