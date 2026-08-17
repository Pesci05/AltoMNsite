from django.shortcuts import render,redirect
from django.views.generic import CreateView,TemplateView
from django.contrib.auth.views import LoginView,LogoutView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from .forms import CustomLoginForm,CustomUserCretionForm
from django.contrib.auth.mixins import LoginRequiredMixin
from teams.forms import AtletaCreationForm, SquadraCreationForm

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
            return '/login/login.html'
        
class DirigentiDashboardView(LoginRequiredMixin,TemplateView):
    template_name='/home/mpesci/AltoMNsite/login/templates/login/dirigentiDashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['atleta_form'] = AtletaCreationForm()
        context['squadra_form'] = SquadraCreationForm()
        return context