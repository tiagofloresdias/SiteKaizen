from django.core.management.base import BaseCommand
from pages.models import StandardPage
from solutions.models import SolutionsPage
from django.utils.text import slugify


class Command(BaseCommand):
    help = "Cria página 'Nossas Soluções' que redireciona para 'Soluções'"

    def handle(self, *args, **options):
        try:
            # Buscar a página raiz
            from wagtail.models import Site
            site = Site.objects.filter(hostname='new.agenciakaizen.com.br').first()
            root = site.root_page

            # Verificar se já existe
            existing_page = root.get_children().filter(slug='nossas-solucoes').first()
            if existing_page:
                self.stdout.write("Página 'Nossas Soluções' já existe")
                return

            # Criar página Nossas Soluções
            nossas_solucoes = StandardPage(
                title='Nossas Soluções',
                slug='nossas-solucoes',
                live=True,
                show_in_menus=False,  # Não mostrar no menu principal
                intro='<p>Redirecionando para nossa página de soluções...</p>',
                body=[('paragraph', '<script>window.location.href="/solucoes/";</script>')]
            )
            
            root.add_child(instance=nossas_solucoes)
            
            self.stdout.write(
                self.style.SUCCESS("Página 'Nossas Soluções' criada com redirecionamento automático!")
            )

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Erro ao criar página: {e}"))
