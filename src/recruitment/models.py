from django.db import models
from django.utils import timezone
from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, TabbedInterface, ObjectList
from wagtail.search import index
from wagtail.blocks import (
    CharBlock, TextBlock, RichTextBlock, 
    StructBlock, ListBlock, URLBlock, IntegerBlock, ChoiceBlock
)
from wagtail.images.blocks import ImageChooserBlock


class RecruitmentApplication(models.Model):
    """
    Modelo para candidaturas de recrutamento
    """
    
    # Dados Pessoais
    full_name = models.CharField(max_length=200, verbose_name="Nome Completo")
    email = models.EmailField(verbose_name="E-mail")
    phone = models.CharField(max_length=20, verbose_name="Telefone")
    birth_date = models.DateField(verbose_name="Data de Nascimento")
    cpf = models.CharField(max_length=14, verbose_name="CPF")
    rg = models.CharField(max_length=20, verbose_name="RG")
    address = models.TextField(verbose_name="Endereço Completo")
    city = models.CharField(max_length=100, verbose_name="Cidade")
    state = models.CharField(max_length=2, verbose_name="Estado")
    zip_code = models.CharField(max_length=10, verbose_name="CEP")
    
    # Informações Profissionais
    current_position = models.CharField(max_length=200, verbose_name="Cargo Atual")
    current_company = models.CharField(max_length=200, verbose_name="Empresa Atual")
    experience_years = models.IntegerField(verbose_name="Anos de Experiência")
    education_level = models.CharField(
        max_length=50,
        choices=[
            ('fundamental', 'Ensino Fundamental'),
            ('medio', 'Ensino Médio'),
            ('tecnico', 'Ensino Técnico'),
            ('superior_incompleto', 'Superior Incompleto'),
            ('superior_completo', 'Superior Completo'),
            ('pos_graduacao', 'Pós-graduação'),
            ('mestrado', 'Mestrado'),
            ('doutorado', 'Doutorado'),
        ],
        verbose_name="Nível de Escolaridade"
    )
    course_name = models.CharField(max_length=200, blank=True, verbose_name="Nome do Curso")
    institution = models.CharField(max_length=200, blank=True, verbose_name="Instituição")
    
    # Área de Interesse
    desired_area = models.CharField(
        max_length=100,
        choices=[
            ('marketing_digital', 'Marketing Digital'),
            ('vendas', 'Vendas'),
            ('desenvolvimento', 'Desenvolvimento'),
            ('design', 'Design'),
            ('atendimento', 'Atendimento'),
            ('rh', 'Recursos Humanos'),
            ('financeiro', 'Financeiro'),
            ('operacional', 'Operacional'),
            ('gestao', 'Gestão'),
            ('outro', 'Outro'),
        ],
        verbose_name="Área de Interesse"
    )
    
    # Disponibilidade
    availability = models.CharField(
        max_length=50,
        choices=[
            ('imediata', 'Imediata'),
            ('1_mes', '1 mês'),
            ('2_meses', '2 meses'),
            ('3_meses', '3 meses'),
            ('mais_3_meses', 'Mais de 3 meses'),
        ],
        verbose_name="Disponibilidade"
    )
    
    # Conhecimentos Técnicos
    technical_skills = models.TextField(verbose_name="Habilidades Técnicas")
    languages = models.TextField(verbose_name="Idiomas")
    certifications = models.TextField(blank=True, verbose_name="Certificações")
    
    # Experiência com Ferramentas
    crm_experience = models.BooleanField(default=False, verbose_name="Experiência com CRM")
    social_media_experience = models.BooleanField(default=False, verbose_name="Experiência com Redes Sociais")
    google_ads_experience = models.BooleanField(default=False, verbose_name="Experiência com Google Ads")
    facebook_ads_experience = models.BooleanField(default=False, verbose_name="Experiência com Facebook Ads")
    analytics_experience = models.BooleanField(default=False, verbose_name="Experiência com Analytics")
    seo_experience = models.BooleanField(default=False, verbose_name="Experiência com SEO")
    content_creation_experience = models.BooleanField(default=False, verbose_name="Experiência com Criação de Conteúdo")
    
    # Motivação e Expectativas
    motivation = models.TextField(verbose_name="Motivação para Trabalhar na Kaizen")
    salary_expectation = models.CharField(max_length=100, verbose_name="Pretensão Salarial")
    career_goals = models.TextField(verbose_name="Objetivos de Carreira")
    
    # Informações Adicionais
    linkedin_profile = models.URLField(blank=True, verbose_name="Perfil LinkedIn")
    instagram_profile = models.CharField(max_length=100, blank=True, verbose_name="Perfil Instagram")
    portfolio_url = models.URLField(blank=True, verbose_name="Portfólio/Website")
    work_modality_preference = models.CharField(
        max_length=20,
        choices=[
            ('presencial', 'Presencial'),
            ('remoto', 'Remoto'),
            ('hibrido', 'Híbrido'),
        ],
        default='remoto',
        blank=True,
        verbose_name="Modalidade de Preferência"
    )
    referral_source = models.CharField(
        max_length=100,
        choices=[
            ('site', 'Site da Empresa'),
            ('linkedin', 'LinkedIn'),
            ('indicação', 'Indicação'),
            ('google', 'Google'),
            ('facebook', 'Facebook'),
            ('instagram', 'Instagram'),
            ('outro', 'Outro'),
        ],
        verbose_name="Como Conheceu a Vaga"
    )
    
    # Documentos
    resume_file = models.FileField(upload_to='recruitment/resumes/', blank=True, verbose_name="Currículo")
    cover_letter = models.TextField(blank=True, verbose_name="Carta de Apresentação")
    
    # Status da Candidatura
    status = models.CharField(
        max_length=50,
        choices=[
            ('nova', 'Nova'),
            ('em_analise', 'Em Análise'),
            ('entrevista', 'Entrevista'),
            ('aprovado', 'Aprovado'),
            ('rejeitado', 'Rejeitado'),
        ],
        default='nova',
        verbose_name="Status"
    )
    
    # Timestamps
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")
    
    class Meta:
        verbose_name = "Candidatura"
        verbose_name_plural = "Candidaturas"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.full_name} - {self.desired_area}"


