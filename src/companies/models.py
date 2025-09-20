from django.db import models
from django.utils import timezone
from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel, TabbedInterface, ObjectList
from wagtail.search import index
from wagtail.snippets.models import register_snippet
from wagtail import blocks
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel


@register_snippet
class CompanyCategory(models.Model):
    """
    Categoria de empresas (ex: CRM, Marketing, Automação, etc.)
    """
    name = models.CharField(max_length=100, verbose_name="Nome")
    slug = models.SlugField(unique=True, max_length=100, verbose_name="Slug")
    description = models.TextField(blank=True, verbose_name="Descrição")
    color = models.CharField(
        max_length=7, 
        default="#D62042", 
        verbose_name="Cor",
        help_text="Cor em hexadecimal (ex: #D62042)"
    )
    
    panels = [
        FieldPanel('name'),
        FieldPanel('slug'),
        FieldPanel('description'),
        FieldPanel('color'),
    ]
    
    class Meta:
        verbose_name = "Categoria de Empresa"
        verbose_name_plural = "Categorias de Empresas"
        ordering = ['name']
    
    def __str__(self):
        return self.name


@register_snippet
class Company(ClusterableModel):
    """
    Modelo para empresas do Grupo Kaizen
    """
    # Informações básicas
    name = models.CharField(max_length=100, verbose_name="Nome da Empresa")
    slug = models.SlugField(unique=True, max_length=100, verbose_name="Slug")
    tagline = models.CharField(max_length=200, verbose_name="Slogan/Tagline")
    description = RichTextField(verbose_name="Descrição")
    
    # Logo e imagens
    logo = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="Logo"
    )
    featured_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="Imagem em destaque"
    )
    
    # Categorização
    category = models.ForeignKey(
        CompanyCategory,
        on_delete=models.CASCADE,
        verbose_name="Categoria"
    )
    
    # URLs e contato
    website_url = models.URLField(blank=True, verbose_name="Site da empresa")
    contact_email = models.EmailField(blank=True, verbose_name="Email de contato")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Telefone")
    
    # Status e ordem
    is_active = models.BooleanField(default=True, verbose_name="Ativo")
    order = models.PositiveIntegerField(default=0, verbose_name="Ordem de exibição")
    
    # SEO
    meta_description = models.TextField(
        max_length=160,
        blank=True,
        help_text="Descrição para SEO (máximo 160 caracteres)"
    )
    
    # Datas
    founded_date = models.DateField(blank=True, null=True, verbose_name="Data de fundação")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")
    
    panels = [
        FieldPanel('name'),
        FieldPanel('slug'),
        FieldPanel('tagline'),
        FieldPanel('category'),
        FieldPanel('description'),
        MultiFieldPanel([
            FieldPanel('logo'),
            FieldPanel('featured_image'),
        ], heading="Imagens"),
        MultiFieldPanel([
            FieldPanel('website_url'),
            FieldPanel('contact_email'),
            FieldPanel('phone'),
        ], heading="Contato"),
        MultiFieldPanel([
            FieldPanel('is_active'),
            FieldPanel('order'),
            FieldPanel('founded_date'),
        ], heading="Configurações"),
        FieldPanel('meta_description'),
    ]
    
    search_fields = [
        index.SearchField('name'),
        index.SearchField('tagline'),
        index.SearchField('description'),
    ]
    
    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name


class CompanyFeature(models.Model):
    """
    Características/funcionalidades de uma empresa
    """
    company = ParentalKey(Company, on_delete=models.CASCADE, related_name='features')
    title = models.CharField(max_length=100, verbose_name="Título")
    description = models.TextField(verbose_name="Descrição")
    icon = models.CharField(
        max_length=50, 
        blank=True, 
        verbose_name="Ícone Font Awesome",
        help_text="Ex: fas fa-chart-line"
    )
    order = models.PositiveIntegerField(default=0, verbose_name="Ordem")
    
    panels = [
        FieldPanel('title'),
        FieldPanel('description'),
        FieldPanel('icon'),
        FieldPanel('order'),
    ]
    
    class Meta:
        verbose_name = "Funcionalidade"
        verbose_name_plural = "Funcionalidades"
        ordering = ['order']
    
    def __str__(self):
        return f"{self.company.name} - {self.title}"


