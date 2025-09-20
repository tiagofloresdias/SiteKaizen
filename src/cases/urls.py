from django.urls import path, include
from wagtail import urls as wagtail_urls

app_name = 'cases'

urlpatterns = [
    path('', include(wagtail_urls)),
]

