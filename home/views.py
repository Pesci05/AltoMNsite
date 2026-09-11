from django.shortcuts import render
from django.views.generic import TemplateView
from teams.models import Matches

# Create your views here.
class HomeView(TemplateView):
    template_name = 'home/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['last_matches'] = Matches.objects.order_by('-giornoPartita')[:5]
        return context

    def post(self, request):
        name = request.POST.get('name','Guest')
        return render(request,'template.html',{'message': f'Hello, {name}!'})