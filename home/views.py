from django.shortcuts import render
from django.views import View

# Create your views here.
class HomeView(View):
    def get(self, request):
        return render(request,'template.html',{'message':'HELLO'})

    def post(self, request):
        name = request.POST.get('name','Guest')
        return render(request,'template.html',{'message': f'Hello, {name}!'})