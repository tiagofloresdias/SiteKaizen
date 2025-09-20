from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.search import index
from wagtail.blocks import CharBlock, RichTextBlock, StructBlock, ListBlock, TextBlock, URLBlock
from wagtail.images.blocks import ImageChooserBlock
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from companies.models import Location


# Blocos para StreamField
class HeroBlock(StructBlock):
    """Bloco para seção Hero"""
    title = CharBlock(max_length=255, label="Título Principal")
    subtitle = RichTextBlock(label="Subtítulo")
    background_image = ImageChooserBlock(required=False, label="Imagem de Fundo")
    cta_text = CharBlock(max_length=100, default="Quero Vender +", label="Texto do Botão")
    cta_url = CharBlock(max_length=255, default="/contato/", label="URL do Botão")

class AboutBlock(StructBlock):
    """Bloco para seção Sobre"""
    title = CharBlock(max_length=255, label="Título")
    text = RichTextBlock(label="Texto")
    image = ImageChooserBlock(required=False, label="Imagem")
    cta_text = CharBlock(max_length=100, default="Nossos Clientes", label="Texto do Botão")
    cta_url = CharBlock(max_length=255, default="/portfolio/", label="URL do Botão")

class ResultCardBlock(StructBlock):
    """Bloco para card de resultado"""
    title = CharBlock(max_length=255, label="Título")
    description = CharBlock(max_length=500, label="Descrição")
    icon = CharBlock(max_length=100, default="fas fa-chart-line", label="Ícone FontAwesome")

class ResultsBlock(StructBlock):
    """Bloco para seção de resultados"""
    title = CharBlock(max_length=255, label="Título da Seção")
    subtitle = CharBlock(max_length=500, label="Subtítulo")
    results = ListBlock(ResultCardBlock, label="Cards de Resultados")
    class Meta:
        template = "home/blocks/results_block.html"

class SolutionCardBlock(StructBlock):
    """Bloco para card de solução"""
    title = CharBlock(max_length=255, label="Título")
    description = CharBlock(max_length=500, label="Descrição")
    icon = CharBlock(max_length=100, default="fas fa-rocket", label="Ícone FontAwesome")

class SolutionsBlock(StructBlock):
    """Bloco para seção de soluções"""
    title = CharBlock(max_length=255, label="Título da Seção")
    subtitle = CharBlock(max_length=500, label="Subtítulo")
    solutions = ListBlock(SolutionCardBlock, label="Cards de Soluções", required=False)
    class Meta:
        template = "home/blocks/solutions_block.html"


class ClientsCarouselBlock(StructBlock):
    """Carrossel de logos de clientes (puxa do snippet Company)"""
    title = CharBlock(max_length=255, default="Marcas que confiam", label="Título")
    class Meta:
        template = "home/blocks/clients_carousel_block.html"

class CompetenceCardBlock(StructBlock):
    """Bloco para card de competência"""
    title = CharBlock(max_length=255, label="Título")
    icon = CharBlock(max_length=100, default="fas fa-bullseye", label="Ícone FontAwesome")

class CompetencesBlock(StructBlock):
    """Bloco para seção de competências"""
    title = CharBlock(max_length=255, label="Título da Seção")
    competences = ListBlock(CompetenceCardBlock, label="Cards de Competências")
    class Meta:
        template = "home/blocks/competences_block.html"

class CTABlock(StructBlock):
    """Bloco para call-to-action"""
    title = CharBlock(max_length=255, label="Título")
    subtitle = CharBlock(max_length=500, label="Subtítulo")
    phone = CharBlock(max_length=50, default="0800-550-8000", label="Telefone")
    whatsapp_text = CharBlock(max_length=200, default="Olá! Vim pelo site da Agência Kaizen e gostaria de saber mais sobre os serviços.", label="Texto do WhatsApp")
    class Meta:
        template = "home/blocks/cta_block.html"

