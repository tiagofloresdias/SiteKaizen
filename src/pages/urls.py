from django.urls import path
from . import views

urlpatterns = [
    path('', views.StandardPageView.as_view(), name='standard_page'),
]

