from django.db import models
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from wagtail.snippets.models import register_snippet


@register_setting
class AnalyticsSettings(BaseSiteSetting):
    """
    Configurações globais de Analytics e Tracking
    """
    # Google Tag Manager
    gtm_container_id = models.CharField(
        max_length=20,
        default="GTM-5JCWMWQ",
        verbose_name="GTM Container ID",
        help_text="ID do container do Google Tag Manager (ex: GTM-5JCWMWQ)"
    )
    gtm_enabled = models.BooleanField(
        default=True,
        verbose_name="GTM Ativo",
        help_text="Ativar/desativar o Google Tag Manager"
    )
    
    # Google Analytics 4
    ga4_measurement_id = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="GA4 Measurement ID",
        help_text="ID de medição do Google Analytics 4 (ex: G-XXXXXXXXXX)"
    )
    ga4_enabled = models.BooleanField(
        default=False,
        verbose_name="GA4 Ativo",
        help_text="Ativar/desativar o Google Analytics 4"
    )
    
    # Facebook Pixel
    facebook_pixel_id = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Facebook Pixel ID",
        help_text="ID do Facebook Pixel"
    )
    facebook_pixel_enabled = models.BooleanField(
        default=False,
        verbose_name="Facebook Pixel Ativo"
    )
    
    # LinkedIn Insight Tag
    linkedin_partner_id = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="LinkedIn Partner ID",
        help_text="ID do LinkedIn Insight Tag"
    )
    linkedin_enabled = models.BooleanField(
        default=False,
        verbose_name="LinkedIn Tracking Ativo"
    )
    
    # Configurações de Eventos
    track_form_submissions = models.BooleanField(
        default=True,
        verbose_name="Rastrear Envio de Formulários",
        help_text="Enviar evento quando formulários forem enviados"
    )
    track_phone_clicks = models.BooleanField(
        default=True,
        verbose_name="Rastrear Cliques em Telefone",
        help_text="Enviar evento quando números de telefone forem clicados"
    )
    track_whatsapp_clicks = models.BooleanField(
        default=True,
        verbose_name="Rastrear Cliques no WhatsApp",
        help_text="Enviar evento quando links do WhatsApp forem clicados"
    )
    track_email_clicks = models.BooleanField(
        default=True,
        verbose_name="Rastrear Cliques em Email",
        help_text="Enviar evento quando links de email forem clicados"
    )
    track_external_links = models.BooleanField(
        default=True,
        verbose_name="Rastrear Links Externos",
        help_text="Enviar evento quando links externos forem clicados"
    )
    track_scroll_depth = models.BooleanField(
        default=True,
        verbose_name="Rastrear Profundidade de Scroll",
        help_text="Enviar eventos de scroll (25%, 50%, 75%, 100%)"
    )
    
    panels = [
        MultiFieldPanel([
            FieldPanel('gtm_container_id'),
            FieldPanel('gtm_enabled'),
        ], heading="Google Tag Manager"),
        
        MultiFieldPanel([
            FieldPanel('ga4_measurement_id'),
            FieldPanel('ga4_enabled'),
        ], heading="Google Analytics 4"),
        
        MultiFieldPanel([
            FieldPanel('facebook_pixel_id'),
            FieldPanel('facebook_pixel_enabled'),
        ], heading="Facebook Pixel"),
        
        MultiFieldPanel([
            FieldPanel('linkedin_partner_id'),
            FieldPanel('linkedin_enabled'),
        ], heading="LinkedIn Insight Tag"),
        
        MultiFieldPanel([
            FieldPanel('track_form_submissions'),
            FieldPanel('track_phone_clicks'),
            FieldPanel('track_whatsapp_clicks'),
            FieldPanel('track_email_clicks'),
            FieldPanel('track_external_links'),
            FieldPanel('track_scroll_depth'),
        ], heading="Configurações de Eventos"),
    ]
    
    class Meta:
        verbose_name = "Configurações de Analytics"
        verbose_name_plural = "Configurações de Analytics"


@register_snippet
class CustomEvent(models.Model):
    """
    Eventos personalizados para tracking
    """
    name = models.CharField(
        max_length=100,
        verbose_name="Nome do Evento",
        help_text="Nome do evento para o GTM (ex: contact_form_submit)"
    )
    display_name = models.CharField(
        max_length=200,
        verbose_name="Nome para Exibição",
        help_text="Nome amigável do evento"
    )
    description = models.TextField(
        blank=True,
        verbose_name="Descrição",
        help_text="Descrição do que o evento rastreia"
    )
    category = models.CharField(
        max_length=50,
        default="engagement",
        verbose_name="Categoria",
        help_text="Categoria do evento (ex: engagement, conversion, navigation)"
    )
    is_conversion = models.BooleanField(
        default=False,
        verbose_name="É Conversão",
        help_text="Marcar se este evento representa uma conversão"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Ativo",
        help_text="Ativar/desativar este evento"
    )
    
    # Parâmetros adicionais
    custom_parameters = models.JSONField(
        default=dict,
        blank=True,
        verbose_name="Parâmetros Personalizados",
        help_text="Parâmetros adicionais em formato JSON"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    panels = [
        FieldPanel('name'),
        FieldPanel('display_name'),
        FieldPanel('description'),
        FieldPanel('category'),
        FieldPanel('is_conversion'),
        FieldPanel('is_active'),
        FieldPanel('custom_parameters'),
    ]
    
    class Meta:
        verbose_name = "Evento Personalizado"
        verbose_name_plural = "Eventos Personalizados"
        ordering = ['category', 'name']
    
    def __str__(self):
        return f"{self.display_name} ({self.name})"
