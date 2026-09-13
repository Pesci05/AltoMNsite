from django import forms
from .models import News

class CreaNewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['titolo', 'contenuto', 'immagine', 'pubblicata']
        widgets = {
            'titolo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Titolo della notizia'}),
            'contenuto': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Contenuto della notizia'}),
            'immagine': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'pubblicata': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }