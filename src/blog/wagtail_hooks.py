from wagtail import hooks
from django.urls import reverse
from wagtail.models import Site
from blog.models import BlogIndexPage


@hooks.register("construct_main_menu")
def add_blog_menu_item(request, menu_items):
    # Tenta localizar a BlogIndexPage do site atual e montar link direto para o Explorer dessa página
    page_id = None
    try:
        site = getattr(request, "site", None) or Site.find_for_request(request)
        if site:
            root = site.root_page
            blog_index = (
                root.get_children().specific().type(BlogIndexPage).live().first()
                or BlogIndexPage.objects.live().first()
            )
            if blog_index:
                page_id = blog_index.id
    except Exception:
        page_id = None

    url = reverse("wagtailadmin_explore_root") if not page_id else reverse("wagtailadmin_explore", args=(page_id,))

    # Inserir o item do menu próximo ao Explorer
    from wagtail.admin.menu import MenuItem
    menu_items.insert(2, MenuItem("Blog", url, icon_name="doc-full-inverse", order=100))
