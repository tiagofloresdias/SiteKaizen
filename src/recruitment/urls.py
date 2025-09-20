from django.urls import path
from . import views

app_name = 'recruitment'

urlpatterns = [
    path('recrutamento/', views.recruitment_page, name='recruitment_page'),
    path('quero-ser-um-foguete/', views.foguete_page, name='foguete_page'),
    path('api/application/', views.RecruitmentAPIView.as_view(), name='recruitment_api'),
]
