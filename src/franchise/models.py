"""
Modelos para o sistema de franquias
"""
from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator
import uuid


class FranchiseApplication(models.Model):
    """
    Modelo para aplicações de franqueados
    """
    MARITAL_STATUS_CHOICES = [
        ('single', 'Solteiro(a)'),
        ('married', 'Casado(a)'),
        ('divorced', 'Divorciado(a)'),
        ('widowed', 'Viúvo(a)'),
    ]
    
    EDUCATION_LEVEL_CHOICES = [
        ('elementary', 'Ensino Fundamental'),
        ('high_school', 'Ensino Médio'),
        ('technical', 'Técnico'),
        ('college', 'Superior'),
        ('postgraduate', 'Pós-graduação'),
        ('master', 'Mestrado'),
        ('phd', 'Doutorado'),
    ]
    
    EXPERIENCE_LEVEL_CHOICES = [
        ('none', 'Nenhuma'),
        ('low', 'Pouca (1-2 anos)'),
        ('medium', 'Média (3-5 anos)'),
        ('high', 'Alta (6-10 anos)'),
        ('expert', 'Expert (10+ anos)'),
    ]
    
    INVESTMENT_CAPACITY_CHOICES = [
        ('low', 'Até R$ 50.000'),
        ('medium', 'R$ 50.000 - R$ 150.000'),
        ('high', 'R$ 150.000 - R$ 300.000'),
        ('very_high', 'Acima de R$ 300.000'),
    ]
    
    TEAM_SIZE_CHOICES = [
        ('solo', 'Só eu'),
        ('small', '2-5 pessoas'),
        ('medium', '6-15 pessoas'),
        ('large', '16-50 pessoas'),
        ('enterprise', '50+ pessoas'),
    ]
    
    RISK_TOLERANCE_CHOICES = [
        ('low', 'Baixa'),
        ('medium', 'Média'),
        ('high', 'Alta'),
    ]
    
    TIME_AVAILABILITY_CHOICES = [
        ('part_time', 'Meio período'),
        ('full_time', 'Tempo integral'),
        ('weekends', 'Fins de semana'),
        ('flexible', 'Flexível'),
    ]
    
    STATUS_CHOICES = [
        ('draft', 'Rascunho'),
        ('submitted', 'Enviada'),
        ('under_review', 'Em Análise'),
        ('approved', 'Aprovada'),
        ('rejected', 'Rejeitada'),
        ('scheduled', 'Agendada'),
        ('completed', 'Concluída'),
    ]
    
    # Identificação única
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    application_number = models.CharField(max_length=20, unique=True, verbose_name="Número da Aplicação")
    
    # Status e timestamps
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', verbose_name="Status")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")
    submitted_at = models.DateTimeField(null=True, blank=True, verbose_name="Enviado em")
    
    # Dados pessoais (Step 1)
    full_name = models.CharField(max_length=200, verbose_name="Nome Completo")
    email = models.EmailField(verbose_name="E-mail")
    phone = models.CharField(
        max_length=20, 
        validators=[RegexValidator(regex=r'^\(\d{2}\)\s\d{4,5}-\d{4}$', message='Formato: (11) 99999-9999')],
        verbose_name="Telefone"
    )
    cpf = models.CharField(
        max_length=14,
        validators=[RegexValidator(regex=r'^\d{3}\.\d{3}\.\d{3}-\d{2}$', message='Formato: 000.000.000-00')],
        verbose_name="CPF"
    )
    rg = models.CharField(max_length=20, verbose_name="RG")
    birth_date = models.DateField(verbose_name="Data de Nascimento")
    marital_status = models.CharField(max_length=20, choices=MARITAL_STATUS_CHOICES, verbose_name="Estado Civil")
    nationality = models.CharField(max_length=100, default='Brasileira', verbose_name="Nacionalidade")
    
    # Endereço
    address = models.CharField(max_length=300, verbose_name="Endereço")
    city = models.CharField(max_length=100, verbose_name="Cidade")
    state = models.CharField(max_length=2, verbose_name="Estado")
    zipcode = models.CharField(
        max_length=9,
        validators=[RegexValidator(regex=r'^\d{5}-\d{3}$', message='Formato: 00000-000')],
        verbose_name="CEP"
    )
    
    # Perfil profissional (Step 2)
    profession = models.CharField(max_length=100, verbose_name="Profissão")
    current_company = models.CharField(max_length=200, blank=True, verbose_name="Empresa Atual")
    current_position = models.CharField(max_length=100, blank=True, verbose_name="Cargo Atual")
    experience_years = models.PositiveIntegerField(verbose_name="Anos de Experiência")
    education_level = models.CharField(max_length=20, choices=EDUCATION_LEVEL_CHOICES, verbose_name="Nível de Escolaridade")
    management_experience = models.CharField(max_length=20, choices=EXPERIENCE_LEVEL_CHOICES, verbose_name="Experiência em Gestão")
    sales_experience = models.CharField(max_length=20, choices=EXPERIENCE_LEVEL_CHOICES, verbose_name="Experiência em Vendas")
    marketing_experience = models.CharField(max_length=20, choices=EXPERIENCE_LEVEL_CHOICES, verbose_name="Experiência em Marketing")
    
    # Investimento e localização (Step 3)
    investment_capacity = models.CharField(max_length=20, choices=INVESTMENT_CAPACITY_CHOICES, verbose_name="Capacidade de Investimento")
    preferred_city = models.CharField(max_length=100, verbose_name="Cidade de Interesse")
    preferred_state = models.CharField(max_length=2, verbose_name="Estado de Interesse")
    preferred_region = models.CharField(max_length=100, blank=True, verbose_name="Região de Interesse")
    expected_start_date = models.DateField(verbose_name="Data Esperada para Início")
    team_size = models.CharField(max_length=20, choices=TEAM_SIZE_CHOICES, verbose_name="Tamanho da Equipe Pretendida")
    target_market = models.CharField(max_length=200, blank=True, verbose_name="Mercado-Alvo de Interesse")
    
    # Objetivos e motivação
    business_goals = models.TextField(verbose_name="Objetivos de Negócio")
    why_franchise = models.TextField(verbose_name="Por que quer ser franqueado?")
    expected_revenue = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name="Receita Esperada")
    available_time = models.CharField(max_length=20, choices=TIME_AVAILABILITY_CHOICES, verbose_name="Tempo Disponível")
    risk_tolerance = models.CharField(max_length=20, choices=RISK_TOLERANCE_CHOICES, verbose_name="Tolerância ao Risco")
    references = models.TextField(blank=True, verbose_name="Referências")
    
    # Documentos (Step 4)
    curriculum = models.FileField(upload_to='franchise/documents/', null=True, blank=True, verbose_name="Currículo")
    business_plan = models.FileField(upload_to='franchise/documents/', null=True, blank=True, verbose_name="Plano de Negócios")
    financial_statement = models.FileField(upload_to='franchise/documents/', null=True, blank=True, verbose_name="Demonstrativo Financeiro")
    identity_document = models.FileField(upload_to='franchise/documents/', null=True, blank=True, verbose_name="Documento de Identidade")
    address_proof = models.FileField(upload_to='franchise/documents/', null=True, blank=True, verbose_name="Comprovante de Endereço")
    income_proof = models.FileField(upload_to='franchise/documents/', null=True, blank=True, verbose_name="Comprovante de Renda")
    
    # Agendamento (Step 5)
    meeting_scheduled = models.BooleanField(default=False, verbose_name="Reunião Agendada")
    meeting_date = models.DateTimeField(null=True, blank=True, verbose_name="Data da Reunião")
    meeting_notes = models.TextField(blank=True, verbose_name="Observações da Reunião")
    
    # Tracking e analytics
    utm_source = models.CharField(max_length=100, blank=True, verbose_name="UTM Source")
    utm_medium = models.CharField(max_length=100, blank=True, verbose_name="UTM Medium")
    utm_campaign = models.CharField(max_length=100, blank=True, verbose_name="UTM Campaign")
    utm_term = models.CharField(max_length=100, blank=True, verbose_name="UTM Term")
    utm_content = models.CharField(max_length=100, blank=True, verbose_name="UTM Content")
    referrer = models.URLField(blank=True, verbose_name="Referrer")
    landing_page = models.URLField(blank=True, verbose_name="Página de Entrada")
    user_agent = models.TextField(blank=True, verbose_name="User Agent")
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name="IP Address")
    session_id = models.CharField(max_length=100, blank=True, verbose_name="Session ID")
    
    # Campos de controle
    is_active = models.BooleanField(default=True, verbose_name="Ativo")
    notes = models.TextField(blank=True, verbose_name="Observações Internas")
    
    class Meta:
        verbose_name = "Aplicação de Franqueado"
        verbose_name_plural = "Aplicações de Franqueados"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.application_number} - {self.full_name}"
    
    def save(self, *args, **kwargs):
        if not self.application_number:
            self.application_number = self.generate_application_number()
        super().save(*args, **kwargs)
    
    def generate_application_number(self):
        """Gera número único da aplicação"""
        import datetime
        now = datetime.datetime.now()
        return f"FR{now.strftime('%Y%m%d')}{FranchiseApplication.objects.count() + 1:04d}"


class FranchiseTouchpoint(models.Model):
    """
    Modelo para tracking de interações do franqueado
    """
    EVENT_TYPES = [
        ('page_view', 'Visualização de Página'),
        ('modal_open', 'Abertura da Modal'),
        ('step1_start', 'Início do Step 1'),
        ('step1_complete', 'Conclusão do Step 1'),
        ('step2_start', 'Início do Step 2'),
        ('step2_complete', 'Conclusão do Step 2'),
        ('step3_start', 'Início do Step 3'),
        ('step3_complete', 'Conclusão do Step 3'),
        ('step4_start', 'Início do Step 4'),
        ('step4_complete', 'Conclusão do Step 4'),
        ('step5_start', 'Início do Step 5'),
        ('step5_complete', 'Conclusão do Step 5'),
        ('step6_complete', 'Conclusão do Step 6'),
        ('form_submit', 'Envio do Formulário'),
        ('document_upload', 'Upload de Documento'),
        ('meeting_scheduled', 'Reunião Agendada'),
        ('application_submitted', 'Aplicação Enviada'),
        ('conversion', 'Conversão Completa'),
    ]
    
    application = models.ForeignKey(
        FranchiseApplication, 
        on_delete=models.CASCADE, 
        related_name='touchpoints',
        verbose_name="Aplicação"
    )
    event_type = models.CharField(max_length=50, choices=EVENT_TYPES, verbose_name="Tipo de Evento")
    event_data = models.JSONField(default=dict, blank=True, verbose_name="Dados do Evento")
    step_number = models.PositiveIntegerField(null=True, blank=True, verbose_name="Número do Step")
    page_url = models.URLField(blank=True, verbose_name="URL da Página")
    timestamp = models.DateTimeField(default=timezone.now, verbose_name="Timestamp")
    
    class Meta:
        verbose_name = "Touchpoint de Franqueado"
        verbose_name_plural = "Touchpoints de Franqueados"
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.application.full_name} - {self.get_event_type_display()}"


