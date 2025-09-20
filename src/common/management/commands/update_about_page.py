"""
Atualiza o conteúdo da AboutPage (Quem Somos) no Wagtail e publica
uma nova revisão. O comando é idempotente: cria a página via
`ensure_about_page` caso não exista.
"""

from django.core.management.base import BaseCommand
from django.db import transaction


class Command(BaseCommand):
    help = "Atualiza conteúdo padrão da página 'Quem Somos' (AboutPage) e publica revisão"

    @transaction.atomic
    def handle(self, *args, **options):
        # Garante que a página exista
        from django.core.management import call_command
        call_command("ensure_about_page")

        from home.models import AboutPage

        about = AboutPage.objects.filter(slug="quem-somos").first()
        if not about:
            self.stdout.write(self.style.ERROR("AboutPage não encontrada após ensure_about_page."))
            return

        # Conteúdos alinhados com o layout atual
        about.hero_title = (
            "Aqui, só decola quem está pronto para voar mais alto."
        )
        about.hero_subtitle = (
            "Desde 2015, a Kaizen não segue o mercado. Ela acelera, transforma e redefine as regras do jogo. "
            "Mais do que uma agência, somos uma aceleradora de vendas que entrega crescimento real. "
            "Se o objetivo é escalar, somos o combustível."
        )

        about.results_title = "Resultados que não cabem em promessas"
        about.results_subtitle = (
            "Nós entregamos performance de verdade. Confira alguns dos nossos resultados:"
        )

        about.history_title = "Conheça nossa história"
        # Texto rico resumido, o restante da timeline está no template visual
        about.history_text = (
            "<p>Em 2015, a Kaizen nasceu com uma visão ambiciosa: transformar estratégias digitais em máquinas de vendas previsíveis. "
            "Nosso primeiro grande teste veio rápido. Em poucos anos, uma única unidade de negócios da Kaizen já havia impulsionado mais de 200 empresas. "
            "A metodologia que criamos foi refinada, testada e comprovada – e hoje é a base do nosso DNA.</p>"
            "<p>Expandimos. Evoluímos. Hoje somos referência. Enquanto muitos intensificam o marketing, nós aceleramos a venda real. "
            "A cada companhia, a cada estratégia, otimizamos processos, gerando decisões mais assertivas e ciclos de melhoria contínua.</p>"
        )

        about.team_title = "Apenas os melhores jogam no nosso time."
        about.team_text = (
            "<p>Nosso time não é feito de especialistas. É feito de estrategistas. Cada profissional da Kaizen entra em campo para entregar resultados. "
            "Aqui, métricas de vaidade não existem. O que importa é o crescimento real.</p>"
            "<p>Se você quer ser mais um no mercado, este não é o seu lugar. Se busca crescimento de verdade, com método e execução afiada, então é com a gente.</p>"
        )

        # SEO básico
        about.meta_description = (
            "Quem Somos da Agência Kaizen: aceleradora de vendas e marketing de performance desde 2015."
        )
        about.meta_keywords = "agência kaizen, quem somos, aceleradora de vendas, marketing de performance"

        about.show_in_menus = True

        about.save()
        about.save_revision().publish()
        self.stdout.write(self.style.SUCCESS("Conteúdo da AboutPage atualizado e publicado."))