class CompaniesIndexPage(Page):
    """
    Página índice das empresas (Nossas Empresas)
    """
    intro = RichTextField(blank=True, help_text="Texto introdutório da página")
    hero_title = models.CharField(
        max_length=200, 
        default="Mais que uma agência, um ecossistema de crescimento.",
        verbose_name="Título principal"
    )
    hero_subtitle = RichTextField(
        blank=True,
        default="<p>A Kaizen é mais que uma agência. Somos um grupo de empresas que acelera negócios em diferentes áreas.</p>",
        verbose_name="Subtítulo principal"
    )
    
    # SEO
    meta_description = models.TextField(
        max_length=160,
        blank=True,
        help_text="Descrição para SEO (máximo 160 caracteres)"
    )
    
    content_panels = Page.content_panels + [
        FieldPanel('hero_title'),
        FieldPanel('hero_subtitle'),
        FieldPanel('intro'),
    ]
    
    promote_panels = [
        MultiFieldPanel([
            FieldPanel('meta_description'),
        ], heading="SEO"),
    ]
    
    def get_context(self, request):
        context = super().get_context(request)
        
        # Empresas ativas ordenadas
        context['companies'] = Company.objects.filter(is_active=True).order_by('order', 'name')
        
        # Categorias para filtros
        context['categories'] = CompanyCategory.objects.all()
        
        return context

    template = "companies/companies_index_page.html"


class CompanyDetailPage(Page):
    """
    Página de detalhes de uma empresa específica
    """
    company = models.ForeignKey(
        Company,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Empresa"
    )
    
    # Conteúdo adicional
    additional_content = RichTextField(blank=True, verbose_name="Conteúdo adicional")
    
    # Call to action
    cta_title = models.CharField(
        max_length=100, 
        default="Interessado em saber mais?",
        verbose_name="Título do CTA"
    )
    cta_text = models.TextField(
        default="Entre em contato e descubra como podemos ajudar seu negócio.",
        verbose_name="Texto do CTA"
    )
    cta_button_text = models.CharField(
        max_length=50,
        default="Fale Conosco",
        verbose_name="Texto do botão"
    )
    cta_button_url = models.URLField(
        blank=True,
        verbose_name="URL do botão",
        help_text="Deixe em branco para usar a página de contato"
    )
    
    content_panels = Page.content_panels + [
        FieldPanel('company'),
        FieldPanel('additional_content'),
        MultiFieldPanel([
            FieldPanel('cta_title'),
            FieldPanel('cta_text'),
            FieldPanel('cta_button_text'),
            FieldPanel('cta_button_url'),
        ], heading="Call to Action"),
    ]
    
    def get_context(self, request):
        context = super().get_context(request)
        context['company'] = self.company
        return context
    
    def save(self, *args, **kwargs):
        # Auto-generate slug based on company name
        if not self.slug and self.company:
            self.slug = self.company.slug
        super().save(*args, **kwargs)


