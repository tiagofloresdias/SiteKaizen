from django.urls import path
from . import views
from . import contact_views

urlpatterns = [
    path('contato/', contact_views.contact_page, name='contact_page'),
    path('contato/ajax/', contact_views.contact_ajax, name='contact_ajax'),
    path('newsletter/', views.newsletter_subscribe, name='newsletter_subscribe'),
    path('newsletter/unsubscribe/<str:email>/', views.newsletter_unsubscribe, name='newsletter_unsubscribe'),
    path('newsletter/ajax/', views.newsletter_ajax, name='newsletter_ajax'),
    path('conecte-se/', views.connect_page, name='connect_page'),
]
