"""
Comando para criar páginas baseadas nos modelos existentes
"""
from django.core.management.base import BaseCommand
from django.db import transaction
from wagtail.models import Page, Site
from django.contrib.auth.models import User
from django.apps import apps


class Command(BaseCommand):
    help = 'Cria páginas baseadas nos modelos existentes'

    def handle(self, *args, **options):
        try:
            with transaction.atomic():
                # Buscar usuário admin
                admin_user = User.objects.filter(is_superuser=True).first()
                if not admin_user:
                    self.stdout.write(self.style.ERROR('Usuário admin não encontrado'))
                    return
                
                # Buscar página Home
                home_page = Page.objects.filter(slug='home').first()
                if not home_page:
                    self.stdout.write(self.style.ERROR('Página Home não encontrada'))
                    return
                
                # Mapear modelos para páginas
                page_models = {
                    'portfolio.PortfolioIndexPage': {
                        'title': 'Portfolio',
                        'slug': 'portfolio',
                        'url_path': '/home/portfolio/',
                    },
                    'services.ServicesIndexPage': {
                        'title': 'Serviços',
                        'slug': 'servicos',
                        'url_path': '/home/servicos/',
                    },
                    'solutions.SolutionsPage': {
                        'title': 'Soluções',
                        'slug': 'solucoes',
                        'url_path': '/home/solucoes/',
                    },
                    'about.AboutPage': {
                        'title': 'Quem Somos',
                        'slug': 'quem-somos',
                        'url_path': '/home/quem-somos/',
                    },
                    'about.OndeEstamosPage': {
                        'title': 'Onde Estamos',
                        'slug': 'onde-estamos',
                        'url_path': '/home/onde-estamos/',
                    },
                    'about.NossasEmpresasPage': {
                        'title': 'Nossas Empresas',
                        'slug': 'nossas-empresas',
                        'url_path': '/home/nossas-empresas/',
                    },
                    'blog.BlogIndexPage': {
                        'title': 'Aprenda Marketing Digital',
                        'slug': 'aprenda-marketing-digital',
                        'url_path': '/home/aprenda-marketing-digital/',
                    },
                    'contact.ConnectPage': {
                        'title': 'Conecte-se',
                        'slug': 'conecte-se',
                        'url_path': '/home/conecte-se/',
                    },
                }
                
                created_count = 0
                for model_path, page_data in page_models.items():
                    try:
                        # Verificar se a página já existe
                        existing_page = Page.objects.filter(slug=page_data['slug']).first()
                        if existing_page:
                            self.stdout.write(f'Página {page_data["title"]} já existe, pulando...')
                            continue
                        
                        # Buscar o modelo
                        app_label, model_name = model_path.split('.')
                        model_class = apps.get_model(app_label, model_name)
                        
                        # Criar nova página
                        page = model_class(
                            title=page_data['title'],
                            slug=page_data['slug'],
                            live=True,
                            url_path=page_data['url_path'],
                            owner=admin_user
                        )
                        
                        # Definir como filha da Home
                        page = home_page.add_child(instance=page)
                        
                        created_count += 1
                        self.stdout.write(f'Página criada: {page.title}')
                        
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f'Erro ao criar página {page_data["title"]}: {e}'))
                
                self.stdout.write(self.style.SUCCESS(f'{created_count} páginas criadas com sucesso!'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erro durante criação das páginas: {e}'))