@register_snippet
class Location(models.Model):
    """
    Modelo para localizações/escritórios da Kaizen
    """
    name = models.CharField(max_length=120, verbose_name="Nome da Unidade", default="Agência Kaizen")
    city = models.CharField(max_length=100, verbose_name="Cidade")
    state = models.CharField(max_length=2, verbose_name="UF", default="SP")
    address = models.TextField(verbose_name="Endereço completo")
    postal_code = models.CharField(max_length=12, blank=True, verbose_name="CEP")
    country = models.CharField(max_length=2, default="BR", verbose_name="País (ISO)")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Telefone")
    email = models.EmailField(blank=True, verbose_name="Email")
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, verbose_name="Latitude")
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, verbose_name="Longitude")
    maps_url = models.URLField(blank=True, verbose_name="URL do Google Maps")
    place_id = models.CharField(max_length=120, blank=True, verbose_name="Google Place ID")
    opening_hours = models.CharField(max_length=200, blank=True, verbose_name="Horário de funcionamento (ex: Mo-Fr 08:00-18:00)")
    is_main_office = models.BooleanField(default=False, verbose_name="Escritório principal")
    is_active = models.BooleanField(default=True, verbose_name="Ativo")
    order = models.PositiveIntegerField(default=0, verbose_name="Ordem de exibição")
    
    panels = [
        FieldPanel('name'),
        MultiFieldPanel([
            FieldPanel('city'),
            FieldPanel('state'),
            FieldPanel('address'),
            FieldPanel('postal_code'),
            FieldPanel('country'),
        ], heading="Endereço"),
        MultiFieldPanel([
            FieldPanel('phone'),
            FieldPanel('email'),
        ], heading="Contato"),
        MultiFieldPanel([
            FieldPanel('latitude'),
            FieldPanel('longitude'),
            FieldPanel('maps_url'),
            FieldPanel('place_id'),
            FieldPanel('opening_hours'),
        ], heading="Mapa / Google"),
        MultiFieldPanel([
            FieldPanel('is_main_office'),
            FieldPanel('is_active'),
            FieldPanel('order'),
        ], heading="Configurações"),
    ]
    
    class Meta:
        verbose_name = "Localização"
        verbose_name_plural = "Localizações"
        ordering = ['order', 'city']
    
    def __str__(self):
        return f"{self.city} - {self.address}"

    # Dados para JSON-LD LocalBusiness
    def jsonld(self, request=None):
        base = {
            "@context": "https://schema.org",
            "@type": "LocalBusiness",
            "@id": f"https://www.agenciakaizen.com.br/onde-estamos/#{self.city.lower().replace(' ', '-')}",
            "name": f"{self.name} - {self.city}",
            "description": "Agência Kaizen - Marketing Digital de Alta Performance.",
            "url": "https://www.agenciakaizen.com.br/onde-estamos/",
            "telephone": self.phone or "",
            "email": self.email or "contato@agenciakaizen.com.br",
            "logo": "https://www.agenciakaizen.com.br/static/images/logo-kaizen-header.webp",
            "image": "https://www.agenciakaizen.com.br/static/images/logo-kaizen-header.webp",
            "address": {
                "@type": "PostalAddress",
                "streetAddress": self.address,
                "addressLocality": self.city,
                "addressRegion": self.state,
                "postalCode": self.postal_code or "",
                "addressCountry": self.country,
            },
        }
        if self.latitude and self.longitude:
            base["geo"] = {
                "@type": "GeoCoordinates",
                "latitude": float(self.latitude),
                "longitude": float(self.longitude),
            }
        if self.opening_hours:
            base["openingHours"] = self.opening_hours
        return base


