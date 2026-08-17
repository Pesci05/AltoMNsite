from django import forms
from django.contrib.auth import get_user_model
from .models import Atleta, Squadre

User = get_user_model()

class SquadraCreationForm(forms.ModelForm):
    allenatori = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(ruolo='allenatori'),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'checkbox-list'}),
        required=False,
        label="Assegna Allenatori"
    )
    class Meta:
        model = Squadre
        fields = ('nome','categoria','allenatori')
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'es. Nome Squadra'}),
            'categoria': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'es. Categoria squadra'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Filtra dinamicamente gli allenatori presenti nel DB al momento dell'apertura della pagina
        if 'allenatori' in self.fields:
            self.fields['allenatori'].queryset = User.objects.filter(ruolo='allenatori')
    

class AtletaCreationForm(forms.ModelForm):
    squadra = forms.ModelChoiceField(
        queryset=Squadre.objects.all(), 
        widget=forms.Select(attrs={'id': 'id_ruolo', 'class': 'form-control'}),
        label = 'Squadra',
        required=False
        )

    first_name = forms.CharField(label='Nome',
                widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Nome'})
                )
    last_name = forms.CharField(label='Cognome',
                widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Cognome'})
                )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'class':'fomr-control','placeholder':'mario.rossi@email.com'}),
        required=False)
    
    class Meta:
        model = Atleta
        fields = ('first_name','last_name','email','squadra','data_nascita')
        widgets = {
            'data_nascita': forms.DateInput(attrs={'type': 'date'}),
        }
        exclude = ['user']
        


    def save(self, commit = True):
        email = self.cleaned_data['email']
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']

        username = email.split('@')[0]
        base_username = username
        i = 0
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{i}"
            i+=1

        user = User.objects.create_user(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            ruolo='atleta'
        )

        password_temp = f"{first_name.capitalize()}{last_name.capitalize()}2026!"
        user.set_password(password_temp)
        user.save()
        atleta = super().save(commit=False)
        atleta.user = user

        if commit:
            atleta.save()

        return atleta


