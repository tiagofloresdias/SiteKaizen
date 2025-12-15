from django.core.management.base import BaseCommand
from solutions.models import SolutionsPage, SolutionSection
from pages.models import StandardPage
from django.utils.text import slugify


class Command(BaseCommand):
    help = "Cria páginas individuais para cada seção de soluções"

    def handle(self, *args, **options):
        try:
            # Buscar a página Soluções
            solutions_page = SolutionsPage.objects.live().first()
            if not solutions_page:
                self.stdout.write(self.style.ERROR("Página 'Soluções' não encontrada!"))
                return

            # Seções de soluções existentes + Desenvolvimento de Sites
            sections_data = [
                {
                    'title': 'Desenvolvimento de Sites',
                    'subtitle': 'Sites modernos, responsivos e otimizados para conversão. Transformamos sua presença digital em uma máquina de vendas.',
                    'content': '''
                        <h2>Por que escolher a Kaizen para seu site?</h2>
                        <p>Desenvolvemos sites que não apenas impressionam, mas convertem visitantes em clientes. Nossa abordagem combina design moderno, performance otimizada e estratégias de conversão comprovadas.</p>
                        
                        <h3>Nossos diferenciais:</h3>
                        <ul>
                            <li><strong>Design Responsivo:</strong> Perfeito em qualquer dispositivo</li>
                            <li><strong>Performance Otimizada:</strong> Carregamento rápido e SEO-friendly</li>
                            <li><strong>Conversão Focada:</strong> Estratégias para maximizar vendas</li>
                            <li><strong>Suporte Contínuo:</strong> Manutenção e atualizações</li>
                        </ul>
                        
                        <h3>Tipos de sites que desenvolvemos:</h3>
                        <ul>
                            <li>Sites institucionais</li>
                            <li>E-commerce</li>
                            <li>Landing pages</li>
                            <li>Sites para profissionais</li>
                            <li>Portais corporativos</li>
                        </ul>
                    ''',
                    'order': 1
                },
                {
                    'title': 'Geração de Oportunidades de Venda',
                    'subtitle': 'Sistema completo para capturar, nutrir e converter leads qualificados em vendas reais.',
                    'content': '''
                        <h2>Sistema completo de geração de leads</h2>
                        <p>Transformamos visitantes em oportunidades de vendas através de estratégias personalizadas e automação inteligente.</p>
                    ''',
                    'order': 2
                },
                {
                    'title': 'Assessoria de Mídia Paga',
                    'subtitle': 'Maximize seu ROI com campanhas otimizadas no Google Ads, Facebook e outras plataformas.',
                    'content': '''
                        <h2>Gestão profissional de mídia paga</h2>
                        <p>Otimizamos suas campanhas para alcançar o público certo, no momento certo, com o melhor custo-benefício.</p>
                    ''',
                    'order': 3
                },
                {
                    'title': 'Branding',
                    'subtitle': 'Construa uma marca forte e memorável que conecta com seu público e gera autoridade.',
                    'content': '''
                        <h2>Desenvolvimento de marca estratégico</h2>
                        <p>Criamos identidades visuais que comunicam valores, diferenciação e propósito da sua empresa.</p>
                    ''',
                    'order': 4
                },
                {
                    'title': 'Consultoria SEO',
                    'subtitle': 'Posicione seu site nas primeiras posições do Google e aumente seu tráfego orgânico.',
                    'content': '''
                        <h2>Otimização para mecanismos de busca</h2>
                        <p>Estratégias técnicas e de conteúdo para melhorar seu posicionamento orgânico no Google.</p>
                    ''',
                    'order': 5
                },
                {
                    'title': 'HUB de Leads Kaizen',
                    'subtitle': 'Plataforma integrada para gerenciar todo o funil de vendas e maximizar conversões.',
                    'content': '''
                        <h2>Central de gestão de leads</h2>
                        <p>Sistema completo para capturar, qualificar e nutrir leads até a conversão final.</p>
                    ''',
                    'order': 6
                },
                {
                    'title': 'Assessoria em Funil de Marketing',
                    'subtitle': 'Otimize cada etapa do seu funil para converter mais visitantes em clientes.',
                    'content': '''
                        <h2>Otimização de funil de vendas</h2>
                        <p>Estratégias para melhorar conversão em cada etapa da jornada do cliente.</p>
                    ''',
                    'order': 7
                },
                {
                    'title': 'Consultoria para E-commerce',
                    'subtitle': 'Especialistas em otimização de lojas virtuais para aumentar vendas online.',
                    'content': '''
                        <h2>Otimização de e-commerce</h2>
                        <p>Estratégias específicas para aumentar conversões e vendas em lojas virtuais.</p>
                    ''',
                    'order': 8
                },
                {
                    'title': 'Consultoria de Conversion Rate Optimization (CRO)',
                    'subtitle': 'Aumente suas conversões através de testes e otimizações baseadas em dados.',
                    'content': '''
                        <h2>Otimização de taxa de conversão</h2>
                        <p>Metodologia científica para identificar e corrigir pontos de fricção que impedem conversões.</p>
                    ''',
                    'order': 9
                }
            ]

            created_count = 0
            for section_data in sections_data:
                slug = slugify(section_data['title'])
                
                # Verificar se a página já existe
                existing_page = solutions_page.get_children().filter(slug=slug).first()
                
                if existing_page:
                    self.stdout.write(f"Página '{section_data['title']}' já existe")
                    continue
                
                # Criar nova página
                page = StandardPage(
                    title=section_data['title'],
                    slug=slug,
                    live=True,
                    show_in_menus=True,
                    intro=section_data['subtitle'],
                    body=[('paragraph', section_data['content'])]
                )
                
                # Adicionar como filha da página Soluções
                solutions_page.add_child(instance=page)
                created_count += 1
                
                self.stdout.write(
                    self.style.SUCCESS(f"Página criada: '{section_data['title']}' -> /{slug}/")
                )

            self.stdout.write(
                self.style.SUCCESS(f"\\n{created_count} páginas de soluções criadas com sucesso!")
            )

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Erro ao criar páginas: {e}"))
