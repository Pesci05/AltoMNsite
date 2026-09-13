from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.text import slugify

# Create your models here.
class News(models.Model):
    titolo = models.CharField(max_length=200, verbose_name="Titolo")
    slug = models.SlugField(max_length=250, unique=True, blank=True, help_text="Generato automaticamente o personalizzato per l'URL")
    contenuto = models.TextField(verbose_name="Contenuto")
    autore = models.ForeignKey(settings.AUTH_USER_MODEL,limit_choices_to={'ruolo':'dirigente'} ,on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Autore")
    data_pubblicazione = models.DateTimeField(default=timezone.now, verbose_name="Data di pubblicazione")
    immagine = models.ImageField(upload_to='news_images/', blank=True, null=True, verbose_name="Immagine in evidenza")
    pubblicata = models.BooleanField(default=True, verbose_name="Pubblicata")

    class Meta:
        ordering = ['-data_pubblicazione']
        verbose_name = "Notizia"
        verbose_name_plural = "Notizie"

    def __str__(self):
        return self.titolo
    
    def save(self, *args, **kwargs):
        # Genera automaticamente lo slug dal titolo se non è già presente
        if not self.slug:
            base_slug = slugify(self.titolo)
            slug = base_slug
            counter = 1
            # Assicura che lo slug sia unico nel database
            while News.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)