from django.conf import settings
from django.urls import include, path
from django.contrib import admin

from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from search import views as search_views
from blog import urls as blog_urls
from blog import api_urls as blog_api_urls
from leads import urls as leads_urls
from contact import urls as contact_urls
from franchise import urls as franchise_urls
from recruitment import urls as recruitment_urls
from services import urls as services_urls
from universidade import urls as universidade_urls

urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("search/", search_views.search, name="search"),
    path("blog/", include(blog_urls)),
    path("api/blog/", include(blog_api_urls)),
    path("leads/", include(leads_urls)),
    path("franchise/", include(franchise_urls)),
    path("", include(services_urls)),
    path("", include(contact_urls)),
    path("", include(universidade_urls)),
    path("", include(recruitment_urls)),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = urlpatterns + [
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    path("", include(wagtail_urls)),
    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    path("pages/", include(wagtail_urls)),
]

# Handlers de erro personalizados
handler400 = 'agenciakaizen_cms.views.custom_400'
handler403 = 'agenciakaizen_cms.views.custom_403'
handler404 = 'agenciakaizen_cms.views.custom_404'
handler500 = 'agenciakaizen_cms.views.custom_500'
