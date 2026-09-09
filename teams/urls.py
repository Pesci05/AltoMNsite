from django.urls import path
from .views import  CreaAtletaView, CreaSquadraView,MatchListView,MatchesDetailView,MatchUpdateView,MatchDeleteView

urlpatterns = [
    path('crea-squadra/', CreaSquadraView.as_view(), name='creaSquadra'),
    path('crea-atleta/', CreaAtletaView.as_view(), name='creaAtleta'),
    path('partite/',MatchListView.as_view(),name='partite'),
    path('crea-partite/',CreaSquadraView.as_view(),name='creaPartite'),
    path('stats-partita/',MatchesDetailView.as_view(),name='statsPartita'),
    path('<int:pk>/modifica/',MatchUpdateView.as_view(),name='modificaPartita'),
    path('<int:pk>/elimina/',MatchDeleteView.as_view(),name='eliminaPartita'),
]