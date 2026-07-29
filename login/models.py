from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, max_length=254)
    RUOLI = (
        ('allenatori','Coach'),
        ('dirigente','Dirigente'),
        ('atleta','Atleta'),
    )
    ruolo = models.CharField(choices=RUOLI, max_length=50,default='dirigente')
    telefono = models.CharField(blank=True,null=True, max_length=20)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f"{self.email} ({self.get_ruolo_display()})"

