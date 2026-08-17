from django.urls import path
from . import views

urlpatterns = [
    path('login/',views.CustomLoginView.as_view(),name='login'),
    path('registrazione/',views.RegisterView.as_view(), name='register'), 
    path('dashboard_dirigente/',views.DirigentiDashboardView.as_view(),name='dashboard_dirigente'),  
]
