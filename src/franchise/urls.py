from django.urls import path
from . import views

urlpatterns = [
    # Fluxo de franqueado - Steps
    path('api/step1/', views.franchise_step1, name='franchise_step1'),
    path('api/step2/', views.franchise_step2, name='franchise_step2'),
    path('api/step3/', views.franchise_step3, name='franchise_step3'),
    path('api/step4/', views.franchise_step4, name='franchise_step4'),
    path('api/step5/', views.franchise_step5, name='franchise_step5'),
    path('api/submit/', views.franchise_submit, name='franchise_submit'),
    
    # Tracking
    path('api/touchpoint/', views.franchise_touchpoint, name='franchise_touchpoint'),
]

