from django.core.management.base import BaseCommand
from wagtail.models import Site


class Command(BaseCommand):
    help = "Atualiza o hostname do objeto Site padrão do Wagtail (idempotente)."

    def add_arguments(self, parser):
        parser.add_argument("hostname", type=str, help="Novo hostname, ex: new.agenciakaizen.com.br")
        parser.add_argument("--port", type=int, default=80, help="Porta (default: 80)")

    def handle(self, *args, **options):
        hostname: str = options["hostname"].strip().lower()
        port: int = options["port"]

        site: Site | None = Site.objects.filter(is_default_site=True).first()
        if not site:
            self.stderr.write("Site padrão não encontrado. Crie/defina um site padrão no admin.")
            return

        changed = False
        if site.hostname != hostname:
            site.hostname = hostname
            changed = True
        if site.port != port:
            site.port = port
            changed = True

        if changed:
            site.save()
            self.stdout.write(self.style.SUCCESS(f"Hostname atualizado: {hostname}:{port}"))
        else:
            self.stdout.write("Nenhuma alteração necessária. Hostname já está correto.")


