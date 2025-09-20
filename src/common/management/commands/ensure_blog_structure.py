from django.core.management.base import BaseCommand
from wagtail.models import Page, Site
from blog.models import BlogIndexPage


class Command(BaseCommand):
    help = "Garante que exista uma BlogIndexPage publicada na raiz do site"

    def handle(self, *args, **options):
        site = Site.objects.filter(is_default_site=True).first() or Site.objects.first()
        if not site:
            self.stdout.write(self.style.ERROR("Nenhum Site do Wagtail encontrado."))
            return

        root = site.root_page.specific
        existing = root.get_children().type(BlogIndexPage).first()
        if existing:
            self.stdout.write(self.style.SUCCESS(f"BlogIndexPage já existe: {existing.title}"))
            return

        blog_index = BlogIndexPage(
            title="Blog",
            slug="blog",
            intro="Últimos artigos da Agência Kaizen",
        )
        root.add_child(instance=blog_index)
        blog_index.save_revision().publish()
        self.stdout.write(self.style.SUCCESS("BlogIndexPage criada e publicada em /blog/"))


