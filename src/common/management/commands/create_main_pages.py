"""
Comando para criar páginas principais do site
"""
from django.core.management.base import BaseCommand
from django.db import transaction
from wagtail.models import Page, Site
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Cria páginas principais do site'

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
                
                # Páginas principais para criar
                pages_to_create = [
                    {
                        'title': 'Quem Somos',
                        'slug': 'quem-somos',
                        'url_path': '/home/quem-somos/',
                        'content': 'Conheça a Agência Kaizen e nossa equipe especializada em marketing digital.'
                    },
                    {
                        'title': 'Serviços',
                        'slug': 'servicos',
                        'url_path': '/home/servicos/',
                        'content': 'Conheça nossos serviços de marketing digital, SEO, Google Ads e muito mais.'
                    },
                    {
                        'title': 'Soluções',
                        'slug': 'solucoes',
                        'url_path': '/home/solucoes/',
                        'content': 'Soluções completas em marketing digital para impulsionar seu negócio.'
                    },
                    {
                        'title': 'Portfolio',
                        'slug': 'portfolio',
                        'url_path': '/home/portfolio/',
                        'content': 'Conheça nossos cases de sucesso e clientes satisfeitos.'
                    },
                    {
                        'title': 'Contato',
                        'slug': 'contato',
                        'url_path': '/home/contato/',
                        'content': 'Entre em contato conosco e solicite um orçamento.'
                    },
                    {
                        'title': 'Onde Estamos',
                        'slug': 'onde-estamos',
                        'url_path': '/home/onde-estamos/',
                        'content': 'Conheça nossos escritórios e localizações.'
                    },
                    {
                        'title': 'Nossas Empresas',
                        'slug': 'nossas-empresas',
                        'url_path': '/home/nossas-empresas/',
                        'content': 'Conheça as empresas do grupo Kaizen.'
                    },
                    {
                        'title': 'Aprenda Marketing Digital',
                        'slug': 'aprenda-marketing-digital',
                        'url_path': '/home/aprenda-marketing-digital/',
                        'content': 'Blog com artigos e dicas sobre marketing digital.'
                    }
                ]
                
                created_count = 0
                for page_data in pages_to_create:
                    # Verificar se a página já existe
                    existing_page = Page.objects.filter(slug=page_data['slug']).first()
                    if existing_page:
                        self.stdout.write(f'Página {page_data["title"]} já existe, pulando...')
                        continue
                    
                    # Criar nova página
                    page = Page(
                        title=page_data['title'],
                        slug=page_data['slug'],
                        live=True,
                        url_path=page_data['url_path'],
                        content_type_id=1,  # Page content type
                        path=home_page.path + '0001',  # Simular path
                        depth=home_page.depth + 1,
                        numchild=0,
                        seo_title=page_data['title'],
                        show_in_menus=True,
                        locked=False,
                        has_unpublished_changes=False,
                        owner=admin_user
                    )
                    
                    # Ajustar path baseado no ID
                    page.save()
                    page.path = f"{home_page.path}{page.id:04d}"
                    page.save()
                    
                    created_count += 1
                    self.stdout.write(f'Página criada: {page.title}')
                
                self.stdout.write(self.style.SUCCESS(f'{created_count} páginas criadas com sucesso!'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erro durante criação das páginas: {e}'))
