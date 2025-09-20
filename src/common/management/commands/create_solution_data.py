"""
Comando para criar dados de soluções
"""
from django.core.management.base import BaseCommand
from django.db import transaction
from solutions.models import ServiceIcon, Service, SolutionSection


class Command(BaseCommand):
    help = 'Cria dados de soluções (ícones, serviços e seções)'

    def handle(self, *args, **options):
        try:
            with transaction.atomic():
                # Criar ícones
                icons_data = [
                    {'name': 'Geração de Leads', 'icon_class': 'fas fa-bullseye', 'description': 'Ícone para geração de leads'},
                    {'name': 'Google Ads', 'icon_class': 'fas fa-google', 'description': 'Ícone para Google Ads'},
                    {'name': 'Facebook Ads', 'icon_class': 'fab fa-facebook', 'description': 'Ícone para Facebook Ads'},
                    {'name': 'SEO', 'icon_class': 'fas fa-search', 'description': 'Ícone para SEO'},
                    {'name': 'Desenvolvimento', 'icon_class': 'fas fa-code', 'description': 'Ícone para desenvolvimento'},
                    {'name': 'E-commerce', 'icon_class': 'fas fa-shopping-cart', 'description': 'Ícone para e-commerce'},
                    {'name': 'Mídia Programática', 'icon_class': 'fas fa-bullseye', 'description': 'Ícone para mídia programática'},
                    {'name': 'Consultoria', 'icon_class': 'fas fa-chart-line', 'description': 'Ícone para consultoria'},
                ]
                
                created_icons = 0
                for icon_data in icons_data:
                    icon, created = ServiceIcon.objects.get_or_create(
                        name=icon_data['name'],
                        defaults=icon_data
                    )
                    if created:
                        created_icons += 1
                        self.stdout.write(f'Ícone criado: {icon.name}')
                
                # Criar serviços
                services_data = [
                    {
                        'title': 'Google Ads',
                        'description': 'Campanhas otimizadas no Google para maximizar ROI e conversões',
                        'icon_class': 'fas fa-google',
                        'is_featured': True,
                        'order': 1
                    },
                    {
                        'title': 'Facebook Ads',
                        'description': 'Anúncios segmentados no Facebook e Instagram para alcançar seu público',
                        'icon_class': 'fab fa-facebook',
                        'is_featured': True,
                        'order': 2
                    },
                    {
                        'title': 'SEO',
                        'description': 'Otimização para buscadores para aumentar visibilidade orgânica',
                        'icon_class': 'fas fa-search',
                        'is_featured': True,
                        'order': 3
                    },
                    {
                        'title': 'Desenvolvimento de Sites',
                        'description': 'Sites responsivos e otimizados para conversão',
                        'icon_class': 'fas fa-code',
                        'is_featured': True,
                        'order': 4
                    },
                    {
                        'title': 'E-commerce',
                        'description': 'Lojas virtuais completas com integração de pagamento',
                        'icon_class': 'fas fa-shopping-cart',
                        'is_featured': False,
                        'order': 5
                    },
                    {
                        'title': 'Mídia Programática',
                        'description': 'Publicidade automatizada com IA para máxima eficiência',
                        'icon_class': 'fas fa-bullseye',
                        'is_featured': False,
                        'order': 6
                    },
                    {
                        'title': 'Consultoria Estratégica',
                        'description': 'Análise completa do seu negócio e estratégia personalizada',
                        'icon_class': 'fas fa-chart-line',
                        'is_featured': False,
                        'order': 7
                    },
                    {
                        'title': 'Geração de Leads',
                        'description': 'Sistemas automatizados para captar e qualificar leads',
                        'icon_class': 'fas fa-users',
                        'is_featured': False,
                        'order': 8
                    },
                ]
                
                created_services = 0
                for service_data in services_data:
                    service, created = Service.objects.get_or_create(
                        title=service_data['title'],
                        defaults=service_data
                    )
                    if created:
                        created_services += 1
                        self.stdout.write(f'Serviço criado: {service.title}')
                
                # Criar seções
                sections_data = [
                    {
                        'title': 'Geração de Oportunidades',
                        'subtitle': 'Transformamos visitantes em clientes através de estratégias comprovadas de conversão',
                        'background_color': 'bg-dark',
                        'cta_text': 'Quero Gerar Mais Leads',
                        'order': 1
                    },
                    {
                        'title': 'Mídia Paga',
                        'subtitle': 'Campanhas inteligentes que maximizam ROI e reduzem custo de aquisição',
                        'background_color': 'bg-black',
                        'cta_text': 'Quero Anunciar Agora',
                        'order': 2
                    },
                    {
                        'title': 'Desenvolvimento Web',
                        'subtitle': 'Sites e sistemas que convertem visitantes em clientes',
                        'background_color': 'bg-dark',
                        'cta_text': 'Quero Meu Site',
                        'order': 3
                    },
                ]
                
                created_sections = 0
                for section_data in sections_data:
                    section, created = SolutionSection.objects.get_or_create(
                        title=section_data['title'],
                        defaults=section_data
                    )
                    if created:
                        created_sections += 1
                        self.stdout.write(f'Seção criada: {section.title}')
                        
                        # Adicionar serviços à seção
                        if section.title == 'Geração de Oportunidades':
                            section.services.add(
                                Service.objects.get(title='SEO'),
                                Service.objects.get(title='Geração de Leads'),
                                Service.objects.get(title='Consultoria Estratégica')
                            )
                        elif section.title == 'Mídia Paga':
                            section.services.add(
                                Service.objects.get(title='Google Ads'),
                                Service.objects.get(title='Facebook Ads'),
                                Service.objects.get(title='Mídia Programática')
                            )
                        elif section.title == 'Desenvolvimento Web':
                            section.services.add(
                                Service.objects.get(title='Desenvolvimento de Sites'),
                                Service.objects.get(title='E-commerce'),
                                Service.objects.get(title='Consultoria Estratégica')
                            )
                
                self.stdout.write(self.style.SUCCESS(f'Dados criados: {created_icons} ícones, {created_services} serviços, {created_sections} seções'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erro durante criação dos dados: {e}'))
