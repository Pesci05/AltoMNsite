from django.urls import path
from . import views

urlpatterns = [
    path('',views.HomeView.as_view(),name='home'),  
    path('crea-news/', views.CreaNewsView.as_view(), name='creaNews'),
    path('notizie/', views.NewsListView.as_view(), name='news_list'),
    path('notizie/<slug:slug>/', views.NewsDetailView.as_view(), name='news_detail'),
    ]