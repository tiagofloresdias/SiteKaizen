from django.shortcuts import render
from .models import UniversidadeKaizenPage, Expert, Curso

def universidade_kaizen_page(request):
    """
    View para a página da Universidade Kaizen
    """
    try:
        page = UniversidadeKaizenPage.objects.filter(slug='universidade-kaizen', live=True).first()
        
        if not page:
            # Se a página não existir, cria uma com conteúdo padrão
            from wagtail.models import Page
            root_page = Page.objects.filter(slug='home').first()
            if root_page:
                page = UniversidadeKaizenPage(
                    title="Universidade Kaizen",
                    slug="universidade-kaizen",
                    live=True,
                    hero_title="<span class='text-pink'>Universidade Kaizen</span>",
                    hero_subtitle="Evolução contínua para performance máxima",
                    hero_description="O conhecimento certo pode transformar qualquer negócio. Na Universidade Kaizen, você tem acesso ao que há de mais avançado em marketing digital, vendas e estratégias de crescimento.",
                    hero_cta_text="QUERO PARTICIPAR",
                    about_title="Por que a Universidade Kaizen?",
                    about_description="Aqui, você encontra cursos gratuitos e trilhas completas ministradas pelos maiores especialistas do mercado. Conteúdo prático, atualizado e focado em resultados reais.",
                    advantages_title="O que você vai encontrar",
                    experts_title="Conheça nossos especialistas",
                    experts_subtitle="Aprenda com os melhores profissionais do mercado",
                    cursos_title="Cursos Disponíveis",
                    cursos_subtitle="Conteúdo prático e atualizado para acelerar seu crescimento",
                    final_cta_title="Pronto para <span class='text-pink'>Evoluir</span> seu Conhecimento?",
                    final_cta_subtitle="Junte-se a milhares de profissionais que já transformaram seus negócios com a Universidade Kaizen.",
                    final_cta_button_text="COMEÇAR AGORA",
                    custom_seo_title="Universidade Kaizen - Evolução Contínua para Performance Máxima",
                    custom_seo_description="Aprenda com os maiores especialistas do mercado. Cursos gratuitos e trilhas completas em marketing digital, vendas e estratégias de crescimento."
                )
                root_page.add_child(instance=page)
                page.save_revision().publish()
    except Exception as e:
        # Fallback para página padrão
        page = None
    
    # Buscar experts e cursos
    experts = Expert.objects.all()[:6]  # Limitar a 6 experts
    cursos = Curso.objects.all()[:8]    # Limitar a 8 cursos
    
    return render(request, 'universidade/universidade_kaizen_page.html', {
        'page': page,
        'experts': experts,
        'cursos': cursos,
        'request': request,
    })

