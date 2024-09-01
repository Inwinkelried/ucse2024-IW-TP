from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import JugadorProfile, Usuario, Roles, ComplejoDePadel


class ComplejoRegisterForm(forms.ModelForm): 
    nombre_complejo = forms.CharField(max_length=100)
    telefono = forms.CharField(max_length=15)
    provincia = forms.CharField(max_length=100)
    ciudad = forms.CharField(max_length=100)
    direccion = forms.CharField(max_length=100)
    class Meta:
        model = ComplejoDePadel
        fields = ('nombre_complejo','telefono','provincia', 'ciudad','direccion')
    def save(self, commit=True):
        complejo = super().save(commit=False)
        complejo.habilitado = False #Un complejo se crea como no habilitado, es decir no se muestra.
        if commit:
            complejo.save()
        return complejo
        
class ComplejoEditForm(forms.ModelForm):
    nombre_complejo = forms.CharField(max_length=100)
    telefono = forms.CharField(max_length=15)
    provincia = forms.CharField(max_length=100)
    ciudad = forms.CharField(max_length=100)
    direccion = forms.CharField(max_length=100)
    tipo_instalacion =  forms.ChoiceField( choices=ComplejoDePadel.TIPOS_INSTALACION, required=False)
    tiene_duchas = forms.BooleanField(required=False)
    tiene_bar = forms.BooleanField(required=False)
    presta_paleta = forms.ChoiceField(choices=ComplejoDePadel.PALETAS_PELOTAS,  required=False)
    prestan_pelotas = forms.ChoiceField(choices=ComplejoDePadel.PALETAS_PELOTAS, required=False)

    class Meta:
        model = ComplejoDePadel
        fields = ('nombre_complejo', 'telefono', 'provincia', 'ciudad', 'direccion', 'tipo_instalacion', 'tiene_duchas', 'tiene_bar', 'presta_paleta', 'prestan_pelotas', 'foto_complejo')

class JugadorRegisterForm(UserCreationForm):
    telefono = forms.CharField(max_length=15)
    categoria = forms.CharField(max_length=50)
    class Meta:
        model = Usuario
        fields = ( 'username','email','password1','password2', 'telefono', 'categoria')

    def save(self, commit=True):
        user = super().save(commit=False)
        rol_jugador = Roles.objects.get(nombre=Roles.JUGADOR)
        user.rol = rol_jugador  # Un Usuario comienza creado como Jugador.
        if commit:
            user.save()
            JugadorProfile.objects.create(
                user=user,
                categoria=self.cleaned_data['categoria']
            )
        return user