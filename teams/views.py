from django.shortcuts import render,get_object_or_404,redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView,DetailView,ListView,UpdateView,DeleteView
from .models import Atleta,Squadre,Matches
from .forms import AtletaCreationForm,SquadraCreationForm,MatchUpdateForm
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class CreaAtletaView(LoginRequiredMixin,CreateView):
    model = Atleta
    form_class = AtletaCreationForm

    def get_success_url(self):
        # 1. Cerca il parametro 'next' inviato dal form
        next_url = self.request.POST.get('next')
        
        # 2. Se 'next' esiste, reindirizza lì
        if next_url:
            return next_url
            
        # 3. Fallback di sicurezza in caso manchi il parametro
        return reverse_lazy('dashboard_dirigente')
    
class CreaSquadraView(LoginRequiredMixin,CreateView):
    model = Squadre
    form_class = SquadraCreationForm
    success_url = reverse_lazy('dashboard_dirigente')

class MatchesDetailView(DetailView):
    model = Matches
    context_object_name = 'match'
    template_name= 'teams/match_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Recupera tutti i tabellini dei giocatori per questa partita ordinati per punti decrescenti
        context['box_score'] = self.object.player_stats.select_related('player').order_by('-points')
        return context

class MatchListView(ListView):
    model=Matches
    template_name='teams/match_list.html'
    context_object_name = 'match'
    paginate_by = 10

class MatchUpdateView(LoginRequiredMixin,UpdateView):
    model=Matches
    form_class=MatchUpdateForm
    template_name="teams/match_update.html"
    success_url = reverse_lazy('dashboard_coach')

class MatchDeleteView(LoginRequiredMixin, DeleteView):
    model = Matches
    success_url = reverse_lazy('dashboard_coach') 

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)