class FranchiseDocument(models.Model):
    """
    Modelo para documentos de franqueados
    """
    DOCUMENT_TYPES = [
        ('curriculum', 'Currículo'),
        ('business_plan', 'Plano de Negócios'),
        ('financial_statement', 'Demonstrativo Financeiro'),
        ('identity_document', 'Documento de Identidade'),
        ('address_proof', 'Comprovante de Endereço'),
        ('income_proof', 'Comprovante de Renda'),
        ('other', 'Outro'),
    ]
    
    application = models.ForeignKey(
        FranchiseApplication,
        on_delete=models.CASCADE,
        related_name='documents',
        verbose_name="Aplicação"
    )
    document_type = models.CharField(max_length=30, choices=DOCUMENT_TYPES, verbose_name="Tipo de Documento")
    file = models.FileField(upload_to='franchise/documents/', verbose_name="Arquivo")
    original_filename = models.CharField(max_length=255, verbose_name="Nome Original")
    file_size = models.PositiveIntegerField(verbose_name="Tamanho do Arquivo")
    mime_type = models.CharField(max_length=100, verbose_name="Tipo MIME")
    uploaded_at = models.DateTimeField(default=timezone.now, verbose_name="Enviado em")
    is_verified = models.BooleanField(default=False, verbose_name="Verificado")
    verification_notes = models.TextField(blank=True, verbose_name="Observações de Verificação")
    
    class Meta:
        verbose_name = "Documento de Franqueado"
        verbose_name_plural = "Documentos de Franqueados"
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"{self.application.full_name} - {self.get_document_type_display()}"

