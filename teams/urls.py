from django.urls import path
from .views import  CreaAtletaView, CreaSquadraView

urlpatterns = [
    path('crea-squadra/', CreaSquadraView.as_view(), name='creaSquadra'),
    path('crea-atleta/', CreaAtletaView.as_view(), name='creaAtleta'),
]