class LocationPage(Page):
    """
    Página "Onde Estamos" com localizações da Kaizen
    """
    # Hero Section
    hero_title = models.CharField(
        max_length=200, 
        default="Presença forte. Crescimento sem limites.",
        verbose_name="Título principal"
    )
    hero_subtitle = RichTextField(
        default="<p>Estamos nas principais regiões do Brasil levando estratégias de alto performance para empresas que querem acelerar. Desde que você esteja, a Kaizen está pronta para impulsionar seu negócio.</p>",
        verbose_name="Subtítulo principal"
    )
    
    # Seção de localizações
    locations_title = models.CharField(
        max_length=200, 
        default="Se sua meta é crescer, nós estamos por perto.",
        verbose_name="Título das localizações"
    )
    locations_subtitle = models.CharField(
        max_length=200, 
        default="Nossas experiências",
        verbose_name="Subtítulo das localizações"
    )
    
    # Seção de franquia
    franchise_title = models.CharField(
        max_length=200, 
        default="Acelere negócios. Expanda com a Kaizen.",
        verbose_name="Título da franquia"
    )
    franchise_subtitle = models.CharField(
        max_length=200, 
        default="SEJA DONO DA SUA PRÓPRIA BASE DE LANÇAMENTO",
        verbose_name="Subtítulo da franquia"
    )
    franchise_text = RichTextField(
        default="<p>A Kaizen não é apenas uma agência, é um modelo de negócio que funciona. Com mais de 15 anos de experiência e resultados comprovados, oferecemos a oportunidade de se tornar um franqueado e replicar nosso sucesso em sua região.</p><p>Nossa metodologia exclusiva, suporte completo e marca reconhecida no mercado garantem que você tenha todas as ferramentas necessárias para acelerar negócios e construir uma base sólida de crescimento.</p>",
        verbose_name="Texto da franquia"
    )
    franchise_button_text = models.CharField(
        max_length=100, 
        default="Quero saber mais sobre a franquia Kaizen",
        verbose_name="Texto do botão da franquia"
    )
    
    # Seção de benefícios da franquia
    benefits_title = models.CharField(
        max_length=200, 
        default="Por que se tornar um franqueado Kaizen?",
        verbose_name="Título dos benefícios"
    )
    
    # Seção de modelos de franquia
    models_title = models.CharField(
        max_length=200, 
        default="Se você quer empreender no mercado de marketing e vendas com um modelo de negócios sólido, esta é a sua chance.",
        verbose_name="Título dos modelos"
    )
    models_subtitle = models.CharField(
        max_length=200, 
        default="Expansão estratégica com alto performance: conheça nossos modelos de franquia",
        verbose_name="Subtítulo dos modelos"
    )
    
    # Seção de investimento
    investment_title = models.CharField(
        max_length=200, 
        default="Acesso exclusivo e investimento sólido",
        verbose_name="Título do investimento"
    )
    investment_text = RichTextField(
        default="<p>Ser um franqueado Kaizen significa ter acesso exclusivo a nossa metodologia comprovada, treinamento especializado e suporte contínuo. Investimos em cada unidade para garantir que você tenha todas as ferramentas necessárias para o sucesso.</p><p>Nossa equipe de especialistas está sempre disponível para apoiar seu crescimento e garantir que você alcance os melhores resultados possíveis.</p>",
        verbose_name="Texto do investimento"
    )
    
    # Seção de depoimentos
    testimonials_title = models.CharField(
        max_length=200, 
        default="Veja o que dizem nossos franqueados",
        verbose_name="Título dos depoimentos"
    )
    
    # Seção de contato
    contact_title = models.CharField(
        max_length=200, 
        default="Expanda. Cresça. Conquiste. Entre para o time Kaizen.",
        verbose_name="Título do contato"
    )
    contact_subtitle = models.CharField(
        max_length=200, 
        default="Preencha o formulário e fale com nosso time de expansão.",
        verbose_name="Subtítulo do contato"
    )
    
    # SEO
    meta_description = models.TextField(
        max_length=160,
        blank=True,
        help_text="Descrição para SEO (máximo 160 caracteres)"
    )
    
    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('hero_title'),
            FieldPanel('hero_subtitle'),
        ], heading="Hero Section"),
        MultiFieldPanel([
            FieldPanel('locations_title'),
            FieldPanel('locations_subtitle'),
        ], heading="Localizações"),
        MultiFieldPanel([
            FieldPanel('franchise_title'),
            FieldPanel('franchise_subtitle'),
            FieldPanel('franchise_text'),
            FieldPanel('franchise_button_text'),
        ], heading="Franquia"),
        MultiFieldPanel([
            FieldPanel('benefits_title'),
        ], heading="Benefícios"),
        MultiFieldPanel([
            FieldPanel('models_title'),
            FieldPanel('models_subtitle'),
        ], heading="Modelos de Franquia"),
        MultiFieldPanel([
            FieldPanel('investment_title'),
            FieldPanel('investment_text'),
        ], heading="Investimento"),
        MultiFieldPanel([
            FieldPanel('testimonials_title'),
        ], heading="Depoimentos"),
        MultiFieldPanel([
            FieldPanel('contact_title'),
            FieldPanel('contact_subtitle'),
        ], heading="Contato"),
    ]
    
    promote_panels = [
        MultiFieldPanel([
            FieldPanel('meta_description'),
        ], heading="SEO"),
    ]
    
    def get_context(self, request):
        context = super().get_context(request)
        context['locations'] = Location.objects.filter(is_active=True).order_by('order', 'city')
        return context


