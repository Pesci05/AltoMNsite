from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

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
    RUOLO_CHOICES = (
        ('Play', 'Playmaker'),
        ('Guardia', 'Guardia'),
        ('Ala', 'Ala'),
        ('AlaGrande', 'Ala Grande'),
        ('Centro', 'Centro'),
    )
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
    posizione = models.CharField(max_length=20, choices=RUOLO_CHOICES,default='Play')
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

class Matches(models.Model):
    LOCATION_CHOICES = (
        ('HOME', 'Casa'),
        ('AWAY', 'Trasferta'),
    )

    team = models.ForeignKey(Squadre, related_name='matches',on_delete=models.CASCADE)
    avversari = models.CharField( max_length=50)
    giornoPartita = models.DateTimeField(auto_now=False, auto_now_add=False)
    giocata = models.BooleanField(default=False)
    location_type=models.CharField(choices=LOCATION_CHOICES, max_length=4)
    indirizzo = models.CharField(max_length=100)

    puntiFatti = models.PositiveIntegerField(null=True,blank=True)
    puntiSubiti = models.PositiveIntegerField(null=True,blank=True)

    

    players_stats = models.ManyToManyField(
        Atleta,
        through='PlayerMatchStats',
        related_name='match_performances'
    )

    class Meta:
        ordering = ['giornoPartita']
        verbose_name_plural = "Matches"
        

    def __str__(self):
        return f"{self.team.nome} vs {self.avversari} ({self.giornoPartita.strftime('%d/%m/%Y')})"

class PlayerMatchStats(models.Model):
    partita = models.ForeignKey(Matches, related_name='player_stats', on_delete=models.CASCADE)
    player = models.ForeignKey(
        Atleta,
        on_delete=models.CASCADE,
        related_name='stats',
        limit_choices_to={'ruolo': 'atleta'}
    )

    points = models.PositiveIntegerField(default=0)
    fouls = models.PositiveIntegerField(default=0)
    
    three_pointers_made = models.PositiveIntegerField(default=0)
    three_pointers_attempted = models.PositiveIntegerField(default=0)
    free_throws_made = models.PositiveIntegerField(default=0)
    free_throws_attempted = models.PositiveIntegerField(default=0)

    numero_maglia = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Numero di maglia",
        validators=[
            MinValueValidator(0),
            MaxValueValidator(99)
        ]
    )

    class Meta:
        verbose_name = "Statistica Giocatore Partita"
        verbose_name_plural = "Statistiche Giocatori Partite"
        constraints = [
                    models.UniqueConstraint(
                        fields=['partita', 'player'],
                        name='unique_player_per_partita'
                    ),
                    # 2° Vincolo: Lo stesso numero di maglia NON può essere usato due volte nella stessa partita
                    models.UniqueConstraint(
                        fields=['partita', 'numero_maglia'],
                        name='unique_numero_maglia_per_partita'
            )
                ]

    def __str__(self):
        return f"{self.player.get_full_name()} - {self.points} pt in {self.partita}"