from django.shortcuts import render
from django.views.generic import TemplateView
from .models import MidiaProgramaticaPage


class MidiaProgramaticaPageView(TemplateView):
    """
    View para a página de Mídia Programática
    """
    template_name = 'services/midia_programatica_page.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Buscar a página de Mídia Programática
        try:
            page = MidiaProgramaticaPage.objects.live().first()
            if not page:
                # Criar página padrão se não existir
                page = MidiaProgramaticaPage(
                    title="Mídia Programática Inteligente",
                    slug="midia-programatica",
                    hero_title="Mídia Programática <span class='text-pink'>Inteligente</span>",
                    hero_subtitle="Alcance seu público-alvo com precisão através de tecnologia avançada de programmatic advertising. Nossa plataforma utiliza inteligência artificial e big data para otimizar campanhas em tempo real.",
                    hero_cta_text="Solicitar Consultoria Gratuita",
                    tech_title="Tecnologia Avançada",
                    tech_description="Nossa plataforma utiliza inteligência artificial e big data para otimizar campanhas em tempo real, garantindo o máximo desempenho e ROI para seu negócio.",
                    channels_title="Canais de Mídia",
                    channels_subtitle="Cobertura completa em todos os pontos de contato com seu público.",
                    process_title="Como Trabalhamos",
                    process_subtitle="Processo estruturado para máxima eficiência e resultados.",
                    benefits_title="Por que Escolher Nossa Plataforma?",
                    final_cta_title="Pronto para <span class='text-white'>Revolucionar</span> sua Mídia Digital?",
                    final_cta_subtitle="Descubra como nossa plataforma de mídia programática pode transformar seus resultados digitais.",
                    final_cta_button_text="Solicitar Consultoria Gratuita",
                    final_cta_secondary_text="Ver Cases de Sucesso",
                    final_cta_secondary_url="/cases/",
                    meta_description="Mídia Programática Inteligente - Alcance seu público-alvo com precisão através de tecnologia avançada de programmatic advertising. Consultoria gratuita disponível."
                )
                page.save()
        except Exception as e:
            # Fallback para página padrão
            page = None
        
        context['page'] = page
        return context
