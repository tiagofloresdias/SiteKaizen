from django.urls import path
from . import views

app_name = 'leads'

urlpatterns = [
    path('api/leads/', views.LeadAPIView.as_view(), name='lead_api'),
    path('api/leads/<int:lead_id>/', views.get_lead_data, name='get_lead_data'),
]
