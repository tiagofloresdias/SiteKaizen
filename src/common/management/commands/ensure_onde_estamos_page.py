"""
Comando idempotente para garantir a criação/publicação da página Onde Estamos
(`home.OndeEstamosPage`) em `/onde-estamos/`, posicionada preferencialmente
como filha da Home, publicada e exibida no menu.
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from wagtail.models import Page, Site


class Command(BaseCommand):
    help = "Garante a existência da página 'Onde Estamos' (OndeEstamosPage) em /onde-estamos/"

    @transaction.atomic
    def handle(self, *args, **options):
        try:
            default_site = Site.objects.filter(is_default_site=True).select_related("root_page").first()
            if not default_site:
                self.stdout.write(self.style.ERROR("Site padrão não encontrado."))
                return

            parent_page = default_site.root_page.specific

            # Preferir a HomePage como parent se existir
            try:
                from home.models import HomePage  # type: ignore
            except Exception:
                HomePage = None  # type: ignore

            if HomePage and not isinstance(parent_page, HomePage):
                home_candidate = parent_page.get_children().specific().type(HomePage).live().first()
                if home_candidate:
                    parent_page = home_candidate

            # Se existir slug com tipo errado, remover para recriar
            existing = Page.objects.filter(slug="onde-estamos").first()
            if existing:
                specific = existing.specific
                from home.models import OndeEstamosPage  # import tardio

                if isinstance(specific, OndeEstamosPage):
                    updated = False
                    if not specific.live:
                        specific.live = True
                        updated = True
                    if not specific.show_in_menus:
                        specific.show_in_menus = True
                        updated = True
                    if updated:
                        specific.save()
                        specific.save_revision().publish()
                    self.stdout.write(self.style.SUCCESS("Página 'Onde Estamos' já existe e foi garantida como publicada."))
                    return

                parent_page = existing.get_parent().specific or parent_page
                existing.delete()
                self.stdout.write("Página existente com slug 'onde-estamos' removida (tipo incorreto).")

            from home.models import OndeEstamosPage

            page = OndeEstamosPage(
                title="Onde Estamos",
                slug="onde-estamos",
                seo_title="Onde Estamos",
                show_in_menus=True,
            )

            parent_page.add_child(instance=page)
            page.save_revision().publish()

            self.stdout.write(self.style.SUCCESS("Página 'Onde Estamos' criada e publicada em /onde-estamos/."))

        except Exception as exc:
            self.stdout.write(self.style.ERROR(f"Falha ao garantir 'Onde Estamos': {exc}"))


