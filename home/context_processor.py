from teams.models import Squadre

def squadre_globali(request):
    return {
        'squadre_globali': Squadre.objects.all()
    }