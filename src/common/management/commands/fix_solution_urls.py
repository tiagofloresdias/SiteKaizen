from django.core.management.base import BaseCommand
from wagtail.models import Page
from wagtail.redirects.models import Redirect
from django.http import HttpResponseRedirect


class Command(BaseCommand):
    help = "Cria redirecionamentos para URLs antigas de soluções"

    def handle(self, *args, **options):
        try:
            # Redirecionamentos necessários
            redirects = [
                {
                    'from_path': '/nossas-solucoes/',
                    'to_path': '/solucoes/',
                    'is_permanent': True
                },
                {
                    'from_path': '/nossas-solucoes/desenvolvimento-de-sites/',
                    'to_path': '/solucoes/desenvolvimento-de-sites/',
                    'is_permanent': True
                },
                {
                    'from_path': '/nossas-solucoes/geracao-de-oportunidades-de-venda/',
                    'to_path': '/solucoes/geracao-de-oportunidades-de-venda/',
                    'is_permanent': True
                },
                {
                    'from_path': '/nossas-solucoes/assessoria-de-midia-paga/',
                    'to_path': '/solucoes/assessoria-de-midia-paga/',
                    'is_permanent': True
                },
                {
                    'from_path': '/nossas-solucoes/branding/',
                    'to_path': '/solucoes/branding/',
                    'is_permanent': True
                },
                {
                    'from_path': '/nossas-solucoes/consultoria-seo/',
                    'to_path': '/solucoes/consultoria-seo/',
                    'is_permanent': True
                },
                {
                    'from_path': '/nossas-solucoes/hub-de-leads-kaizen/',
                    'to_path': '/solucoes/hub-de-leads-kaizen/',
                    'is_permanent': True
                },
                {
                    'from_path': '/nossas-solucoes/assessoria-em-funil-de-marketing/',
                    'to_path': '/solucoes/assessoria-em-funil-de-marketing/',
                    'is_permanent': True
                },
                {
                    'from_path': '/nossas-solucoes/consultoria-para-e-commerce/',
                    'to_path': '/solucoes/consultoria-para-e-commerce/',
                    'is_permanent': True
                },
                {
                    'from_path': '/nossas-solucoes/consultoria-de-conversion-rate-optimization-cro/',
                    'to_path': '/solucoes/consultoria-de-conversion-rate-optimization-cro/',
                    'is_permanent': True
                }
            ]

            created_count = 0
            for redirect_data in redirects:
                # Verificar se o redirecionamento já existe
                existing_redirect = Redirect.objects.filter(
                    old_path=redirect_data['from_path']
                ).first()
                
                if existing_redirect:
                    self.stdout.write(f"Redirecionamento já existe: {redirect_data['from_path']}")
                    continue
                
                # Criar redirecionamento
                redirect = Redirect(
                    old_path=redirect_data['from_path'],
                    redirect_to=redirect_data['to_path'],
                    is_permanent=redirect_data['is_permanent']
                )
                redirect.save()
                created_count += 1
                
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Redirecionamento criado: {redirect_data['from_path']} -> {redirect_data['to_path']}"
                    )
                )

            self.stdout.write(
                self.style.SUCCESS(f"\\n{created_count} redirecionamentos criados com sucesso!")
            )

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Erro ao criar redirecionamentos: {e}"))
