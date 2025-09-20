from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator
import json


class UTMParameters(models.Model):
    """
    Modelo para rastrear parâmetros UTM dos leads
    """
    utm_source = models.CharField(max_length=100, blank=True, verbose_name="UTM Source")
    utm_medium = models.CharField(max_length=100, blank=True, verbose_name="UTM Medium")
    utm_campaign = models.CharField(max_length=100, blank=True, verbose_name="UTM Campaign")
    utm_term = models.CharField(max_length=100, blank=True, verbose_name="UTM Term")
    utm_content = models.CharField(max_length=100, blank=True, verbose_name="UTM Content")
    
    # Parâmetros adicionais de tracking
    referrer = models.URLField(blank=True, verbose_name="Referrer")
    landing_page = models.URLField(blank=True, verbose_name="Página de Entrada")
    user_agent = models.TextField(blank=True, verbose_name="User Agent")
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name="IP Address")
    
    # Dados de sessão
    session_id = models.CharField(max_length=100, blank=True, verbose_name="Session ID")
    device_type = models.CharField(max_length=50, blank=True, verbose_name="Tipo de Dispositivo")
    browser = models.CharField(max_length=50, blank=True, verbose_name="Navegador")
    os = models.CharField(max_length=50, blank=True, verbose_name="Sistema Operacional")
    
    # Timestamps
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Criado em")
    
    class Meta:
        verbose_name = "UTM Parameters"
        verbose_name_plural = "UTM Parameters"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"UTM: {self.utm_source} - {self.utm_medium} - {self.utm_campaign}"
    
    def get_utm_summary(self):
        """Retorna um resumo dos parâmetros UTM"""
        return {
            'source': self.utm_source,
            'medium': self.utm_medium,
            'campaign': self.utm_campaign,
            'term': self.utm_term,
            'content': self.utm_content
        }


class Touchpoint(models.Model):
    """
    Modelo para rastrear eventos de interação do lead
    """
    EVENT_TYPES = [
        ('page_view', 'Visualização de Página'),
        ('modal_open', 'Abertura da Modal'),
        ('step1_start', 'Início do Step 1'),
        ('step1_complete', 'Conclusão do Step 1'),
        ('step2_start', 'Início do Step 2'),
        ('step2_complete', 'Conclusão do Step 2'),
        ('step3_start', 'Início do Step 3 (Calendly)'),
        ('step3_complete', 'Conclusão do Step 3'),
        ('step4_complete', 'Conclusão do Step 4'),
        ('form_submit', 'Envio do Formulário'),
        ('calendly_scheduled', 'Agendamento no Calendly'),
        ('email_sent', 'Email Enviado'),
        ('conversion', 'Conversão Completa'),
    ]
    
    lead = models.ForeignKey('Lead', on_delete=models.CASCADE, related_name='touchpoints', verbose_name="Lead")
    event_type = models.CharField(max_length=50, choices=EVENT_TYPES, verbose_name="Tipo de Evento")
    event_data = models.JSONField(default=dict, blank=True, verbose_name="Dados do Evento")
    step_number = models.PositiveIntegerField(null=True, blank=True, verbose_name="Número do Step")
    page_url = models.URLField(blank=True, verbose_name="URL da Página")
    timestamp = models.DateTimeField(default=timezone.now, verbose_name="Timestamp")
    
    class Meta:
        verbose_name = "Touchpoint"
        verbose_name_plural = "Touchpoints"
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.lead.name} - {self.get_event_type_display()} - {self.timestamp}"