class FoguetePage(Page):
    """
    Página "Quero Ser um Foguete" - Cultura Kaizen
    """
    template = "recruitment/foguete_page.html"
    parent_page_types = ['home.HomePage']
    
    hero_title = models.CharField(
        max_length=200, 
        default="Quero Ser um Foguete Kaizen",
        verbose_name="Título do Hero"
    )
    hero_subtitle = models.TextField(
        default="Faça parte de uma equipe que acredita na melhoria contínua e na excelência operacional.",
        verbose_name="Subtítulo do Hero"
    )
    
    # Seção sobre Cultura Kaizen
    culture_title = models.CharField(
        max_length=200,
        default="Nossa Cultura Kaizen",
        verbose_name="Título da Cultura"
    )
    culture_content = RichTextField(
        default="A filosofia Kaizen é o coração da nossa empresa. Acreditamos na melhoria contínua e no poder das pequenas mudanças que geram grandes transformações.",
        verbose_name="Conteúdo sobre Cultura"
    )
    
    # Seção sobre os 5S
    five_s_title = models.CharField(
        max_length=200,
        default="Os 5S da Kaizen",
        verbose_name="Título dos 5S"
    )
    five_s_content = RichTextField(
        default="Nossos valores são baseados nos 5S da filosofia Kaizen: Seiri (Organização), Seiton (Ordenação), Seiso (Limpeza), Seiketsu (Padronização) e Shitsuke (Disciplina).",
        verbose_name="Conteúdo dos 5S"
    )
    
    # Seção de Benefícios
    benefits_title = models.CharField(
        max_length=200,
        default="Por que ser um Foguete Kaizen?",
        verbose_name="Título dos Benefícios"
    )
    benefits_content = RichTextField(
        default="Junte-se a uma equipe que valoriza a inovação, o crescimento pessoal e profissional, e a busca constante pela excelência.",
        verbose_name="Conteúdo dos Benefícios"
    )
    
    # CTA para Recrutamento
    cta_title = models.CharField(
        max_length=200,
        default="Pronto para Decolar?",
        verbose_name="Título do CTA"
    )
    cta_subtitle = models.TextField(
        default="Envie sua candidatura e faça parte da nossa missão de transformar negócios através do marketing digital.",
        verbose_name="Subtítulo do CTA"
    )
    
    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('hero_title'),
            FieldPanel('hero_subtitle'),
        ], heading="Hero Section"),
        MultiFieldPanel([
            FieldPanel('culture_title'),
            FieldPanel('culture_content'),
        ], heading="Cultura Kaizen"),
        MultiFieldPanel([
            FieldPanel('five_s_title'),
            FieldPanel('five_s_content'),
        ], heading="Os 5S"),
        MultiFieldPanel([
            FieldPanel('benefits_title'),
            FieldPanel('benefits_content'),
        ], heading="Benefícios"),
        MultiFieldPanel([
            FieldPanel('cta_title'),
            FieldPanel('cta_subtitle'),
        ], heading="Call to Action"),
    ]
    
    class Meta:
        verbose_name = "Página Quero Ser um Foguete"
        verbose_name_plural = "Páginas Quero Ser um Foguete"


class RecruitmentPage(Page):
    """
    Página de Recrutamento com formulário completo
    """
    template = "recruitment/recruitment_page.html"
    parent_page_types = ['recruitment.FoguetePage']
    
    hero_title = models.CharField(
        max_length=200,
        default="Formulário de Candidatura",
        verbose_name="Título do Hero"
    )
    hero_subtitle = models.TextField(
        default="Preencha o formulário abaixo para se candidatar a uma vaga na Kaizen.",
        verbose_name="Subtítulo do Hero"
    )
    
    # Instruções do formulário
    form_instructions = RichTextField(
        default="Por favor, preencha todos os campos obrigatórios com informações verdadeiras e atualizadas.",
        verbose_name="Instruções do Formulário"
    )
    
    # Política de privacidade
    privacy_policy = RichTextField(
        default="Seus dados serão utilizados exclusivamente para o processo seletivo e não serão compartilhados com terceiros.",
        verbose_name="Política de Privacidade"
    )
    
    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('hero_title'),
            FieldPanel('hero_subtitle'),
        ], heading="Hero Section"),
        FieldPanel('form_instructions'),
        FieldPanel('privacy_policy'),
    ]
    
    class Meta:
        verbose_name = "Página de Recrutamento"
        verbose_name_plural = "Páginas de Recrutamento"