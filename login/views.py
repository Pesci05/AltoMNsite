from django.shortcuts import render,redirect
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView,LogoutView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from .forms import CustomLoginForm,CustomUserCretionForm

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

    def get_success_url(self):
        return reverse_lazy('home')