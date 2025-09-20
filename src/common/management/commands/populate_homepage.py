from django.core.management.base import BaseCommand
from home.models import HomePage
from wagtail.blocks import StreamValue


class Command(BaseCommand):
    help = "Popula a HomePage com blocos de conteúdo básicos"

    def handle(self, *args, **options):
        try:
            # Buscar HomePage
            hp = HomePage.objects.live().first()
            if not hp:
                self.stdout.write(self.style.ERROR("Nenhuma HomePage encontrada!"))
                return

            # Limpar blocos existentes
            hp.body = []
            hp.save()

            # Criar blocos básicos
            blocks_data = [
                ('results_section', {
                    'title': 'Resultados que não cabem em promessas',
                    'subtitle': 'Nós entregamos performance de verdade. Confira alguns dos nossos resultados:',
                    'results': [
                        {
                            'title': '1500+',
                            'description': 'Projetos entregues',
                            'icon': 'fas fa-rocket'
                        },
                        {
                            'title': '500+',
                            'description': 'Clientes satisfeitos',
                            'icon': 'fas fa-users'
                        },
                        {
                            'title': '15 anos',
                            'description': 'De experiência',
                            'icon': 'fas fa-calendar'
                        },
                        {
                            'title': 'R$ 50M+',
                            'description': 'Em vendas geradas',
                            'icon': 'fas fa-dollar-sign'
                        }
                    ]
                }),
                ('solutions_section', {
                    'title': 'Nossas Soluções',
                    'subtitle': 'Estratégias personalizadas para acelerar seu negócio',
                    'solutions': [
                        {
                            'title': 'Marketing Digital',
                            'description': 'Estratégias completas para maximizar seus resultados',
                            'icon': 'fas fa-bullhorn'
                        },
                        {
                            'title': 'Geração de Leads',
                            'description': 'Sistema automatizado para capturar oportunidades',
                            'icon': 'fas fa-magnet'
                        },
                        {
                            'title': 'Consultoria SEO',
                            'description': 'Posicionamento orgânico no Google',
                            'icon': 'fas fa-search'
                        }
                    ]
                }),
                ('cta_section', {
                    'title': 'Pronto para acelerar seu negócio?',
                    'subtitle': 'Fale com nossos especialistas e descubra como podemos ajudar',
                    'phone': '0800-550-8000',
                    'whatsapp_text': 'Olá! Vim pelo site da Agência Kaizen e gostaria de saber mais sobre os serviços.'
                })
            ]

            # Adicionar blocos usando StreamValue
            stream_value = StreamValue(hp.body.stream_block, blocks_data)
            hp.body = stream_value
            hp.save()

            self.stdout.write(
                self.style.SUCCESS(f"HomePage '{hp.title}' populada com {len(blocks_data)} blocos!")
            )
            self.stdout.write("Blocos adicionados:")
            for block_type, block_value in blocks_data:
                self.stdout.write(f"  - {block_type}: {block_value['title']}")

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Erro ao popular HomePage: {e}"))
