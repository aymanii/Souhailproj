from django import forms
from .models import Patient,RendezVous,Visite

class PatientForm(forms.ModelForm):
    password2 = forms.CharField(label='Confirmez le mot de passe', widget=forms.PasswordInput)

    class Meta:
        model = Patient
        fields = ['nom', 'prenom', 'dateNaissance', 'adresse', 'telephone', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput,
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password and password2 and password != password2:
            self.add_error('password2', 'Les mots de passe ne correspondent pas.')

        return cleaned_data
    

class RendezVousForm(forms.ModelForm):
    class Meta:
        model = RendezVous
        fields = ['dateHeure', 'symptome']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['dateHeure'].widget = forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M')
        self.fields['dateHeure'].input_formats = ['%Y-%m-%dT%H:%M']