class Lead(models.Model):
    """
    Modelo para captura de leads do formulário multi-passo
    """
    # Passo 1 - Dados básicos
    name = models.CharField(max_length=100, verbose_name="Nome")
    email = models.EmailField(verbose_name="E-mail")
    phone = models.CharField(
        max_length=20, 
        verbose_name="Telefone",
        validators=[RegexValidator(
            regex=r'^\(\d{2}\)\s\d{4,5}-\d{4}$',
            message='Formato: (11) 99999-9999'
        )]
    )
    
    # Passo 2 - Informações do negócio
    monthly_revenue = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Faturamento Mensal",
        choices=[
            ('ate_10k', 'Até R$ 10.000'),
            ('10k_50k', 'R$ 10.000 - R$ 50.000'),
            ('50k_100k', 'R$ 50.000 - R$ 100.000'),
            ('100k_500k', 'R$ 100.000 - R$ 500.000'),
            ('500k_1m', 'R$ 500.000 - R$ 1.000.000'),
            ('acima_1m', 'Acima de R$ 1.000.000'),
        ]
    )
    business_area = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Área do Negócio",
        choices=[
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
    )
    main_challenge = models.TextField(
        blank=True,
        verbose_name="Principal Desafio do Negócio",
        help_text="Descreva o principal desafio de marketing que podemos ajudar"
    )
    website_social = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Site ou Rede Social",
        help_text="Website ou rede social da empresa"
    )
    
    # Campos específicos para franqueados
    lead_type = models.CharField(
        max_length=20,
        choices=[
            ('business', 'Lead de Negócio'),
            ('franchise', 'Lead de Franquia'),
        ],
        default='business',
        verbose_name="Tipo de Lead"
    )
    
    # Dados específicos de franqueados
    current_activity = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Área de Atuação Atual",
        choices=[
            ('marketing-digital', 'Marketing Digital'),
            ('vendas', 'Vendas'),
            ('gestao-empresarial', 'Gestão Empresarial'),
            ('tecnologia', 'Tecnologia'),
            ('consultoria', 'Consultoria'),
            ('outro', 'Outro'),
        ]
    )
    experience_years = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Anos de Experiência",
        choices=[
            ('0-1', '0 a 1 ano'),
            ('2-5', '2 a 5 anos'),
            ('6-10', '6 a 10 anos'),
            ('10+', 'Mais de 10 anos'),
        ]
    )
    franchise_timeline = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Prazo para Início da Franquia",
        choices=[
            ('imediato', 'Imediato (até 30 dias)'),
            ('3-meses', '3 meses'),
            ('6-meses', '6 meses'),
            ('1-ano', '1 ano'),
            ('mais-1-ano', 'Mais de 1 ano'),
        ]
    )
    franchise_type = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Tipo de Franquia de Interesse",
        choices=[
            ('consultoria', 'Franquia de Consultoria'),
            ('agencia', 'Franquia de Agência'),
            ('ambas', 'Ambas as opções'),
        ]
    )
    investment_range = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Faixa de Investimento",
        choices=[
            ('ate-50k', 'Até R$ 50.000'),
            ('50k-100k', 'R$ 50.000 a R$ 100.000'),
            ('100k-200k', 'R$ 100.000 a R$ 200.000'),
            ('200k-500k', 'R$ 200.000 a R$ 500.000'),
            ('acima-500k', 'Acima de R$ 500.000'),
        ]
    )
    additional_info = models.TextField(
        blank=True,
        verbose_name="Informações Adicionais",
        help_text="Informações adicionais sobre objetivos e expectativas"
    )
    
    # Status do lead
    STATUS_CHOICES = [
        ('step1', 'Passo 1 - Dados Básicos'),
        ('step2', 'Passo 2 - Informações do Negócio'),
        ('step3', 'Passo 3 - Calendly'),
        ('completed', 'Completo'),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='step1',
        verbose_name="Status"
    )
    
    # Dados do agendamento
    calendly_event_id = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="ID do Evento Calendly"
    )
    scheduled_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Data do Agendamento"
    )
    
    # Email de confirmação
    confirmation_email_sent = models.BooleanField(
        default=False,
        verbose_name="Email de Confirmação Enviado"
    )
    
    # UTM Parameters
    utm_parameters = models.ForeignKey(
        UTMParameters, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='leads',
        verbose_name="Parâmetros UTM"
    )
    
    # Timestamps
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")
    
    class Meta:
        verbose_name = "Lead"
        verbose_name_plural = "Leads"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.email}"
    
    def get_phone_display(self):
        """Retorna o telefone formatado para exibição"""
        return self.phone
    
    def get_monthly_revenue_display(self):
        """Retorna o faturamento formatado para exibição"""
        return dict(self._meta.get_field('monthly_revenue').choices).get(
            self.monthly_revenue, self.monthly_revenue
        )
    
    def get_business_area_display(self):
        """Retorna a área do negócio formatada para exibição"""
        return dict(self._meta.get_field('business_area').choices).get(
            self.business_area, self.business_area
        )
    
    def get_current_activity_display(self):
        """Retorna a área de atuação atual formatada para exibição"""
        return dict(self._meta.get_field('current_activity').choices).get(
            self.current_activity, self.current_activity
        )
    
    def get_experience_years_display(self):
        """Retorna os anos de experiência formatados para exibição"""
        return dict(self._meta.get_field('experience_years').choices).get(
            self.experience_years, self.experience_years
        )
    
    def get_franchise_timeline_display(self):
        """Retorna o prazo para início da franquia formatado para exibição"""
        return dict(self._meta.get_field('franchise_timeline').choices).get(
            self.franchise_timeline, self.franchise_timeline
        )
    
    def get_franchise_type_display(self):
        """Retorna o tipo de franquia formatado para exibição"""
        return dict(self._meta.get_field('franchise_type').choices).get(
            self.franchise_type, self.franchise_type
        )
    
    def get_investment_range_display(self):
        """Retorna a faixa de investimento formatada para exibição"""
        return dict(self._meta.get_field('investment_range').choices).get(
            self.investment_range, self.investment_range
        )
