from django.db.models.aggregates import Avg,Sum
from django.shortcuts import render,get_object_or_404,redirect
from django.urls import reverse_lazy
from django.forms import inlineformset_factory
from django.views.generic import CreateView,DetailView,ListView,UpdateView,DeleteView,View
from .models import Atleta,Squadre,Matches,PlayerMatchStats
from .forms import AtletaCreationForm,SquadraCreationForm,MatchUpdateForm,TabellinoPartitaForm
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class CreaAtletaView(LoginRequiredMixin,CreateView):
    model = Atleta
    form_class = AtletaCreationForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Passa l'utente loggato al form per filtrare le squadre
        kwargs['user'] = self.request.user
        return kwargs

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
        context['stats_list'] = self.object.player_stats.all().order_by('-points')
        context['totale_punti'] = self.object.player_stats.aggregate(Sum('points'))['points__sum'] or 0
        context['totale_falli'] = self.object.player_stats.aggregate(Sum('fouls'))['fouls__sum'] or 0
        context['show_totals'] = True
        return context

class MatchListView(ListView):
    model=Matches
    template_name='teams/match_list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['squadre'] = Squadre.objects.all()
        context['matches'] = Matches.objects.all()

        return context

class MatchUpdateView(LoginRequiredMixin,UpdateView):
    model = Matches
    form_class = MatchUpdateForm
    template_name = "teams/match_update.html"
    success_url = reverse_lazy('dashboard_coach')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        match = self.object

        # Se 'formset' non è nel context, significa che stiamo caricando la pagina la prima volta (GET)
        if 'formset' not in context:
            # 1. Recuperiamo tutti i giocatori della squadra
            atleti_squadra = match.team.atleti.select_related('user').all()
            giocatori_squadra = [atleta.user for atleta in atleti_squadra]
            
            # 2. Recuperiamo i giocatori che hanno GIÀ salvato statistiche per questa partita
            stats_esistenti = match.player_stats.all()
            giocatori_con_stat = [stat.player for stat in stats_esistenti]
            
            # 3. Creiamo le righe vuote SOLO per i giocatori mancanti
            initial_data = [
                {'player': utente} 
                for utente in giocatori_squadra 
                if utente not in giocatori_con_stat
            ]

            # 4. Inizializziamo il formset con i form extra esatti
            StatsFormSet = inlineformset_factory(
                Matches, 
                PlayerMatchStats, 
                form=TabellinoPartitaForm, 
                extra=len(initial_data), 
                can_delete=False
            )

            # Passando instance=match carica i dati vecchi, passando initial popola i nuovi
            context['formset'] = StatsFormSet(instance=match, initial=initial_data)

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        
        # SCENARIO A: L'utente ha cliccato "Salva Partita"
        if 'btn_submit_match' in request.POST:
            form = self.get_form()
            if form.is_valid():
                form.save()
                return redirect('dashboard_coach')
            else:
                return self.render_to_response(self.get_context_data(form=form))

        # SCENARIO B: L'utente ha cliccato "Salva Tabellino"
        elif 'btn_salva_tabellino' in request.POST:
            StatsFormSet = inlineformset_factory(
                Matches, 
                PlayerMatchStats, 
                form=TabellinoPartitaForm, 
                extra=0, # Durante il POST basta extra=0, i form totali vengono letti da request.POST
                can_delete=False
            )
            formset = StatsFormSet(request.POST, instance=self.object)
            
            if formset.is_valid():
                formset.save()
                return redirect('dashboard_coach')
            else:
                # Se il formset ha errori, ricarichiamo la pagina passandolo al context
                form = self.get_form_class()(instance=self.object, user=request.user)
                return self.render_to_response(self.get_context_data(form=form, formset=formset))

        return redirect('dashboard_coach')

class MatchDeleteView(LoginRequiredMixin, DeleteView):
    model = Matches
    success_url = reverse_lazy('dashboard_coach') 

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

class TeamDetailView(DetailView):
    model = Squadre
    context_object_name = 'squadra'
    template_name = 'teams/team_detail.html'

class AtletaDetailView(DetailView):
    model = Atleta
    template_name = 'teams/player_detail.html'
    context_object_name = 'atleta'

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        atleta = self.object
        partite = PlayerMatchStats.objects.filter(player=atleta)
       
        print(f"Atleta: {atleta}, ID: {atleta.pk}")
        
        context['totale_punti'] = partite.aggregate(Sum('points'))['points__sum'] or 0
        context['totale_falli'] = partite.aggregate(Sum('fouls'))['fouls__sum'] or 0
        context['three_pointers_made'] = partite.aggregate(Sum('three_pointers_made'))['three_pointers_made__sum'] or 0
        context['three_pointers_attempted'] = partite.aggregate(Sum('three_pointers_attempted'))['three_pointers_attempted__sum'] or 0
        context['free_throws_made'] = partite.aggregate(Sum('free_throws_made'))['free_throws_made__sum'] or 0
        context['free_throws_attempted'] = partite.aggregate(Sum('free_throws_attempted'))['free_throws_attempted__sum'] or 0
        context['three_pointers_percentage'] = (context['three_pointers_made'] / context['three_pointers_attempted'] * 100) if context['three_pointers_attempted'] > 0 else 0
        context['free_throws_percentage'] = (context['free_throws_made'] / context['free_throws_attempted'] * 100) if context['free_throws_attempted'] > 0 else 0
        context['partite'] = partite.count()
        return context
