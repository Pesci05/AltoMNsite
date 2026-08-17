from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .models import Atleta,Squadre
from .forms import AtletaCreationForm,SquadraCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class CreaAtletaView(LoginRequiredMixin,CreateView):
    model = Atleta
    form_class = AtletaCreationForm
    success_url = reverse_lazy('dashboard_dirigente')

class CreaSquadraView(LoginRequiredMixin,CreateView):
    model = Squadre
    form_class = SquadraCreationForm
    success_url = reverse_lazy('dashboard_dirigente')