# ===== Blocos adicionais para AboutPage =====
class MetricBlock(StructBlock):
    """Métrica com contagem animada"""
    value = CharBlock(max_length=20, label="Valor alvo (ex: 1500)")
    suffix = CharBlock(max_length=10, required=False, label="Sufixo (ex: +, %)")
    label = CharBlock(max_length=80, label="Legenda")
    icon = CharBlock(max_length=100, default="fas fa-check-circle", label="Ícone FontAwesome")


class MetricsBlock(StructBlock):
    title = CharBlock(max_length=255, default="Resultados que não cabem em promessas", label="Título")
    metrics = ListBlock(MetricBlock, label="Métricas")


class CEOSocialLinkBlock(StructBlock):
    platform = CharBlock(max_length=30, label="Plataforma (ex: linkedin)")
    url = URLBlock(label="URL")


class CEOBlock(StructBlock):
    name = CharBlock(max_length=120, default="CEO", label="Nome")
    role = CharBlock(max_length=120, default="Chief Executive Officer", label="Cargo")
    photo = ImageChooserBlock(required=False, label="Foto")
    bio = RichTextBlock(required=False, label="Bio curta")
    social = ListBlock(CEOSocialLinkBlock, required=False, label="Links sociais")


class ValueCardBlock(StructBlock):
    icon = CharBlock(max_length=100, default="fas fa-rocket", label="Ícone")
    title = CharBlock(max_length=120, label="Título")
    text = TextBlock(label="Texto")


class ValuesBlock(StructBlock):
    title = CharBlock(max_length=255, default="Nossos valores", label="Título")
    values = ListBlock(ValueCardBlock, label="Valores")


class UnitCardBlock(StructBlock):
    icon = CharBlock(max_length=100, default="fas fa-building", label="Ícone")
    title = CharBlock(max_length=120, label="Título")
    description = TextBlock(label="Descrição")
    url = URLBlock(required=False, label="URL do Card")


class UnitsBlock(StructBlock):
    title = CharBlock(max_length=255, default="Unidades de negócio", label="Título")
    subtitle = CharBlock(max_length=500, required=False, label="Subtítulo")
    units = ListBlock(UnitCardBlock, label="Cards")

class HomePage(Page):
    """
    Página inicial da agência com seções dinâmicas
    """
    # Seção Hero
    hero_title = models.CharField(max_length=255, verbose_name="Título Principal", default="Aceleramos negócios e lançamos foguetes")
    hero_subtitle = RichTextField(blank=True, verbose_name="Subtítulo", default="<p>Desde 2014, ajudamos empresas a crescer com estratégias afiadas, dados precisos e um time de elite. Se sua meta é escalar, nós temos o combustível.</p>")
    hero_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="Imagem Hero"
    )
    
    # Seção Sobre
    about_title = models.CharField(max_length=255, blank=True, verbose_name="Título Sobre", default="Somos uma aceleradora de vendas.")
    about_text = RichTextField(blank=True, verbose_name="Texto Sobre", default="<p>Com processos, metodologia e execução prática, ajudamos empresas a crescer de forma sustentável e escalável.</p>")
    about_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="Imagem Sobre"
    )
    
    # StreamField para seções dinâmicas
    body = StreamField([
        ('results_section', ResultsBlock(label="Seção de Resultados")),
        ('solutions_section', SolutionsBlock(label="Seção de Soluções")),
        ('competences_section', CompetencesBlock(label="Seção de Competências")),
        ('clients_carousel', ClientsCarouselBlock(label="Carrossel de Clientes")),
        ('cta_section', CTABlock(label="Seção de Call-to-Action")),
    ], blank=True, use_json_field=True, verbose_name="Seções da Página")
    
    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('hero_title'),
            FieldPanel('hero_subtitle'),
            FieldPanel('hero_image'),
        ], heading="Seção Hero"),
        MultiFieldPanel([
            FieldPanel('about_title'),
            FieldPanel('about_text'),
            FieldPanel('about_image'),
        ], heading="Seção Sobre"),
        FieldPanel('body'),
    ]

    template = "home/home_page.html"
    
    search_fields = Page.search_fields + [
        index.SearchField('hero_title'),
        index.SearchField('hero_subtitle'),
        index.SearchField('about_text'),
        index.SearchField('body'),
    ]

    def get_context(self, request):
        from solutions.models import SolutionSection
        from companies.models import Company
        context = super().get_context(request)
        context['sections'] = SolutionSection.objects.filter(is_active=True).order_by('order')
        context['companies'] = Company.objects.filter(is_active=True).order_by('order', 'name')
        return context


