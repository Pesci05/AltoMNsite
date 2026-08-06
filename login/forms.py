from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser
from django import forms

class CustomUserCretionForm(UserCreationForm):
    RUOLI_REGISTRAZIONE = (
        ('allenatori', 'Coach'),
        ('dirigente', 'Dirigente'),
    )

    ruolo = forms.ChoiceField(
        choices=RUOLI_REGISTRAZIONE,
        widget=forms.Select(attrs={'id': 'id_ruolo', 'class': 'form-control'}),
        label="Ruolo in società"
    )
    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'first_name', 'last_name', 'ruolo', 'telefono')
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'es. mario.rossi@email.it'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cognome'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Opzionale'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Conferma Password'})

    def save(self, commit = True):
        user =  super().save(commit=False)
        user.username = self.cleaned_data['email']
        if commit:
            user.save()
        return user



class CustomLoginForm(AuthenticationForm):
    username = forms.EmailField(
        label="Email",
        widget= forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'La tua email'})
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'La tua password'})
    )
