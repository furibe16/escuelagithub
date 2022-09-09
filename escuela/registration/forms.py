from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import perfil


class RegistroConMail(UserCreationForm):
    email = forms.EmailField(required=True,
                             help_text='Campo requerido y debe ser valido, hasta 254 caracteres como maximo')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email):
            raise forms.ValidationError('El email ya existe, ingresa uno nuevo')
        return email


LISTA_SEXOS = (
    ('F', 'Femenino'),  # Primer tuple
    ('M', 'Masculino')  # Segundo tuple
)


class PerfilForm(forms.ModelForm):
    class Meta:
        model = perfil
        fields = ('nombre', 'avatar', 'biografia', 'recibemails', 'sexo', 'nacimiento')

        widgets = {'nombre': forms.TextInput(attrs={'class': 'form-control'}),
                   'avatar': forms.ClearableFileInput(attrs={'class': 'form-control'}),
                   'biografia': forms.Textarea(attrs={'class': 'form-control'}),
                   'recibemails': forms.CheckboxInput(),
                   'sexo': forms.RadioSelect(choices=LISTA_SEXOS),
                   'nacimiento': forms.DateInput(attrs={'class': 'form-control'}, format="%m/%d/%Y")
                   }

        labels = {'nombre': 'Nombre',
                  'avatar': 'Logo',
                  'biografia': 'Experiencia',
                  'recibemails': 'Puede recibir eMails',
                  'sexo': 'Sexo',
                  'nacimiento': 'Fecha de nacimiento'}



    """def clean(self):
        data = self.cleaned_data
        nombre = data.get('nombre')
        descripcion = data.get('descripcion')
        if nombre != "Hola" or descripcion != "Como estas":
            raise ValidationError('El nombre debe ser Hola y la biografia como estas')"""


