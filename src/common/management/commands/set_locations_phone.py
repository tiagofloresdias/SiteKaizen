from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Define o telefone de todas as Localizações para 0800-550-8000"

    def handle(self, *args, **kwargs):
        try:
            from companies.models import Location
            total = Location.objects.update(phone="0800-550-8000")
            self.stdout.write(self.style.SUCCESS(f"Telefones atualizados para 0800-550-8000 em {total} localizações."))
        except Exception as exc:
            self.stdout.write(self.style.ERROR(f"Falha ao atualizar telefones: {exc}"))


