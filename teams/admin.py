from django.contrib import admin
from .models import Squadre,Atleta,PlayerMatchStats,Matches

# Register your models here.
admin.site.register(Squadre)
admin.site.register(Atleta)
class PlayerMatchStatInline(admin.TabularInline):
    model = PlayerMatchStats
    extra = 5  # Mostra 5 righe vuote per l'inserimento rapido
    autocomplete_fields = ['player'] # Utile se hai molti utenti

@admin.register(Matches)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('team', 'avversari', 'giornoPartita', 'puntiFatti', 'puntiSubiti')
   