class AboutPage(Page):
    """
    Página Quem Somos da agência
    """
    hero_title = models.CharField(
        max_length=255,
        default="Aqui, só decola quem está pronto para voar mais alto.",
        verbose_name="Título Principal"
    )
    hero_subtitle = RichTextField(
        default="Desde 2015, a Kaizen não segue o mercado. Ela acelera, transforma e redefine as regras do jogo. Mais do que uma agência, somos uma aceleradora de vendas que entrega crescimento real. Se o objetivo é escalar, somos o combustível.",
        verbose_name="Subtítulo Principal"
    )
    hero_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="Imagem de Fundo do Hero"
    )
    
    # Seção de Resultados
    results_title = models.CharField(
        max_length=255,
        default="Resultados que não cabem em promessas",
        verbose_name="Título da Seção de Resultados"
    )
    results_subtitle = models.TextField(
        default="Nós entregamos performance de verdade. Confira alguns dos nossos resultados:",
        verbose_name="Subtítulo da Seção de Resultados"
    )
    
    # Métricas (count-up)
    metrics_block = StreamField([
        ("metrics", MetricsBlock()),
    ], blank=True, use_json_field=True, verbose_name="Seção de Métricas")

    # CEO + Missão/Propósito
    ceo = StreamField([
        ("ceo", CEOBlock()),
    ], blank=True, use_json_field=True, verbose_name="Seção CEO")
    mission_title = models.CharField(max_length=255, default="Nossa missão e propósito", blank=True)
    mission_text = RichTextField(blank=True)

    # Valores
    values_block = StreamField([
        ("values", ValuesBlock()),
    ], blank=True, use_json_field=True, verbose_name="Valores")

    # Unidades de negócio / Produtos
    units_block = StreamField([
        ("units", UnitsBlock()),
    ], blank=True, use_json_field=True, verbose_name="Unidades de Negócio")

    # CTA final
    final_cta_title = models.CharField(max_length=255, default="Pronto para decolar?", blank=True)
    final_cta_subtitle = models.CharField(max_length=500, blank=True, default="Vamos acelerar seu crescimento com método e performance.")
    final_cta_button_text = models.CharField(max_length=80, default="FALAR COM ESPECIALISTA")
    final_cta_button_url = models.CharField(max_length=255, default="/contato/")

    # Seção História
    history_title = models.CharField(
        max_length=255,
        default="Conheça nossa história",
        verbose_name="Título da Seção de História"
    )
    history_text = RichTextField(
        blank=True,
        verbose_name="Texto da História"
    )
    
    # Seção Time
    team_title = models.CharField(
        max_length=255,
        default="Apenas os melhores jogam no nosso time.",
        verbose_name="Título da Seção do Time"
    )
    team_text = RichTextField(
        blank=True,
        verbose_name="Texto da Seção do Time"
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
            FieldPanel('hero_image'),
        ], heading="Hero Section"),
        MultiFieldPanel([
            FieldPanel('results_title'),
            FieldPanel('results_subtitle'),
        ], heading="Seção de Resultados"),
        MultiFieldPanel([
            FieldPanel('history_title'),
            FieldPanel('history_text'),
        ], heading="Seção de História"),
        MultiFieldPanel([
            FieldPanel('team_title'),
            FieldPanel('team_text'),
        ], heading="Seção do Time"),
        MultiFieldPanel([
            FieldPanel('metrics_block'),
        ], heading="Seção de Métricas"),
        MultiFieldPanel([
            FieldPanel('ceo'),
            FieldPanel('mission_title'),
            FieldPanel('mission_text'),
        ], heading="Seção CEO & Missão"),
        MultiFieldPanel([
            FieldPanel('values_block'),
        ], heading="Valores"),
        MultiFieldPanel([
            FieldPanel('units_block'),
        ], heading="Unidades de Negócio"),
        MultiFieldPanel([
            FieldPanel('final_cta_title'),
            FieldPanel('final_cta_subtitle'),
            FieldPanel('final_cta_button_text'),
            FieldPanel('final_cta_button_url'),
        ], heading="CTA Final"),
    ]
    
    promote_panels = [
        MultiFieldPanel([
            FieldPanel('meta_description'),
            FieldPanel('meta_keywords'),
        ], heading="SEO"),
    ]
    
    search_fields = Page.search_fields + [
        index.SearchField('hero_title'),
        index.SearchField('hero_subtitle'),
        index.SearchField('results_title'),
        index.SearchField('history_text'),
        index.SearchField('team_text'),
        index.SearchField('mission_text'),
    ]
    
    template = "about/about_page.html"
    
    class Meta:
        verbose_name = "Página Quem Somos"
        verbose_name_plural = "Páginas Quem Somos"

