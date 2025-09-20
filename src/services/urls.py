from django.urls import path
from . import views

urlpatterns = [
    path('midia-programatica/', views.MidiaProgramaticaPageView.as_view(), name='midia_programatica_page'),
]

