from django.shortcuts import render,redirect
from django.views.generic import CreateView,TemplateView
from django.contrib.auth.views import LoginView,LogoutView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin

from home.forms import CreaNewsForm
from .forms import CustomLoginForm,CustomUserCretionForm
from django.contrib.auth.mixins import LoginRequiredMixin
from teams.forms import AtletaCreationForm, SquadraCreationForm, MatchCreationForm
from teams.models import Matches

# Create your views here.
class RegisterView(SuccessMessageMixin,CreateView):
    form_class=CustomUserCretionForm
    template_name = 'login/register.html'
    success_url = reverse_lazy('login')
    success_message = "Account creato con successo! Ora puoi effettuare l'accesso."

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

class CustomLoginView(LoginView):
    form_class=CustomLoginForm
    template_name='login/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        user = self.request.user

        if user.ruolo == 'dirigente':
            return '/login/dashboard_dirigente'
        elif user.ruolo == 'allenatori':
            return '/login/dashboard_coach'
        
class DirigentiDashboardView(LoginRequiredMixin,TemplateView):
    template_name='login/dirigentiDashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'atleta_form' not in context:
            context['atleta_form'] = AtletaCreationForm(user=self.request.user)

        if 'squadra_form' not in context:    
            context['squadra_form'] = SquadraCreationForm()
        if 'cera_news_form' not in context:
            context['crea_news_form'] = CreaNewsForm()
        return context

    def post(self, request, *args, **kwargs):
        # Recupera il contesto base
        context = self.get_context_data()

        
        # 1. GESTIONE FORM ATLETA (esempio)
        if 'submit_atleta' in request.POST:
            form_atleta = AtletaCreationForm(request.POST, user=request.user)
            if form_atleta.is_valid():
                form_atleta.save()
                return redirect('dashboard_dirigente')
            else:
                context['atleta_form'] = form_atleta

        # 2. GESTIONE FORM SQUADRA (esempio)
        elif 'submit_squadra' in request.POST:
            form_squadra = SquadraCreationForm(request.POST)
            if form_squadra.is_valid():
                form_squadra.save()
                return redirect('dashboard_dirigente')
            else:
                context['squadra_form'] = form_squadra

        # Se ci sono errori, ricarica la pagina mostrando i messaggi di errore nei form
        return self.render_to_response(context)
class CoachDashboardView(LoginRequiredMixin,TemplateView):
    template_name = 'login/coachDashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'atleta_form' not in context:
            context['atleta_form'] = AtletaCreationForm(user=self.request.user)
            
        # 2. Form per la partita (passiamo l'utente loggato per filtrare le sue squadre)
        if 'crea_match_form' not in context:
            context['crea_match_form'] = MatchCreationForm(user=self.request.user)

        context['partite'] = Matches.objects.filter(team__allenatori=self.request.user)
        return context
    
    def post(self, request, *args, **kwargs):
        # A. Se è stato cliccato il pulsante per salvare la partita
        if 'btn_submit_match' in request.POST:
            crea_match_form = MatchCreationForm(request.POST, user=request.user)
            if crea_match_form.is_valid():
                crea_match_form.save()
                return redirect('dashboard_coach')  # Sostituisci col nome della tua URL della dashboard
            else:
                # Se ci sono errori, ricarichiamo il form compilato con i messaggi di errore
                return self.render_to_response(
                    self.get_context_data(crea_match_form=crea_match_form)
                )

        # B. Se è stato cliccato il pulsante per creare l'atleta
        elif 'btn_submit_atleta' in request.POST:
            atleta_form = AtletaCreationForm(request.POST)
            if atleta_form.is_valid():
                atleta_form.save()
                return redirect('dashboard_coach')
            else:
                return self.render_to_response(
                    self.get_context_data(atleta_form=atleta_form)
                )

        # Fallback se non corrisponde a nessuno dei due
        return self.get(request, *args, **kwargs)
    