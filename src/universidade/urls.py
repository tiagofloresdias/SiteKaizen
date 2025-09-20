from django.urls import path
from . import views

app_name = 'universidade'

urlpatterns = [
    path('universidade-kaizen/', views.universidade_kaizen_page, name='universidade_kaizen_page'),
]