class OfficeBlock(StructBlock):
    """Bloco de escritório para a página Onde Estamos"""
    name = CharBlock(max_length=100, label="Cidade/Unidade")
    address = TextBlock(label="Endereço (linhas com <br>)")
    phone = CharBlock(max_length=50, label="Telefone (com DDD)")
    map_url = URLBlock(label="URL do Google Maps")


class BenefitBlock(StructBlock):
    """Benefício/razão para franquia"""
    title = CharBlock(max_length=120, label="Título")
    description = TextBlock(label="Descrição")


class FranchiseBlock(StructBlock):
    """Opção de franquia apresentada na página"""
    title = CharBlock(max_length=150, label="Título")
    description = TextBlock(label="Descrição")
    cta_text = CharBlock(max_length=80, default="QUERO MAIS INFORMAÇÕES", label="Texto do Botão")
    cta_url = CharBlock(max_length=255, default="/contato/", label="URL do Botão")


class TestimonialBlock(StructBlock):
    """Depoimentos"""
    quote = TextBlock(label="Citação")
    author = CharBlock(max_length=120, label="Autor")
    role = CharBlock(max_length=120, label="Cargo/Unidade", required=False)


class OndeEstamosPage(Page):
    """
    Página "Onde Estamos" com conteúdo totalmente gerenciável via Wagtail,
    mantendo o layout original do site.
    """

    # Hero
    hero_title = models.CharField(
        max_length=255,
        default="Presença forte.\nCrescimento sem limites.",
        verbose_name="Título Principal (Hero)"
    )
    hero_subtitle = RichTextField(
        default=(
            "Com escritórios estrategicamente posicionados nas principais capitais do Brasil, "
            "estamos próximos aos nossos clientes. Onde quer que você esteja, a Kaizen está "
            "pronta para acelerar seu negócio."
        ),
        verbose_name="Subtítulo do Hero"
    )

    # Escritórios
    offices = StreamField(
        [
            ("office", OfficeBlock()),
        ],
        blank=True,
        use_json_field=True,
        verbose_name="Escritórios"
    )

    # CTA telefone
    cta_phone = models.CharField(
        max_length=50,
        default="0800-550-8000",
        verbose_name="Telefone CTA"
    )

    # Seção Acelere/Expansão
    expansion_title = models.CharField(
        max_length=255,
        default="Acelere negócios.\nExpanda com a Kaizen.",
        verbose_name="Título da Seção de Expansão"
    )
    expansion_text_1 = RichTextField(
        default=(
            "A Kaizen é mais que uma agência. É uma aceleradora de negócios com presença nacional "
            "e metodologia comprovada. Nossos escritórios não são apenas endereços, são centros de "
            "inovação onde estratégias se transformam em resultados."
        ),
        verbose_name="Texto 1 da Seção de Expansão"
    )
    expansion_text_2 = RichTextField(
        default=(
            "Seja qual for sua cidade, nossa expertise é sua grande aliada para escalar vendas, "
            "otimizar processos e transformar seu negócio em uma máquina de crescimento."
        ),
        verbose_name="Texto 2 da Seção de Expansão"
    )
    expansion_cta_text = models.CharField(
        max_length=80,
        default="QUERO MAIS SOBRE A EXPANSÃO KAIZEN",
        verbose_name="Texto do Botão (Expansão)"
    )
    expansion_cta_url = models.CharField(
        max_length=255,
        default="/contato/",
        verbose_name="URL do Botão (Expansão)"
    )

    # Benefícios Franquia
    franchise_title = models.CharField(
        max_length=255,
        default="Por que se tornar um franqueado Kaizen?",
        verbose_name="Título Benefícios Franquia"
    )
    franchise_benefits = StreamField(
        [
            ("benefit", BenefitBlock()),
        ],
        blank=True,
        use_json_field=True,
        verbose_name="Benefícios"
    )

    # Opções de franquia
    franchises = StreamField(
        [
            ("franchise", FranchiseBlock()),
        ],
        blank=True,
        use_json_field=True,
        verbose_name="Opções de Franquia"
    )

    # Seção Acesso/Investimento
    access_title = models.CharField(
        max_length=255,
        default="Acesso exclusivo e\ninvestimento sólido",
        verbose_name="Título Seção Acesso"
    )
    access_text = RichTextField(
        blank=True,
        verbose_name="Texto Seção Acesso"
    )
    access_cta_text = models.CharField(
        max_length=80,
        default="QUERO SABER MAIS",
        verbose_name="Texto do Botão (Acesso)"
    )
    access_cta_url = models.CharField(
        max_length=255,
        default="/contato/",
        verbose_name="URL do Botão (Acesso)"
    )

    # Depoimentos
    testimonials = StreamField(
        [
            ("testimonial", TestimonialBlock()),
        ],
        blank=True,
        use_json_field=True,
        verbose_name="Depoimentos"
    )

    # CTA final
    final_cta_title = models.CharField(
        max_length=255,
        default="Expanda. Cresça. Conquiste. Entre para o time Kaizen.",
        verbose_name="Título CTA Final"
    )
    final_cta_text = RichTextField(
        blank=True,
        default=(
            "Pronto para fazer parte de um dos grupos que mais cresce no Brasil? "
            "Preencha o formulário e descubra como se tornar um franqueado Kaizen."
        ),
        verbose_name="Texto CTA Final"
    )
    show_interest_form = models.BooleanField(default=True, verbose_name="Exibir formulário de interesse")

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel("hero_title"),
            FieldPanel("hero_subtitle"),
        ], heading="Hero"),
        MultiFieldPanel([
            FieldPanel("offices"),
        ], heading="Escritórios"),
        MultiFieldPanel([
            FieldPanel("cta_phone"),
        ], heading="CTA Telefone"),
        MultiFieldPanel([
            FieldPanel("expansion_title"),
            FieldPanel("expansion_text_1"),
            FieldPanel("expansion_text_2"),
            FieldPanel("expansion_cta_text"),
            FieldPanel("expansion_cta_url"),
        ], heading="Seção Expansão"),
        MultiFieldPanel([
            FieldPanel("franchise_title"),
            FieldPanel("franchise_benefits"),
        ], heading="Benefícios Franquia"),
        MultiFieldPanel([
            FieldPanel("franchises"),
        ], heading="Opções de Franquia"),
        MultiFieldPanel([
            FieldPanel("access_title"),
            FieldPanel("access_text"),
            FieldPanel("access_cta_text"),
            FieldPanel("access_cta_url"),
        ], heading="Seção Acesso/Investimento"),
        MultiFieldPanel([
            FieldPanel("testimonials"),
        ], heading="Depoimentos"),
        MultiFieldPanel([
            FieldPanel("final_cta_title"),
            FieldPanel("final_cta_text"),
            FieldPanel("show_interest_form"),
        ], heading="CTA Final"),
    ]

    template = "about/onde_estamos_page.html"

    def get_context(self, request):
        context = super().get_context(request)
        context["locations"] = Location.objects.filter(is_active=True).order_by("order", "city")
        return context

    class Meta:
        verbose_name = "Página Onde Estamos"
        verbose_name_plural = "Páginas Onde Estamos"
