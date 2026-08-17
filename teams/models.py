from django.db import models
from django.conf import settings

# Create your models here.
class Squadre(models.Model):
    nome = models.CharField(max_length=50)
    categoria = models.CharField(max_length=50)
    allenatori = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        limit_choices_to={'ruolo':'allenatori'},
        blank=True,
        related_name='squadre'
    )

    def __str__(self):
        return f"{self.nome} ({self.categoria})"

class Atleta(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profilo_atleta',
    )
    data_nascita=models.DateField(auto_now=False, auto_now_add=False)
    squadra = models.ForeignKey(
        Squadre,
        on_delete=models.CASCADE,
        related_name='atleti'
    )

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"