from django import forms
from django.contrib.auth import get_user_model
from .models import Atleta, Squadre,Matches,PlayerMatchStats

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
        queryset=Squadre.objects.none(), 
        widget=forms.Select(attrs={'class': 'custom-selection'}),
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
    ruolo = forms.ChoiceField(
        choices=Atleta.RUOLO_CHOICES,
        label='Ruolo',
        widget=forms.Select(attrs={'class': 'custom-selection'})
    )

    
    class Meta:
        model = Atleta
        fields = ('first_name','last_name','email','squadra','data_nascita','ruolo')
        widgets = {
            'data_nascita': forms.DateInput(attrs={'type': 'date'}),
        }
        exclude = ['user']
        
    def clean(self):
        cleaned_data = super().clean()
        squadra = cleaned_data.get('squadra')
        numero_maglia = cleaned_data.get('numero_maglia')

        if squadra and numero_maglia is not None:
            # Verifica se esiste già un atleta con lo stesso numero nella stessa squadra
            if Atleta.objects.filter(squadra=squadra, numero_maglia=numero_maglia).exists():
                self.add_error(
                    'numero_maglia',
                    f"Il numero {numero_maglia} è già assegnato a un altro atleta del/della {squadra.nome}."
                )

        return cleaned_data

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

    def __init__(self, *args, **kwargs):
            user = kwargs.pop('user', None)
            
            super().__init__(*args, **kwargs)
    
            if user:
                if user.ruolo == 'allenatori':
                    self.fields['squadra'].queryset = Squadre.objects.filter(allenatori=user)
                elif user.ruolo == 'dirigente':
                    self.fields['squadra'].queryset = Squadre.objects.all()
                


class MatchCreationForm(forms.ModelForm):
    class Meta:
        model = Matches
        # Escludiamo players_stats perché i tabellini si inseriscono con i FormSet separatamente
        fields = [
            'team', 
            'avversari', 
            'giornoPartita', 
            'location_type', 
            'indirizzo', 
            'giocata',
        ]
        
        # Personalizziamo i widget per un aspetto e un'usabilità migliori
        widgets = {
            'team': forms.Select(attrs={'class': 'custom-selection'}),
            'avversari': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Es. Virtus Bologna'
            }),
            'giornoPartita': forms.DateTimeInput(attrs={
                'class': 'form-control', 
                'type': 'datetime-local' # Mostra il selettore data/ora nel browser
            }),
            'location_type': forms.Select(attrs={'class': 'custom-selection'}),
            'indirizzo': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Via e Città del palazzetto'
            }),
            'giocata': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        
        labels = {
            'team': 'Squadra',
            'avversari': 'Squadra Avversaria',
            'giornoPartita': 'Data e Ora',
            'location_type': 'In Casa / Trasferta',
            'indirizzo': 'Indirizzo Campo',
            'giocata': 'Partita Conclusa?',
        }
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        print("UTENTE:", user)
        print("RUOLO:", getattr(user, 'ruolo', 'Nessun ruolo'))

        if user:
            if user.ruolo == 'allenatori':
                self.fields['team'].queryset = Squadre.objects.filter(allenatori=user)
                print("Squadre allenatore:", self.fields['team'].queryset)
            elif user.ruolo == 'dirigente':
                self.fields['team'].queryset = Squadre.objects.all()
                print("Tutte le squadre per dirigente:", self.fields['team'].queryset)
class MatchUpdateForm(forms.ModelForm):
    class Meta:
        model = Matches
        fields = [
            'team', 
            'avversari', 
            'giornoPartita', 
            'location_type', 
            'indirizzo', 
            'giocata', 
            'puntiFatti', 
            'puntiSubiti'
        ]
        widgets = {
            'team': forms.Select(attrs={'class': 'custom-selection'}),
            'avversari': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Es. Virtus Bologna'}),
            'giornoPartita': forms.DateTimeInput(attrs={
                'class': 'form-control', 
                'type': 'datetime-local'  # Selettore data/ora HTML5
            }),
            'location_type': forms.Select(attrs={'class': 'custom-selection'}),
            'indirizzo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Via e Città del palazzetto'}),
            'giocata': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'puntiFatti': forms.NumberInput(attrs={'class': 'form-control'}),
            'puntiSubiti': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'team': 'Squadra',
            'avversari': 'Squadra Avversaria',
            'giornoPartita': 'Data e Ora',
            'location_type': 'Casa / Trasferta',
            'indirizzo': 'Palazzetto / Indirizzo',
            'giocata': 'Partita Conclusa',
            'puntiFatti': 'Punti Segnati',
            'puntiSubiti': 'Punti Subiti',
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        
        super().__init__(*args, **kwargs)

        if user:
            if user.ruolo == 'allenatori':
                self.fields['team'].queryset = Squadre.objects.filter(allenatori=user)
            else:
                print("--- DEBUG FORM: Utente non è . Mostro tutte le squadre. ---")

class TabellinoPartitaForm(forms.ModelForm):
    class Meta:
        model = PlayerMatchStats
        # Campi allineati esattamente a quanto richiesto dalla griglia e dal modello
        fields = [
            'player',
            'numero_maglia',
            'points',
            'fouls',
            'three_pointers_made',
            'three_pointers_attempted',
            'free_throws_made',
            'free_throws_attempted',
        ]
        widgets = {
            'player': forms.HiddenInput(),
            'numero_maglia': forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'min': 0, 'max': 99}),
            'points': forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'min': 0}),
            'fouls': forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'min': 0, 'max': 5}),
            'three_pointers_made': forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'min': 0}),
            'three_pointers_attempted': forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'min': 0}),
            'free_throws_made': forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'min': 0}),
            'free_throws_attempted': forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'min': 0}),
        }
        labels = {
            'player': 'Giocatore',
            'numero_maglia': 'N° Maglia',
            'points': 'Punti',
            'fouls': 'Falli',
            'three_pointers_made': 'Triple Segnate',
            'three_pointers_attempted': 'Triple Tentate',
            'free_throws_made': 'TL Segnati',
            'free_throws_attempted': 'TL Tentati',
        }