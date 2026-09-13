from django.shortcuts import render
from django.views.generic import CreateView, DetailView, ListView, TemplateView
from home.models import News
from teams.models import Matches
from .forms import CreaNewsForm
from django.urls import reverse_lazy


# Create your views here.
class HomeView(TemplateView):
    template_name = 'home/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['last_matches'] = Matches.objects.order_by('-giornoPartita')[:5]
        context['last_news'] = News.objects.filter(pubblicata=True).order_by('-data_pubblicazione')[:5]
        return context

    def post(self, request):
        name = request.POST.get('name','Guest')
        return render(request,'template.html',{'message': f'Hello, {name}!'})

class CreaNewsView(CreateView):
    template_name = 'home/crea_news.html'
    form_class = CreaNewsForm
    success_url = reverse_lazy('dashboard_dirigente')  # Redirect to the dashboard after successful creation

class NewsListView(ListView):
    template_name = 'home/news_list.html'
    model = News

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['news_list'] = News.objects.filter(pubblicata=True).order_by('-data_pubblicazione')
        return context

class NewsDetailView(DetailView):
    template_name = 'home/news_detail.html'
    model = News

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get('slug')
        context['news'] = News.objects.get(slug=slug)
        return context