class FluxoPage(Page):
    """
    Página específica da Fluxo - Automação + CRM
    """
    # Hero Section
    hero_title = models.CharField(
        max_length=200,
        default="Potencialize suas vendas com automação + CRM",
        verbose_name="Título principal"
    )
    hero_subtitle = models.CharField(
        max_length=200,
        default="Menos esforço. Mais conversões. Gestão otimizada.",
        verbose_name="Subtítulo principal"
    )
    hero_description = RichTextField(
        default="<p>Integre automação de vendas e CRM em uma única solução. Transforme leads em clientes de forma automática e eficiente, com controle total sobre seu funil de vendas.</p>",
        verbose_name="Descrição do hero"
    )
    hero_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="Imagem do hero"
    )
    
    # Seção de Problemas
    problem_title = models.CharField(
        max_length=200,
        default="Você sabe quanto tempo e dinheiro está perdendo?",
        verbose_name="Título dos problemas"
    )
    problem_text = RichTextField(
        default="<p>Se a sua empresa enfrenta esses desafios, está na hora de transformar seu processo comercial.</p><p>Com o Fluxo, você automatiza suas vendas e estrutura um CRM eficiente para acelerar seus resultados.</p>",
        verbose_name="Texto dos problemas"
    )
    
    # Seção de Solução
    solution_title = models.CharField(
        max_length=200,
        default="Fluxo: Automação inteligente para sua empresa crescer",
        verbose_name="Título da solução"
    )
    solution_description = RichTextField(
        default="<p>O Fluxo da Kaizen é uma solução completa de automação comercial + CRM, criada para empresas que querem crescer sem perder controle sobre seus processos.</p>",
        verbose_name="Descrição da solução"
    )
    solution_conclusion = RichTextField(
        default="<p>Esqueça planilhas e processos manuais. Com o Fluxo, sua empresa opera no piloto automático e foca no que realmente importa: vender mais!</p>",
        verbose_name="Conclusão da solução"
    )
    
    # Seção de Benefícios
    benefits_title = models.CharField(
        max_length=200,
        default="Empresas que implementam automação de vendas e CRM têm:",
        verbose_name="Título dos benefícios"
    )
    benefits_conclusion = RichTextField(
        default="<p>Chegou a hora de estruturar sua operação comercial e escalar suas vendas.</p>",
        verbose_name="Conclusão dos benefícios"
    )
    
    # Seção Como Funciona
    how_it_works_title = models.CharField(
        max_length=200,
        default="Como Funciona?",
        verbose_name="Título como funciona"
    )
    how_it_works_conclusion = RichTextField(
        default="<p>Chegou a hora de estruturar sua operação comercial e escalar suas vendas.</p>",
        verbose_name="Conclusão como funciona"
    )
    
    # Seção FAQ
    faq_title = models.CharField(
        max_length=200,
        default="Perguntas frequentes",
        verbose_name="Título FAQ"
    )
    
    # Seção Kaizen
    kaizen_title = RichTextField(
        default="<p>A Kaizen é referência em estratégias de automação de marketing e vendas, ajudando empresas a estruturar processos eficientes e previsíveis.</p>",
        verbose_name="Título Kaizen"
    )
    kaizen_conclusion = RichTextField(
        default="<p>Vamos transformar sua operação comercial? Entre em contato agora!</p>",
        verbose_name="Conclusão Kaizen"
    )
    
    # Seção Final CTA
    final_cta_title = models.CharField(
        max_length=200,
        default="Não fique para trás! Empresas que automatizam suas vendas crescem mais rápido e com previsibilidade.",
        verbose_name="Título CTA final"
    )
    final_cta_subtitle = models.CharField(
        max_length=200,
        default="Preencha o formulário e descubra como transformar sua operação comercial!",
        verbose_name="Subtítulo CTA final"
    )
    
    # SEO
    meta_description = models.TextField(
        max_length=160,
        default="Fluxo: Solução completa de automação comercial + CRM da Kaizen. Automatize suas vendas, qualifique leads e acelere conversões.",
        help_text="Descrição para SEO (máximo 160 caracteres)"
    )
    
    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('hero_title'),
            FieldPanel('hero_subtitle'),
            FieldPanel('hero_description'),
            FieldPanel('hero_image'),
        ], heading="Hero Section"),
        MultiFieldPanel([
            FieldPanel('problem_title'),
            FieldPanel('problem_text'),
        ], heading="Seção de Problemas"),
        MultiFieldPanel([
            FieldPanel('solution_title'),
            FieldPanel('solution_description'),
            FieldPanel('solution_conclusion'),
        ], heading="Seção de Solução"),
        MultiFieldPanel([
            FieldPanel('benefits_title'),
            FieldPanel('benefits_conclusion'),
        ], heading="Seção de Benefícios"),
        MultiFieldPanel([
            FieldPanel('how_it_works_title'),
            FieldPanel('how_it_works_conclusion'),
        ], heading="Como Funciona"),
        MultiFieldPanel([
            FieldPanel('faq_title'),
        ], heading="FAQ"),
        MultiFieldPanel([
            FieldPanel('kaizen_title'),
            FieldPanel('kaizen_conclusion'),
        ], heading="Seção Kaizen"),
        MultiFieldPanel([
            FieldPanel('final_cta_title'),
            FieldPanel('final_cta_subtitle'),
        ], heading="CTA Final"),
    ]
    
    promote_panels = [
        MultiFieldPanel([
            FieldPanel('meta_description'),
        ], heading="SEO"),
    ]
    
    def get_context(self, request):
        context = super().get_context(request)
        return context