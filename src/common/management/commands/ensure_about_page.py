"""
Comando idempotente para garantir a criação/publicação da página Quem Somos
(
AboutPage do app `home`), sob a raiz do site, com slug `/quem-somos/`.

Se existir uma página com esse slug mas de outro tipo (ex.: `wagtailcore.Page`),
o comando a remove e cria a `AboutPage` correta no mesmo parent.
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from wagtail.models import Page, Site


class Command(BaseCommand):
    help = "Garante a existência da página 'Quem Somos' (AboutPage) em /quem-somos/"

    @transaction.atomic
    def handle(self, *args, **options):
        try:
            # Descobrir parent: raiz do site padrão
            default_site = Site.objects.filter(is_default_site=True).select_related("root_page").first()
            if not default_site:
                self.stdout.write(self.style.ERROR("Site padrão não encontrado."))
                return

            parent_page = default_site.root_page.specific

            # Evitar criação sob a Root se o root_page não for a Home real
            # Se o root tiver um único filho vivo do tipo HomePage, usar como parent
            try:
                from home.models import HomePage  # import lazily para evitar dependências na inicialização
            except Exception:
                HomePage = None  # type: ignore

            if HomePage and not isinstance(parent_page, HomePage):
                home_candidate = (
                    parent_page.get_children().specific().type(HomePage).live().first()
                )
                if home_candidate:
                    parent_page = home_candidate

            # Verificar existência por slug
            existing = Page.objects.filter(slug="quem-somos").first()

            # Se já for AboutPage e estiver ok, publicar e sair
            if existing:
                specific = existing.specific
                from home.models import AboutPage

                if isinstance(specific, AboutPage):
                    # Garantir publicação e visibilidade em menus
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
                    self.stdout.write(self.style.SUCCESS("Página 'Quem Somos' já existe e foi garantida como publicada."))
                    return

                # Se não for AboutPage, remover para recriar corretamente
                parent_page = existing.get_parent().specific or parent_page
                existing.delete()
                self.stdout.write("Página existente com slug 'quem-somos' removida (tipo incorreto).")

            # Criar AboutPage com conteúdos padrão
            from home.models import AboutPage

            about_page = AboutPage(
                title="Quem Somos",
                slug="quem-somos",
                seo_title="Quem Somos",
                show_in_menus=True,
            )

            parent_page.add_child(instance=about_page)
            about_page.save_revision().publish()

            self.stdout.write(self.style.SUCCESS("Página 'Quem Somos' criada e publicada em /quem-somos/."))

        except Exception as exc:
            self.stdout.write(self.style.ERROR(f"Falha ao garantir 'Quem Somos': {exc}"))


